import streamlit as st
import tempfile
import os
from services.ml_service import predict_ml_score
from services.ann_service import predict_ann_score
from utils.scoring import aggregate_scores, get_performance_status
from services.cnn_service import analyze_thumbnail_frame
from services.gemini_service import analyze_script

def render():
    st.markdown("""
        <div class="saas-header">
            <div>
                <span class="saas-title">🎬 Analyze Reel (Video & Visual Intelligence)</span>
                <p style="color: #9CA3AF; margin-top: 4px; font-size: 0.9rem;">
                    Dual Pipeline: Spoken Content Transcript (ML + ANN) & Thumbnail Visual Quality (CNN).
                </p>
            </div>
            <div>
                <span class="saas-badge">Separate CNN Visual Module</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    c_vid, c_res = st.columns([5, 7])
    
    with c_vid:
        st.markdown("### 📹 Upload Video File")
        uploaded_video = st.file_uploader("Upload Reel Video (MP4 / MOV / AVI)", type=["mp4", "mov", "avi", "mkv"])
        
        # Audio / Transcript Input Fallback
        st.markdown("**Spoken Content Transcript:**")
        sample_transcript = st.text_area(
            "Extracted Video Transcript (Auto-extracted or edit manually):",
            value="Stop scrolling if you have 50 Lakhs budget and want a 2BHK luxury flat in city center! Comment 'HOME' for direct location details.",
            height=120
        )
        
        run_reel_analysis = st.button("🚀 Run Reel Analysis (Script ML/ANN + CNN Visual)", use_container_width=True)

    with c_res:
        st.markdown("### 📊 Dual Intelligence Diagnosis")
        
        if run_reel_analysis:
            with st.spinner("Processing Reel Pipelines (Speech Content ML/ANN + Thumbnail CNN)..."):
                # Pipeline 1: Script Intelligence
                ml_score, features = predict_ml_score(sample_transcript)
                ann_score = predict_ann_score(sample_transcript)
                script_score = aggregate_scores(ml_score, ann_score)
                script_status = get_performance_status(script_score)
                
                # Pipeline 2: Thumbnail Visual Intelligence (CNN)
                # Pass frame sample or uploaded file
                cnn_res = analyze_thumbnail_frame(uploaded_video if uploaded_video else "sample")
                visual_score = cnn_res['visual_quality_score']
                
                st.session_state["latest_reel_analysis"] = {
                    'transcript': sample_transcript,
                    'ml_score': ml_score,
                    'ann_score': ann_score,
                    'script_score': script_score,
                    'script_status': script_status,
                    'cnn_res': cnn_res,
                    'visual_score': visual_score
                }
                
        if "latest_reel_analysis" in st.session_state:
            res = st.session_state["latest_reel_analysis"]
            
            # Script Intelligence Box
            st.markdown(f"""
            <div class="content-card" style="border-left: 4px solid #6366F1;">
                <h4 style="margin: 0 0 6px 0; color: #FFFFFF;">🗣️ Pipeline 1: Script Content Intelligence (ML + ANN)</h4>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.8rem; font-weight: 700; color: #FFFFFF;">{res['script_score']}%</span>
                        <span style="color: #9CA3AF; font-size: 0.85rem; margin-left: 10px;">(ML: {res['ml_score']}% | ANN: {res['ann_score']}%)</span>
                    </div>
                    <div>
                        <span class="score-pill score-high">{res['script_status']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Visual Intelligence Box (CNN)
            st.markdown(f"""
            <div class="content-card" style="border-left: 4px solid #10B981;">
                <h4 style="margin: 0 0 6px 0; color: #FFFFFF;">🖼️ Pipeline 2: Visual Thumbnail Intelligence (CNN)</h4>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.8rem; font-weight: 700; color: #FFFFFF;">{res['visual_score']}%</span>
                        <span style="color: #9CA3AF; font-size: 0.85rem; margin-left: 10px;">(Clarity: {res['cnn_res']['clarity_rating']})</span>
                    </div>
                    <div>
                        <span class="score-pill score-high">CNN Visual Quality</span>
                    </div>
                </div>
                <div style="margin-top: 10px; font-size: 0.88rem; color: #D1D5DB;">
                    • <strong>Text Visibility:</strong> {res['cnn_res']['text_visibility']}<br>
                    • <strong>Subject Framing:</strong> {res['cnn_res']['subject_prominence']}<br>
                    • <strong>Recommendation:</strong> {res['cnn_res']['recommendation']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Upload a video or use the sample transcript to trigger the dual-pipeline analysis.")
