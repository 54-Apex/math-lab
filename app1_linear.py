import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random
import sympy as sp

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Linear Functions | Math Lab",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CUSTOM CSS (TIGHT PADDING & MOBILE POLISH)
# ============================================
st.markdown("""
    <style>
    /* Force high contrast text on dark backgrounds */
    .stAppViewContainer, .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%) !important;
        color: #F8FAFC !important;
    }
    
    /* Ensure headers and markdown text are bright white/light gray */
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #F8FAFC !important;
    }
    
    /* Make LaTeX math readable */
    .katex {
        color: #60A5FA !important; /* Soft blue highlight for math */
        font-size: 1.2rem !important;
    }
    
    /* Subtitles / Secondary text */
    .caption-text {
        color: #94A3B8 !important;
    }

    /* Make cards/containers responsive with visible borders */
    div[data-testid="stVerticalBlock"] > div[style*="background-color"] {
        background-color: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
        padding: 1rem !important;
    }
    
    /* Slider styling for mobile touch target */
    .stSlider > div {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# APP HEADER (CLEAN ICON & ZERO TOP GAP)
# ============================================
st.title("📈 Linear Functions Explorer")
st.caption("Interactive visual module for exploring slope, intercept, and linear algebraic behavior.")

st.markdown("---")

# ============================================
# INTERACTIVE CONTROLS
# ============================================
col_params, col_point = st.columns(2)

with col_params:
    st.subheader("🎛️ Equation Parameters")
    m = st.slider("Slope (m)", -5.0, 5.0, 2.0, 0.1)
    c = st.slider("y-intercept (c)", -10.0, 10.0, 3.0, 0.5)
    
    sign = "+" if c >= 0 else "-"
    st.latex(f"y = {m:.1f}x {sign} {abs(c):.1f}")

with col_point:
    st.subheader("📍 Point Evaluator")
    x_display = st.slider("Select Point x =", -10, 10, 2, 1)
    y_display = m * x_display + c
    
    st.markdown("**Evaluated Coordinate:**")
    st.latex(f"({x_display},\\ {y_display:.2f})")

# ============================================
# PLOTLY CHART (MOBILE ADAPTIVE)
# ============================================
x = np.linspace(-10, 10, 400)
y = m * x + c

fig = go.Figure()

# Main Linear Trace
fig.add_trace(go.Scatter(
    x=list(x), y=list(y),
    mode='lines',
    name=f'y = {m}x + {c}',
    line=dict(color='#818cf8', width=3.5)
))

# Evaluated Point Marker
fig.add_trace(go.Scatter(
    x=[x_display], y=[y_display],
    mode='markers+text',
    name='Evaluated Point',
    marker=dict(color='#f43f5e', size=12),
    text=[f" ({x_display}, {y_display:.1f})"],
    textposition="top right",
    textfont=dict(color='#f43f5e', size=12)
))

# Intercept Marker
fig.add_trace(go.Scatter(
    x=[0], y=[c],
    mode='markers+text',
    name='y-intercept',
    marker=dict(color='#10b981', size=10),
    text=[f" (0, {c:.1f})"],
    textposition="bottom right",
    textfont=dict(color='#10b981', size=11)
))

# Layout Customization with Tight Margins
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(15, 23, 42, 0.5)',
    height=420,
    margin=dict(l=10, r=10, t=20, b=10),
    xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='#64748b', gridcolor='rgba(255,255,255,0.05)', range=[-10, 10]),
    yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='#64748b', gridcolor='rgba(255,255,255,0.05)', range=[-10, 10]),
    autosize=True
)

st.plotly_chart(fig, use_container_width=True)

# ============================================
# CHALLENGE MODE (CASE-INSENSITIVE & IMPLICIT MULTIPLICATION)
# ============================================
st.markdown("---")
st.subheader("🎯 Challenge Mode: Practice Problem")

from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

transformations = standard_transformations + (implicit_multiplication_application,)

if 'q_m' not in st.session_state:
    st.session_state['q_m'] = 2
    st.session_state['q_c'] = 7
    st.session_state['answered'] = False

btn1, btn2 = st.columns(2)
with btn1:
    if st.button("🎲 Generate New Question", use_container_width=True):
        st.session_state['q_m'] = random.randint(-5, 5)
        st.session_state['q_c'] = random.randint(-8, 8)
        st.session_state['answered'] = False
        st.rerun()

st.markdown(f"> **Target:** Construct an equation with **m = {st.session_state['q_m']}** and **c = {st.session_state['q_c']}**")

user_input = st.text_input("Enter equation (e.g. y = 2x + 7):", key="user_input")

if st.button("✅ Verify Answer"):
    if user_input:
        try:
            # Normalize input to lower case for case-insensitivity (e.g., 'X' -> 'x', 'Y' -> 'y')
            cleaned_input = user_input.lower().strip()
            
            x_s, y_s = sp.symbols('x y')
            
            # Target expression: y - (mx + c)
            target = y_s - (st.session_state['q_m'] * x_s + st.session_state['q_c'])
            
            # Parse lowercased equation with implicit multiplication allowed
            if "=" in cleaned_input:
                lhs_str, rhs_str = cleaned_input.split("=", 1)
                lhs_expr = parse_expr(lhs_str, transformations=transformations)
                rhs_expr = parse_expr(rhs_str, transformations=transformations)
                user_expr = lhs_expr - rhs_expr
            else:
                user_expr = parse_expr(cleaned_input, transformations=transformations) - target
            
            # Check algebraic equivalence
            diff = sp.simplify(user_expr - target)
            ratio = sp.simplify(user_expr / target)
            
            if diff == 0 or ratio.is_constant():
                st.success("🎉 Correct! Mathematical equivalence verified.")
                st.balloons()
            else:
                st.error("❌ Not quite. Check your slope and intercept values!")
        except Exception:
            st.warning("Please type a valid equation format (e.g., `y = 2x + 7` or `Y - 2X = 7`).")