import streamlit as st
from services.gemini_service import get_gemini_client
from database.crud import get_all_scripts, get_all_predictions

def render():
    st.markdown("""
        <div class="saas-header">
            <div>
                <span class="saas-title">💬 AI Script Advisor & Content Assistant</span>
                <p style="color: #9CA3AF; margin-top: 4px; font-size: 0.9rem;">
                    Chat with an AI content strategist aware of your ML + ANN model evaluations and SQLite project history.
                </p>
            </div>
            <div>
                <span class="saas-badge">RAG AI Advisor</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize Chat History
    if "advisor_messages" not in st.session_state:
        st.session_state.advisor_messages = [
            {
                "role": "assistant",
                "content": "Hello! I am your **ViralIQ AI Advisor**. I analyze your script performance metrics, model evaluations, and viral library patterns. How can I help optimize your content today?"
            }
        ]
        
    # Suggested Prompts
    st.markdown("**Suggested Questions:**")
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    with s_col1:
        if st.button("🪝 How do I make a 3-second hook viral?"):
            st.session_state.user_prompt_input = "How do I make a 3-second hook viral for Instagram Reels?"
    with s_col2:
        if st.button("📉 Why did my script score below 80%?"):
            st.session_state.user_prompt_input = "Why did my recent script score below 80%? What feature metrics failed?"
    with s_col3:
        if st.button("📢 Give me 3 high-converting CTAs"):
            st.session_state.user_prompt_input = "Give me 3 high-converting Call To Action examples for real estate and finance reels."
    with s_col4:
        if st.button("🤖 Explain ML vs ANN model scores"):
            st.session_state.user_prompt_input = "Explain how the Random Forest ML score and Keras ANN score are aggregated."

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display Chat History
    for msg in st.session_state.advisor_messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
            
    # Chat Input
    prompt_in = st.chat_input("Ask ViralIQ Advisor anything about your scripts...")
    
    # Handle suggested prompt click
    if "user_prompt_input" in st.session_state:
        prompt_in = st.session_state.user_prompt_input
        del st.session_state.user_prompt_input

    if prompt_in:
        st.chat_message("user").write(prompt_in)
        st.session_state.advisor_messages.append({"role": "user", "content": prompt_in})
        
        # Context Retrieval from SQLite
        recent_preds = get_all_predictions()[:3]
        ctx_str = ""
        if recent_preds:
            ctx_str = "User's Recent Model Predictions:\n"
            for p in recent_preds:
                ctx_str += f"- Script '{p.get('script_title', 'Untitled')}': ML Score={p['ml_score']}%, ANN Score={p['ann_score']}%, Aggregated Score={p['final_score']}%\n"
                
        api_key = st.session_state.get("gemini_api_key", None)
        
        with st.spinner("AI Advisor analyzing project context..."):
            try:
                model = get_gemini_client(api_key)
                system_prompt = (
                    "You are ViralIQ's AI Content Strategist and Script Advisor.\n"
                    "Provide clear, actionable, concise advice for short-form video creators.\n"
                    "Never fabricate fake model scores. Rely on provided project context.\n\n"
                    f"{ctx_str}\n\n"
                    f"User Question: {prompt_in}"
                )
                res = model.generate_content(system_prompt)
                reply = res.text.strip()
            except Exception as e:
                reply = (
                    f"I evaluated your request. Based on ViralIQ's scoring methodology:\n"
                    f"- High curiosity hooks (containing metrics, 'stop' triggers, or questions) boost retention.\n"
                    f"- Direct engagement CTAs (asking users to comment a specific keyword for DM automation) increase algorithmic velocity.\n"
                    f"(System note: Provide a valid Gemini API Key in Settings to unlock dynamic generative answers)."
                )
                
            st.chat_message("assistant").write(reply)
            st.session_state.advisor_messages.append({"role": "assistant", "content": reply})
