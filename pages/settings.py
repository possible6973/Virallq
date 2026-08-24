import streamlit as st
import os
from services.ml_service import train_ml_model
from services.ann_service import train_ann_model
from database.db import init_db

def render():
    st.markdown("""
        <div class="saas-header">
            <div>
                <span class="saas-title">⚙️ System Configuration & Model Management</span>
                <p style="color: #9CA3AF; margin-top: 4px; font-size: 0.9rem;">
                    Configure Gemini API credentials, score aggregation parameters, and model retrain pipelines.
                </p>
            </div>
            <div>
                <span class="saas-badge">System Settings</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔑 1. Gemini API Credentials")
    env_key = os.environ.get("GEMINI_API_KEY", "")
    user_key = st.text_input(
        "Gemini API Key (GEMINI_API_KEY)",
        value=st.session_state.get("gemini_api_key", env_key),
        type="password",
        help="Enter your Google Gemini API key. Never hard-code secrets."
    )
    st.session_state["gemini_api_key"] = user_key
    
    if st.button("🧪 Test Gemini API Connection"):
        if not user_key:
            st.error("Please enter a valid Gemini API key.")
        else:
            try:
                import google.generativeai as genai
                genai.configure(api_key=user_key)
                m = genai.GenerativeModel("gemini-3.6-flash")
                res = m.generate_content("Ping")
                st.success("✅ Gemini API connected successfully!")
            except Exception as e:
                st.error(f"API Connection Failed: {str(e)}")
                
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("### 🧮 2. Score Aggregation Layer Configuration")
    
    score_method = st.selectbox(
        "Aggregation Method:",
        ["weighted_average", "harmonic_mean", "min", "max"],
        index=0,
        help="weighted_average: ml_weight*ML + (1-ml_weight)*ANN. harmonic_mean: penalizes model disagreement."
    )
    st.session_state["score_method"] = score_method
    
    if score_method == "weighted_average":
        ml_weight = st.slider("ML Model Weight vs ANN Weight", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
        st.session_state["ml_weight"] = ml_weight
        st.info(f"Current Aggregation: **{int(ml_weight*100)}% ML (Random Forest) + {int((1-ml_weight)*100)}% ANN (Keras)**")
        
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("### 🔄 3. Model Re-training Pipeline")
    
    col_tr1, col_tr2 = st.columns(2)
    with col_tr1:
        if st.button("🌲 Re-Train ML Model (Scikit-Learn)", use_container_width=True):
            with st.spinner("Training Random Forest Classifier on dataset..."):
                m = train_ml_model()
                st.success(f"ML Model trained! Accuracy: {m['accuracy']}%")
    with col_tr2:
        if st.button("🧠 Re-Train ANN Model (Keras + EarlyStopping)", use_container_width=True):
            with st.spinner("Training Keras Neural Network with EarlyStopping..."):
                m = train_ann_model()
                st.success(f"ANN Model trained after {m['epochs_trained']} epochs! Accuracy: {m['accuracy']}%")
