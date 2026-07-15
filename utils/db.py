import os
from sqlalchemy import create_engine, text
import json
from decimal import Decimal
from datetime import datetime, date
import base64

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

def get_engine():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        try:
            import streamlit as st
            db_url = st.secrets["DATABASE_URL"]
        except (ImportError, FileNotFoundError, KeyError, Exception):
            pass
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables or secrets")
    return create_engine(db_url)

def get_base64_image(slug):
    try:
        with open(f"data/images/{slug}.jpg", "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded}"
    except Exception:
        # Fallback to an empty image or keep it null if preferred
        return ""

def fetch_roster_data():
    engine = get_engine()
    with engine.connect() as conn:
        # Fetch latest snapshot date for dynamic date
        snapshot_res = conn.execute(text("SELECT snapshot_date FROM snapshots ORDER BY snapshot_date DESC LIMIT 1")).fetchone()
        current_date = snapshot_res[0].isoformat() if snapshot_res else date.today().isoformat()

        # Fetch artists
        artists_res = conn.execute(text("SELECT * FROM artists"))
        artists = [dict(row._mapping) for row in artists_res]
        
        # Fetch all social links at once
        links_res = conn.execute(text("SELECT artist_slug, platform, url FROM artist_social_links"))
        all_links = {}
        for row in links_res:
            slug = row._mapping['artist_slug']
            if slug not in all_links:
                all_links[slug] = {}
            all_links[slug][row._mapping['platform']] = row._mapping['url']
            
        for artist in artists:
            artist['social_links'] = all_links.get(artist['slug'], {})
            artist['image_url'] = get_base64_image(artist['slug'])
            artist['image_local_path'] = f"data/images/{artist['slug']}.jpg"
            
        roster_data = {
            "roster_date": current_date,
            "source": "PostgreSQL Database",
            "artist_count": len(artists),
            "artists": artists
        }
        return json.dumps(roster_data, cls=CustomEncoder)

def fetch_snapshot_data():
    engine = get_engine()
    with engine.connect() as conn:
        snapshots_res = conn.execute(text("SELECT * FROM snapshots ORDER BY snapshot_date DESC LIMIT 1")).fetchone()
        
        if not snapshots_res:
            return json.dumps({"artists": []})
        
        snapshot = dict(snapshots_res._mapping)
        snapshot_date = snapshot['snapshot_date']
        
        # Fetch artists
        artists_res = conn.execute(text("SELECT slug as artist_slug, name as artist_name, current_tier as tier, country, label_status, status, priority, genre_tags FROM artists"))
        artists_dict = {row._mapping['artist_slug']: dict(row._mapping) for row in artists_res}
        for slug in artists_dict:
            artists_dict[slug]['kpis'] = []
            
        # Fetch all KPIs for the snapshot
        kpis_res = conn.execute(text(f"""
            SELECT akv.*, kc.name as kpi_name, kc.unit, kc.higher_is_better 
            FROM artist_kpi_values akv 
            JOIN kpi_catalog kc ON akv.kpi_id = kc.kpi_id 
            WHERE akv.snapshot_date = '{snapshot_date}'
        """))
        
        for kpi_row in kpis_res:
            kpi = dict(kpi_row._mapping)
            slug = kpi['artist_slug']
            if slug in artists_dict:
                extra = kpi.get('extra', {})
                if isinstance(extra, str):
                    extra = json.loads(extra)
                    
                kpi_data = {
                    "kpi_id": kpi['kpi_id'],
                    "kpi_name": kpi['kpi_name'],
                    "unit": kpi['unit'],
                    "higher_is_better": kpi['higher_is_better'],
                    "current_value": kpi['current_value'],
                    "previous_value": kpi['previous_value'],
                    "delta_absolute": kpi['delta_absolute'],
                    "delta_percent": kpi['delta_percent'],
                    "trend": kpi['trend'],
                    "alert": kpi['alert'],
                    "benchmark_tier": kpi['benchmark_tier'],
                    "components": extra
                }
                artists_dict[slug]['kpis'].append(kpi_data)
            
        snapshot_data = {
            "snapshot_date": snapshot['snapshot_date'],
            "previous_snapshot_date": snapshot['previous_snapshot_date'],
            "artists": list(artists_dict.values())
        }
        return json.dumps(snapshot_data, cls=CustomEncoder)

def fetch_news_data():
    engine = get_engine()
    with engine.connect() as conn:
        snapshot_res = conn.execute(text("SELECT snapshot_date FROM snapshots ORDER BY snapshot_date DESC LIMIT 1")).fetchone()
        current_date = snapshot_res[0].isoformat() if snapshot_res else date.today().isoformat()
        
        news_res = conn.execute(text("SELECT * FROM news_signals ORDER BY news_date DESC LIMIT 10"))
        news_list = [dict(row._mapping) for row in news_res]
        
        if not news_list:
            return json.dumps({"items": []})
            
        news_ids = [str(n['id']) for n in news_list]
        news_ids_str = ",".join(news_ids)
        
        artist_slugs = list(set([n['artist_slug'] for n in news_list]))
        artist_slugs_str = ",".join([f"'{slug}'" for slug in artist_slugs])
        
        artists_dict = {}
        if artist_slugs:
            artist_res = conn.execute(text(f"SELECT slug, name, current_tier FROM artists WHERE slug IN ({artist_slugs_str})"))
            artists_dict = {row._mapping['slug']: dict(row._mapping) for row in artist_res}
            
        impacts_dict = {}
        if news_ids:
            impacts_res = conn.execute(text(f"""
                SELECT nski.*, kc.name as kpi_name 
                FROM news_signal_kpi_impacts nski
                JOIN kpi_catalog kc ON nski.kpi_id = kc.kpi_id
                WHERE nski.news_signal_id IN ({news_ids_str})
            """))
            for imp_row in impacts_res:
                imp = dict(imp_row._mapping)
                nid = imp['news_signal_id']
                if nid not in impacts_dict:
                    impacts_dict[nid] = []
                impacts_dict[nid].append({
                    "kpi_id": imp['kpi_id'],
                    "kpi_name": imp['kpi_name'],
                    "current_value": imp['current_value'],
                    "benchmark_tier": imp['benchmark_tier'],
                    "delta_absolute": imp['delta_absolute'],
                    "delta_percent": imp['delta_percent'],
                    "direction": imp['direction']
                })
        
        items = []
        for news in news_list:
            artist = artists_dict.get(news['artist_slug'], {})
            news['artist_name'] = artist.get('name', 'Unknown')
            news['artist_tier'] = artist.get('current_tier', 'Unknown')
            news['kpi_impact'] = impacts_dict.get(news['id'], [])
            
            # Format according to json structure
            formatted_news = {
                "priority": news['priority'],
                "score": news['score'],
                "signal_type": news['signal_type'],
                "headline": news['headline'],
                "artist_name": news['artist_name'],
                "artist_slug": news['artist_slug'],
                "artist_tier": news['artist_tier'],
                "image_url": get_base64_image(news['artist_slug']),
                "kpi_impact": news['kpi_impact'],
                "summary": news['summary'],
                "source": news['source'],
                "data_confidence": news['data_confidence'],
                "timestamp": news['occurred_at']
            }
            items.append(formatted_news)
            
        news_data = {
            "news_date": current_date,
            "source_snapshot": current_date,
            "total_signals_detected": len(items),
            "items": items
        }
        return json.dumps(news_data, cls=CustomEncoder)
