import streamlit as st

# Custom CSS for modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stSlider > div {
        background: rgba(255,255,255,0.5);
        padding: 1rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
        border-radius: 12px;
        padding: 1rem;
        color: white;
    }
    
    .stError {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 12px;
        padding: 1rem;
        color: white;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f2994a 0%, #f2c94a 100%);
        border-radius: 12px;
        padding: 1rem;
        color: white;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 12px;
        padding: 1rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Math Lab",
    page_icon="📐",
    layout="centered"
)

st.title("📐 Math Lab - Interactive Math Explorers")

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
