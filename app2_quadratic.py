import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import sympy as sp
import re

st.set_page_config(page_title="Quadratic Explorer", page_icon="📈", layout="wide")

# Modern styling, zero top whitespace, and compact UI blocks
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    /* Remove white space above header */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    #MainMenu, footer, header, .stDeployButton { display: none; }
    
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
    
    /* Compact inputs & cards */
    .stMarkdown, .stSlider, .stTextInput, .stSelectbox, .stNumberInput {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        padding: 0.8rem 1rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 0.3rem;
    }
    
    .stSlider > div { background: transparent; padding: 0; }
    .stSlider label, .stTextInput label, .stSelectbox label, .stNumberInput label { 
        color: rgba(255,255,255,0.9) !important; 
        font-weight: 600 !important; 
    }
    
    .stButton > button {
        background: linear-gradient(-45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 0.3rem;
        margin-bottom: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        color: rgba(255,255,255,0.6);
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(-45deg, #667eea, #764ba2);
        color: white;
    }
    
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 0.6rem;
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stMetric"] label { color: rgba(255,255,255,0.7) !important; }
    [data-testid="stMetric"] div { color: white !important; font-weight: 800 !important; }
    
    h1, h2, h3, h4, p, li, label, .katex { color: white !important; }
    h1 { font-size: 1.8rem !important; margin-bottom: 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

# Global Session State Initialization
if 'q_score' not in st.session_state:
    st.session_state.q_score = 0
if 'q_attempts' not in st.session_state:
    st.session_state.q_attempts = 0
if 'q_history' not in st.session_state:
    st.session_state.q_history = []

def fix_implicit_multiplication(expr):
    """Insert * between numbers and variables, e.g., 3x -> 3*x"""
    expr = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'([a-zA-Z])(\d+)', r'\1*\2', expr)
    expr = re.sub(r'\)\(', r')*(', expr)
    return expr

def style_plot(fig, ax):
    """Clean dark plot styling using valid RGBA tuple"""
    fig.patch.set_facecolor('none')
    ax.set_facecolor((0.06, 0.05, 0.16, 0.65))
    ax.spines['bottom'].set_color('#ffffff')
    ax.spines['left'].set_color('#ffffff')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.grid(True, linestyle='--', alpha=0.15, color='white')

st.title("📈 Quadratic Functions: y = ax² + bx + c")

# ============================================
# TABS SETUP
# ============================================
tab1, tab2 = st.tabs(["✍️ Enter Equation", "🎚️ Use Sliders"])

# TAB 1: ENTER EQUATION
with tab1:
    col_in, col_btn = st.columns([3, 1])
    with col_in:
        equation_input = st.text_input(
            "Enter Equation (e.g. 3x^2 - 5x + 1):",
            value="x^2 - 4x + 3",
            key="equation_input"
        )
    with col_btn:
        st.write(" ") 
        parse_button = st.button("📊 Plot Equation", use_container_width=True)

    if equation_input:
        try:
            expr_str = equation_input.strip()
            if "=" in expr_str:
                expr_str = expr_str.split("=")[1].strip()
            
            expr_str = expr_str.replace("^", "**")
            expr_str = fix_implicit_multiplication(expr_str)
            
            x = sp.Symbol('x')
            expr = sp.sympify(expr_str)
            expr_expanded = sp.expand(expr)
            
            try:
                poly = sp.Poly(expr_expanded, x)
                coeffs = poly.all_coeffs()
                if len(coeffs) == 3:
                    a, b, c = float(coeffs[0]), float(coeffs[1]), float(coeffs[2])
                elif len(coeffs) == 2:
                    a, b, c = 0.0, float(coeffs[0]), float(coeffs[1])
                elif len(coeffs) == 1:
                    a, b, c = 0.0, 0.0, float(coeffs[0])
                else:
                    a, b, c = 0.0, 0.0, 0.0
            except:
                a = float(sp.coeff(expr_expanded, x, 2))
                b = float(sp.coeff(expr_expanded, x, 1))
                c = float(sp.coeff(expr_expanded, x, 0))
            
            is_quadratic = (a != 0)
            
            x_vals = np.linspace(-10, 10, 500)
            y_vals = [float(expr.subs(x, val)) for val in x_vals]
            
            fig, ax = plt.subplots(figsize=(8, 3.8))
            ax.plot(x_vals, y_vals, color='#c084fc', linewidth=3, label="f(x)")
            ax.axhline(0, color='white', linewidth=0.8, alpha=0.5)
            ax.axvline(0, color='white', linewidth=0.8, alpha=0.5)
            
            y_min, y_max = min(y_vals), max(y_vals)
            y_range = max(y_max - y_min, 1)
            ax.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)
            ax.set_xlim(-10, 10)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            
            style_plot(fig, ax)
            
            if is_quadratic:
                discriminant = b**2 - 4*a*c
                vertex_x = -b / (2*a)
                vertex_y = a * vertex_x**2 + b * vertex_x + c
                ax.plot(vertex_x, vertex_y, 'o', color='#22c55e', markersize=8)
                ax.annotate(f"Vertex ({vertex_x:.2f}, {vertex_y:.2f})", 
                            (vertex_x, vertex_y), xytext=(10, 10), 
                            textcoords='offset points', fontsize=8, color='#4ade80', weight='bold')
                
                if discriminant >= 0:
                    root1 = (-b - math.sqrt(discriminant)) / (2*a)
                    root2 = (-b + math.sqrt(discriminant)) / (2*a)
                    ax.plot([root1, root2], [0, 0], 'o', color='#ef4444', markersize=6)
                
                ax.plot(0, c, 'o', color='#3b82f6', markersize=6)
            
            st.pyplot(fig)
            
            if is_quadratic:
                col1, col2, col3 = st.columns(3)
                with col1: st.metric("📍 Vertex", f"({vertex_x:.2f}, {vertex_y:.2f})")
                with col2: st.metric("🔵 Discriminant", f"{discriminant:.2f}")
                with col3: st.metric("🔄 Direction", "Opens Up" if a > 0 else "Opens Down")
                
                if discriminant >= 0:
                    st.info(f"**Roots:** x = {root1:.2f} and x = {root2:.2f}")
                else:
                    st.warning("No real roots")
        except Exception:
            st.error("Invalid equation format. Try format like: `3x^2 - 5x + 1`")

# TAB 2: USE SLIDERS
with tab2:
    col1, col2, col3 = st.columns(3)
    with col1: a = st.slider("a", -3.0, 3.0, 1.0, 0.1, key="slider_a")
    with col2: b = st.slider("b", -10.0, 10.0, 0.0, 0.5, key="slider_b")
    with col3: c = st.slider("c", -10.0, 10.0, 0.0, 0.5, key="slider_c")
    
    st.latex(f"y = {a}x^2 + {b}x + {c}")
    
    x_plot = np.linspace(-10, 10, 500)
    y_plot = a * x_plot**2 + b * x_plot + c
    
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.plot(x_plot, y_plot, color='#c084fc', linewidth=3)
    ax.axhline(0, color='white', linewidth=0.8, alpha=0.5)
    ax.axvline(0, color='white', linewidth=0.8, alpha=0.5)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-20, 20)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    
    style_plot(fig, ax)
    
    discriminant = b**2 - 4*a*c
    
    if a != 0:
        vertex_x = -b / (2*a)
        vertex_y = a * vertex_x**2 + b * vertex_x + c
        ax.plot(vertex_x, vertex_y, 'o', color='#22c55e', markersize=8)
        
        if discriminant >= 0:
            root1 = (-b - math.sqrt(discriminant)) / (2*a)
            root2 = (-b + math.sqrt(discriminant)) / (2*a)
            ax.plot([root1, root2], [0, 0], 'o', color='#ef4444', markersize=6)
    
    ax.plot(0, c, 'o', color='#3b82f6', markersize=6)
    st.pyplot(fig)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("📍 Vertex", f"({vertex_x:.2f}, {vertex_y:.2f})" if a != 0 else "N/A")
    with col2: st.metric("🔵 Discriminant", f"{discriminant:.2f}")
    with col3: st.metric("🔄 Direction", "Opens Up" if a > 0 else "Opens Down" if a < 0 else "Linear")

# ============================================
# FUNCTION: Challenge Mode
# ============================================
def challenge_mode(tab_id="quadratic"):
    if f'q_challenge_active_{tab_id}' not in st.session_state:
        st.session_state[f'q_challenge_active_{tab_id}'] = False
    if f'q_challenge_answered_{tab_id}' not in st.session_state:
        st.session_state[f'q_challenge_answered_{tab_id}'] = False
    
    st.subheader("🎯 Challenge Mode - Test Your Skills!")
    
    if st.button("🔄 Generate New Quadratic Challenge", key=f"generate_{tab_id}"):
        st.session_state[f'q_challenge_a_{tab_id}'] = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        st.session_state[f'q_challenge_b_{tab_id}'] = random.randint(-10, 10)
        st.session_state[f'q_challenge_c_{tab_id}'] = random.randint(-10, 10)
        st.session_state[f'q_challenge_active_{tab_id}'] = True
        st.session_state[f'q_challenge_answered_{tab_id}'] = False
    
    if st.session_state[f'q_challenge_active_{tab_id}'] and not st.session_state[f'q_challenge_answered_{tab_id}']:
        a_q = st.session_state[f'q_challenge_a_{tab_id}']
        b_q = st.session_state[f'q_challenge_b_{tab_id}']
        c_q = st.session_state[f'q_challenge_c_{tab_id}']
        
        st.markdown(f"Given equation: **y = {a_q}x² + {b_q}x + {c_q}**")
        
        vertex_x = -b_q / (2*a_q)
        vertex_y = a_q * vertex_x**2 + b_q * vertex_x + c_q
        
        col1, col2 = st.columns(2)
        with col1:
            user_vx = st.number_input("Vertex x-coord:", value=0.0, step=0.5, key=f"user_vx_{tab_id}")
        with col2:
            user_vy = st.number_input("Vertex y-coord:", value=0.0, step=0.5, key=f"user_vy_{tab_id}")
        
        disc = b_q**2 - 4*a_q*c_q
        if disc >= 0:
            root1 = (-b_q - math.sqrt(disc)) / (2*a_q)
            root2 = (-b_q + math.sqrt(disc)) / (2*a_q)
            col1, col2 = st.columns(2)
            with col1: user_root1 = st.number_input("First root:", value=0.0, step=0.5, key=f"user_root1_{tab_id}")
            with col2: user_root2 = st.number_input("Second root:", value=0.0, step=0.5, key=f"user_root2_{tab_id}")
        else:
            st.info("💡 Note: This equation has NO real roots.")
            user_root1, user_root2 = 0.0, 0.0
        
        direction = st.selectbox("Direction:", ["Select...", "Opens Up", "Opens Down"], key=f"direction_{tab_id}")
        
        if st.button("✅ Check My Answers", key=f"check_{tab_id}"):
            score = 0
            if abs(user_vx - vertex_x) < 0.1 and abs(user_vy - vertex_y) < 0.1:
                score += 1
                st.success("✅ Vertex is correct!")
            else:
                st.error(f"❌ Correct Vertex: ({vertex_x:.2f}, {vertex_y:.2f})")
            
            if disc >= 0:
                if (abs(user_root1 - root1) < 0.1 and abs(user_root2 - root2) < 0.1) or \
                   (abs(user_root1 - root2) < 0.1 and abs(user_root2 - root1) < 0.1):
                    score += 1
                    st.success("✅ Roots are correct!")
                else:
                    st.error(f"❌ Correct Roots: {root1:.2f} and {root2:.2f}")
            else:
                score += 1
            
            correct_direction = "Opens Up" if a_q > 0 else "Opens Down"
            if direction == correct_direction:
                score += 1
                st.success("✅ Direction is correct!")
            else:
                st.error(f"❌ Correct Direction: {correct_direction}")
            
            st.session_state.q_score += score
            st.session_state.q_attempts += 1
            st.session_state.q_history.append(f"y = {a_q}x² + {b_q}x + {c_q} → Score: {score}/3")
            st.session_state[f'q_challenge_answered_{tab_id}'] = True

    if len(st.session_state.q_history) > 0:
        with st.expander("📜 History & Scorecard"):
            st.write(f"**Total Score:** {st.session_state.q_score} points across {st.session_state.q_attempts} challenges")
            for item in st.session_state.q_history[-5:]:
                st.write(f"- {item}")

# Execute Challenge Mode at bottom
challenge_mode("quadratic")

st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.4); font-size: 0.8rem; margin-top: 1.5rem;'>Created for Mathematics Education | ApexTech</p>", unsafe_allow_html=True)