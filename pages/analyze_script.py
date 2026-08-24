import streamlit as st
import pandas as pd
import json
from database.crud import create_script, save_prediction, save_report
from database.models import Script, Prediction, Report
from utils.feature_extraction import extract_script_features
from services.ml_service import predict_ml_score
from services.ann_service import predict_ann_score
from utils.scoring import aggregate_scores, get_performance_status
from services.gemini_service import analyze_script, improve_script

def render():
    st.markdown("""
        <div class="saas-header">
            <div>
                <span class="saas-title">🔬 Script Intelligence & Performance Analysis</span>
                <p style="color: #9CA3AF; margin-top: 4px; font-size: 0.9rem;">
                    Evaluate any reel script using trained Scikit-Learn ML and TensorFlow/Keras ANN models.
                </p>
            </div>
            <div>
                <span class="saas-badge">Dual-Model Inference Engine</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    c_left, c_right = st.columns([6, 6])
    
    with c_left:
        st.markdown("### 📝 Input Script")
        
        # Preset Example Selector
        example_choice = st.selectbox(
            "Select an Example Script or Paste Below:",
            ["Custom Script", "Real Estate - 50 Lakh Flat", "Finance - 50/30/20 Rule", "Tech - 3 Secret AI Tools", "Weak Script - Basic Vlog"]
        )
        
        default_text = ""
        if example_choice == "Real Estate - 50 Lakh Flat":
            default_text = "Stop scrolling if you have 50 Lakhs budget and want a dream home! Today we are inside a 2BHK luxury flat with a private balcony and modular kitchen. Located just 10 mins from IT park. Comment 'HOME' below and I will DM you direct location!"
        elif example_choice == "Finance - 50/30/20 Rule":
            default_text = "The 50/30/20 budgeting rule is failing in 2026, do this instead! If you earn ₹60,000 per month, inflation will eat 60% of your paycheck in rent. Use the modified 40-30-30 breakdown smart investors use. Save this reel and share with a friend!"
        elif example_choice == "Tech - 3 Secret AI Tools":
            default_text = "Here are 3 secret AI tools that will double your productivity in 5 minutes! Number 1: Gamma App converts text notes into pitch decks. Number 2: ElevenLabs creates human voiceovers. Comment 'AI' for direct links!"
        elif example_choice == "Weak Script - Basic Vlog":
            default_text = "Hello guys welcome back to my channel. Today I am going to show you my home flat. It has nice rooms and good lighting. Hope you like this video. Call me if interested."
            
        script_title = st.text_input("Script Title", value=example_choice if example_choice != "Custom Script" else "My Reel Draft")
        script_text = st.text_area("Script Content", value=default_text, height=220, placeholder="Paste your reel script here...")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            category = st.selectbox("Category", ["Real Estate", "Finance & Wealth", "Tech & AI", "Fitness & Health", "E-commerce", "Education", "General"])
        with col_m2:
            audience = st.selectbox("Audience", ["First-time Buyers", "Salaried Professionals", "Students & Freelancers", "Fitness Seekers", "General"])
        with col_m3:
            platform = st.selectbox("Platform", ["Instagram", "YouTube Shorts", "TikTok"])
        with col_m4:
            duration = st.number_input("Duration (s)", min_value=15, max_value=90, value=30)
            
        run_analysis = st.button("🚀 Analyze Script Performance", use_container_width=True)

    with c_right:
        st.markdown("### 📊 Performance Diagnosis")
        
        if run_analysis:
            if not script_text.strip():
                st.error("Please enter a valid script text to analyze.")
                return
                
            with st.spinner("Extracting features and running ML + ANN inference..."):
                # 1. Feature extraction
                features = extract_script_features(script_text, target_duration=duration)
                
                # 2. ML model prediction (Scikit-Learn Random Forest)
                ml_score, _ = predict_ml_score(script_text, target_duration=duration)
                
                # 3. ANN model prediction (TensorFlow/Keras)
                ann_score = predict_ann_score(script_text, target_duration=duration)
                
                # 4. Aggregated Score
                score_method = st.session_state.get("score_method", "weighted_average")
                ml_weight = st.session_state.get("ml_weight", 0.5)
                final_score = aggregate_scores(ml_score, ann_score, method=score_method, ml_weight=ml_weight)
                
                status = get_performance_status(final_score)
                
                # 5. Gemini LLM Analysis
                api_key = st.session_state.get("gemini_api_key", None)
                analysis_data = analyze_script(script_text, ml_score, ann_score, final_score, api_key=api_key)
                
                # 6. Save in SQLite DB
                script_obj = Script(
                    id=None,
                    title=script_title,
                    script_text=script_text,
                    category=category,
                    audience=audience,
                    platform=platform,
                    duration=duration
                )
                script_id = create_script(script_obj)
                
                pred_obj = Prediction(
                    id=None,
                    script_id=script_id,
                    ml_score=ml_score,
                    ann_score=ann_score,
                    final_score=final_score,
                    status=status
                )
                save_prediction(pred_obj)
                
                report_obj = Report(
                    id=None,
                    script_id=script_id,
                    analysis=json.dumps(analysis_data),
                    recommendations=json.dumps(analysis_data.get("recommendations", []))
                )
                save_report(report_obj)
                
                st.session_state["latest_analysis"] = {
                    "script_id": script_id,
                    "title": script_title,
                    "script_text": script_text,
                    "ml_score": ml_score,
                    "ann_score": ann_score,
                    "final_score": final_score,
                    "status": status,
                    "features": features,
                    "analysis_data": analysis_data,
                    "category": category,
                    "audience": audience,
                    "platform": platform,
                    "duration": duration
                }
                
        # Display Analysis Results
        if "latest_analysis" in st.session_state:
            res = st.session_state["latest_analysis"]
            
            # Score Header Card
            pill_class = "score-high" if res['final_score'] >= 80 else ("score-moderate" if res['final_score'] >= 65 else "score-low")
            
            st.markdown(f"""
            <div class="content-card" style="border-left: 4px solid {'#10B981' if res['final_score']>=80 else ('#F59E0B' if res['final_score']>=65 else '#EF4444')};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 0.85rem; color: #9CA3AF; font-weight: 600;">PREDICTED PERFORMANCE SCORE</span>
                        <h2 style="font-size: 2.2rem; margin: 0; color: #FFFFFF;">{res['final_score']}%</h2>
                    </div>
                    <div>
                        <span class="score-pill {pill_class}">{res['status']}</span>
                    </div>
                </div>
                <p style="font-size: 0.8rem; color: #6B7280; margin-top: 8px;">
                    *Optimization target: 80%. This score indicates predicted performance potential based on quantitative feature indicators, not a scientific guarantee of virality.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Dual Model Score Breakdown
            s1, s2 = st.columns(2)
            with s1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Scikit-Learn ML Score</div>
                    <div class="metric-value">{res['ml_score']}%</div>
                    <div class="metric-delta delta-positive">Random Forest Model</div>
                </div>
                """, unsafe_allow_html=True)
            with s2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Keras ANN Score</div>
                    <div class="metric-value">{res['ann_score']}%</div>
                    <div class="metric-delta delta-positive">Deep Neural Network</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Feature Breakdown Tabs
            t_feat, t_llm = st.tabs(["🔍 Extracted Features", "🧠 AI Qualitative Critique"])
            
            with t_feat:
                df_f = pd.DataFrame(list(res['features'].items()), columns=["Feature Metric", "Extracted Value"])
                st.dataframe(df_f, use_container_width=True, hide_index=True)
                
            with t_llm:
                crit = res['analysis_data']
                st.markdown(f"**🪝 Hook Analysis:** {crit.get('hook_critique', 'N/A')}")
                st.markdown(f"**⏱️ Body Pacing:** {crit.get('body_pacing', 'N/A')}")
                st.markdown(f"**🎯 CTA Strength:** {crit.get('cta_strength', 'N/A')}")
                
                st.markdown("**⚠️ Weaknesses:**")
                for w in crit.get('weaknesses', []):
                    st.markdown(f"- {w}")
                    
                st.markdown("**💡 Actionable Recommendations:**")
                for r in crit.get('recommendations', []):
                    st.markdown(f"- {r}")

            # Optimization Action Trigger
            if res['final_score'] < 80.0:
                st.warning("Score is below the 80% optimization target. Launch the Multi-Candidate Optimization Loop to generate higher-scoring candidates!")
                if st.button("✨ Optimize Script via Multi-Candidate Engine", use_container_width=True):
                    st.session_state.informal_input_prompt = res['script_text']
                    st.session_state.opt_category = res['category']
                    st.session_state.opt_audience = res['audience']
                    st.session_state.opt_platform = res['platform']
                    st.session_state.opt_duration = res['duration']
                    st.session_state.page = "Generate Script"
                    st.rerun()
        else:
            st.info("Paste or select a script on the left and click **Analyze Script Performance** to view ML + ANN diagnosis.")
