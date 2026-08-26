import streamlit as st

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Math Lab",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CUSTOM CSS
# ============================================
css_code = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Hide Streamlit Branding & Controls */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Reduce Streamlit container default top padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 1200px;
    }
    
    /* === MAIN BACKGROUND === */
    .stApp {
        background: #f8fafc;
    }
    
    /* === TOP NAV === */
    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.6rem 0 0.6rem 0;
        border-bottom: 1px solid #e8ecf0;
        margin-bottom: 1.2rem;
    }
    
    .nav-left {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .nav-left .logo-icon {
        font-size: 1.6rem;
    }
    
    .nav-left .logo-text {
        font-size: 1.2rem;
        font-weight: 800;
        color: #1a1a2e;
        letter-spacing: -0.5px;
    }
    
    .nav-left .logo-text span {
        color: #4f46e5;
    }
    
    .nav-right {
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    
    .nav-right .nav-link {
        color: #64748b;
        text-decoration: none;
        font-size: 0.8rem;
        font-weight: 500;
        padding: 0.3rem 0.7rem;
        border-radius: 6px;
        transition: all 0.2s ease;
    }
    
    .nav-right .nav-link:hover {
        background: #4f46e510;
        color: #4f46e5;
    }
    
    .nav-right .nav-link-cta {
        background: #4f46e5;
        color: white;
        padding: 0.38rem 0.9rem;
        border-radius: 20px;
        text-decoration: none;
        font-size: 0.75rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .nav-right .nav-link-cta:hover {
        background: #4338ca;
        transform: scale(1.02);
    }
    
    /* === HERO === */
    .hero {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #ffffff;
        border-radius: 12px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        animation: fadeInUp 0.8s ease forwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hero-left h1 {
        font-size: 1.6rem;
        font-weight: 800;
        color: #1a1a2e;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }
    
    .hero-left h1 span {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-left p {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 0.8rem;
        font-weight: 400;
    }
    
    .hero-stats {
        display: flex;
        gap: 1.2rem;
    }
    
    .hero-stats .stat-item {
        transition: all 0.2s ease;
    }
    
    .hero-stats .stat-item:hover .number {
        color: #4f46e5;
    }
    
    .hero-stats .stat-item .number {
        font-size: 1rem;
        font-weight: 700;
        color: #1a1a2e;
        transition: color 0.2s ease;
    }
    
    .hero-stats .stat-item .label {
        font-size: 0.7rem;
        color: #94a3b8;
        font-weight: 400;
        margin-left: 0.2rem;
    }
    
    .hero-right .floating-icons {
        font-size: 1.8rem;
        display: flex;
        gap: 0.6rem;
        background: #f8fafc;
        padding: 0.6rem 1.2rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .hero-right .floating-icons span {
        padding: 0.2rem 0.4rem;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    .hero-right .floating-icons span:hover {
        background: #eef2ff;
        transform: scale(1.08);
    }
    
    /* === SECTION TITLE === */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a1a2e;
        margin: 0.5rem 0 0.8rem 0;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    /* === TOOLS GRID === */
    .tools-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 0.5rem 0 1.5rem 0;
    }
    
    .tool-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.4rem 1rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-decoration: none;
        color: inherit;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        animation: fadeInUp 0.6s ease forwards;
        opacity: 0;
    }
    
    .tool-card:nth-child(1) { animation-delay: 0.1s; }
    .tool-card:nth-child(2) { animation-delay: 0.2s; }
    .tool-card:nth-child(3) { animation-delay: 0.3s; }
    .tool-card:nth-child(4) { animation-delay: 0.4s; }
    
    .tool-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(79, 70, 229, 0.08);
        border-color: #c7d2fe;
    }
    
    .tool-card .icon {
        font-size: 2rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .tool-card h3 {
        font-size: 0.95rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    
    .tool-card p {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 400;
        line-height: 1.4;
        margin-bottom: 0.8rem;
    }
    
    .tool-card .badge {
        display: inline-block;
        font-size: 0.6rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }
    
    /* === BADGE COLORS === */
    .badge-intro {
        background: #eef2ff;
        color: #4f46e5;
    }
    
    .badge-intermediate {
        background: #ecfdf5;
        color: #059669;
    }
    
    .badge-advanced {
        background: #fffbeb;
        color: #d97706;
    }
    
    /* === FEATURES ROW === */
    .features-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.6rem;
        padding: 1rem 0 0.5rem 0;
        border-top: 1px solid #e2e8f0;
        margin-top: 1rem;
    }
    
    .feature-item {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        padding: 0.5rem;
        border-radius: 8px;
        transition: all 0.2s ease;
        color: #64748b;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .feature-item:hover {
        background: #f1f5f9;
        color: #1a1a2e;
    }
    
    .feature-item .emoji {
        font-size: 1rem;
    }
    
    /* === FOOTER === */
    .footer {
        text-align: center;
        padding: 1.2rem 0 0.5rem 0;
        color: #94a3b8;
        font-size: 0.75rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 1rem;
    }
    
    .footer .heart {
        color: #ef4444;
    }
    
    /* === RESPONSIVE MEDIA QUERIES === */
    @media (max-width: 900px) {
        .tools-grid {
            grid-template-columns: repeat(2, 1fr) !important;
        }
        .features-row {
            grid-template-columns: repeat(2, 1fr) !important;
        }
        .hero {
            flex-direction: column;
            text-align: center;
            gap: 1rem;
        }
        .hero-stats {
            justify-content: center;
        }
    }
    
    @media (max-width: 550px) {
        .tools-grid {
            grid-template-columns: 1fr !important;
        }
        .features-row {
            grid-template-columns: 1fr !important;
        }
        .top-nav {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
        }
        .hero-left h1 {
            font-size: 1.3rem;
        }
        .hero-right .floating-icons {
            font-size: 1.4rem;
            padding: 0.4rem 0.8rem;
        }
    }
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# ============================================
# TOP NAVIGATION
# ============================================
top_nav_html = """
<div class="top-nav">
    <div class="nav-left">
        <span class="logo-icon">📐</span>
        <span class="logo-text">Math <span>Lab</span></span>
    </div>
    <div class="nav-right">
        <a href="#" class="nav-link">Explore</a>
        <a href="#" class="nav-link">About</a>
        <a href="https://math-lab-nfwbmpekzmcjaqbt97zfce.streamlit.app/" target="_blank" class="nav-link-cta">🎯 Challenge</a>
    </div>
</div>
"""
st.markdown(top_nav_html, unsafe_allow_html=True)

# ============================================
# HERO SECTION
# ============================================
hero_html = """
<div class="hero">
    <div class="hero-left">
        <h1>Learn Math <span>Visually</span></h1>
        <p>Interactive tools for exploring algebra, functions, and calculus.</p>
        <div class="hero-stats">
            <div class="stat-item">
                <span class="number">4</span>
                <span class="label">Tools</span>
            </div>
            <div class="stat-item">
                <span class="number">∞</span>
                <span class="label">Challenges</span>
            </div>
            <div class="stat-item">
                <span class="number">Free</span>
                <span class="label">Always</span>
            </div>
        </div>
    </div>
    <div class="hero-right">
        <div class="floating-icons">
            <span>📈</span>
            <span>📊</span>
            <span>🔢</span>
            <span>∫</span>
        </div>
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# ============================================
# TOOLS GRID SECTION
# ============================================
grid_html = """
<div class="section-title"><span>🛠️</span> Choose Your Tool</div>
<div class="tools-grid">

<!-- Card 1: Linear Functions -->
<a href="https://math-lab-nfwbmpekzmcjaqbt97zfce.streamlit.app/" target="_blank" class="tool-card">
    <div>
        <span class="icon">📈</span>
        <h3>Linear Functions</h3>
        <p>Slope, intercepts, graphing</p>
    </div>
    <span class="badge badge-intro">Introductory</span>
</a>

<!-- Card 2: Quadratic Functions -->
<a href="https://math-lab-fmdbv9utg75beebjgmg5cw.streamlit.app/" target="_blank" class="tool-card">
    <div>
        <span class="icon">📊</span>
        <h3>Quadratic Functions</h3>
        <p>Parabolas, vertex, roots</p>
    </div>
    <span class="badge badge-intermediate">Intermediate</span>
</a>

<!-- Card 3: Polynomial Solver -->
<a href="https://math-lab-6xbscvtsxvjsrn5lpspaje.streamlit.app/" target="_blank" class="tool-card">
    <div>
        <span class="icon">🔢</span>
        <h3>Polynomial Solver</h3>
        <p>Higher degree roots &amp; graphs</p>
    </div>
    <span class="badge badge-advanced">Advanced</span>
</a>

<!-- Card 4: Calculus Explorer -->
<a href="https://w8ynfocpak99duzyypg2yk.streamlit.app/" target="_blank" class="tool-card">
    <div>
        <span class="icon">∫</span>
        <h3>Calculus Explorer</h3>
        <p>Derivatives, integrals, areas</p>
    </div>
    <span class="badge badge-advanced">Advanced</span>
</a>

</div>
"""
st.markdown(grid_html, unsafe_allow_html=True)

# ============================================
# FEATURES ROW
# ============================================
features_html = """
<div class="features-row">
    <div class="feature-item"><span class="emoji">🧠</span> Visual Learning</div>
    <div class="feature-item"><span class="emoji">🎯</span> Instant Feedback</div>
    <div class="feature-item"><span class="emoji">📱</span> Mobile Friendly</div>
    <div class="feature-item"><span class="emoji">🔓</span> Completely Free</div>
</div>
"""
st.markdown(features_html, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
footer_html = """
<div class="footer">
    <p>Built with love <span class="heart">❤️</span> for Mathematics Education</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)