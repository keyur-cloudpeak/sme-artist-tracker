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
    roster_json = fetch_roster_data()
    snapshot_json = fetch_snapshot_data()
    news_json = fetch_news_data()

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
                width: 100%;
                height: 100vh;
                border: none;
            }
            /* Remove Streamlit's default padding to make the app fullscreen */
            .block-container {
                padding: 0 !important;
                max-width: 100% !important;
            }
            header[data-testid="stHeader"] {
                display: none;
            }
        </style>
    ''', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading dashboard: {e}")

