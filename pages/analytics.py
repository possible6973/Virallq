import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from services.ml_service import get_ml_metrics
from services.ann_service import get_ann_metrics
from database.crud import get_all_predictions

def render():
    st.markdown("""
        <div class="saas-header">
            <div>
                <span class="saas-title">📈 Academic & Model Evaluation Analytics</span>
                <p style="color: #9CA3AF; margin-top: 4px; font-size: 0.9rem;">
                    Empirical performance metrics, confusion matrices, and loss curves for ML (AI-503) and ANN (AI-505).
                </p>
            </div>
            <div>
                <span class="saas-badge">Empirical AI Metrics</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Load Model Metrics
    ml_metrics = get_ml_metrics()
    ann_metrics = get_ann_metrics()
    
    # Metric Summary Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ML Accuracy (Random Forest)</div>
            <div class="metric-value">{ml_metrics.get('accuracy', 0.0)}%</div>
            <div class="metric-delta delta-positive">Precision: {ml_metrics.get('precision', 0.0)}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ANN Accuracy (Keras)</div>
            <div class="metric-value">{ann_metrics.get('accuracy', 0.0)}%</div>
            <div class="metric-delta delta-positive">Recall: {ann_metrics.get('recall', 0.0)}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ANN Epochs Trained</div>
            <div class="metric-value">{ann_metrics.get('epochs_trained', 0)}</div>
            <div class="metric-delta delta-positive">Stopped via EarlyStopping</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ANN Validation Loss</div>
            <div class="metric-value">{ann_metrics.get('final_val_loss', 0.0)}</div>
            <div class="metric-delta delta-positive">Binary Crossentropy</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    t1, t2, t3 = st.tabs(["🤖 ML & ANN Model Comparison", "📉 ANN EarlyStopping Loss Curves", "🌲 Feature Importances"])
    
    with t1:
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("### ML vs ANN Score Correlation")
            preds = get_all_predictions()
            if preds:
                df_p = pd.DataFrame(preds)
                fig_scat = px.scatter(
                    df_p,
                    x='ml_score',
                    y='ann_score',
                    color='final_score',
                    hover_data=['script_title', 'status'],
                    labels={'ml_score': 'Random Forest ML Score (%)', 'ann_score': 'Keras ANN Score (%)'},
                    color_continuous_scale='Purples'
                )
                fig_scat.add_shape(
                    type="line", x0=0, y0=0, x1=100, y1=100,
                    line=dict(color="#6B7280", dash="dash")
                )
                fig_scat.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#F3F4F6')
                )
                st.plotly_chart(fig_scat, use_container_width=True)
            else:
                st.info("No prediction data available yet for correlation plotting.")
                
        with c2:
            st.markdown("### Model Confusion Matrix (Random Forest)")
            cm = ml_metrics.get('confusion_matrix', [[50, 0], [0, 50]])
            df_cm = pd.DataFrame(cm, index=["Actual Low", "Actual High"], columns=["Pred Low", "Pred High"])
            
            fig_cm = px.imshow(
                df_cm,
                text_auto=True,
                color_continuous_scale='Viridis',
                labels=dict(x="Predicted Label", y="Actual Label", color="Count")
            )
            fig_cm.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#F3F4F6')
            )
            st.plotly_chart(fig_cm, use_container_width=True)

    with t2:
        st.markdown("### Keras ANN Training & Validation Loss (EarlyStopping Profile)")
        hist = ann_metrics.get('history', {})
        if hist and 'loss' in hist:
            epochs = list(range(1, len(hist['loss']) + 1))
            fig_loss = go.Figure()
            fig_loss.add_trace(go.Scatter(x=epochs, y=hist['loss'], mode='lines+markers', name='Training Loss', line=dict(color='#8B5CF6')))
            fig_loss.add_trace(go.Scatter(x=epochs, y=hist['val_loss'], mode='lines+markers', name='Validation Loss', line=dict(color='#10B981', dash='dash')))
            
            fig_loss.update_layout(
                xaxis_title="Epoch",
                yaxis_title="Loss (Binary Crossentropy)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#F3F4F6'),
                legend=dict(font=dict(color='#9CA3AF'))
            )
            st.plotly_chart(fig_loss, use_container_width=True)
        else:
            st.info("ANN history metrics unavailable. Re-train ANN model in Settings to refresh loss curves.")

    with t3:
        st.markdown("### Scikit-Learn Feature Importances")
        fi = ml_metrics.get('feature_importances', {})
        if fi:
            df_fi = pd.DataFrame(list(fi.items()), columns=['Feature Metric', 'Importance Score']).sort_values('Importance Score', ascending=True)
            fig_fi = px.bar(
                df_fi,
                x='Importance Score',
                y='Feature Metric',
                orientation='h',
                color='Importance Score',
                color_continuous_scale='Purples'
            )
            fig_fi.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#F3F4F6')
            )
            st.plotly_chart(fig_fi, use_container_width=True)
