from flask import Flask, render_template, request, jsonify
import main  # your existing chatbot logic from main.py

app = Flask(__name__)

def greet_user():
    return "Hello! How are you today?"

def show_time():
    now = datetime.now()
    return f"The current time is {now.strftime('%H:%M:%S')}"

def tell_joke():
    jokes = [
        "Why did the computer go to the doctor? Because it caught a virus!",
        "Why do programmers prefer dark mode? Because light attracts bugs!"
    ]
    return random.choice(jokes)

@app.route("/")
def index():
    return render_template("UI.html")  # or 'index.html' if you renamed

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    # Replace this with actual AI response from main.py
    ai_reply = main.get_ai_response(user_msg)  # you can define this in main.py
    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
