import os
import streamlit as st
import streamlit.components.v1 as components

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

# ── Fullscreen CSS — injected FIRST so it applies before any component renders ──
st.markdown("""
    <style>
        /* ── Kill ALL Streamlit chrome ── */
        header[data-testid="stHeader"],
        header,
        footer,
        #MainMenu,
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="manage-app-button"],
        .stDeployButton,
        [data-testid="stSidebarNav"] { display: none !important; visibility: hidden !important; }

        /* ── Zero out every Streamlit wrapper (no overflow:hidden so iframe can scroll internally) ── */
        html, body {
            margin: 0 !important; padding: 0 !important;
            height: 100vh !important; width: 100vw !important;
            overflow: hidden !important;
        }
        [data-testid="stAppViewContainer"],
        [data-testid="stApp"],
        .stApp,
        [data-testid="stMain"],
        .main, section.main {
            padding: 0 !important; margin: 0 !important;
            height: 100vh !important; width: 100vw !important;
            overflow: hidden !important;
        }
        .block-container,
        [data-testid="stBlockContainer"],
        [data-testid="stVerticalBlock"] {
            padding: 0 !important; margin: 0 !important;
            max-width: 100vw !important;
            height: 100vh !important;
            overflow: hidden !important;
        }
        /* Remove margins from Streamlit element wrappers */
        .element-container, .stMarkdown {
            padding: 0 !important; margin: 0 !important;
        }

        /* ── Main dashboard iframe — true fullscreen, scrolling handled INSIDE iframe ── */
        iframe:first-of-type {
            position: fixed !important;
            inset: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            outline: none !important;
            z-index: 2147483647 !important;
            display: block !important;
            background: #0f1115 !important;
        }

        /* ── Bridge iframes — completely hidden ── */
        iframe:not(:first-of-type) {
            position: fixed !important;
            top: -9999px !important; left: -9999px !important;
            width: 1px !important; height: 1px !important;
            opacity: 0 !important; pointer-events: none !important;
            z-index: -9999 !important;
        }

        /* Hide scrollbars on the STREAMLIT parent page only (not inside iframe) */
        html::-webkit-scrollbar, body::-webkit-scrollbar { display: none !important; }
        html, body { scrollbar-width: none !important; -ms-overflow-style: none !important; }
    </style>
""", unsafe_allow_html=True)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass



# ── Session state initialisation ───────────────────────────────────────────

if "ai_question" not in st.session_state:
    st.session_state.ai_question = None
if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []
if "ai_answer" not in st.session_state:
    st.session_state.ai_answer = None
if "ai_system_prompt" not in st.session_state:
    st.session_state.ai_system_prompt = ""



try:
    from utils.db import fetch_roster_data, fetch_snapshot_data, fetch_news_data

    try:
        with open("data/images/Sony-Music-cursor.png", "rb") as f:
            import base64
            loader_b64 = base64.b64encode(f.read()).decode("utf-8")
            loader_img_url = f"data:image/png;base64,{loader_b64}"
    except Exception:
        loader_img_url = ""

    loader_placeholder = st.empty()
    loader_placeholder.markdown(f"""
        <style>
        .custom-loader-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #0f1115;
            z-index: 999999;
        }}
        .zoom-logo {{
            animation: pulse-zoom 1.5s ease-in-out infinite;
            width: 240px;
            height: auto;
        }}
        @keyframes pulse-zoom {{
            0% {{ transform: scale(1); opacity: 0.7; }}
            50% {{ transform: scale(1.15); opacity: 1; }}
            100% {{ transform: scale(1); opacity: 0.7; }}
        }}
        </style>
        <div class="custom-loader-container">
            <svg class="zoom-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 176 36" height="60" aria-label="Sony Music Latin" role="img">
                <image href="{loader_img_url}" x="0" y="0" width="36" height="36" />
                <g transform="translate(46, 0)">
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

    # ── Main dashboard HTML (identical design, no proxy URL needed) ────────
    html_content = """<!doctype html>
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
    """ + get_style_css() + """
    </style>
    <script>
      (function () {
        var t = localStorage.getItem('sml-pulse-theme');
        if (t !== 'dark' && t !== 'light') {
          t = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
        }
        document.documentElement.setAttribute('data-theme', t);
      })();
    </script>
  </head>
  <body>
    <div id="root"></div>

    <script>
      // Injected data
      window.INJECTED_ROSTER = """ + roster_json + """;
      window.INJECTED_SNAPSHOT = """ + snapshot_json + """;
      window.INJECTED_NEWS = """ + news_json + """;
    </script>

    <script>
    """ + get_utils() + """
    """ + get_theme() + """
    """ + get_overview() + """
    """ + get_stories() + """
    """ + get_roster() + """
    """ + get_leaderboards() + """
    """ + get_analyst() + """
    """ + get_frontend() + """
    </script>
  </body>
</html>"""

    components.html(html_content, height=10000, scrolling=True)



    pass  # Fullscreen CSS already injected at top
except Exception as e:
    st.error(f"Error loading dashboard: {e}")