import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.crud import get_all_scripts, get_all_predictions, get_all_viral_scripts

def render():
    st.markdown("""
        <div class="saas-header">
            <div>
                <span class="saas-title">⚡ Executive Dashboard</span>
                <p style="color: #9CA3AF; margin-top: 4px; font-size: 0.9rem;">
                    Real-time script performance predictions, optimization analytics, and viral patterns.
                </p>
            </div>
            <div>
                <span class="saas-badge">ViralIQ v1.0 • System Operational</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Fetch real SQLite data
    scripts = get_all_scripts()
    predictions = get_all_predictions()
    viral_lib = get_all_viral_scripts()
    
    total_scripts = len(scripts)
    total_analyzed = len(predictions)
    
    if predictions:
        avg_score = round(sum(p['final_score'] for p in predictions) / len(predictions), 1)
        best_score = round(max(p['final_score'] for p in predictions), 1)
    else:
        avg_score = 0.0
        best_score = 0.0
        
    optimized_count = sum(1 for p in predictions if p['final_score'] >= 80.0)
    
    # Key Metric Cards
    m1, m2, m3, m4, m5 = st.columns(5)
    
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Scripts</div>
            <div class="metric-value">{total_scripts}</div>
            <div class="metric-delta delta-positive">📁 Stored in DB</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Reels Analyzed</div>
            <div class="metric-value">{total_analyzed}</div>
            <div class="metric-delta delta-positive">🧠 ML + ANN Evaluated</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Predicted Score</div>
            <div class="metric-value">{avg_score}%</div>
            <div class="metric-delta {'delta-positive' if avg_score>=75 else 'delta-warning'}">Target Threshold: 80%</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Best Performance</div>
            <div class="metric-value">{best_score}%</div>
            <div class="metric-delta delta-positive">🏆 Global Peak</div>
        </div>
        """, unsafe_allow_html=True)

    with m5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Target Reached</div>
            <div class="metric-value">{optimized_count}</div>
            <div class="metric-delta delta-positive">✨ Scores ≥ 80%</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Content Columns
    c1, c2 = st.columns([7, 5])
    
    with c1:
        st.markdown("### 📊 Recent Analysis History")
        if predictions:
            df_preds = pd.DataFrame(predictions)
            df_preds['created_at'] = pd.to_datetime(df_preds['created_at']).dt.strftime('%b %d, %H:%M')
            
            st.dataframe(
                df_preds[['id', 'script_title', 'ml_score', 'ann_score', 'final_score', 'status', 'created_at']],
                column_config={
                    "id": "ID",
                    "script_title": "Script Title",
                    "ml_score": st.column_config.NumberColumn("ML Score", format="%.1f%%"),
                    "ann_score": st.column_config.NumberColumn("ANN Score", format="%.1f%%"),
                    "final_score": st.column_config.NumberColumn("Final Performance Score", format="%.1f%%"),
                    "status": "Status",
                    "created_at": "Analyzed At"
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No script analyses recorded yet. Head over to **Analyze Script** or **Generate Script** to run your first evaluation!")
            
    with c2:
        st.markdown("### 🎯 Script Categories Distribution")
        if scripts:
            df_s = pd.DataFrame(scripts)
            cat_counts = df_s['category'].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Count']
            
            fig = px.pie(
                cat_counts,
                values='Count',
                names='Category',
                hole=0.4,
                color_discrete_sequence=['#6366F1', '#8B5CF6', '#10B981', '#F59E0B', '#EC4899']
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#F3F4F6'),
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(font=dict(color='#9CA3AF'))
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div class="content-card" style="text-align: center; padding: 2rem;">
                <p style="color: #9CA3AF;">No category data available yet.</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Workflow Actions
    st.markdown("### 🚀 Quick Workflow Actions")
    q1, q2, q3 = st.columns(3)
    
    with q1:
        st.markdown("""
        <div class="content-card">
            <h4 style="margin-bottom: 8px;">📝 Analyze Script</h4>
            <p style="color: #9CA3AF; font-size: 0.88rem;">Paste any raw draft to extract features and compute real ML + ANN performance scores.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Analyze Script", key="btn_dash_analyze"):
            st.session_state.page = "Analyze Script"
            st.rerun()

    with q2:
        st.markdown("""
        <div class="content-card">
            <h4 style="margin-bottom: 8px;">✨ Generate & Optimize</h4>
            <p style="color: #9CA3AF; font-size: 0.88rem;">Use Enhance Prompt & Gemini multi-candidate loop to discover high-scoring scripts.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Script Generator", key="btn_dash_generate"):
            st.session_state.page = "Generate Script"
            st.rerun()

    with q3:
        st.markdown("""
        <div class="content-card">
            <h4 style="margin-bottom: 8px;">📚 Viral Script Library</h4>
            <p style="color: #9CA3AF; font-size: 0.88rem;">Explore high-engagement benchmark script templates and structural patterns.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Browse Library", key="btn_dash_library"):
            st.session_state.page = "Viral Library"
            st.rerun()
