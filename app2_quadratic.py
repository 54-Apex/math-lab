import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import math

st.set_page_config(page_title="Quadratic Explorer", page_icon="📈")
st.title("📈 Quadratic Functions: y = ax² + bx + c")

# Create tabs for two modes
tab1, tab2 = st.tabs(["✍️ Enter Equation", "🎚️ Use Sliders"])

with tab1:
    st.markdown("### Enter a quadratic equation and see it graphed instantly!")
    st.markdown("Examples: `x^2 - 3x + 2`, `2x^2 + 5x - 3`, `-x^2 + 4`")
    
    # User input
    equation_input = st.text_input(
        "Enter your equation (use x as the variable):",
        placeholder="e.g. x^2 - 3x + 2",
        key="equation_input"
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        parse_button = st.button("📊 Plot Equation", use_container_width=True)
    
    if parse_button and equation_input:
        try:
            # Parse the equation - replace ^ with **
            cleaned = equation_input.replace("^", "**")
            # Handle cases where user types y = ...
            if "=" in cleaned:
                cleaned = cleaned.split("=")[1].strip()
            
            # Create function from string
            def f(x_val):
                # Safely evaluate the expression with x as variable
                return eval(cleaned, {"x": x_val, "np": np, "math": math})
            
            # Generate x values
            x_vals = np.linspace(-10, 10, 500)
            y_vals = [f(x) for x in x_vals]
            
            # Extract coefficients for display
            # Try to extract a, b, c for features
            a = 0
            b = 0
            c = 0
            # Simple parsing attempts
            # Remove spaces and handle special cases
            cleaned_display = cleaned.replace("**", "^")
            
            # Try to parse coefficients (basic)
            # This is a simple parser - handles standard forms
            import re
            # Remove spaces
            expr = cleaned.replace(" ", "")
            
            # Find coefficient of x^2
            if "x**2" in expr:
                parts = expr.split("x**2")
                if parts[0] in ["", "+"]:
                    a = 1
                elif parts[0] == "-":
                    a = -1
                else:
                    try:
                        a = float(parts[0])
                    except:
                        a = 1
                
                # Find coefficient of x
                remaining = parts[1] if len(parts) > 1 else ""
                if "x" in remaining:
                    x_parts = remaining.split("x")
                    if x_parts[0] in ["", "+"]:
                        b = 1
                    elif x_parts[0] == "-":
                        b = -1
                    else:
                        try:
                            b = float(x_parts[0])
                        except:
                            b = 0
                    # Find constant
                    if len(x_parts) > 1 and x_parts[1]:
                        try:
                            c = float(x_parts[1])
                        except:
                            c = 0
                else:
                    # No x term
                    try:
                        c = float(remaining)
                    except:
                        c = 0
            elif "x" in expr and "**2" not in expr:
                # Linear function
                st.warning("⚠️ This is a linear function, not a quadratic!")
                a = 0
                if expr.startswith("x"):
                    b = 1
                    c = 0
                elif expr.startswith("-x"):
                    b = -1
                    c = 0
                else:
                    # Try to parse b and c
                    if "x" in expr:
                        x_parts = expr.split("x")
                        if x_parts[0] in ["", "+"]:
                            b = 1
                        elif x_parts[0] == "-":
                            b = -1
                        else:
                            try:
                                b = float(x_parts[0])
                            except:
                                b = 0
                        if len(x_parts) > 1 and x_parts[1]:
                            try:
                                c = float(x_parts[1])
                            except:
                                c = 0
                    else:
                        c = float(expr)
            else:
                # Constant
                a = 0
                b = 0
                c = float(expr) if expr else 0
            
            # Check if it's a valid quadratic
            is_quadratic = a != 0
            
            # Display the equation
            display_eq = f"y = {equation_input}"
            if "=" not in equation_input:
                display_eq = f"y = {equation_input}"
            st.latex(display_eq)
            
            # Create plot
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Plot
            ax.plot(x_vals, y_vals, color='purple', linewidth=3)
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)
            ax.grid(True, alpha=0.3)
            
            # Set dynamic limits
            y_min = min(y_vals)
            y_max = max(y_vals)
            y_range = y_max - y_min
            if y_range < 0.1:
                y_range = 1
            ax.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)
            
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(f"{display_eq}", fontsize=14)
            
            # Calculate features if quadratic
            if is_quadratic:
                discriminant = b**2 - 4*a*c
                
                # Vertex
                vertex_x = -b / (2*a)
                vertex_y = a * vertex_x**2 + b * vertex_x + c
                ax.plot(vertex_x, vertex_y, 'go', markersize=10)
                ax.annotate(f"Vertex ({vertex_x:.2f}, {vertex_y:.2f})", 
                            (vertex_x, vertex_y), xytext=(10, 10), 
                            textcoords='offset points', fontsize=10, color='green')
                
                # Roots
                if discriminant >= 0:
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
            
            # Display features
            if is_quadratic:
                st.subheader("📊 Key Features")
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
                    st.info(f"**Roots (x-intercepts):** x = {root1:.2f} and x = {root2:.2f}")
                else:
                    st.info("**No real roots** – the parabola does not cross the x-axis")
            else:
                st.warning("⚠️ This is not a quadratic function (a = 0)")
                # Still show linear features if applicable
                if b != 0:
                    st.info(f"**Linear function:** y = {b}x + {c}")
                    st.info(f"**Slope:** {b}")
                    st.info(f"**y-intercept:** {c}")
                else:
                    st.info(f"**Constant function:** y = {c}")
            
            st.divider()
            st.caption("📖 Tip: Enter equations like `2x^2 + 3x - 5`, `x^2 - 4`, or `-x^2 + 2x + 1`")
            
        except Exception as e:
            st.error(f"❌ Error: Could not parse your equation. Please check the format.")
            st.write(f"**Details:** {e}")
            st.info("💡 Try formats like: `x^2 - 3x + 2`, `2x^2 + 5x - 3`, or `-x^2 + 4`")
    
    elif parse_button:
        st.info(" Please enter an equation first.")

with tab2:
    st.markdown("*Move the sliders to explore how a, b, and c change the parabola!*")


    # Initialize session state for score tracking
    if 'q_score' not in st.session_state:
        st.session_state.q_score = 0
    if 'q_attempts' not in st.session_state:
        st.session_state.q_attempts = 0

# Main sliders
    col1, col2, col3 = st.columns(3)
    with col1:
        a = st.slider("a (quadratic)", -3.0, 3.0, 1.0, 0.1)
    with col2:
        b = st.slider("b (linear)", -10.0, 10.0, 0.0, 0.5)
    with col3:
        c = st.slider("c (constant)", -10.0, 10.0, 0.0, 0.5)

# Display the equation
st.latex(f"y = {a}x² + {b}x + {c}")

# Generate data for plotting
x_plot = np.linspace(-10, 10, 500)
y_plot = a * x_plot**2 + b * x_plot + c

# Create plot
fig, ax = plt.subplots(figsize=(8, 5))

# Plot the parabola
ax.plot(x_plot, y_plot, color='purple', linewidth=3, label=f'y = {a}x² + {b}x + {c}')
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(True, alpha=0.3)
ax.set_xlim(-10, 10)
ax.set_ylim(-20, 20)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title(f"y = {a}x² + {b}x + {c}", fontsize=14)

# Calculate key features
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

# Key features summary
st.subheader(" Key Features")
col1, col2, col3 = st.columns(3)

with col1:
    if a != 0:
        vertex_x = -b / (2*a)
        vertex_y = a * vertex_x**2 + b * vertex_x + c
        st.metric(" Vertex", f"({vertex_x:.2f}, {vertex_y:.2f})")
    else:
        st.metric(" Vertex", "Not a quadratic")

with col2:
    st.metric(" Discriminant", f"{discriminant:.2f}")
    if discriminant > 0:
        st.write("2 distinct real roots")
    elif discriminant == 0:
        st.write("1 repeated real root")
    else:
        st.write("No real roots (complex)")

with col3:
    st.metric("🔄 Direction", "Opens Up" if a > 0 else "Opens Down" if a < 0 else "Linear")

# Show roots if they exist
if a != 0 and discriminant >= 0:
    root1 = (-b - math.sqrt(discriminant)) / (2*a)
    root2 = (-b + math.sqrt(discriminant)) / (2*a)
    st.info(f"**Roots (x-intercepts):** x = {root1:.2f} and x = {root2:.2f}")
elif a != 0 and discriminant < 0:
    st.warning("⚠️ No real roots – the parabola does not cross the x-axis")
elif a == 0:
    st.info("This is a linear function (a = 0)")

# Challenge Mode - Quadratic
st.divider()
st.subheader("Challenge Mode - Find the Key Features!")

# Initialize session state for challenge
if 'q_challenge_active' not in st.session_state:
    st.session_state.q_challenge_active = False
if 'q_challenge_answered' not in st.session_state:
    st.session_state.q_challenge_answered = False
if 'q_challenge_attempts' not in st.session_state:
    st.session_state.q_challenge_attempts = 0

if st.button("🔄 Generate New Quadratic Challenge"):
    # Generate random a, b, c
    st.session_state.q_challenge_a = random.randint(-5, 5)
    # Make sure a is not 0
    while st.session_state.q_challenge_a == 0:
        st.session_state.q_challenge_a = random.randint(-5, 5)
    st.session_state.q_challenge_b = random.randint(-10, 10)
    st.session_state.q_challenge_c = random.randint(-10, 10)
    st.session_state.q_challenge_active = True
    st.session_state.q_challenge_answered = False
    st.session_state.q_challenge_attempts = 0

if st.session_state.q_challenge_active and not st.session_state.q_challenge_answered:
    a_q = st.session_state.q_challenge_a
    b_q = st.session_state.q_challenge_b
    c_q = st.session_state.q_challenge_c
    
    st.markdown(f"""
    ### Your Task:
    Given the quadratic function:
    
    **y = {a_q}x² + {b_q}x + {c_q}**
    
    Answer the questions below:
    """)
    
    # Question 1: Vertex
    vertex_x = -b_q / (2*a_q)
    vertex_y = a_q * vertex_x**2 + b_q * vertex_x + c_q
    
    st.markdown("**1. What is the vertex?**")
    col1, col2 = st.columns(2)
    with col1:
        user_vx = st.number_input("x-coordinate:", value=0.0, step=0.5, key="user_vx")
    with col2:
        user_vy = st.number_input("y-coordinate:", value=0.0, step=0.5, key="user_vy")
    
    # Question 2: Roots
    disc = b_q**2 - 4*a_q*c_q
    st.markdown("**2. What are the roots (x-intercepts)?**")
    
    if disc < 0:
        st.info("This parabola has NO real roots (discriminant < 0)")
        user_root1 = 0.0
        user_root2 = 0.0
    else:
        root1 = (-b_q - math.sqrt(disc)) / (2*a_q)
        root2 = (-b_q + math.sqrt(disc)) / (2*a_q)
        col1, col2 = st.columns(2)
        with col1:
            user_root1 = st.number_input("First root:", value=0.0, step=0.5, key="user_root1")
        with col2:
            user_root2 = st.number_input("Second root:", value=0.0, step=0.5, key="user_root2")
    
    # Question 3: Direction
    st.markdown("**3. Does the parabola open up or down?**")
    direction = st.selectbox("Direction:", ["Select...", "Opens Up", "Opens Down"], key="direction")
    
    # Check Answers Button
    if st.button("✅ Check My Answers"):
        st.session_state.q_challenge_attempts += 1
        score = 0
        total = 3  # Total questions
        
        # Check vertex
        if abs(user_vx - vertex_x) < 0.1 and abs(user_vy - vertex_y) < 0.1:
            score += 1
            st.success("✅ Vertex is correct!")
        else:
            st.error(f"❌ Vertex: The correct answer is ({vertex_x:.2f}, {vertex_y:.2f})")
        
        # Check roots
        if disc < 0:
            st.info("ℹ️ No real roots – that was a trick question!")
            score += 1  # Give them the point if they recognized it
        else:
            if abs(user_root1 - root1) < 0.1 and abs(user_root2 - root2) < 0.1:
                score += 1
                st.success("✅ Roots are correct!")
            elif abs(user_root1 - root2) < 0.1 and abs(user_root2 - root1) < 0.1:
                score += 1
                st.success("✅ Roots are correct (order doesn't matter)!")
            else:
                st.error(f"❌ Roots: The correct answers are {root1:.2f} and {root2:.2f}")
        
        # Check direction
        correct_direction = "Opens Up" if a_q > 0 else "Opens Down"
        if direction == correct_direction:
            score += 1
            st.success("✅ Direction is correct!")
        else:
            st.error(f"❌ Direction: The parabola {correct_direction}")
        
        # Show final score
        st.divider()
        st.subheader(f" Your Score: {score}/{total}")
        st.session_state.q_score += score
        st.session_state.q_attempts += 1
        
        # Show accuracy
        if st.session_state.q_attempts > 0:
            accuracy = (st.session_state.q_score / (st.session_state.q_attempts * 3)) * 100
            st.metric("Overall Accuracy", f"{accuracy:.0f}%")
        
        # Feedback based on score
        if score == 3:
            st.success("Perfect! You're a quadratic master!")
            st.balloons()
        elif score >= 2:
            st.info("Good job! Almost perfect – review the errors above.")
        else:
            st.warning("Keep practicing! Use the sliders above to explore more.")
        
        # Add to history
        if 'q_history' not in st.session_state:
            st.session_state.q_history = []
        st.session_state.q_history.append(f"y = {a_q}x² + {b_q}x + {c_q} → Score: {score}/3")
        
        st.session_state.q_challenge_answered = True

# Display history
if st.session_state.q_challenge_active:
    with st.expander("Challenge History"):
        if 'q_history' in st.session_state and len(st.session_state.q_history) > 0:
            for item in st.session_state.q_history[-10:]:  # Show last 10
                st.write(f"- {item}")
        else:
            st.write("No challenges completed yet.")

# Reset button
if st.session_state.q_challenge_answered:
    if st.button("🔄 Try Another Challenge"):
        st.session_state.q_challenge_active = False
        st.session_state.q_challenge_answered = False
        st.session_state.q_challenge_attempts = 0
        st.rerun()

st.markdown("**Created for Mathematics Students** | Explore how a, b, and c shape the parabola!")