import streamlit as st
from generator import generate_workout_plan

# Page configuration
st.set_page_config(page_title="AI Workout Planner", page_icon="🏋️", layout="centered")

st.title("🏋️ Personalized AI Workout Plan Generator")
st.write("Fill in your details below and get a custom weekly routine designed by an AI coach.")

# 1. Initialize session state memory (Stretch Goal 1)
if "workout_plan" not in st.session_state:
    st.session_state["workout_plan"] = None

# 2. Structured Inputs
col1, col2 = st.columns(2)

with col1:
    fitness_goal = st.selectbox(
        "Fitness Goal",
        ["Build muscle", "Lose fat", "General fitness", "Improve endurance"]
    )
    experience_level = st.selectbox(
        "Experience Level",
        ["Beginner", "Intermediate", "Advanced"]
    )
    equipment_access = st.selectbox(
        "Equipment Access",
        ["No equipment (Bodyweight)", "Home dumbbells", "Full gym"]
    )

with col2:
    days_per_week = st.slider("Days available per week", min_value=1, max_value=7, value=3)
    time_per_day = st.slider("Time per session (minutes)", min_value=15, max_value=120, value=45, step=5)
    current_weight = st.number_input("Current Weight (kg)", min_value=15, max_value=300, value=70)

injuries_or_limitations = st.text_input(
    "Injuries or Physical Limitations (optional)",
    placeholder="e.g. bad knees, lower back pain, no overhead pressing"
)

# 3. Action Button
if st.button("Generate Workout Plan", type="primary", use_container_width=True):
    with st.spinner("Consulting your AI Personal Trainer..."):
        plan = generate_workout_plan(
            fitness_goal=fitness_goal,
            experience_level=experience_level,
            days_per_week=days_per_week,
            equipment_access=equipment_access,
            current_weight=int(current_weight),
            time_per_day=time_per_day,
            injuries_or_limitations=injuries_or_limitations
        )
        # Store in session state so it survives widget interactions!
        st.session_state["workout_plan"] = plan
        
# 4. Display Result & Stretch Goals (Download & Reset)
if st.session_state["workout_plan"]:
    st.markdown("---")

    # Action buttons above the plan
    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        st.download_button(
            label="📥 Download Plan (.md)",
            data=st.session_state["workout_plan"],
            file_name="my_workout_plan.md",
            mime="text/markdown",
            use_container_width=True
        )

    with btn_col2:
        if st.button("🗑️ Clear Plan", use_container_width=True):
            st.session_state["workout_plan"] = None
            st.rerun()

    # Render the formatted markdown plan
    st.markdown(st.session_state["workout_plan"])