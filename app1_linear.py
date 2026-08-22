import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Linear Functions", page_icon="📐")
st.title("📐 Linear Functions Explorer")
st.markdown("*Created by ApexTech*")
st.markdown("Move the sliders to explore how changing **m** and **c** affects the line!")

# Main sliders
col1, col2 = st.columns(2)
with col1:
    m = st.slider("Slope (m)", -5.0, 5.0, 2.0, 0.1)
with col2:
    c = st.slider("y-intercept (c)", -10.0, 10.0, 3.0, 0.1)

st.latex(f"y = {m}x + {c}")

# Generate data
x = np.linspace(-10, 10, 200)
y = m * x + c

# Point selector
x_display = st.slider("🔍 Show point at x =", -10, 10, 0, 1)
y_display = m * x_display + c
st.markdown(f"**📍 At x = {x_display}, y = {y_display:.2f}**")

# Create plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, color='purple', linewidth=3, label=f'y = {m}x + {c}')
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(True, alpha=0.3)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title(f"y = {m}x + {c}", fontsize=14)

# Selected point
ax.plot(x_display, y_display, 'ro', markersize=10)
ax.annotate(f"({x_display}, {y_display:.2f})", (x_display, y_display), 
            xytext=(10, 10), textcoords='offset points', fontsize=12, color='red')

# y-intercept
ax.plot(0, c, 'go', markersize=8)
ax.annotate(f"y-intercept (0, {c:.1f})", (0, c), xytext=(10, -15), 
            textcoords='offset points', fontsize=10, color='green')

# Slope triangle (if m != 0)
if abs(m) > 0.1:
    x_tri = 2
    y_tri = m * x_tri + c
    ax.plot([x_tri, x_tri + 1], [y_tri, y_tri], 'k--', linewidth=1, alpha=0.5)
    ax.plot([x_tri + 1, x_tri + 1], [y_tri, y_tri + m], 'k--', linewidth=1, alpha=0.5)
    ax.annotate(f"Δy = {m:.1f}", (x_tri + 1.5, y_tri + m/2), fontsize=10, color='blue')
    ax.annotate(f"Δx = 1", (x_tri + 0.5, y_tri - 1.5), fontsize=10, color='blue')

st.pyplot(fig)

# Table of values
with st.expander("📊 Table of Values (x from -5 to 5)"):
    x_vals = np.arange(-5, 6, 1)
    y_vals = m * x_vals + c
    table_data = {"x": x_vals, "y": [f"{y:.2f}" for y in y_vals]}
    st.table(table_data)
    
    if m > 0.1:
        st.info(f"📈 The line is **increasing** (slope = {m} > 0)")
    elif m < -0.1:
        st.info(f"📉 The line is **decreasing** (slope = {m} < 0)")
    else:
        st.info(f"➡️ The line is **horizontal** (slope = {m} ≈ 0)")

# Challenge Mode - Equation Entry
st.divider()
st.subheader("🎯 Challenge Mode - Write the Equation!")

if st.button("🔄 Generate New Question"):
    st.session_state['q_m'] = random.randint(-5, 5)
    st.session_state['q_c'] = random.randint(-10, 10)
    st.session_state['question_active'] = True
    st.session_state['attempts'] = 0
    st.session_state['answered'] = False

if 'question_active' in st.session_state and st.session_state['question_active']:
    st.markdown(f"""
    ### 📝 Your Task:
    Write the equation of the line with:
    - **Slope (m) = {st.session_state['q_m']}**
    - **y-intercept (c) = {st.session_state['q_c']}**
    """)
    
    # Student types the equation
    user_equation = st.text_input(
        "Enter your equation in the form **y = mx + c**:",
        placeholder="e.g. y = 2x + 3",
        key="user_equation",
        disabled=st.session_state.get('answered', False)
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("✅ Check Answer", disabled=st.session_state.get('answered', False)):
            # Clean up user input - remove spaces and make lowercase
            cleaned = user_equation.strip().lower().replace(" ", "")
            
            # Build the correct answer in different formats
            correct_form1 = f"y={st.session_state['q_m']}x+{st.session_state['q_c']}"
            correct_form2 = f"y={st.session_state['q_m']}x+{st.session_state['q_c']}.0"
            correct_form3 = f"y={st.session_state['q_m']}x-{abs(st.session_state['q_c'])}" if st.session_state['q_c'] < 0 else None
            
            # Also handle if they type y = mx + c format with spaces
            possible_answers = [correct_form1, correct_form2]
            if correct_form3:
                possible_answers.append(correct_form3)
            
            # Check if answer matches any format
            if cleaned in possible_answers:
                st.success(f"✅ Perfect! y = {st.session_state['q_m']}x + {st.session_state['q_c']} 🎉")
                st.balloons()
                st.session_state['answered'] = True
            else:
                st.session_state['attempts'] = st.session_state.get('attempts', 0) + 1
                remaining = 3 - st.session_state['attempts']
                
                if st.session_state['attempts'] >= 3:
                    st.error(f"❌ The correct answer is **y = {st.session_state['q_m']}x + {st.session_state['q_c']}**")
                    st.info("💡 Remember: **y = mx + c** where m is slope and c is y-intercept!")
                    st.session_state['answered'] = True
                else:
                    st.warning(f"❌ Not quite. Try again! ({remaining} attempts remaining)")
                    
                    # Give a hint
                    if st.session_state['q_c'] < 0:
                        st.info(f"💡 Hint: Since c = {st.session_state['q_c']}, your equation should end with **- {abs(st.session_state['q_c'])}**")
                    else:
                        st.info(f"💡 Hint: Since c = {st.session_state['q_c']}, your equation should end with **+ {st.session_state['q_c']}**")
    
    with col2:
        if st.button("🔄 New Question", disabled=st.session_state.get('answered', False)):
            # Generate new question
            st.session_state['q_m'] = random.randint(-5, 5)
            st.session_state['q_c'] = random.randint(-10, 10)
            st.session_state['attempts'] = 0
            st.session_state['answered'] = False
            st.rerun()
    
    # Show the correct format example
    with st.expander("📖 How to type your answer"):
        st.markdown("""
        Type the equation exactly like this:
        - **y = 2x + 3** (for m=2, c=3)
        - **y = -3x + 5** (for m=-3, c=5)
        - **y = 4x - 2** (for m=4, c=-2)
        
        *Don't worry about spaces – we'll accept them!*
        """)

# Teacher Notes
with st.expander("💡 Teacher's Notes"):
    st.markdown(f"""
    ### Key Concepts for Students:
    
    - **Slope (m) = {m}**: 
        - {'↗️ Positive' if m > 0.1 else '↘️ Negative' if m < -0.1 else '➡️ Zero'}
        - Rise over run: for every 1 step right, line goes {'up' if m > 0.1 else 'down' if m < -0.1 else 'nowhere'} by {abs(m):.1f} steps
    
    - **y-intercept (c) = {c}**: The line crosses the y-axis at (0, {c})
    
    ### Try These Explorations:
    1. Set **m = 1, c = 0** → What do you notice? (It's y = x, a 45° angle)
    2. Set **m = -1, c = 0** → What's different? (It slopes downward)
    3. Set **m = 0, c = 5** → What shape is this? (A horizontal line)
    4. Set **m = 2, c = -3** → Where does it cross the x-axis? (Hint: set y = 0 and solve)
    
    ### Real-World Connection:
    - This is how we model **constant speed** (distance vs time)
    - **Phone bills** (fixed monthly cost + per-minute charge)
    - **Exchange rates** (converting currency)
    """)

st.divider()
st.markdown("👩‍🏫 **Created for Mathematics Students** | Move the sliders and explore!")