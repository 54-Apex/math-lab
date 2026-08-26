import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import re
import random

st.set_page_config(
    page_title="Polynomial Solver",
    page_icon="🔢",
    layout="wide"
)

# Modern glassmorphism styling, zero top whitespace, & compact UI blocks
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
    
    /* Compact inputs & glassmorphic cards */
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

# ============================================
# INITIALIZE SESSION STATE FOR CHALLENGES
# ============================================
if 'poly_score' not in st.session_state:
    st.session_state.poly_score = 0
if 'poly_attempts' not in st.session_state:
    st.session_state.poly_attempts = 0
if 'poly_history' not in st.session_state:
    st.session_state.poly_history = []

# ============================================
# HELPER FUNCTIONS
# ============================================
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

def parse_polynomial(expr_str):
    """Parse polynomial string and return coefficients, sympy expression, and function"""
    expr_str = expr_str.strip()
    
    if "=" in expr_str:
        expr_str = expr_str.split("=")[1].strip()
    
    expr_str = expr_str.replace("^", "**")
    expr_str = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expr_str)
    expr_str = re.sub(r'([a-zA-Z])(\d+)', r'\1*\2', expr_str)
    
    x = sp.Symbol('x')
    expr = sp.sympify(expr_str)
    expr_expanded = sp.expand(expr)
    
    poly = sp.Poly(expr_expanded, x)
    coeffs = poly.all_coeffs()
    coeffs_float = [float(c) for c in coeffs]
    
    def f(val):
        return float(expr.subs(x, val))
    
    return coeffs_float, expr, f, expr_expanded

# ============================================
# FUNCTION: Challenge Mode
# ============================================
def polynomial_challenge():
    """Display challenge mode for polynomials"""
    
    if 'poly_challenge_active' not in st.session_state:
        st.session_state.poly_challenge_active = False
    if 'poly_challenge_answered' not in st.session_state:
        st.session_state.poly_challenge_answered = False
    if 'poly_challenge_attempts' not in st.session_state:
        st.session_state.poly_challenge_attempts = 0
    
    st.subheader("🎯 Challenge Mode - Test Your Skills!")
    
    if st.button("🔄 Generate New Polynomial Challenge", key="poly_generate"):
        degree = random.randint(2, 4)
        coeffs = []
        for i in range(degree + 1):
            coeff = random.randint(-5, 5)
            if i == 0:
                while coeff == 0:
                    coeff = random.randint(-5, 5)
            coeffs.append(coeff)
        
        x = sp.Symbol('x')
        expr = 0
        for i, c in enumerate(coeffs):
            expr += c * x**(degree - i)
        
        st.session_state.poly_challenge_expr = expr
        st.session_state.poly_challenge_coeffs = coeffs
        st.session_state.poly_challenge_active = True
        st.session_state.poly_challenge_answered = False
        st.session_state.poly_challenge_attempts = 0
    
    if st.session_state.get('poly_challenge_active', False) and not st.session_state.get('poly_challenge_answered', False):
        expr = st.session_state.poly_challenge_expr
        coeffs = st.session_state.poly_challenge_coeffs
        degree = len(coeffs) - 1
        
        st.markdown(f"""
        ### 📝 Your Task:
        Given the polynomial:
        
        $${sp.latex(expr)}$$
        
        Answer the questions below:
        """)
        
        st.markdown("**1. What is the degree of this polynomial?**")
        user_degree = st.number_input("Degree:", value=0, step=1, key="poly_degree")
        
        st.markdown("**2. What is the leading coefficient?**")
        user_leading = st.number_input("Leading coefficient:", value=0.0, step=0.5, key="poly_leading")
        
        y_intercept = coeffs[-1]
        st.markdown("**3. What is the y-intercept?**")
        user_yint = st.number_input("y-intercept:", value=0.0, step=0.5, key="poly_yint")
        
        if st.button("✅ Check My Answers", key="poly_check"):
            st.session_state.poly_challenge_attempts += 1
            score = 0
            total = 3
            
            if user_degree == degree:
                score += 1
                st.success("✅ Degree is correct!")
            else:
                st.error(f"❌ Degree: The correct answer is {degree}")
            
            if abs(user_leading - coeffs[0]) < 0.1:
                score += 1
                st.success("✅ Leading coefficient is correct!")
            else:
                st.error(f"❌ Leading coefficient: The correct answer is {coeffs[0]}")
            
            if abs(user_yint - y_intercept) < 0.1:
                score += 1
                st.success("✅ y-intercept is correct!")
            else:
                st.error(f"❌ y-intercept: The correct answer is {y_intercept}")
            
            st.subheader(f"📊 Your Score: {score}/{total}")
            st.session_state.poly_score += score
            st.session_state.poly_attempts += 1
            
            if st.session_state.poly_attempts > 0:
                accuracy = (st.session_state.poly_score / (st.session_state.poly_attempts * 3)) * 100
                st.metric("🎯 Overall Accuracy", f"{accuracy:.0f}%")
            
            if score == 3:
                st.success("🌟 Perfect! You're a polynomial master!")
                st.balloons()
            elif score >= 2:
                st.info("👍 Good job! Almost perfect – review the errors above.")
            else:
                st.warning("📚 Keep practicing! Use the explorer above to learn more.")
            
            st.session_state.poly_history.append(f"{sp.latex(expr)} → Score: {score}/3")
            st.session_state.poly_challenge_answered = True
    
    if st.session_state.get('poly_challenge_active', False):
        with st.expander("📜 Challenge History"):
            if len(st.session_state.poly_history) > 0:
                for item in st.session_state.poly_history[-10:]:
                    st.write(f"- {item}")
            else:
                st.write("No challenges completed yet.")
    
    if st.session_state.get('poly_challenge_answered', False):
        if st.button("🔄 Try Another Challenge", key="poly_another"):
            st.session_state.poly_challenge_active = False
            st.session_state.poly_challenge_answered = False
            st.session_state.poly_challenge_attempts = 0
            st.rerun()

# ============================================
# APP TITLE & SOLVER UI
# ============================================
st.title("🔢 Polynomial Solver")
st.markdown("Enter a polynomial to find its roots, degree, and graph!")

st.markdown("### Enter a polynomial to find its roots and graph")
st.markdown("**Examples:** `x^3 - 6x^2 + 11x - 6`, `x^4 - 13x^2 + 36`, `2x^5 - 3x^3 + x`")

poly_input = st.text_input(
    "Enter your polynomial (use x as the variable):",
    placeholder="e.g. x^3 - 6x^2 + 11x - 6",
    key="solve_input"
)

col1, col2 = st.columns([1, 3])
with col1:
    solve_button = st.button("📊 Solve & Graph", use_container_width=True)

if solve_button and poly_input:
    try:
        coeffs, expr, f, expr_expanded = parse_polynomial(poly_input)
        degree = len(coeffs) - 1
        
        st.success(f"✅ Parsed: {degree} degree polynomial")
        
        display_eq = f"y = {poly_input}"
        st.latex(display_eq)
        
        x_vals = np.linspace(-10, 10, 500)
        y_vals = [f(val) for val in x_vals]
        
        roots = np.roots(coeffs)
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x_vals, y_vals, color='#c084fc', linewidth=3, label='Polynomial')
        ax.axhline(0, color='white', linewidth=0.8, alpha=0.5)
        ax.axvline(0, color='white', linewidth=0.8, alpha=0.5)
        
        style_plot(fig, ax)
        
        y_min = min(y_vals)
        y_max = max(y_vals)
        y_range = max(y_max - y_min, 1)
        
        ax.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)
        ax.set_xlim(-10, 10)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"{display_eq}", fontsize=12)
        
        real_roots = []
        complex_roots = []
        for root in roots:
            if np.isreal(root):
                real_roots.append(root.real)
                ax.plot(root.real, 0, 'o', color='#ef4444', markersize=8)
                ax.annotate(f"x = {root.real:.2f}", (root.real, 0), 
                            xytext=(5, -20), textcoords='offset points', 
                            fontsize=8, color='#f87171', weight='bold')
            else:
                complex_roots.append(root)
        
        y_intercept = coeffs[-1]
        ax.plot(0, y_intercept, 'o', color='#3b82f6', markersize=8)
        ax.annotate(f"y-intercept (0, {y_intercept:.1f})", (0, y_intercept), 
                    xytext=(10, 10), textcoords='offset points', 
                    fontsize=9, color='#60a5fa', weight='bold')
        
        st.pyplot(fig)
        
        # === DISPLAY ROOTS ===
        st.subheader("📊 Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎓 Degree", degree)
        with col2:
            st.metric("📐 Leading Coefficient", f"{coeffs[0]:.2f}")
        with col3:
            st.metric("📍 y-intercept", f"{y_intercept:.2f}")
        
        st.write("**Roots:**")
        
        if len(real_roots) > 0:
            real_roots_sorted = sorted(real_roots)
            root_string = "x ∈ { " + ", ".join([f"{root:.4f}" for root in real_roots_sorted]) + " }"
            st.success(f"✅ **Real Roots:** {root_string}")
        else:
            st.warning("⚠️ No real roots found.")
        
        if len(complex_roots) > 0:
            complex_string = "x ∈ { " + ", ".join([f"{root:.4f}" for root in complex_roots]) + " }"
            st.info(f"🧮 **Complex Roots:** {complex_string}")
        
        st.caption("📖 Note: Roots with very small imaginary parts are treated as real numbers.")
        
    except Exception as e:
        st.error("❌ Error: Could not parse your polynomial.")
        st.write(f"**Details:** {e}")
        st.info("💡 Try formats like: `x^3 - 6x^2 + 11x - 6` or `x^4 - 13x^2 + 36`")

elif solve_button:
    st.info("📝 Please enter a polynomial first.")

# ============================================
# EXECUTE CHALLENGE MODE & FOOTER
# ============================================
polynomial_challenge()

st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.4); font-size: 0.8rem; margin-top: 1.5rem;'>Created for Mathematics Education | ApexTech</p>", unsafe_allow_html=True)