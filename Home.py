import streamlit as st

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
    <a href="https://math-lab-umf7fzwm4xpdo2fhauwhls.streamlit.app/app1_linear" target="_blank" style="
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
    <a href="https://math-lab-umf7fzwm4xpdo2fhauwhls.streamlit.app/app2_quadratic" target="_blank" style="
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