import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Math Lab | Interactive Exploration",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS (Theme-Adaptive & Card Polish)
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Top Bar & Footers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Layout Tightening */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px;
    }
    
    /* Card Container Styling - Adaptive to Light & Dark Theme */
    div[data-testid="stColumn"] > div {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 1.2rem;
        transition: all 0.25s ease-in-out;
    }
    
    div[data-testid="stColumn"] > div:hover {
        transform: translateY(-4px);
        border-color: #6366f1;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.15);
    }
    
    /* Ensure Metric Text stays high contrast */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: var(--text-color) !important;
    }
    
    /* Custom Badges */
    .badge {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }
    .badge-intro { background: #eef2ff; color: #4f46e5; }
    .badge-inter { background: #ecfdf5; color: #059669; }
    .badge-adv   { background: #fffbeb; color: #d97706; }
</style>
""", unsafe_allow_html=True)

# ============================================
# NAVIGATION & HEADER
# ============================================
st.title("📐 Math Lab")
st.caption("Interactive visual tools for exploring algebra, function behavior, and calculus concepts.")

st.markdown("---")

# ============================================
# LIVE INTERACTIVE PLAYGROUND
# ============================================
st.subheader("⚡ Dynamic Playground")

with st.sidebar:
    st.header("🎛️ Live Sandbox Controls")
    func_type = st.selectbox("Select Function Family", ["Linear: f(x) = mx + c", "Quadratic: f(x) = ax² + bx + c"])
    
    x_val = np.linspace(-10, 10, 400)
    
    if "Linear" in func_type:
        m = st.slider("Slope (m)", -5.0, 5.0, 2.4, 0.1)
        c = st.slider("Y-Intercept (c)", -10.0, 10.0, -6.5, 0.5)
        y_val = m * x_val + c
        
        # Clean mathematical sign formatting (+ / -)
        sign = "+" if c >= 0 else "-"
        title_str = f"f(x) = {m}x {sign} {abs(c)}"
    else:
        a = st.slider("Curvature (a)", -3.0, 3.0, 1.0, 0.1)
        b = st.slider("Linear Term (b)", -5.0, 5.0, 0.0, 0.5)
        c = st.slider("Y-Intercept (c)", -10.0, 10.0, -2.0, 0.5)
        y_val = a * (x_val**2) + b * x_val + c
        
        b_sign = "+" if b >= 0 else "-"
        c_sign = "+" if c >= 0 else "-"
        title_str = f"f(x) = {a}x² {b_sign} {abs(b)}x {c_sign} {abs(c)}"

# Render Plotly Visualizer
fig = go.Figure()
fig.add_trace(go.Scatter(x=x_val, y=y_val, mode='lines', name=title_str, line=dict(color='#6366f1', width=3)))
fig.update_layout(
    title=f"Live Plot: {title_str}",
    xaxis_title="x",
    yaxis_title="f(x)",
    xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='#64748b', range=[-10, 10]),
    yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='#64748b', range=[-10, 10]),
    template="plotly_dark",
    height=380,
    margin=dict(l=20, r=20, t=40, b=20)
)

col_graph, col_metrics = st.columns([2, 1])

with col_graph:
    st.plotly_chart(fig, use_container_width=True)

with col_metrics:
    st.markdown("### 📊 Live Analytics")
    if "Linear" in func_type:
        st.metric(label="Slope (m)", value=m)
        root = -c/m if m != 0 else "None"
        st.metric(label="X-Intercept (Root)", value=f"{root:.2f}" if isinstance(root, float) else root)
    else:
        vertex_x = -b / (2*a) if a != 0 else 0
        vertex_y = a*(vertex_x**2) + b*vertex_x + c
        st.metric(label="Vertex Coordinates", value=f"({vertex_x:.2f}, {vertex_y:.2f})")
        disc = b**2 - 4*a*c
        st.metric(label="Discriminant (Δ)", value=f"{disc:.2f}")

st.markdown("---")

# ============================================
# MODULES DASHBOARD GRID
# ============================================
st.subheader("🛠️ Dedicated Explorer Modules")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 📈 Linear")
    st.write("Explore slopes, rates of change, standard form, and dual-intercept properties.")
    st.markdown('<span class="badge badge-intro">Introductory</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("Launch Tool ➔", "https://math-lab-nfwbmpekzmcjaqbt97zfce.streamlit.app/", use_container_width=True)

with col2:
    st.markdown("### 📊 Quadratic")
    st.write("Analyze parabolas, vertex optimization, real/complex roots, and axis symmetry.")
    st.markdown('<span class="badge badge-inter">Intermediate</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("Launch Tool ➔", "https://math-lab-fmdbv9utg75beebjgmg5cw.streamlit.app/", use_container_width=True)

with col3:
    st.markdown("### 🔢 Polynomial")
    st.write("Higher-degree function behavior, synthetic division, and local extrema.")
    st.markdown('<span class="badge badge-adv">Advanced</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("Launch Tool ➔", "https://math-lab-6xbscvtsxvjsrn5lpspaje.streamlit.app/", use_container_width=True)

with col4:
    st.markdown("### ∫ Calculus")
    st.write("Visual derivatives, secant-to-tangent limits, and definite integral areas.")
    st.markdown('<span class="badge badge-adv">Advanced</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("Launch Tool ➔", "https://w8ynfocpak99duzyypg2yk.streamlit.app/", use_container_width=True)

st.markdown("---")

# ============================================
# QUICK CALC UTILITY
# ============================================
with st.expander("🧮 Quick Math Engine"):
    st.write("Perform fast symbolic expression evaluations:")
    expr_input = st.text_input("Enter a mathematical expression in terms of `x`:", value="x**3 - 3*x + 2")
    eval_x = st.number_input("Evaluate at x =", value=2.0)
    
    try:
        allowed_names = {"x": eval_x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "sqrt": np.sqrt}
        res = eval(expr_input, {"__builtins__": None}, allowed_names)
        st.success(f"Result: **f({eval_x}) = {res}**")
    except Exception as e:
        st.error(f"Invalid Expression: {e}")