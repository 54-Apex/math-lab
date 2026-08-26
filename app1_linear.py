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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Hide Branding & Top Header Space */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden; height: 0px !important;}
    .stDeployButton {display: none;}
    
    /* REMOVE TOP WHITE SPACE / GAP */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px;
    }
    
    /* App Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%) !important;
    }
    
    /* Glass Cards */
    div[data-testid="stColumn"] > div {
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 1.25rem !important;
    }
    
    /* Glow Action Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
    }
    
    /* Input Fields */
    .stTextInput input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }

    /* MOBILE SPECIFIC OPTIMIZATIONS */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 0.2rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }
        div[data-testid="stColumn"] > div {
            padding: 0.8rem !important;
            margin-bottom: 0.5rem !important;
        }
        .stButton > button {
            width: 100% !important;
        }
        h1 {
            font-size: 1.6rem !important;
        }
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