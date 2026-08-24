import streamlit as st
import os
import sys
from pathlib import Path

# Ensure root dir in path
sys.path.insert(0, str(Path(__file__).parent))

# Load database schema on startup
from database.db import init_db
init_db()

# Load seed data if empty
from data.seed_data import seed_database
seed_database()

# Load SaaS Custom CSS
from utils.css_styles import get_saas_theme_css
st.set_page_config(
    page_title="ViralIQ — AI Script Optimization SaaS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(get_saas_theme_css(), unsafe_allow_html=True)

# Session State for Page Navigation
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# Sidebar Branding & Navigation
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0; border-bottom: 1px solid #232D3F; margin-bottom: 15px;">
            <h2 style="margin: 0; color: #FFFFFF; font-weight: 800; font-size: 1.5rem; letter-spacing: -0.03em; display: flex; align-items: center; gap: 8px;">
                ⚡ <span style="background: linear-gradient(135deg, #FFFFFF 0%, #818CF8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">ViralIQ</span>
            </h2>
            <p style="margin: 4px 0 0 0; color: #6B7280; font-size: 0.78rem; font-weight: 500;">
                AI Script Performance Intelligence
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    NAV_OPTIONS = [
        "Dashboard",
        "Analyze Script",
        "Generate Script",
        "Analyze Reel",
        "Viral Library",
        "My Scripts",
        "AI Advisor",
        "Analytics",
        "Reports",
        "Settings"
    ]
    
    NAV_ICONS = {
        "Dashboard": "⚡",
        "Analyze Script": "🔬",
        "Generate Script": "✨",
        "Analyze Reel": "🎬",
        "Viral Library": "📚",
        "My Scripts": "📂",
        "AI Advisor": "💬",
        "Analytics": "📈",
        "Reports": "📑",
        "Settings": "⚙️"
    }
    
    current_index = NAV_OPTIONS.index(st.session_state.page) if st.session_state.page in NAV_OPTIONS else 0
    
    selected_page = st.radio(
        "NAVIGATION",
        NAV_OPTIONS,
        index=current_index,
        format_func=lambda page: f"{NAV_ICONS.get(page, '•')}  {page}"
    )
    
    st.session_state.page = selected_page
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="padding: 12px; background: #131822; border-radius: 8px; border: 1px solid #232D3F; font-size: 0.78rem; color: #9CA3AF;">
            <strong>AI Subject Mapping:</strong><br>
            • AI-503: ML + SQLite CRUD<br>
            • AI-504: Prompt Eng + Gemini LLM<br>
            • AI-505: Keras ANN + CNN Visual
        </div>
    """, unsafe_allow_html=True)

# Route to Page Modules
if selected_page == "Dashboard":
    from pages import dashboard
    dashboard.render()
elif selected_page == "Analyze Script":
    from pages import analyze_script
    analyze_script.render()
elif selected_page == "Generate Script":
    from pages import generate_script
    generate_script.render()
elif selected_page == "Analyze Reel":
    from pages import analyze_reel
    analyze_reel.render()
elif selected_page == "Viral Library":
    from pages import viral_library
    viral_library.render()
elif selected_page == "My Scripts":
    from pages import my_scripts
    my_scripts.render()
elif selected_page == "AI Advisor":
    from pages import ai_advisor
    ai_advisor.render()
elif selected_page == "Analytics":
    from pages import analytics
    analytics.render()
elif selected_page == "Reports":
    from pages import reports
    reports.render()
elif selected_page == "Settings":
    from pages import settings
    settings.render()
