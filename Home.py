import streamlit as st

st.set_page_config(
    page_title="Math Lab",
    page_icon="📐",
    layout="centered"
)
# Custom CSS for modern design - Optimized for mobile
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * { 
        font-family: 'Inter', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
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
        padding: 3rem 1.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 1.5rem 0 2rem 0;
        box-shadow: 0 25px 80px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes heroBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero .emoji {
        font-size: 3.5rem;
        display: block;
        margin-bottom: 0.8rem;
        position: relative;
    }
    
    .hero h1 {
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: -1px;
        position: relative;
        background: linear-gradient(to right, #fff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    
    .hero p {
        font-size: 1.1rem;
        font-weight: 500;
        opacity: 0.95;
        max-width: 600px;
        margin: 0.8rem auto 0;
        position: relative;
        -webkit-text-fill-color: white;
        line-height: 1.6;
    }
    
    .hero .badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
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
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .card {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255,255,255,0.08);
        text-align: center;
    }
    
    .card:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 30px 80px rgba(0,0,0,0.4);
        border-color: rgba(255,255,255,0.2);
    }
    
    .card .icon {
        font-size: 3.5rem;
        margin-bottom: 0.8rem;
    }
    
    .card h2 {
        color: white;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 0.6rem;
        letter-spacing: -0.5px;
    }
    
    .card p {
        color: rgba(255,255,255,0.8);
        font-size: 0.95rem;
        font-weight: 400;
        line-height: 1.7;
        margin-bottom: 1.2rem;
    }
    
    .card .features {
        text-align: left;
        color: rgba(255,255,255,0.9);
        font-size: 0.9rem;
        font-weight: 400;
        list-style: none;
        padding: 0;
        margin-bottom: 1.5rem;
    }
    
    .card .features li {
        padding: 0.4rem 0;
        display: flex;
        align-items: center;
        gap: 0.7rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-weight: 400;
    }
    
    .card .features li:last-child {
        border-bottom: none;
    }
    
    .card .features li::before {
        content: "✦";
        color: #f093fb;
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    
    /* === BUTTONS === */
    .btn {
        display: inline-block;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        width: 100%;
        letter-spacing: 0.3px;
    }
    
    .btn-primary {
        background: linear-gradient(-45deg, #667eea, #764ba2);
        background-size: 200% 200%;
        animation: btnGlow 4s ease-in-out infinite;
        color: white;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
    }
    
    .btn-primary:hover {
        transform: scale(1.03);
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
        transform: scale(1.03);
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
        gap: 1rem;
        margin: 2rem 0 1.5rem 0;
    }
    
    .stat-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        padding: 1.2rem;
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
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(-45deg, #667eea, #f093fb);
        background-size: 200% 200%;
        animation: gradientBG 4s ease-in-out infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-card .label {
        color: rgba(255,255,255,0.7);
        font-size: 0.85rem;
        font-weight: 400;
        margin-top: 0.3rem;
        display: block;
    }
    
    /* === FOOTER === */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: rgba(255,255,255,0.35);
        font-size: 0.85rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin-top: 1.5rem;
        font-weight: 400;
    }
    
    .footer .heart {
        color: #f5576c;
        animation: heartbeat 1.5s ease-in-out infinite;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.3); }
    }
    
    /* === RESPONSIVE - MOBILE FIXES === */
    @media (max-width: 768px) {
        .card-grid {
            grid-template-columns: 1fr;
            gap: 1.2rem;
        }
        .stats {
            grid-template-columns: 1fr 1fr;
            gap: 0.8rem;
        }
        .stats .stat-card:last-child {
            grid-column: span 2;
        }
        .hero {
            padding: 2rem 1.2rem;
            margin: 1rem 0 1.5rem 0;
            border-radius: 16px;
        }
        .hero h1 {
            font-size: 2.2rem;
        }
        .hero p {
            font-size: 1rem;
            font-weight: 500;
            opacity: 0.95;
            -webkit-text-fill-color: white;
        }
        .hero .emoji {
            font-size: 3rem;
        }
        .hero .badge {
            font-size: 0.8rem;
            padding: 0.4rem 1.2rem;
        }
        .card {
            padding: 1.5rem 1.2rem;
            border-radius: 16px;
        }
        .card h2 {
            font-size: 1.3rem;
        }
        .card p {
            font-size: 0.9rem;
        }
        .card .features {
            font-size: 0.85rem;
        }
        .btn {
            font-size: 0.9rem;
            padding: 0.7rem 1.5rem;
        }
        .stat-card .number {
            font-size: 1.8rem;
        }
        .stat-card .label {
            font-size: 0.75rem;
        }
        .footer {
            font-size: 0.75rem;
        }
    }
    
    /* === EXTRA SMALL PHONES === */
    @media (max-width: 480px) {
        .hero h1 {
            font-size: 1.8rem;
        }
        .hero p {
            font-size: 0.9rem;
        }
        .card h2 {
            font-size: 1.1rem;
        }
        .card p {
            font-size: 0.85rem;
        }
        .stats {
            grid-template-columns: 1fr;
        }
        .stats .stat-card:last-child {
            grid-column: span 1;
        }
        .stat-card {
            padding: 0.8rem;
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
