import os
from typing import Optional
from dotenv import load_dotenv
from groq import Groq

#load variables from .env file into python environment
load_dotenv()

def generate_workout_plan(
    fitness_goal: str,
    experience_level: str,
    days_per_week: int,
    equipment_access: str,
    current_weight: int,
    time_per_day: int,
    injuries_or_limitations: Optional[str] = None,
) -> str:
    """
    Generates a personalized weekly workout plan using Groq's LLM.
    Returns the plan as a string (or an error message if something fails).
    """
    # 1. Validate inputs (Guard clauses)
    if days_per_week < 1 or days_per_week > 7:
        return "⚠️ Error: Please select between 1 and 7 workout days per week."
        
    if time_per_day < 10:
        return "⚠️ Error: Workout time per day must be at least 10 minutes."

    if current_weight < 15:
        return "⚠️ Error: Current weight is too low for these exercises."

    # 2. Check for Groq API Key and model
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "⚠️ Error: GROQ_API_KEY is not set. Please check your .env file."

    model_name= os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-120b")

    # 3. Define the System Prompt (Role, Constraints & Formatting Rules)
    system_prompt = """You are an elite, certified personal trainer and strength coach.
    Your job is to design highly personalized, realistic weekly workout plans tailored to each client's unique profile.

    Follow these strict principles when designing the plan:
    1. Primary Driver (Goal): The fitness goal is your north star. Tailor the rep ranges, intensity, and volume to this goal.
    2. Experience Level: Calibrate exercise complexity and training split (e.g., Full Body, Upper/Lower, Push/Pull/Legs) to their experience.
    3. Schedule Constraints: You must provide EXACTLY the number of workout days requested. Fit the session within the requested time per day.
    4. Equipment Access: ONLY prescribe exercises that can be performed with the specified equipment. If "No equipment", prescribe bodyweight only.
    5. Injuries & Safety: Strictly avoid movements that aggravate specified injuries. If an injury is present, include a safety note and medical disclaimer recommending consultation with a doctor or physical therapist.
    6. Daily Protein Recommendation: Based on their goal, weight, and training volume, provide an estimated daily protein intake range (in grams).

    Output Format:
    - Program Overview (Goal, Split, Daily Protein Target)
    - Day-by-Day Breakdown (e.g., Day 1: [Focus], Day 2: [Focus]...):
    - List each exercise with Sets, Reps, and Rest periods.
    - Safety & Injury Disclaimer (if injuries are noted)."""

    # 4. Define the User Prompt (Injecting the client's metrics)
    injury_text = injuries_or_limitations.strip() if injuries_or_limitations else "None"
    
    user_prompt = f"""Please create my custom workout plan based on my profile:
    - Fitness Goal: {fitness_goal}
    - Experience Level: {experience_level}
    - Current Weight: {current_weight} kg
    - Days Available per Week: {days_per_week} days
    - Time Available per Session: {time_per_day} minutes
    - Equipment Access: {equipment_access}
    - Injuries / Physical Limitations: {injury_text}"""

    # 5. Call the Groq API inside a try/except block   
    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )

        # 6. Extract and validate response
        plan = response.choices[0].message.content
        
        if not plan:
            return "⚠️ Error: AI did not generate a workout plan. Please try again."

        return plan

    except Exception as e:
        # Gracefully handle API errors, rate limits, or network failures
        return f"⚠️ An error occurred while generating your plan: {str(e)}"

if __name__ == "__main__":
    print("Testing workout generator...")
    sample_plan = generate_workout_plan(
        fitness_goal="Build muscle",
        experience_level="Beginner",
        days_per_week=3,
        equipment_access="Home dumbbells",
        current_weight=70,
        time_per_day=45,
        injuries_or_limitations="bad knees"
    )
    print("\n--- GENERATED PLAN ---\n")
    print(sample_plan)

   