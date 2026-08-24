import streamlit as st
import pandas as pd
from services.prompt_service import enhance_user_prompt
from services.optimization_service import BatchOptimizationEngine
from database.crud import create_script, save_prediction
from database.models import Script, Prediction

def render():
    st.markdown("""
        <div class="saas-header">
            <div>
                <span class="saas-title">✨ AI Script Generator & Multi-Candidate Optimization</span>
                <p style="color: #9CA3AF; margin-top: 4px; font-size: 0.9rem;">
                    Prompt Engineering + Gemini LLM Candidate Generation + ML/ANN Dual-Model Evaluation Loop.
                </p>
            </div>
            <div>
                <span class="saas-badge">Multi-Candidate Optimization Loop</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_input, col_output = st.columns([5, 7])
    
    with col_input:
        st.markdown("### 🎯 Script Generation Requirements")
        
        # Informal user input
        default_informal = st.session_state.get("informal_input_prompt", "real estate 50 lakh na ghar sale")
        informal_text = st.text_area(
            "Informal Idea / Natural Prompt",
            value=default_informal,
            height=100,
            help="Enter any informal idea, e.g. 'real estate 50 lakh na ghar sale' or 'how to save tax in salary'."
        )
        
        # Structured Fields
        c1, c2 = st.columns(2)
        with c1:
            category = st.selectbox("Category", ["Real Estate", "Finance & Wealth", "Tech & AI", "Fitness & Health", "E-commerce", "Education", "General"], index=0)
            audience = st.selectbox("Audience", ["First-time Buyers", "Salaried Professionals", "Students & Freelancers", "Fitness Seekers", "Entrepreneurs", "General"], index=0)
            platform = st.selectbox("Platform", ["Instagram", "YouTube Shorts", "TikTok"], index=0)
            duration = st.number_input("Target Duration (seconds)", min_value=15, max_value=90, value=30)
        with c2:
            goal = st.selectbox("CTA Goal", ["Lead Generation (Comment keyword)", "Direct Sales (Link in Bio)", "Follow & Audience Growth", "Save & Share Viral Reach"])
            tone = st.selectbox("Tone", ["High Energy & Urgency", "Professional & Authoritative", "Storytelling & Relatable", "Curious & Intriguing"])
            language = st.selectbox("Language", ["Hinglish / Mixed English", "Pure English", "Hindi"])
            content_type = st.selectbox("Content Type", ["Listicle / 3 Secrets", "Problem-Solution Breakdown", "Myth Busting", "Property / Product Showcase"])

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Grammarly-style ✨ Enhance Prompt Button
        st.markdown('<div class="enhance-btn-wrap">', unsafe_allow_html=True)
        btn_enhance = st.button("✨ Enhance Prompt (Grammarly-Style Prompt Engineering)", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if btn_enhance:
            if not informal_text.strip():
                st.error("Please enter an informal prompt first.")
            else:
                with st.spinner("Transforming informal request into structured Prompt Engineering framework..."):
                    api_key = st.session_state.get("gemini_api_key", None)
                    enhanced = enhance_user_prompt(
                        informal_text=informal_text,
                        category=category,
                        audience=audience,
                        platform=platform,
                        duration=duration,
                        api_key=api_key
                    )
                    st.session_state["enhanced_prompt_preview"] = enhanced
                    
        # Enhanced Prompt Preview Box
        if "enhanced_prompt_preview" in st.session_state:
            st.markdown("### 📑 Enhanced Prompt Preview")
            
            enhanced_editable = st.text_area(
                "Structured Prompt (Preview & Edit):",
                value=st.session_state["enhanced_prompt_preview"],
                height=220
            )
            st.session_state["enhanced_prompt_preview"] = enhanced_editable
            
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                if st.button("📋 Copy Prompt Text"):
                    st.toast("Prompt copied to clipboard!", icon="✅")
            with b_col2:
                if st.button("👍 Use This Enhanced Prompt"):
                    st.toast("Enhanced prompt locked for candidate generation!", icon="🎯")

    with col_output:
        st.markdown("### ⚡ Multi-Candidate Optimization Engine")
        
        # Configurable Settings Expander
        with st.expander("⚙️ Optimization Loop Settings (Configurable)", expanded=False):
            cfg_batch_size = st.slider("Candidate Batch Size (N candidates / batch)", min_value=3, max_value=20, value=5)
            cfg_target_score = st.slider("Target Performance Threshold (%)", min_value=60, max_value=95, value=80)
            cfg_max_batches = st.slider("Maximum Batches (Safe Upper Limit)", min_value=1, max_value=10, value=5)
            
        btn_generate = st.button("🔥 Generate & Evaluate Best Script (Launch Loop)", use_container_width=True)
        
        if btn_generate:
            prompt_to_use = st.session_state.get("enhanced_prompt_preview", "")
            if not prompt_to_use:
                # Auto enhance if user clicked generate directly
                api_key = st.session_state.get("gemini_api_key", None)
                prompt_to_use = enhance_user_prompt(informal_text, category, audience, platform, duration, api_key)
                st.session_state["enhanced_prompt_preview"] = prompt_to_use
                
            engine = BatchOptimizationEngine(
                batch_size=cfg_batch_size,
                target_score=float(cfg_target_score),
                max_batches=cfg_max_batches,
                score_method=st.session_state.get("score_method", "weighted_average"),
                ml_weight=st.session_state.get("ml_weight", 0.5)
            )
            
            progress_placeholder = st.empty()
            api_key = st.session_state.get("gemini_api_key", None)
            
            def on_progress(info):
                with progress_placeholder.container():
                    st.markdown(f"""
                    <div class="batch-step-box">
                        <strong>Batch {info['current_batch']} of {info['max_batches']}</strong> | Evaluated {cfg_batch_size} candidates.<br>
                        <span style="color: #9CA3AF;">Batch Peak Score:</span> <strong>{info['batch_best']}%</strong> | 
                        <span style="color: #6366F1;">Global Highest Score:</span> <strong>{info['global_best']}%</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
            with st.spinner("Executing Multi-Candidate Optimization Loop across Gemini + ML + ANN..."):
                opt_res = engine.optimize_script_generation(
                    enhanced_prompt=prompt_to_use,
                    category=category,
                    api_key=api_key,
                    progress_callback=on_progress
                )
                
            st.session_state["latest_optimization"] = opt_res
            
            # Save winner to DB
            best = opt_res['global_best']
            script_id = create_script(Script(
                id=None,
                title=f"{category} Optimized Reel",
                script_text=best['script_text'],
                category=category,
                audience=audience,
                platform=platform,
                duration=duration
            ))
            save_prediction(Prediction(
                id=None,
                script_id=script_id,
                ml_score=best['ml_score'],
                ann_score=best['ann_score'],
                final_score=best['final_score'],
                status=best['status']
            ))
            
        # Display Optimization Results
        if "latest_optimization" in st.session_state:
            opt = st.session_state["latest_optimization"]
            best = opt['global_best']
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🏆 Global Best Candidate (Winner)")
            
            status_color = "#10B981" if best['final_score'] >= 80 else "#F59E0B"
            
            st.markdown(f"""
            <div class="content-card" style="border: 2px solid {status_color}; background: #151C28;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div>
                        <span class="saas-badge" style="background: rgba(16,185,129,0.15); color: #34D399;">
                            Found in Batch {best['batch_number']} (Candidate #{best['candidate_number']})
                        </span>
                        <h3 style="margin: 6px 0 0 0; color: #FFFFFF;">Global Best Performance Score: {best['final_score']}%</h3>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 0.85rem; color: #9CA3AF;">ML: {best['ml_score']}% | ANN: {best['ann_score']}%</span>
                    </div>
                </div>
                <div style="background: #0B0E14; padding: 1rem; border-radius: 8px; border: 1px solid #232D3F; font-family: monospace; white-space: pre-wrap; color: #F3F4F6;">
{best['script_text']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if opt['target_achieved']:
                st.success(f"🎯 Optimization Target ({cfg_target_score}%) achieved in Batch {best['batch_number']}!")
            else:
                st.info(f"Reached maximum configured batches ({opt['total_batches_run']}). Returned the highest-scoring candidate found across all {opt['total_candidates_evaluated']} evaluated candidates ({best['final_score']}%).")
                
            # Candidate Comparison Table
            with st.expander("📊 Candidate Batch Progression & Comparison"):
                st.markdown(f"**Total Candidates Evaluated:** {opt['total_candidates_evaluated']} across {opt['total_batches_run']} batches")
                
                df_all = pd.DataFrame(opt['all_candidates'])
                st.dataframe(
                    df_all[['batch_number', 'candidate_number', 'ml_score', 'ann_score', 'final_score', 'status']],
                    column_config={
                        "batch_number": "Batch #",
                        "candidate_number": "Candidate #",
                        "ml_score": st.column_config.NumberColumn("ML Score", format="%.1f%%"),
                        "ann_score": st.column_config.NumberColumn("ANN Score", format="%.1f%%"),
                        "final_score": st.column_config.NumberColumn("Final Score", format="%.1f%%"),
                        "status": "Status"
                    },
                    use_container_width=True,
                    hide_index=True
                )
