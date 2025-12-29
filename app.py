import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from sidebar import render_sidebar
from PIL import Image
import io

# Konfigurasi halaman
st.set_page_config(
    page_title="Klasifikasi Siput Laut",
    page_icon="🐚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #1e3a8a;
        font-weight: 700;
    }
    h2, h3 {
        color: #2563eb;
    }
    
    /* Sidebar Dark Theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #2d3748 !important;
    }
    
    /* Upload Box Styling */
    .upload-box {
        background: white;
        padding: 40px;
        border-radius: 15px;
        border: 3px dashed #3b82f6;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* Result Card */
    .result-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #10b981;
    }
    </style>
""", unsafe_allow_html=True)

# Render Sidebar dan dapatkan menu yang dipilih
selected_menu = render_sidebar()

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🐚 Sistem Klasifikasi Siput Laut")
with col2:
    st.write("")
    st.write("")
    st.info(f"📅 {datetime.now().strftime('%d %B %Y')}")

# ==================== MENU 1: KLASIFIKASI ====================
if selected_menu == "🔍 Klasifikasi":
    st.markdown("---")
    
    # Upload Section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Gambar Siput Laut")
        
        uploaded_file = st.file_uploader(
            "Pilih gambar siput laut (JPG, PNG, JPEG)",
            type=['jpg', 'jpeg', 'png'],
            help="Upload gambar siput laut untuk diklasifikasi"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Gambar yang di-upload", use_container_width=True)
            
            # Tombol Klasifikasi
            if st.button("🚀 Mulai Klasifikasi", type="primary", use_container_width=True):
                with st.spinner("Sedang menganalisis gambar..."):
                    # Simulasi proses klasifikasi
                    import time
                    time.sleep(2)
                    
                    # Hasil klasifikasi (dummy data)
                    st.session_state['classification_done'] = True
                    st.session_state['predicted_class'] = "Conus striatus"
                    st.session_state['confidence'] = 94.8
                    st.session_state['predictions'] = {
                        "Conus striatus": 94.8,
                        "Conus textile": 3.2,
                        "Conus geographus": 1.5,
                        "Conus marmoreus": 0.3,
                        "Conus magus": 0.2
                    }
        else:
            st.markdown("""
                <div class='upload-box'>
                    <h3>📸 Upload Gambar</h3>
                    <p>Drag and drop atau klik untuk memilih gambar</p>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Hasil Klasifikasi")
        
        if 'classification_done' in st.session_state and st.session_state['classification_done']:
            # Result Card
            st.markdown(f"""
                <div class='result-card'>
                    <h2 style='color: #10b981; margin: 0;'>✓ Klasifikasi Berhasil!</h2>
                    <hr style='border-color: #d1d5db;'>
                    <h3 style='color: #1e3a8a;'>Spesies: {st.session_state['predicted_class']}</h3>
                    <h4 style='color: #6b7280;'>Confidence: {st.session_state['confidence']}%</h4>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            
            # Probability Chart
            st.markdown("#### 📈 Probabilitas untuk Setiap Kelas")
            
            pred_df = pd.DataFrame(
                list(st.session_state['predictions'].items()),
                columns=['Spesies', 'Probabilitas']
            )
            
            fig = px.bar(
                pred_df,
                x='Probabilitas',
                y='Spesies',
                orientation='h',
                color='Probabilitas',
                color_continuous_scale='Blues',
                text='Probabilitas'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#1e3a8a'),
                xaxis=dict(showgrid=True, gridcolor='#e5e7eb', range=[0, 100]),
                yaxis=dict(showgrid=False),
                showlegend=False,
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Additional Info
            with st.expander("ℹ️ Informasi Spesies"):
                st.markdown(f"""
                **{st.session_state['predicted_class']}**
                
                - **Famili**: Conidae
                - **Habitat**: Perairan tropis Indo-Pasifik
                - **Karakteristik**: Memiliki cangkang berbentuk kerucut dengan pola garis-garis
                - **Status Konservasi**: Least Concern (LC)
                - **Bahaya**: Berbisa, harus ditangani dengan hati-hati
                """)
        else:
            st.info("👆 Upload gambar terlebih dahulu untuk melihat hasil klasifikasi")
    
    # Riwayat Klasifikasi
    st.markdown("---")
    st.markdown("### 📜 Riwayat Klasifikasi Terakhir")
    
    history_data = {
        'Timestamp': [''],
        'Spesies': [''],
        'Confidence': ['']
    }
    
    df_history = pd.DataFrame(history_data)
    st.dataframe(df_history, use_container_width=True, hide_index=True)

# ==================== MENU 2: MODEL PERFORMANCE ====================
elif selected_menu == "📈 Model Performance":
    st.markdown("---")
    
    # Metrics Overview
    st.markdown("### 📊 Metrik Performa Model")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Accuracy",
            value="95.3%",
            delta="2.1%"
        )
    
    with col2:
        st.metric(
            label="📊 Precision",
            value="94.7%",
            delta="1.8%"
        )
    
    with col3:
        st.metric(
            label="🔍 Recall",
            value="95.1%",
            delta="2.3%"
        )
    
    with col4:
        st.metric(
            label="⚖️ F1-Score",
            value="94.9%",
            delta="2.0%"
        )
    
    st.markdown("---")
    
    # Confusion Matrix
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 🎯 Confusion Matrix")
        
        # Generate confusion matrix data
        classes = ['C. striatus', 'C. textile', 'C. geographus', 'C. marmoreus', 'C. magus']
        conf_matrix = np.array([
            [95, 2, 1, 1, 1],
            [3, 92, 2, 2, 1],
            [1, 2, 96, 1, 0],
            [2, 3, 1, 93, 1],
            [1, 1, 0, 2, 96]
        ])
        
        fig_cm = go.Figure(data=go.Heatmap(
            z=conf_matrix,
            x=classes,
            y=classes,
            colorscale='Blues',
            text=conf_matrix,
            texttemplate='%{text}',
            textfont={"size": 14},
            showscale=True
        ))
        
        fig_cm.update_layout(
            xaxis_title="Predicted",
            yaxis_title="Actual",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#1e3a8a'),
            height=500
        )
        
        st.plotly_chart(fig_cm, use_container_width=True)
    
    with col2:
        st.markdown("### 📉 Classification Report")
        
        report_data = {
            'Class': classes,
            'Precision': [0.95, 0.92, 0.96, 0.93, 0.96],
            'Recall': [0.95, 0.92, 0.96, 0.93, 0.96],
            'F1-Score': [0.95, 0.92, 0.96, 0.93, 0.96],
            'Support': [100, 100, 100, 100, 100]
        }
        
        df_report = pd.DataFrame(report_data)
        st.dataframe(df_report, use_container_width=True, hide_index=True)
        
        # st.markdown("#### 📌 Kesimpulan")
        # st.success("""
        # Model menunjukkan performa yang sangat baik dengan:
        # - Akurasi keseluruhan 95.3%
        # - Konsistensi tinggi di semua kelas
        # - C. geographus memiliki performa terbaik (96%)
        # """)
    
    st.markdown("---")
    
    # Training History
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Training & Validation Accuracy")
        
        epochs = list(range(1, 51))
        train_acc = [0.7 + (0.25 * (1 - np.exp(-i/10))) + np.random.uniform(-0.02, 0.02) for i in epochs]
        val_acc = [0.65 + (0.28 * (1 - np.exp(-i/12))) + np.random.uniform(-0.03, 0.03) for i in epochs]
        
        fig_acc = go.Figure()
        fig_acc.add_trace(go.Scatter(x=epochs, y=train_acc, mode='lines', name='Training', line=dict(color='#3b82f6', width=3)))
        fig_acc.add_trace(go.Scatter(x=epochs, y=val_acc, mode='lines', name='Validation', line=dict(color='#10b981', width=3)))
        
        fig_acc.update_layout(
            xaxis_title="Epoch",
            yaxis_title="Accuracy",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#1e3a8a'),
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            yaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            legend=dict(x=0.7, y=0.1),
            height=400
        )
        
        st.plotly_chart(fig_acc, use_container_width=True)
    
    with col2:
        st.markdown("### 📉 Training & Validation Loss")
        
        train_loss = [1.5 * np.exp(-i/8) + np.random.uniform(-0.05, 0.05) for i in epochs]
        val_loss = [1.6 * np.exp(-i/9) + np.random.uniform(-0.06, 0.06) for i in epochs]
        
        fig_loss = go.Figure()
        fig_loss.add_trace(go.Scatter(x=epochs, y=train_loss, mode='lines', name='Training', line=dict(color='#ef4444', width=3)))
        fig_loss.add_trace(go.Scatter(x=epochs, y=val_loss, mode='lines', name='Validation', line=dict(color='#f97316', width=3)))
        
        fig_loss.update_layout(
            xaxis_title="Epoch",
            yaxis_title="Loss",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#1e3a8a'),
            xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            yaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
            legend=dict(x=0.7, y=0.9),
            height=400
        )
        
        st.plotly_chart(fig_loss, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6b7280;'>
        <p>🐚 Sistem Klasifikasi Siput Laut v1.0 | Powered by Deep Learning & Streamlit</p>
    </div>
""", unsafe_allow_html=True)