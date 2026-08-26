import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import re
import random

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Calculus Explorer",
    page_icon="🧮",
    layout="wide"
)

# ============================================
# INITIALIZE SESSION STATE FOR CHALLENGES
# ============================================
if 'calc_score' not in st.session_state:
    st.session_state.calc_score = 0
if 'calc_attempts' not in st.session_state:
    st.session_state.calc_attempts = 0
if 'calc_history' not in st.session_state:
    st.session_state.calc_history = []

# ============================================
# SIDEBAR SCOREBOARD
# ============================================
with st.sidebar:
    st.header("🏆 Performance Dashboard")
    st.metric(label="Total Score", value=f"{st.session_state.calc_score} pts")
    st.metric(label="Challenges Attempted", value=st.session_state.calc_attempts)
    
    if st.session_state.calc_attempts > 0:
        accuracy = (st.session_state.calc_score / (st.session_state.calc_attempts * 3)) * 100
        st.write(f"**Accuracy:** {accuracy:.1f}%")
        
    st.divider()
    if st.button("🔄 Reset Score"):
        st.session_state.calc_score = 0
        st.session_state.calc_attempts = 0
        st.rerun()

# ============================================
# APP TITLE
# ============================================
st.title("🧮 Calculus Explorer")
st.markdown("Explore derivatives and integrals of polynomial functions with interactive plots and practice challenges!")

# ============================================
# TABS
# ============================================
tab1, tab2 = st.tabs(["f' Derivative Explorer", "∫ Integral Explorer"])

# ============================================
# TAB 1: DERIVATIVE EXPLORER
# ============================================
with tab1:
    st.markdown("### Enter a polynomial to find its derivative")
    st.markdown("**Examples:** `x^3 - 6x^2 + 11x - 6`, `x^4 - 13x^2 + 36`, `2x^5 - 3x^3 + x`")
    
    # Initialize session state for derivative
    if 'show_second_deriv' not in st.session_state:
        st.session_state.show_second_deriv = False
    if 'deriv_result' not in st.session_state:
        st.session_state.deriv_result = None
    if 'deriv_original' not in st.session_state:
        st.session_state.deriv_original = None
    if 'deriv_x_symbol' not in st.session_state:
        st.session_state.deriv_x_symbol = None
    
    deriv_input = st.text_input(
        "Enter your polynomial (use x as the variable):",
        placeholder="e.g. x^3 - 6x^2 + 11x - 6",
        key="deriv_input"
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        deriv_button = st.button("📐 Find Derivative", use_container_width=True, key="deriv_calc")
    
    if deriv_button and deriv_input:
        try:
            x = sp.Symbol('x')
            
            expr_str = deriv_input.strip()
            if "=" in expr_str:
                expr_str = expr_str.split("=")[1].strip()
            expr_str = expr_str.replace("^", "**")
            expr_str = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expr_str)
            expr_str = re.sub(r'([a-zA-Z])(\d+)', r'\1*\2', expr_str)
            
            expr = sp.sympify(expr_str)
            expr_expanded = sp.expand(expr)
            
            deriv = sp.diff(expr_expanded, x)
            deriv_expanded = sp.expand(deriv)
            
            st.session_state.deriv_original = expr_expanded
            st.session_state.deriv_result = deriv_expanded
            st.session_state.deriv_x_symbol = x
            
        except Exception as e:
            st.error("❌ Error: Could not parse your polynomial.")
            st.write(f"**Details:** {e}")
            st.info("💡 Try formats like: `x^3 - 6x^2 + 11x - 6`")
    
    # Display results if we have them in session state
    if st.session_state.deriv_result is not None:
        x = st.session_state.deriv_x_symbol if st.session_state.deriv_x_symbol is not None else sp.Symbol('x')
        expr_expanded = st.session_state.deriv_original
        deriv_expanded = st.session_state.deriv_result
        
        st.latex(f"f(x) = {sp.latex(expr_expanded)}")
        st.latex(f"f'(x) = {sp.latex(deriv_expanded)}")
        
        def f_original(val):
            return float(expr_expanded.subs(x, val))
        
        def f_derivative(val):
            return float(deriv_expanded.subs(x, val))
        
        x_vals = np.linspace(-10, 10, 500)
        y_original = [f_original(val) for val in x_vals]
        y_derivative = [f_derivative(val) for val in x_vals]
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x_vals, y_original, color='purple', linewidth=3, label="Original f(x)")
        ax.plot(x_vals, y_derivative, color='orange', linewidth=2, linestyle='--', label="Derivative f'(x)")
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-10, 10)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
        ax.set_title("Original vs Derivative", fontsize=14)
        
        st.pyplot(fig)
        
        # Second derivative checkbox with session state
        st.session_state.show_second_deriv = st.checkbox(
            "Show second derivative f''(x)", 
            value=st.session_state.show_second_deriv
        )
        
        if st.session_state.show_second_deriv:
            deriv2 = sp.diff(deriv_expanded, x)
            deriv2_expanded = sp.expand(deriv2)
            st.latex(f"f''(x) = {sp.latex(deriv2_expanded)}")
            
            def f_second(val):
                return float(deriv2_expanded.subs(x, val))
            
            y_second = [f_second(val) for val in x_vals]
            
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            ax2.plot(x_vals, y_original, color='purple', linewidth=3, label="Original f(x)")
            ax2.plot(x_vals, y_derivative, color='orange', linewidth=2, linestyle='--', label="Derivative f'(x)")
            ax2.plot(x_vals, y_second, color='green', linewidth=2, linestyle=':', label="Second Derivative f''(x)")
            ax2.axhline(0, color='black', linewidth=0.5)
            ax2.axvline(0, color='black', linewidth=0.5)
            ax2.grid(True, alpha=0.3)
            ax2.set_xlim(-10, 10)
            ax2.set_xlabel("x")
            ax2.set_ylabel("y")
            ax2.legend()
            ax2.set_title("Original vs Derivatives", fontsize=14)
            
            st.pyplot(fig2)
        
        # === CHALLENGE MODE - DERIVATIVE ===
        st.divider()
        st.subheader("🎯 Challenge Mode - Derivative Practice!")
        
        # Initialize derivative challenge state
        if 'deriv_challenge_active' not in st.session_state:
            st.session_state.deriv_challenge_active = False
        if 'deriv_challenge_answered' not in st.session_state:
            st.session_state.deriv_challenge_answered = False
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 Generate Derivative Challenge", key="deriv_challenge"):
                # Reset state
                st.session_state.deriv_challenge_active = False
                st.session_state.deriv_challenge_answered = False
                
                # Generate random polynomial (degree 2-4)
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
                
                # Calculate derivative
                deriv = sp.diff(expr, x)
                deriv_expanded = sp.expand(deriv)
                
                st.session_state.deriv_challenge_expr = expr
                st.session_state.deriv_challenge_answer = deriv_expanded
                st.session_state.deriv_challenge_active = True
                st.session_state.deriv_challenge_answered = False
                st.rerun()
        
        # Display the challenge if active
        if st.session_state.get('deriv_challenge_active', False):
            expr = st.session_state.deriv_challenge_expr
            correct_deriv = st.session_state.deriv_challenge_answer
            
            st.markdown(f"""
            ### 📝 Your Task:
            Find the derivative of:
            
            $${sp.latex(expr)}$$
            
            Enter your answer below (use x as the variable):
            """)
            
            # Show examples of acceptable formats
            with st.expander("📖 How to enter your answer"):
                st.markdown("""
                **Acceptable formats:**
                - `3x^2 - 4x + 2` (for 3x² - 4x + 2)
                - `-2x^3 + 5x - 1` (for -2x³ + 5x - 1)
                - `0.5*x^2 + 3x` (decimal)
                - `x^2/2 + 2x` (fractions)
                
                **Important:** Use **lowercase `x`** (not uppercase X)!
                """)
            
            user_deriv = st.text_input("Your derivative:", placeholder="e.g. 3x^2 - 4x + 2", key="user_deriv")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✅ Check My Answer", key="deriv_check"):
                    try:
                        user_str = user_deriv.strip()
                        user_str = user_str.replace("^", "**")
                        user_str = user_str.replace('X', 'x')
                        user_str = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', user_str)
                        user_str = re.sub(r'([a-zA-Z])(\d+)', r'\1*\2', user_str)
                        
                        x = sp.Symbol('x')
                        
                        try:
                            user_expr = sp.sympify(user_str)
                        except Exception:
                            user_str = user_str.replace(" ", "")
                            user_expr = sp.sympify(user_str)
                        
                        user_expanded = sp.expand(user_expr)
                        correct_expanded = sp.expand(correct_deriv)
                        
                        is_correct = False
                        if user_expanded == correct_expanded:
                            is_correct = True
                        else:
                            diff = sp.simplify(user_expanded - correct_expanded)
                            if diff == 0:
                                is_correct = True
                        
                        if is_correct:
                            st.success("✅ Perfect! Your derivative is correct! 🎉")
                            st.balloons()
                            st.session_state.calc_score += 3
                        else:
                            st.error(f"❌ Not quite. The correct answer is {sp.latex(correct_deriv)}")
                            st.info("💡 Hint: Apply the power rule: multiply by the exponent and reduce the exponent by 1.")
                            
                            st.write("**Your answer:**")
                            st.latex(sp.latex(user_expanded))
                            st.write("**Expected:**")
                            st.latex(sp.latex(correct_expanded))
                            
                            try:
                                ratio = sp.simplify(user_expanded / correct_expanded)
                                if ratio.is_constant():
                                    st.warning(f"💡 Your answer is {sp.latex(ratio)} times the correct derivative. Check your coefficients!")
                            except Exception:
                                pass
                        
                        st.session_state.deriv_challenge_answered = True
                        st.session_state.calc_attempts += 1
                        
                    except Exception as e:
                        st.error("❌ Could not parse your answer. Check the format.")
                        st.info("💡 Try formats like: `3x^2 - 4x + 2`")
                        st.write(f"**Details:** {e}")
            
            with col2:
                if st.button("🔄 Skip This Question", key="deriv_skip"):
                    st.session_state.deriv_challenge_active = False
                    st.session_state.deriv_challenge_answered = False
                    st.rerun()
            
            if st.session_state.get('deriv_challenge_answered', False):
                if st.button("🔄 Try Another Derivative Challenge", key="deriv_another"):
                    st.session_state.deriv_challenge_active = False
                    st.session_state.deriv_challenge_answered = False
                    st.rerun()

# ============================================
# TAB 2: INTEGRAL EXPLORER
# ============================================
with tab2:
    st.markdown("### Enter a polynomial to find its integral")
    st.markdown("**Examples:** `x^2 + 3x + 2`, `x^3 - 6x^2 + 11x - 6`, `2x^2 - 5`")
    
    if 'integral_result' not in st.session_state:
        st.session_state.integral_result = None
    if 'integral_original' not in st.session_state:
        st.session_state.integral_original = None
    if 'integral_x_symbol' not in st.session_state:
        st.session_state.integral_x_symbol = None
    
    integral_input = st.text_input(
        "Enter your polynomial (use x as the variable):",
        placeholder="e.g. x^2 + 3x + 2",
        key="integral_input"
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        integral_button = st.button("∫ Find Integral", use_container_width=True, key="integral_calc")
    
    if integral_button and integral_input:
        try:
            x = sp.Symbol('x')
            
            expr_str = integral_input.strip()
            if "=" in expr_str:
                expr_str = expr_str.split("=")[1].strip()
            expr_str = expr_str.replace("^", "**")
            expr_str = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expr_str)
            expr_str = re.sub(r'([a-zA-Z])(\d+)', r'\1*\2', expr_str)
            
            expr = sp.sympify(expr_str)
            expr_expanded = sp.expand(expr)
            
            integral = sp.integrate(expr_expanded, x)
            integral_expanded = sp.expand(integral)
            
            st.session_state.integral_original = expr_expanded
            st.session_state.integral_result = integral_expanded
            st.session_state.integral_x_symbol = x
            
        except Exception as e:
            st.error("❌ Error: Could not parse your polynomial.")
            st.write(f"**Details:** {e}")
            st.info("💡 Try formats like: `x^2 + 3x + 2` or `x^3 - 6x^2 + 11x - 6`")
    
    if st.session_state.integral_result is not None:
        x = st.session_state.integral_x_symbol if st.session_state.integral_x_symbol is not None else sp.Symbol('x')
        expr_expanded = st.session_state.integral_original
        integral_expanded = st.session_state.integral_result
        
        st.latex(f"f(x) = {sp.latex(expr_expanded)}")
        st.latex(f"\\int f(x) \\, dx = {sp.latex(integral_expanded)} + C")
        
        # === DEFINITE INTEGRAL SECTION ===
        st.subheader("📊 Definite Integral")
        col1, col2 = st.columns(2)
        with col1:
            lower_bound = st.number_input("Lower bound (a):", value=0.0, step=0.5, key="lower_bound")
        with col2:
            upper_bound = st.number_input("Upper bound (b):", value=1.0, step=0.5, key="upper_bound")
        
        if st.button("Calculate Definite Integral", key="definite_button"):
            try:
                x = st.session_state.integral_x_symbol if st.session_state.integral_x_symbol is not None else sp.Symbol('x')
                
                definite_result = sp.integrate(expr_expanded, (x, lower_bound, upper_bound))
                result_float = float(definite_result)
                
                st.success(f"∫ from {lower_bound} to {upper_bound} = {result_float:.6f}")
                
                x_vals = np.linspace(lower_bound - 1, upper_bound + 1, 500)
                y_vals = [float(expr_expanded.subs(x, val)) for val in x_vals]
                
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.plot(x_vals, y_vals, color='purple', linewidth=3, label="f(x)")
                
                x_fill = np.linspace(lower_bound, upper_bound, 100)
                y_fill = [float(expr_expanded.subs(x, val)) for val in x_fill]
                ax.fill_between(x_fill, 0, y_fill, alpha=0.3, color='purple', label=f'Area = {result_float:.3f}')
                
                ax.axhline(0, color='black', linewidth=0.5)
                ax.axvline(0, color='black', linewidth=0.5)
                ax.grid(True, alpha=0.3)
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.legend()
                ax.set_title(f"Area under f(x) from {lower_bound} to {upper_bound}", fontsize=14)
                
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"❌ Error calculating definite integral: {e}")
                st.info("💡 Make sure your function is continuous on the interval and try integer bounds.")
        
        # === INDEFINITE INTEGRAL GRAPH ===
        st.subheader("📈 Integral Graph (C = 0)")
        
        def f_original(val):
            return float(expr_expanded.subs(x, val))
        
        def f_integral(val):
            return float(integral_expanded.subs(x, val))
        
        x_vals = np.linspace(-10, 10, 500)
        y_original = [f_original(val) for val in x_vals]
        y_integral = [f_integral(val) for val in x_vals]
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x_vals, y_original, color='purple', linewidth=3, label="Original f(x)")
        ax.plot(x_vals, y_integral, color='green', linewidth=2, linestyle='--', label="Integral (C=0)")
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-10, 10)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
        ax.set_title("Original vs Integral", fontsize=14)
        
        st.pyplot(fig)
        
        # === CHALLENGE MODE - INTEGRAL ===
        st.divider()
        st.subheader("🎯 Challenge Mode - Integral Practice!")
        
        if 'integral_challenge_active' not in st.session_state:
            st.session_state.integral_challenge_active = False
        if 'integral_challenge_answered' not in st.session_state:
            st.session_state.integral_challenge_answered = False
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 Generate Integral Challenge", key="integral_challenge"):
                st.session_state.integral_challenge_active = False
                st.session_state.integral_challenge_answered = False
                
                degree = random.randint(1, 3)
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
                
                integral = sp.integrate(expr, x)
                integral_expanded = sp.expand(integral)
                
                st.session_state.integral_challenge_expr = expr
                st.session_state.integral_challenge_answer = integral_expanded
                st.session_state.integral_challenge_active = True
                st.session_state.integral_challenge_answered = False
                st.rerun()
        
        if st.session_state.get('integral_challenge_active', False):
            expr = st.session_state.integral_challenge_expr
            correct_integral = st.session_state.integral_challenge_answer
            
            st.markdown(f"""
            ### 📝 Your Task:
            Find the integral of:
            
            $${sp.latex(expr)}$$
            
            Enter your answer below (use x as the variable):
            """)
            
            with st.expander("📖 How to enter your answer"):
                st.markdown("""
                **Acceptable formats:**
                - `x^2/2` (for x²/2)
                - `-3x^4/4` (for -3x⁴/4)
                - `0.5*x^2` (decimal)
                - `x^2/2 + 2x` (multiple terms)
                - `(x^2)/2` (with parentheses)
                
                **Important:** Use **lowercase `x`** (not uppercase X)!
                """)
            
            user_integral = st.text_input("Your integral:", placeholder="e.g. x^2/2 + 2x", key="user_integral")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✅ Check My Answer", key="integral_check"):
                    try:
                        user_str = user_integral.strip()
                        user_str = user_str.replace("^", "**")
                        user_str = user_str.replace('X', 'x')
                        user_str = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', user_str)
                        user_str = re.sub(r'([a-zA-Z])(\d+)', r'\1*\2', user_str)
                        
                        x = sp.Symbol('x')
                        
                        try:
                            user_expr = sp.sympify(user_str)
                        except Exception:
                            user_str = user_str.replace(" ", "")
                            user_expr = sp.sympify(user_str)
                        
                        derivative_check = sp.diff(user_expr, x)
                        derivative_check_expanded = sp.expand(derivative_check)
                        original_expanded = sp.expand(expr)
                        
                        is_correct = False
                        if derivative_check_expanded == original_expanded:
                            is_correct = True
                        else:
                            diff = sp.simplify(derivative_check_expanded - original_expanded)
                            if diff == 0:
                                is_correct = True
                        
                        if is_correct:
                            st.success("✅ Perfect! Your integral is correct! 🎉")
                            st.balloons()
                            st.session_state.calc_score += 3
                        else:
                            st.error(f"❌ Not quite. The correct answer is {sp.latex(correct_integral)} + C")
                            st.info("💡 Hint: Differentiate your answer and see if you get the original function!")
                            
                            st.write("**Your derivative:**")
                            st.latex(sp.latex(derivative_check_expanded))
                            st.write("**Expected:**")
                            st.latex(sp.latex(original_expanded))
                            
                            try:
                                ratio = sp.simplify(derivative_check_expanded / original_expanded)
                                if ratio.is_constant():
                                    st.warning(f"💡 Your derivative is {sp.latex(ratio)} times the original function. Check your coefficients!")
                            except Exception:
                                pass
                        
                        st.session_state.integral_challenge_answered = True
                        st.session_state.calc_attempts += 1
                        
                    except Exception as e:
                        st.error("❌ Could not parse your answer. Check the format.")
                        st.info("💡 Try formats like: `x^2/2` or `0.5*x^2`")
                        st.write(f"**Details:** {e}")
            
            with col2:
                if st.button("🔄 Skip This Question", key="integral_skip"):
                    st.session_state.integral_challenge_active = False
                    st.session_state.integral_challenge_answered = False
                    st.rerun()
            
            if st.session_state.get('integral_challenge_answered', False):
                if st.button("🔄 Try Another Integral Challenge", key="integral_another"):
                    st.session_state.integral_challenge_active = False
                    st.session_state.integral_challenge_answered = False
                    st.rerun()

# ============================================
# FOOTER
# ============================================
st.divider()
st.markdown("Created with love ❤️ for Mathematics Education by ApexTech")