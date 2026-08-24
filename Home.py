import streamlit as st

st.set_page_config(
    page_title="Math Lab",
    page_icon="📐",
    layout="centered"
)
# Custom CSS for modern design with animated background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* === ANIMATED GRADIENT BACKGROUND === */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* === ANIMATED HERO === */
    .hero {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 300% 300%;
        animation: heroBG 8s ease infinite;
        padding: 4rem 2rem;
        border-radius: 24px;
        text-align: center;
        color: white;
        margin: 2rem 0 3rem 0;
        box-shadow: 0 25px 80px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes heroBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* === FLOATING PARTICLES (subtle) === */
    .hero::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(255,255,255,0.03) 0%, transparent 60%);
        animation: floatParticles 20s linear infinite;
        pointer-events: none;
    }
    
    @keyframes floatParticles {
        0% { transform: translate(0, 0) rotate(0deg); }
        100% { transform: translate(10%, 5%) rotate(360deg); }
    }
    
    /* === REST OF YOUR CSS === */
    .hero .emoji {
        font-size: 4.5rem;
        display: block;
        margin-bottom: 1rem;
        position: relative;
    }
    
    .hero h1 {
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: -2px;
        position: relative;
        background: linear-gradient(to right, #fff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero p {
        font-size: 1.3rem;
        opacity: 0.9;
        max-width: 600px;
        margin: 0 auto;
        position: relative;
        -webkit-text-fill-color: white;
    }
    
    .hero .badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding: 0.4rem 1.5rem;
        border-radius: 50px;
        font-size: 0.9rem;
        margin-top: 1rem;
        position: relative;
        -webkit-text-fill-color: white;
        border: 1px solid rgba(255,255,255,0.25);
        animation: pulseBadge 3s ease-in-out infinite;
    }
    
    @keyframes pulseBadge {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* === CARD GRID === */
    .card-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255,255,255,0.08);
        text-align: center;
    }
    
    .card:hover {
        transform: translateY(-12px) scale(1.01);
        box-shadow: 0 30px 80px rgba(0,0,0,0.4);
        border-color: rgba(255,255,255,0.2);
    }
    
    .card .icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .card h2 {
        color: white;
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 0.8rem;
    }
    
    .card p {
        color: rgba(255,255,255,0.7);
        font-size: 1rem;
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }
    
    .card .features {
        text-align: left;
        color: rgba(255,255,255,0.85);
        font-size: 0.95rem;
        list-style: none;
        padding: 0;
        margin-bottom: 2rem;
    }
    
    .card .features li {
        padding: 0.4rem 0;
        display: flex;
        align-items: center;
        gap: 0.7rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .card .features li:last-child {
        border-bottom: none;
    }
    
    .card .features li::before {
        content: "✦";
        color: #f093fb;
        font-size: 1.2rem;
    }
    
    /* === BUTTONS === */
    .btn {
        display: inline-block;
        padding: 0.9rem 2.5rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        width: 100%;
        letter-spacing: 0.5px;
    }
    
    .btn-primary {
        background: linear-gradient(-45deg, #667eea, #764ba2);
        background-size: 200% 200%;
        animation: btnGlow 4s ease-in-out infinite;
        color: white;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
    }
    
    .btn-primary:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6);
    }
    
    .btn-secondary {
        background: linear-gradient(-45deg, #f093fb, #f5576c);
        background-size: 200% 200%;
        animation: btnGlow2 4s ease-in-out infinite;
        color: white;
        box-shadow: 0 8px 30px rgba(245, 87, 108, 0.4);
    }
    
    .btn-secondary:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 40px rgba(245, 87, 108, 0.6);
    }
    
    @keyframes btnGlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes btnGlow2 {
        0%, 100% { background-position: 100% 50%; }
        50% { background-position: 0% 50%; }
    }
    
    /* === STATS ROW === */
    .stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 3rem 0 2rem 0;
    }
    
    .stat-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: scale(1.05);
        background: rgba(255,255,255,0.08);
    }
    
    .stat-card .number {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(-45deg, #667eea, #f093fb);
        background-size: 200% 200%;
        animation: gradientBG 4s ease-in-out infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-card .label {
        color: rgba(255,255,255,0.6);
        font-size: 0.9rem;
        margin-top: 0.3rem;
        display: block;
    }
    
    /* === FOOTER === */
    .footer {
        text-align: center;
        padding: 2.5rem 0 1rem 0;
        color: rgba(255,255,255,0.3);
        font-size: 0.85rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin-top: 2rem;
    }
    
    .footer .heart {
        color: #f5576c;
        animation: heartbeat 1.5s ease-in-out infinite;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.3); }
    }
    
    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .card-grid {
            grid-template-columns: 1fr;
        }
        .stats {
            grid-template-columns: 1fr;
        }
        .hero h1 {
            font-size: 2.5rem;
        }
        .hero {
            padding: 2.5rem 1.5rem;
        }
        .card {
            padding: 1.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title(" Math Lab - Interactive Math Explorers")

st.markdown("""
Welcome to the Math Lab! Explore math through interactive graphs and challenges.

---

### 📈 Linear Functions Explorer

**What you'll learn:**
- How **slope (m)** and **y-intercept (c)** affect a line
- Identify x-intercepts, y-intercepts, and slope
- Test yourself with Challenge Mode!
""")

# Use HTML link instead of st.page_link
st.markdown("""
<div style="text-align: center;">
    <a href="https://math-lab-nfwbmpekzmcjaqbt97zfce.streamlit.app/" target="_blank" style="
        display: inline-block;
        padding: 12px 32px;
        background-color: #6c63ff;
        color: white;
        text-decoration: none;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        margin: 10px 0;
    ">
        🚀 Open Linear Functions Explorer
    </a>
</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("""
### 📊 Quadratic Functions Explorer

**What you'll learn:**
- How **a, b, c** shape a parabola
- Find the **vertex**, **roots**, and **discriminant**
- Type ANY quadratic equation and see it graphed
- Test yourself with Challenge Mode!
""")

st.markdown("""
<div style="text-align: center;">
    <a href="https://math-lab-fmdbv9utg75beebjgmg5cw.streamlit.app/" target="_blank" style="
        display: inline-block;
        padding: 12px 32px;
        background-color: #ff6b6b;
        color: white;
        text-decoration: none;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        margin: 10px 0;
    ">
        🚀 Open Quadratic Functions Explorer
    </a>
</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("""
### 🎯 Challenge Yourself!

Both apps include a **Challenge Mode** that tests your understanding. Can you get a perfect score?

---

**Created with ❤️ for Mathematics Students**

*Built using Python, Streamlit, and Sympy*
""")

st.caption("📖 Move sliders, type equations, explore graphs, and challenge yourself!")