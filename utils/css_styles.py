def get_saas_theme_css() -> str:
    return """
    <style>
    /* Premium Linear/Vercel Dark Palette */
    :root {
        --bg-main: #0B0E14;
        --bg-card: #131822;
        --bg-hover: #1A202C;
        --border-color: #232D3F;
        --accent-primary: #6366F1;
        --accent-glow: rgba(99, 102, 241, 0.15);
        --text-primary: #F3F4F6;
        --text-secondary: #9CA3AF;
        --text-muted: #6B7280;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
    }
    
    /* Main App Container Styling */
    .stApp {
        background-color: var(--bg-main);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0F131C;
        border-right: 1px solid var(--border-color);
    }
    
    /* Premium Header Title Bar */
    .saas-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 0;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
    }
    
    .saas-title {
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .saas-badge {
        background: rgba(99, 102, 241, 0.12);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Metric Cards */
    .metric-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.25rem;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    
    .metric-card:hover {
        border-color: var(--accent-primary);
        transform: translateY(-2px);
    }
    
    .metric-label {
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--text-secondary);
        margin-bottom: 0.4rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.02em;
    }

    .metric-delta {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }
    .delta-positive { color: var(--success); }
    .delta-warning { color: var(--warning); }
    
    /* Content Cards */
    .content-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
    }
    
    /* Custom Score Badges */
    .score-pill {
        display: inline-flex;
        align-items: center;
        padding: 0.3rem 0.8rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .score-high {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .score-moderate {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .score-low {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }

    /* Primary Accent Button Customization */
    div.stButton > button {
        background-color: var(--accent-primary) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background-color: #4F46E5 !important;
        box-shadow: 0 0 12px var(--accent-glow) !important;
    }
    
    /* Enhance Prompt Special Button */
    .enhance-btn-wrap div.stButton > button {
        background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(139, 92, 246, 0.3) !important;
    }

    /* Batch Optimization Step Container */
    .batch-step-box {
        border-left: 3px solid var(--accent-primary);
        background: rgba(19, 24, 34, 0.8);
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.8rem;
    }
    
    /* Hide Streamlit Default Menu Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
