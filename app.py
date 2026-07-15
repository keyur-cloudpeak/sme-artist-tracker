import os
import streamlit as st
import streamlit.components.v1 as components
import json

from utils.utils import get_utils
from theme.theme import get_theme
from components.overview import get_overview
from components.stories import get_stories
from components.roster import get_roster
from components.leaderboards import get_leaderboards
from components.analyst import get_analyst
from frontend import get_frontend
from theme.style_css import get_style_css

st.set_page_config(
    page_title="SME Pulse",
    page_icon="📊",
    layout="wide"
)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from utils.db import fetch_roster_data, fetch_snapshot_data, fetch_news_data
    
    loader_placeholder = st.empty()
    loader_placeholder.markdown("""
        <style>
        .custom-loader-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #0f1115; /* Dark background matching theme */
            z-index: 999999;
        }
        .zoom-logo {
            animation: pulse-zoom 1.5s ease-in-out infinite;
            width: 240px;
            height: auto;
        }
        @keyframes pulse-zoom {
            0% { transform: scale(1); opacity: 0.7; }
            50% { transform: scale(1.15); opacity: 1; }
            100% { transform: scale(1); opacity: 0.7; }
        }
        </style>
        <div class="custom-loader-container">
            <svg class="zoom-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 181.6 35.4" height="60" aria-label="Sony Music Latin" role="img">
                <g><circle cx="8.4" cy="2.2" r="2.2" fill="#CC0000"/><circle cx="14.6" cy="2.2" r="2.2" fill="#CC0000"/><circle cx="20.8" cy="2.2" r="2.2" fill="#CC0000"/><circle cx="27.0" cy="2.2" r="2.2" fill="#CC0000"/><circle cx="33.2" cy="2.2" r="2.2" fill="#CC0000"/><circle cx="2.2" cy="8.4" r="2.2" fill="#CC0000"/><circle cx="8.4" cy="8.4" r="2.2" fill="#CC0000"/><circle cx="14.6" cy="8.4" r="2.2" fill="#CC0000"/><circle cx="20.8" cy="8.4" r="2.2" fill="#CC0000"/><circle cx="27.0" cy="8.4" r="2.2" fill="#CC0000"/><circle cx="33.2" cy="8.4" r="2.2" fill="#CC0000"/><circle cx="39.4" cy="8.4" r="2.2" fill="#CC0000"/><circle cx="2.2" cy="14.6" r="2.2" fill="#CC0000"/><circle cx="8.4" cy="14.6" r="2.2" fill="#CC0000"/><circle cx="14.6" cy="14.6" r="2.2" fill="#CC0000"/><circle cx="20.8" cy="14.6" r="2.2" fill="#CC0000"/><circle cx="27.0" cy="14.6" r="2.2" fill="#CC0000"/><circle cx="33.2" cy="14.6" r="2.2" fill="#CC0000"/><circle cx="39.4" cy="14.6" r="2.2" fill="#CC0000"/><circle cx="2.2" cy="20.8" r="2.2" fill="#CC0000"/><circle cx="8.4" cy="20.8" r="2.2" fill="#CC0000"/><circle cx="14.6" cy="20.8" r="2.2" fill="#CC0000"/><circle cx="20.8" cy="20.8" r="2.2" fill="#CC0000"/><circle cx="27.0" cy="20.8" r="2.2" fill="#CC0000"/><circle cx="33.2" cy="20.8" r="2.2" fill="#CC0000"/><circle cx="39.4" cy="20.8" r="2.2" fill="#CC0000"/><circle cx="2.2" cy="27.0" r="2.2" fill="#CC0000"/><circle cx="8.4" cy="27.0" r="2.2" fill="#CC0000"/><circle cx="14.6" cy="27.0" r="2.2" fill="#CC0000"/><circle cx="20.8" cy="27.0" r="2.2" fill="#CC0000"/><circle cx="27.0" cy="27.0" r="2.2" fill="#CC0000"/><circle cx="33.2" cy="27.0" r="2.2" fill="#CC0000"/><circle cx="39.4" cy="27.0" r="2.2" fill="#CC0000"/><circle cx="8.4" cy="33.2" r="2.2" fill="#CC0000"/><circle cx="14.6" cy="33.2" r="2.2" fill="#CC0000"/><circle cx="20.8" cy="33.2" r="2.2" fill="#CC0000"/><circle cx="27.0" cy="33.2" r="2.2" fill="#CC0000"/><circle cx="33.2" cy="33.2" r="2.2" fill="#CC0000"/></g>
                <g transform="translate(51.6, 0)">
                    <text x="0" y="14.7" font-family="'DM Sans','Helvetica Neue',Arial,sans-serif" font-size="12" font-weight="700" letter-spacing="0.08em" fill="#FFFFFF">SONY MUSIC</text>
                    <line x1="0" y1="18.7" x2="120" y2="18.7" stroke="#FFFFFF" stroke-width="0.6" opacity="0.35"/>
                    <text x="0" y="22.7" font-family="'DM Sans','Helvetica Neue',Arial,sans-serif" font-size="10" font-weight="500" letter-spacing="0.22em" fill="#999999" dominant-baseline="hanging">LATIN</text>
                </g>
            </svg>
        </div>
    """, unsafe_allow_html=True)

    roster_json = fetch_roster_data()
    snapshot_json = fetch_snapshot_data()
    news_json = fetch_news_data()
    
    loader_placeholder.empty()

    # Get API key from Streamlit secrets or environment variable
    try:
        anthropic_api_key = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY", ""))
    except Exception:
        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    html_content = f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Sony Music Latin Pulse — Daily Briefing</title>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link
          href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=IBM+Plex+Mono:wght@400;500&family=DM+Sans:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
        <style>
        {get_style_css()}
        </style>
        <script>
          // Sync theme before paint to prevent flash
          (function () {{
            var t = localStorage.getItem('sml-pulse-theme');
            if (t !== 'dark' && t !== 'light') {{
              t = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
            }}
            document.documentElement.setAttribute('data-theme', t);
          }})();
        </script>
      </head>
      <body>
        <div id="root"></div>

        <script>
          // Inject data directly to bypass fetch() latency and static asset issues
          window.INJECTED_ROSTER = {roster_json};
          window.INJECTED_SNAPSHOT = {snapshot_json};
          window.INJECTED_NEWS = {news_json};
          window.INJECTED_API_KEY = "{anthropic_api_key}";
        </script>

        <script>
        {get_utils()}
        {get_theme()}
        {get_overview()}
        {get_stories()}
        {get_roster()}
        {get_leaderboards()}
        {get_analyst()}
        {get_frontend()}
        </script>
      </body>
    </html>
    """

    components.html(html_content, height=1200, scrolling=True)

    st.markdown('''
        <style>
            iframe {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                border: none;
                display: block;
                z-index: 99999;
            }
             /* Remove Streamlit's default padding to make the app fullscreen */
            .block-container, [data-testid="stBlockContainer"] {
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
                height: 100vh !important;
            }
            header[data-testid="stHeader"] {
                display: none;
            }
            /* Hide Streamlit's parent scrollbars and prevent scrolling */
            html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], section.main, .main {
                overflow: hidden !important;
                height: 100vh !important;
                margin: 0 !important;
                padding: 0 !important;
                scrollbar-width: none;
                -ms-overflow-style: none;
            }
            html::-webkit-scrollbar, body::-webkit-scrollbar, [data-testid="stAppViewContainer"]::-webkit-scrollbar, [data-testid="stMain"]::-webkit-scrollbar, section.main::-webkit-scrollbar {
                display: none;
            }
        </style>
    ''', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading dashboard: {e}")

