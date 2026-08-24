import streamlit as st
import pandas as pd
import json
from database.crud import get_all_reports, get_all_scripts, get_script_by_id, get_predictions_for_script
from services.gemini_service import generate_report

def render():
    st.markdown("""
        <div class="saas-header">
            <div>
                <span class="saas-title">📑 Script Performance Reports</span>
                <p style="color: #9CA3AF; margin-top: 4px; font-size: 0.9rem;">
                    Generate and download executive script performance audit reports.
                </p>
            </div>
            <div>
                <span class="saas-badge">Automated Report Generator</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    scripts = get_all_scripts()
    if not scripts:
        st.info("No script records found to generate reports for.")
        return
        
    script_map = {s['id']: f"#{s['id']} — {s['title']}" for s in scripts}
    selected_script_id = st.selectbox("Select Script to Audit & Generate Report:", list(script_map.keys()), format_func=lambda x: script_map[x])
    
    s_data = get_script_by_id(selected_script_id)
    preds = get_predictions_for_script(selected_script_id)
    
    if not preds:
        st.warning("This script has not been analyzed yet. Run analysis first in **Analyze Script**.")
        return
        
    p_data = preds[0] # latest prediction
    
    gen_report = st.button("📄 Generate Comprehensive Report", use_container_width=True)
    
    if gen_report or "current_report_md" in st.session_state:
        if gen_report:
            api_key = st.session_state.get("gemini_api_key", None)
            dummy_crit = {
                "hook_critique": "Strong opening hook with curiosity metric.",
                "body_pacing": "Fast-paced with direct bullet points.",
                "cta_strength": "Direct keyword comment call to action.",
                "weaknesses": ["Minor filler words in body sentence 2"],
                "recommendations": ["Add direct urgency keyword in opening line"]
            }
            report_md = generate_report(
                script_title=s_data['title'],
                script_text=s_data['script_text'],
                ml_score=p_data['ml_score'],
                ann_score=p_data['ann_score'],
                final_score=p_data['final_score'],
                analysis=dummy_crit,
                api_key=api_key
            )
            st.session_state["current_report_md"] = report_md
            
        report_text = st.session_state["current_report_md"]
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="content-card">
        """, unsafe_allow_html=True)
        st.markdown(report_text)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Download Option
        st.download_button(
            label="💾 Download Markdown Report (.md)",
            data=report_text,
            file_name=f"ViralIQ_Report_{s_data['title'].replace(' ', '_')}.md",
            mime="text/markdown"
        )
