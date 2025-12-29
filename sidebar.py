import streamlit as st
from datetime import datetime

def render_sidebar():
    
    with st.sidebar:
        # Logo
        st.markdown("""
            <div style='text-align: center; padding: 10px 0; margin-top:-20px;'>
                <div style='
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 10px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                '>
                    <h2 style='margin: 0; color: white; font-weight: 700;'>🐚 SISKLASILA </h2>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        # Menu selection dengan radio button
        menu_options = [
            "🔍 Klasifikasi",
            "📈 Model Performance"
        ]
        
        selected_menu = st.radio(
            "Pilih Menu:",
            menu_options,
            label_visibility="collapsed"
        )
    
    return selected_menu