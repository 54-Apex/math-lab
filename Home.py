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

### 📈 [Linear Functions Explorer](/app1_linear)

**What you'll learn:**
- How **slope (m)** and **y-intercept (c)** affect a line
- Identify x-intercepts, y-intercepts, and slope
- Test yourself with Challenge Mode!

👉 **Click the link above to start!**

---

### 📊 [Quadratic Functions Explorer](/app2_quadratic)

**What you'll learn:**
- How **a, b, c** shape a parabola
- Find the **vertex**, **roots**, and **discriminant**
- Type ANY quadratic equation and see it graphed
- Test yourself with Challenge Mode!

👉 **Click the link above to start!**





""")

st.divider()
st.caption("📖 Move sliders, type equations, explore graphs, and challenge yourself!")