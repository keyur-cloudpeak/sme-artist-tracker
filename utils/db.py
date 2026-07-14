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
        raise ValueError("DATABASE_URL not found in environment variables")
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
        # Fetch artists
        artists_res = conn.execute(text("SELECT * FROM artists"))
        artists = []
        for row in artists_res:
            artist = dict(row._mapping)
            
            # Fetch social links
            links_res = conn.execute(
                text(f"SELECT platform, url FROM artist_social_links WHERE artist_slug = '{artist['slug']}'")
            )
            social_links = {link._mapping['platform']: link._mapping['url'] for link in links_res}
            artist['social_links'] = social_links
            artist['image_url'] = get_base64_image(artist['slug'])
            artist['image_local_path'] = f"data/images/{artist['slug']}.jpg"
            
            artists.append(artist)
            
        roster_data = {
            "roster_date": "2026-07-14", # You can make this dynamic
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
        
        # Fetch artists and their KPIs
        artists_res = conn.execute(text("SELECT slug, name, current_tier, country, label_status, status, priority, genre_tags FROM artists"))
        artists = []
        for row in artists_res:
            artist_dict = dict(row._mapping)
            artist = {
                "artist_slug": artist_dict['slug'],
                "artist_name": artist_dict['name'],
                "tier": artist_dict['current_tier'],
                "country": artist_dict['country'],
                "label_status": artist_dict['label_status'],
                "status": artist_dict['status'],
                "priority": artist_dict['priority'],
                "genre_tags": artist_dict['genre_tags']
            }
            
            # Fetch KPIs
            kpis_res = conn.execute(text(f"""
                SELECT akv.*, kc.name as kpi_name, kc.unit, kc.higher_is_better 
                FROM artist_kpi_values akv 
                JOIN kpi_catalog kc ON akv.kpi_id = kc.kpi_id 
                WHERE akv.artist_slug = '{artist['artist_slug']}' 
                AND akv.snapshot_date = '{snapshot_date}'
            """))
            kpis = []
            for kpi_row in kpis_res:
                kpi = dict(kpi_row._mapping)
                # extra JSONB comes as dict or str
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
                kpis.append(kpi_data)
            artist['kpis'] = kpis
            artists.append(artist)
            
        snapshot_data = {
            "snapshot_date": snapshot['snapshot_date'],
            "previous_snapshot_date": snapshot['previous_snapshot_date'],
            "artists": artists
        }
        return json.dumps(snapshot_data, cls=CustomEncoder)

def fetch_news_data():
    engine = get_engine()
    with engine.connect() as conn:
        news_res = conn.execute(text("SELECT * FROM news_signals ORDER BY news_date DESC LIMIT 10"))
        items = []
        for row in news_res:
            news = dict(row._mapping)
            
            # Fetch artist details for the news
            artist_res = conn.execute(text(f"SELECT name, current_tier FROM artists WHERE slug = '{news['artist_slug']}'")).fetchone()
            if artist_res:
                news['artist_name'] = artist_res._mapping['name']
                news['artist_tier'] = artist_res._mapping['current_tier']
            else:
                news['artist_name'] = "Unknown"
                news['artist_tier'] = "Unknown"
            
            # Fetch impacts
            impacts_res = conn.execute(text(f"""
                SELECT nski.*, kc.name as kpi_name 
                FROM news_signal_kpi_impacts nski
                JOIN kpi_catalog kc ON nski.kpi_id = kc.kpi_id
                WHERE nski.news_signal_id = {news['id']}
            """))
            impacts = []
            for imp_row in impacts_res:
                imp = dict(imp_row._mapping)
                impacts.append({
                    "kpi_id": imp['kpi_id'],
                    "kpi_name": imp['kpi_name'],
                    "current_value": imp['current_value'],
                    "benchmark_tier": imp['benchmark_tier'],
                    "delta_absolute": imp['delta_absolute'],
                    "delta_percent": imp['delta_percent'],
                    "direction": imp['direction']
                })
            news['kpi_impact'] = impacts
            
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
                "kpi_impact": impacts,
                "summary": news['summary'],
                "source": news['source'],
                "data_confidence": news['data_confidence'],
                "timestamp": news['occurred_at']
            }
            items.append(formatted_news)
            
        news_data = {
            "news_date": "2026-07-14", # Make dynamic
            "source_snapshot": "2026-07-14",
            "total_signals_detected": len(items),
            "items": items
        }
        return json.dumps(news_data, cls=CustomEncoder)
