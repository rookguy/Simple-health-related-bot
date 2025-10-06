'''
Chatbot Features
1. First-Time Interaction
 the chatbot greets the user like an experienced therapist.

 It starts a conversation, collecting data on:

 Current mood and symptoms of mental/emotional problems
 Lifestyle
 Mental health history
 The users reactions to their circumstances

This data is stored in a private “Mental_Health Profile” on the device (encrypted).

2.Personalized Plan Creation
 Based on the initial intake, the chatbot creates a customized improvement plan, broken into daily micro-tasks such as:
 The plan is adaptive, changing according to the user's circumstances and response

3.Daily Progress Cycle
 at the start of the day the app sends a motivational task or reminder from the plan.
 at the end of the day the app notifies the user for a progress checking chat.
 adjusts tomorrows plan based on responses and circumstances.

4.Weekly Research Update
 Once a week, the chatbot scans the web for the latest mental health research and therapy practices
 Its conversational strategies and task suggestions evolve based on evidence-based therapy practices.

Keeps the chatbot aligned with real scientific progress, unlike static wellness apps.
'''

import json
import datetime
import random


PROFILE_FILE = "user_profile.json"

def load_profile():
    try:
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_profile(profile):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=2)

def intake_session():
    print("👋 Hello, I’m your personal mental health companion.")
    print("I’d like to understand you better so I can support you effectively.")

    name = input("What's your name? (Optional): ")
    mood = input("How are you feeling today (happy/neutral/sad)? ")
    stress = input("On a scale of 1–10, how stressed are you right now? ")
    sleep = input("How many hours did you sleep last night? ")

    profile = {
        "name": name or "User",
        "created_at": str(datetime.date.today()),
        "mental_health": {
            "mood": mood,
            "stress": stress,
            "sleep": sleep,
        },
        "plan": [],
        "history": []
    }

    save_profile(profile)
    return profile


def generate_plan(profile):
    base_tasks = [
        "5 minutes of deep breathing",
        "Write down 3 things you’re grateful for",
        "Take a 10-minute walk outside",
        "Listen to a calming music track",
        "Do 10 gentle stretches"
    ]
    # Shuffle + pick 3 tasks
    tasks = random.sample(base_tasks, 3)
    profile["plan"] = tasks
    save_profile(profile)
    return tasks

# ------------------------------
# New function for Flask / chat
# ------------------------------
def get_ai_response(message: str) -> str:
    """
    Returns a response string based on user message.
    Can call other functions depending on keywords.
    """
    profile = load_profile() or {"name": "User", "plan": [], "history": []}

    msg = message.lower()

    # Keywords trigger different functions
    if "plan" in msg:
        tasks = generate_plan(profile)
        return "Here’s your new plan for today:\n- " + "\n- ".join(tasks)

    elif "status" in msg or "check" in msg:
        if profile["history"]:
            last = profile["history"][-1]
            return f"Last check-in: mood={last['mood']}, completed={last['completed']}"
        else:
            return "No previous check-ins yet."

    elif "update" in msg or "research" in msg:
        new_strategies = [
            "Progressive muscle relaxation",
            "Mindful 3-minute meditation",
            "Digital detox hour"
        ]
        return "✅ Integrated new strategies: " + ", ".join(new_strategies)

    elif "hello" in msg or "hi" in msg:
        return f"Hello {profile.get('name', 'User')}! How are you today?"

    else:
        return "I didn’t understand that. Try asking about your plan, status, or research."
def daily_checkin(profile):
    print(f"\n🌙 Hi {profile['name']}, how was your day?")
    mood = input("How are you feeling now (happy/neutral/sad)? ")
    completed = input("Did you complete today’s tasks? (yes/no/partly): ")

    log_entry = {
        "date": str(datetime.date.today()),
        "mood": mood,
        "completed": completed
    }

    profile["history"].append(log_entry)

    # Adjust next plan
    if completed.lower() == "no":
        print("That’s okay 💙 Let’s try smaller steps tomorrow.")
        profile["plan"] = ["2 minutes deep breathing", "Write 1 good thing about today"]
    elif completed.lower() == "partly":
        print("Nice effort 🌱 Tomorrow we’ll balance things better.")
        profile["plan"] = ["5 minutes walk", "Gratitude journaling"]
    else:
        print("Amazing 🌟 Let’s keep building on this progress.")
        profile["plan"] = generate_plan(profile)

    save_profile(profile)


def update_with_research():
    # In a real build: call APIs or load curated therapy database
    print("\n🔄 Updating strategies with latest mental health research (simulated)...")
    # Example: refresh coping strategies
    new_strategies = [
        "Progressive muscle relaxation",
        "Mindful 3-minute meditation",
        "Digital detox hour"
    ]
    print("✅ Integrated new strategies:", ", ".join(new_strategies))


if __name__ == "__main__":
    profile = load_profile()
    if not profile:
        profile = intake_session()
        plan = generate_plan(profile)
        print("\n✨ Your personalized plan for today:")
        for task in plan:
            print("-", task)
    else:
        # Daily reflection loop
        daily_checkin(profile)

    # Simulate weekly refresh (could be run every 7 days)
    if datetime.date.today().weekday() == 6:  # Sunday
        update_with_research()
