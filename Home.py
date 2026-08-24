import streamlit as st

st.set_page_config(
    page_title="Math Lab",
    page_icon="📐",
    layout="centered"
)

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

# Use st.page_link for proper navigation
st.page_link("app1_linear.py", label=" Open Linear Functions Explorer", icon="📈")

st.divider()

st.markdown("""
### 📊 Quadratic Functions Explorer

**What you'll learn:**
- How **a, b, c** shape a parabola
- Find the **vertex**, **roots**, and **discriminant**
- Type ANY quadratic equation and see it graphed
- Test yourself with Challenge Mode!
""")

st.page_link("app2_quadratic.py", label=" Open Quadratic Functions Explorer", icon="📊")

st.divider()

st.markdown("""
### Challenge Yourself!

Both apps include a **Challenge Mode** that tests your understanding. Can you get a perfect score?

---

**Created with love (❤️) for Mathematics Education**

""")

st.caption("📖 Move sliders, type equations, explore graphs, and challenge yourself!")
