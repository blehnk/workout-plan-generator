# 🏋️ Personalized AI Workout Plan Generator

A single-page Streamlit web application that generates structured, personalized weekly workout routines using LLM inference via the Groq API.

Built as part of the **Codebasics AI Engineering Cohort (Session 2 Assignment)**.

---

## 🌟 Key Features

- **Structured Inputs (No Free-Text Chaos):** Collects user fitness goals, experience levels, equipment availability, weekly schedule, workout duration, bodyweight, and injury constraints using native Streamlit UI widgets.
- **CRAFT-Based Prompt Engineering:** The system prompt enforces strict constraints (sets, reps, rest periods, split logic) rather than generating generic advice.
- **Safety & Injury Accommodation:** Dynamically detects physical limitations (e.g., bad knees, shoulder impingement) and inserts safety disclaimers with exercise substitutions.
- **Tailored Nutrition Target:** Calculates personalized daily protein intake targets based on user bodyweight, training volume, and fitness goals.
- **Persistent Session State:** Plans survive widget interactions and adjustments via `st.session_state`.
- **Export to Markdown:** Users can download their plan directly as a `.md` file for offline use.
- **Defensive Backend Architecture:** The generation engine in `generator.py` features type hints, input validation guard clauses, and graceful exception handling.

---

## 🧠 Prompt Design Philosophy (CRAFT Framework)

Rather than concatenating inputs into a simple prompt, the app utilizes a two-tier chat completion structure:

1. **System Prompt (Role & Constraints):**
   - **Role:** Certified personal trainer and strength coach.
   - **Action:** Formulates split logic (Full Body, PPL, Upper/Lower) according to experience level and frequency.
   - **Format:** Strict day-by-day table/bulleted structure (Exercise, Sets, Reps, Rest).
   - **Target:** Delivers achievable plans adhering strictly to available gear (Bodyweight, Dumbbells, Full Gym).

2. **User Prompt (Profile Injection):**
   - Dynamic f-string injecting verified metrics and constraints into the model context.

---

## 🛠️ Project Structure

```text
workout-plan-generator/
├── generator.py         # Modular LLM logic, prompt engineering & Groq API call
├── app.py               # Streamlit frontend with session state management
├── pyproject.toml       # Modern Python project configuration (uv)
├── requirements.txt     # Pinned dependencies for standard pip installs
├── .env.example         # Environment template for API keys
├── .gitignore           # Protects secrets, cache, and virtual environments
└── README.md            # Project documentation
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone git@github.com:blehnk/workout-plan-generator.git
cd workout-plan-generator
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and add your Groq API key (get a free key at [console.groq.com](https://console.groq.com)):
```env
GROQ_API_KEY=your_actual_key_here
GROQ_MODEL_NAME=openai/gpt-oss-120b
```

### 3. Install Dependencies & Run

#### Using `uv` (Recommended):
```bash
uv sync
uv run streamlit run app.py
```

#### Using standard `pip`:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser to start generating plans!
