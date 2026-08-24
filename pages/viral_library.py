import streamlit as st
import pandas as pd
from database.crud import get_all_viral_scripts, search_viral_scripts, add_viral_script, delete_viral_script
from database.models import ViralScript

def render():
    st.markdown("""
        <div class="saas-header">
            <div>
                <span class="saas-title">📚 Viral Script Knowledge Library</span>
                <p style="color: #9CA3AF; margin-top: 4px; font-size: 0.9rem;">
                    Benchmark repository of high-performing reel templates used for RAG context injection.
                </p>
            </div>
            <div>
                <span class="saas-badge">SQLite Knowledge Base</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Filtering Controls
    f1, f2, f3 = st.columns([4, 4, 4])
    
    with f1:
        search_query = st.text_input("🔍 Search Topic, Hook, or Keyword", placeholder="e.g. 50 lakh, AI tools, oats...")
    with f2:
        selected_cat = st.selectbox("Category Filter", ["All", "Real Estate", "Finance & Wealth", "Tech & AI", "Fitness & Health", "E-commerce", "Education & Career"])
    with f3:
        sort_by = st.selectbox("Sort By", ["Engagement Rate (High to Low)", "Views (High to Low)", "Likes (High to Low)"])
        
    scripts = search_viral_scripts(category=selected_cat, topic=search_query, limit=50)
    
    if sort_by == "Views (High to Low)":
        scripts = sorted(scripts, key=lambda x: x['views'], reverse=True)
    elif sort_by == "Likes (High to Low)":
        scripts = sorted(scripts, key=lambda x: x['likes'], reverse=True)
        
    st.markdown(f"**Found {len(scripts)} Benchmark Records**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display Script Grid / Cards
    for idx, item in enumerate(scripts):
        with st.container():
            st.markdown(f"""
            <div class="content-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <div>
                        <span class="saas-badge" style="background: rgba(99,102,241,0.15); color: #818CF8;">{item['category']}</span>
                        <h3 style="margin: 6px 0 2px 0; color: #FFFFFF;">{item['topic']}</h3>
                        <span style="font-size: 0.82rem; color: #9CA3AF;">Audience: {item['audience']} • Duration: {item['duration']}s</span>
                    </div>
                    <div style="text-align: right;">
                        <span class="score-pill score-high">⚡ {item['engagement_rate']}% ER</span>
                    </div>
                </div>
                <div style="background: #0B0E14; padding: 0.8rem 1rem; border-radius: 8px; border: 1px solid #232D3F; margin: 10px 0;">
                    <strong style="color: #818CF8;">🪝 Curiosity Hook:</strong> <span style="color: #F3F4F6;">"{item['hook']}"</span><br><br>
                    <span style="color: #D1D5DB; font-size: 0.9rem;">{item['script_text']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem; color: #6B7280; margin-top: 8px;">
                    <div>
                        👁️ {item['views']:,} views | ❤️ {item['likes']:,} likes | 💬 {item['comments']:,} comments | 🔄 {item['shares']:,} shares
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c_act1, c_act2 = st.columns([3, 9])
            with c_act1:
                if st.button(f"✨ Use as Context Reference", key=f"btn_ref_{item['id']}"):
                    st.session_state.informal_input_prompt = item['hook']
                    st.session_state.opt_category = item['category']
                    st.session_state.page = "Generate Script"
                    st.toast("Loaded into Script Generator!", icon="🎯")
                    st.rerun()

    # Form to add a new Viral Script Reference into SQLite DB
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    with st.expander("➕ Add New Benchmark Viral Script to SQLite Library"):
        with st.form("add_viral_script_form"):
            a_cat = st.selectbox("Category", ["Real Estate", "Finance & Wealth", "Tech & AI", "Fitness & Health", "E-commerce", "Education & Career"])
            a_topic = st.text_input("Topic / Title")
            a_aud = st.text_input("Audience", value="General")
            a_hook = st.text_input("Curiosity Hook")
            a_text = st.text_area("Full Script Text")
            a_dur = st.number_input("Duration (s)", value=30)
            a_er = st.number_input("Engagement Rate (%)", value=8.5)
            
            sub = st.form_submit_button("Save Benchmark Script to DB")
            if sub:
                if not a_topic or not a_text:
                    st.error("Please fill in topic and script text.")
                else:
                    new_vs = ViralScript(
                        id=None,
                        category=a_cat,
                        topic=a_topic,
                        audience=a_aud,
                        hook=a_hook if a_hook else a_text[:50],
                        script_text=a_text,
                        duration=a_dur,
                        views=100000,
                        likes=8000,
                        comments=500,
                        shares=1200,
                        engagement_rate=a_er,
                        performance_label="High Potential"
                    )
                    add_viral_script(new_vs)
                    st.success("New viral benchmark script added to SQLite database!")
                    st.rerun()
