import streamlit as st
import pandas as pd
from database.crud import get_all_scripts, get_script_by_id, update_script, delete_script, create_script
from database.models import Script

def render():
    st.markdown("""
        <div class="saas-header">
            <div>
                <span class="saas-title">📂 My Scripts Management (SQLite CRUD)</span>
                <p style="color: #9CA3AF; margin-top: 4px; font-size: 0.9rem;">
                    Full Create, Read, Update, and Delete operations for user script records in SQLite.
                </p>
            </div>
            <div>
                <span class="saas-badge">SQLite Database CRUD</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Top Action Row
    c_btn1, c_btn2 = st.columns([8, 4])
    with c_btn2:
        with st.expander("➕ Create New Script Record"):
            with st.form("create_new_script_form"):
                new_title = st.text_input("Script Title")
                new_category = st.selectbox("Category", ["Real Estate", "Finance & Wealth", "Tech & AI", "Fitness & Health", "E-commerce", "Education", "General"])
                new_audience = st.text_input("Audience", value="General")
                new_platform = st.selectbox("Platform", ["Instagram", "YouTube Shorts", "TikTok"])
                new_dur = st.number_input("Duration (s)", value=30)
                new_text = st.text_area("Script Content")
                
                btn_sub = st.form_submit_button("Save Script to DB")
                if btn_sub:
                    if not new_title or not new_text:
                        st.error("Title and Script Content are required.")
                    else:
                        create_script(Script(
                            id=None,
                            title=new_title,
                            script_text=new_text,
                            category=new_category,
                            audience=new_audience,
                            platform=new_platform,
                            duration=new_dur
                        ))
                        st.success("Script created successfully in SQLite DB!")
                        st.rerun()

    scripts = get_all_scripts()
    
    if not scripts:
        st.info("No saved scripts found in database. Create a script or generate one using the AI Generator!")
        return
        
    df_s = pd.DataFrame(scripts)
    st.markdown(f"**Total Script Records in Database:** {len(df_s)}")
    
    # Table View
    st.dataframe(
        df_s[['id', 'title', 'category', 'platform', 'duration', 'created_at']],
        column_config={
            "id": "ID",
            "title": "Script Title",
            "category": "Category",
            "platform": "Platform",
            "duration": "Duration (s)",
            "created_at": "Created At"
        },
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ✏️ View, Edit, or Delete Script Record")
    
    script_ids = [s['id'] for s in scripts]
    selected_id = st.selectbox("Select Script ID to Manage:", script_ids, format_func=lambda x: f"ID #{x} — {next(s['title'] for s in scripts if s['id']==x)}")
    
    target_script = get_script_by_id(selected_id)
    
    if target_script:
        with st.form("edit_script_form"):
            st.markdown(f"**Editing Script ID #{target_script['id']}**")
            
            e_title = st.text_input("Title", value=target_script['title'])
            col_e1, col_e2, col_e3 = st.columns(3)
            with col_e1:
                e_category = st.selectbox("Category", ["Real Estate", "Finance & Wealth", "Tech & AI", "Fitness & Health", "E-commerce", "Education", "General"], index=["Real Estate", "Finance & Wealth", "Tech & AI", "Fitness & Health", "E-commerce", "Education", "General"].index(target_script.get('category', 'General')) if target_script.get('category') in ["Real Estate", "Finance & Wealth", "Tech & AI", "Fitness & Health", "E-commerce", "Education", "General"] else 0)
            with col_e2:
                e_audience = st.text_input("Audience", value=target_script.get('audience', 'General'))
            with col_e3:
                e_dur = st.number_input("Duration (s)", value=int(target_script.get('duration', 30)))
                
            e_platform = st.selectbox("Platform", ["Instagram", "YouTube Shorts", "TikTok"], index=0)
            e_text = st.text_area("Script Content", value=target_script['script_text'], height=180)
            
            b_update, b_delete = st.columns(2)
            with b_update:
                update_clicked = st.form_submit_button("💾 Save Updates (Update CRUD)", use_container_width=True)
            with b_delete:
                delete_clicked = st.form_submit_button("🗑️ Delete Script (Delete CRUD)", use_container_width=True)
                
            if update_clicked:
                res = update_script(
                    script_id=selected_id,
                    title=e_title,
                    script_text=e_text,
                    category=e_category,
                    audience=e_audience,
                    platform=e_platform,
                    duration=e_dur
                )
                if res:
                    st.success(f"Script #{selected_id} updated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to update script.")
                    
            if delete_clicked:
                res = delete_script(selected_id)
                if res:
                    st.success(f"Script #{selected_id} deleted successfully from SQLite database!")
                    st.rerun()
                else:
                    st.error("Failed to delete script.")
