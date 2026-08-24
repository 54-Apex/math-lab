import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import sympy as sp
import re

st.set_page_config(page_title="Quadratic Explorer", page_icon="📈")
st.title("📈 Quadratic Functions: y = ax² + bx + c")

# Initialize session state
if 'q_score' not in st.session_state:
    st.session_state.q_score = 0
if 'q_attempts' not in st.session_state:
    st.session_state.q_attempts = 0
if 'q_history' not in st.session_state:
    st.session_state.q_history = []

# Function to fix implicit multiplication
def fix_implicit_multiplication(expr):
    """Insert * between numbers and variables, e.g., 3x -> 3*x"""
    expr = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'([a-zA-Z])(\d+)', r'\1*\2', expr)
    expr = re.sub(r'\)\(', r')*(', expr)
    return expr

# ============================================
# FUNCTION: Challenge Mode (reused in both tabs)
# ============================================
def challenge_mode(tab_id):
    """Display challenge mode - reused in both tabs"""
    
    if f'q_challenge_active_{tab_id}' not in st.session_state:
        st.session_state[f'q_challenge_active_{tab_id}'] = False
    if f'q_challenge_answered_{tab_id}' not in st.session_state:
        st.session_state[f'q_challenge_answered_{tab_id}'] = False
    if f'q_challenge_attempts_{tab_id}' not in st.session_state:
        st.session_state[f'q_challenge_attempts_{tab_id}'] = 0
    
    st.divider()
    st.subheader("🎯 Challenge Mode - Find the Key Features!")
    
    # Use unique key for this button
    if st.button(f"🔄 Generate New Quadratic Challenge", key=f"generate_{tab_id}"):
        st.session_state[f'q_challenge_a_{tab_id}'] = random.randint(-5, 5)
        while st.session_state[f'q_challenge_a_{tab_id}'] == 0:
            st.session_state[f'q_challenge_a_{tab_id}'] = random.randint(-5, 5)
        st.session_state[f'q_challenge_b_{tab_id}'] = random.randint(-10, 10)
        st.session_state[f'q_challenge_c_{tab_id}'] = random.randint(-10, 10)
        st.session_state[f'q_challenge_active_{tab_id}'] = True
        st.session_state[f'q_challenge_answered_{tab_id}'] = False
        st.session_state[f'q_challenge_attempts_{tab_id}'] = 0
    
    if st.session_state[f'q_challenge_active_{tab_id}'] and not st.session_state[f'q_challenge_answered_{tab_id}']:
        a_q = st.session_state[f'q_challenge_a_{tab_id}']
        b_q = st.session_state[f'q_challenge_b_{tab_id}']
        c_q = st.session_state[f'q_challenge_c_{tab_id}']
        
        st.markdown(f"""
        ### 📝 Your Task:
        Given the quadratic function:
        
        **y = {a_q}x² + {b_q}x + {c_q}**
        
        Answer the questions below:
        """)
        
        vertex_x = -b_q / (2*a_q)
        vertex_y = a_q * vertex_x**2 + b_q * vertex_x + c_q
        
        st.markdown("**1. What is the vertex?**")
        col1, col2 = st.columns(2)
        with col1:
            user_vx = st.number_input("x-coordinate:", value=0.0, step=0.5, key=f"user_vx_{tab_id}")
        with col2:
            user_vy = st.number_input("y-coordinate:", value=0.0, step=0.5, key=f"user_vy_{tab_id}")
        
        disc = b_q**2 - 4*a_q*c_q
        st.markdown("**2. What are the roots (x-intercepts)?**")
        
        if disc < 0:
            st.info("💡 This parabola has NO real roots (discriminant < 0)")
            user_root1 = 0.0
            user_root2 = 0.0
        else:
            root1 = (-b_q - math.sqrt(disc)) / (2*a_q)
            root2 = (-b_q + math.sqrt(disc)) / (2*a_q)
            col1, col2 = st.columns(2)
            with col1:
                user_root1 = st.number_input("First root:", value=0.0, step=0.5, key=f"user_root1_{tab_id}")
            with col2:
                user_root2 = st.number_input("Second root:", value=0.0, step=0.5, key=f"user_root2_{tab_id}")
        
        st.markdown("**3. Does the parabola open up or down?**")
        direction = st.selectbox("Direction:", ["Select...", "Opens Up", "Opens Down"], key=f"direction_{tab_id}")
        
        if st.button("✅ Check My Answers", key=f"check_{tab_id}"):
            st.session_state[f'q_challenge_attempts_{tab_id}'] += 1
            score = 0
            total = 3
            
            if abs(user_vx - vertex_x) < 0.1 and abs(user_vy - vertex_y) < 0.1:
                score += 1
                st.success("✅ Vertex is correct!")
            else:
                st.error(f"❌ Vertex: The correct answer is ({vertex_x:.2f}, {vertex_y:.2f})")
            
            if disc < 0:
                st.info("ℹ️ No real roots – that was a trick question!")
                score += 1
            else:
                if abs(user_root1 - root1) < 0.1 and abs(user_root2 - root2) < 0.1:
                    score += 1
                    st.success("✅ Roots are correct!")
                elif abs(user_root1 - root2) < 0.1 and abs(user_root2 - root1) < 0.1:
                    score += 1
                    st.success("✅ Roots are correct (order doesn't matter)!")
                else:
                    st.error(f"❌ Roots: The correct answers are {root1:.2f} and {root2:.2f}")
            
            correct_direction = "Opens Up" if a_q > 0 else "Opens Down"
            if direction == correct_direction:
                score += 1
                st.success("✅ Direction is correct!")
            else:
                st.error(f"❌ Direction: The parabola {correct_direction}")
            
            st.divider()
            st.subheader(f"📊 Your Score: {score}/{total}")
            st.session_state.q_score += score
            st.session_state.q_attempts += 1
            
            if st.session_state.q_attempts > 0:
                accuracy = (st.session_state.q_score / (st.session_state.q_attempts * 3)) * 100
                st.metric("🎯 Overall Accuracy", f"{accuracy:.0f}%")
            
            if score == 3:
                st.success("🌟 Perfect! You're a quadratic master!")
                st.balloons()
            elif score >= 2:
                st.info("👍 Good job! Almost perfect – review the errors above.")
            else:
                st.warning("📚 Keep practicing! Use the sliders above to explore more.")
            
            st.session_state.q_history.append(f"y = {a_q}x² + {b_q}x + {c_q} → Score: {score}/3")
            st.session_state[f'q_challenge_answered_{tab_id}'] = True
    
    if st.session_state[f'q_challenge_active_{tab_id}']:
        with st.expander("📜 Challenge History"):
            if len(st.session_state.q_history) > 0:
                for item in st.session_state.q_history[-10:]:
                    st.write(f"- {item}")
            else:
                st.write("No challenges completed yet.")
    
    if st.session_state.get(f'q_challenge_answered_{tab_id}', False):
        if st.button("🔄 Try Another Challenge", key=f"another_{tab_id}"):
            st.session_state[f'q_challenge_active_{tab_id}'] = False
            st.session_state[f'q_challenge_answered_{tab_id}'] = False
            st.session_state[f'q_challenge_attempts_{tab_id}'] = 0
            st.rerun()

# ============================================
# Create Tabs
# ============================================
tab1, tab2 = st.tabs(["✍️ Enter Equation", "🎚️ Use Sliders"])

# ============================================
# TAB 1: Enter Equation
# ============================================
with tab1:
    st.markdown("### Enter a quadratic equation and see it graphed instantly!")
    st.markdown("**Examples:** `3x^2 - 5x + 1`, `x^2 - 4`, `2x^2 + 3x`")
    
    equation_input = st.text_input(
        "Enter your equation (use x as the variable):",
        placeholder="e.g. 3x^2 - 5x + 1",
        key="equation_input"
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        parse_button = st.button("📊 Plot Equation", use_container_width=True)
    
    if parse_button and equation_input:
        try:
            # Clean up the input
            expr_str = equation_input.strip()
            
            if "=" in expr_str:
                expr_str = expr_str.split("=")[1].strip()
            
            expr_str = expr_str.replace("^", "**")
            expr_str = fix_implicit_multiplication(expr_str)
            
            x = sp.Symbol('x')
            expr = sp.sympify(expr_str)
            expr_expanded = sp.expand(expr)
            
            # Get coefficients
            try:
                poly = sp.Poly(expr_expanded, x)
                coeffs = poly.all_coeffs()
                
                if len(coeffs) == 3:
                    a = float(coeffs[0])
                    b = float(coeffs[1])
                    c = float(coeffs[2])
                elif len(coeffs) == 2:
                    a = 0.0
                    b = float(coeffs[0])
                    c = float(coeffs[1])
                elif len(coeffs) == 1:
                    a = 0.0
                    b = 0.0
                    c = float(coeffs[0])
                else:
                    a, b, c = 0, 0, 0
            except:
                a = float(sp.coeff(expr_expanded, x, 2)) if sp.coeff(expr_expanded, x, 2) != 0 else 0.0
                b = float(sp.coeff(expr_expanded, x, 1)) if sp.coeff(expr_expanded, x, 1) != 0 else 0.0
                c = float(sp.coeff(expr_expanded, x, 0)) if sp.coeff(expr_expanded, x, 0) != 0 else 0.0
            
            is_quadratic = (a != 0)
            
            def f(val):
                return float(expr.subs(x, val))
            
            x_vals = np.linspace(-10, 10, 500)
            y_vals = [f(val) for val in x_vals]
            
            display_eq = f"y = {equation_input}"
            if "=" not in equation_input:
                display_eq = f"y = {equation_input}"
            st.latex(display_eq)
            
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(x_vals, y_vals, color='purple', linewidth=3)
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)
            ax.grid(True, alpha=0.3)
            
            y_min = min(y_vals)
            y_max = max(y_vals)
            y_range = y_max - y_min
            if y_range < 0.1:
                y_range = 1
            ax.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)
            ax.set_xlim(-10, 10)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(f"{display_eq}", fontsize=14)
            
            if is_quadratic:
                discriminant = b**2 - 4*a*c
                vertex_x = -b / (2*a)
                vertex_y = a * vertex_x**2 + b * vertex_x + c
                ax.plot(vertex_x, vertex_y, 'go', markersize=10)
                ax.annotate(f"Vertex ({vertex_x:.2f}, {vertex_y:.2f})", 
                            (vertex_x, vertex_y), xytext=(10, 10), 
                            textcoords='offset points', fontsize=10, color='green')
                
                if discriminant >= 0:
                    root1 = (-b - math.sqrt(discriminant)) / (2*a)
                    root2 = (-b + math.sqrt(discriminant)) / (2*a)
                    ax.plot(root1, 0, 'ro', markersize=8)
                    ax.plot(root2, 0, 'ro', markersize=8)
                    ax.annotate(f"x = {root1:.2f}", (root1, 0), xytext=(5, -15), 
                                textcoords='offset points', fontsize=9, color='red')
                    ax.annotate(f"x = {root2:.2f}", (root2, 0), xytext=(5, -15), 
                                textcoords='offset points', fontsize=9, color='red')
                
                ax.plot(0, c, 'bo', markersize=8)
                ax.annotate(f"y-intercept (0, {c:.1f})", (0, c), xytext=(10, -15), 
                            textcoords='offset points', fontsize=10, color='blue')
            
            st.pyplot(fig)
            
            if is_quadratic:
                st.subheader("📊 Key Features")
                discriminant = b**2 - 4*a*c
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📍 Vertex", f"({vertex_x:.2f}, {vertex_y:.2f})")
                with col2:
                    st.metric("🔵 Discriminant", f"{discriminant:.2f}")
                    if discriminant > 0:
                        st.write("✅ 2 real roots")
                    elif discriminant == 0:
                        st.write("✅ 1 repeated root")
                    else:
                        st.write("❌ No real roots")
                with col3:
                    st.metric("🔄 Direction", "Opens Up" if a > 0 else "Opens Down")
                
                if discriminant >= 0:
                    st.success(f"**Roots (x-intercepts):** x = {root1:.2f} and x = {root2:.2f}")
                else:
                    st.info("**No real roots** – the parabola does not cross the x-axis")
                
                st.divider()
                st.write(f"**Coefficients:** a = {a:.2f}, b = {b:.2f}, c = {c:.2f}")
            elif b != 0:
                st.info(f"📉 **Linear function:** y = {b}x + {c}")
                st.info(f"**Slope:** {b}")
                st.info(f"**y-intercept:** {c}")
            else:
                st.info(f"📊 **Constant function:** y = {c}")
            
            st.divider()
            st.caption("📖 Tip: Enter equations like `3x^2 - 5x + 1`, `x^2 - 4`, or `-2x^2 + 3x - 1`")
            
        except Exception as e:
            st.error(f"❌ Error: Could not parse your equation. Please check the format.")
            st.write(f"**Details:** {e}")
            st.info("💡 Try formats like: `3x^2 - 5x + 1`, `x^2 - 4`, or `2x^2 + 3x`")
    
    elif parse_button:
        st.info("📝 Please enter an equation first.")
    
# ============================================
# TAB 2: Use Sliders
# ============================================
with tab2:
    st.markdown("*Move the sliders to explore how a, b, and c change the parabola!*")
    
    # Main sliders
    col1, col2, col3 = st.columns(3)
    with col1:
        a = st.slider("a (quadratic)", -3.0, 3.0, 1.0, 0.1, key="slider_a")
    with col2:
        b = st.slider("b (linear)", -10.0, 10.0, 0.0, 0.5, key="slider_b")
    with col3:
        c = st.slider("c (constant)", -10.0, 10.0, 0.0, 0.5, key="slider_c")
    
    st.latex(f"y = {a}x² + {b}x + {c}")
    
    # Generate data
    x_plot = np.linspace(-10, 10, 500)
    y_plot = a * x_plot**2 + b * x_plot + c
    
    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_plot, y_plot, color='purple', linewidth=3)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-20, 20)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"y = {a}x² + {b}x + {c}", fontsize=14)
    
    discriminant = b**2 - 4*a*c
    
    # Vertex
    if a != 0:
        vertex_x = -b / (2*a)
        vertex_y = a * vertex_x**2 + b * vertex_x + c
        ax.plot(vertex_x, vertex_y, 'go', markersize=10)
        ax.annotate(f"Vertex ({vertex_x:.2f}, {vertex_y:.2f})", 
                    (vertex_x, vertex_y), xytext=(10, 10), 
                    textcoords='offset points', fontsize=10, color='green')
    
    # Roots
    if a != 0 and discriminant >= 0:
        root1 = (-b - math.sqrt(discriminant)) / (2*a)
        root2 = (-b + math.sqrt(discriminant)) / (2*a)
        ax.plot(root1, 0, 'ro', markersize=8)
        ax.plot(root2, 0, 'ro', markersize=8)
        ax.annotate(f"x = {root1:.2f}", (root1, 0), xytext=(5, -15), 
                    textcoords='offset points', fontsize=9, color='red')
        ax.annotate(f"x = {root2:.2f}", (root2, 0), xytext=(5, -15), 
                    textcoords='offset points', fontsize=9, color='red')
    
    # y-intercept
    ax.plot(0, c, 'bo', markersize=8)
    ax.annotate(f"y-intercept (0, {c:.1f})", (0, c), xytext=(10, -15), 
                textcoords='offset points', fontsize=10, color='blue')
    
    st.pyplot(fig)
    
    # Key features
    st.subheader("🔍 Key Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if a != 0:
            vertex_x = -b / (2*a)
            vertex_y = a * vertex_x**2 + b * vertex_x + c
            st.metric(" Vertex", f"({vertex_x:.2f}, {vertex_y:.2f})")
        else:
            st.metric("Vertex", "Not a quadratic")
    
    with col2:
        st.metric("🔵 Discriminant", f"{discriminant:.2f}")
        if discriminant > 0:
            st.write("✅ 2 distinct real roots")
        elif discriminant == 0:
            st.write("✅ 1 repeated real root")
        else:
            st.write("❌ No real roots (complex)")
    
    with col3:
        st.metric("🔄 Direction", "Opens Up" if a > 0 else "Opens Down" if a < 0 else "Linear")
    
    if a != 0 and discriminant >= 0:
        root1 = (-b - math.sqrt(discriminant)) / (2*a)
        root2 = (-b + math.sqrt(discriminant)) / (2*a)
        st.info(f"**Roots (x-intercepts):** x = {root1:.2f} and x = {root2:.2f}")
    elif a != 0 and discriminant < 0:
        st.warning("⚠️ No real roots – the parabola does not cross the x-axis")
    elif a == 0:
        st.info("📉 This is a linear function (a = 0)")
    
# Render one shared challenge section below both exploration modes.
challenge_mode("quadratic")

st.divider()
st.markdown("👩‍🏫 **Created by ApexTech for Mathematics Teachers and Students** | Explore how a, b, and c shape the parabola!")