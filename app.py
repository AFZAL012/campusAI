from flask import Flask, render_template, request, jsonify, session, redirect
import json
from pymongo import MongoClient
import bcrypt
from nlp.processor import get_response, recommend_scholarships

app = Flask(__name__)
app.secret_key = "campusai_secret_key"

ANALYTICS_FILE = "data/analytics.json"

# ---------------- MONGODB CONNECTION ----------------
client = MongoClient("mongodb://localhost:27017")
db = client["campusai"]
users_col = db["users"]

# ---------------- HOME ----------------
@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html", role=session.get("role"))

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    # Check if user exists
    if users_col.find_one({"email": email}):
        return jsonify({"status": "error", "message": "User already exists"}), 409

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user_doc = {
        "email": email,
        "password": hashed_pw,
        "role": "student"   # default role
    }

    users_col.insert_one(user_doc)
    return jsonify({"status": "success"})


# ---------------- LOGIN (ROLE PROTECTED) ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.json

    email = data.get("username")
    password = data.get("password")
    role = data.get("role")   # 👈 frontend se aane wala role

    if not email or not password or not role:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    user = users_col.find_one({"email": email})

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 401

    # password verify
    if not bcrypt.checkpw(password.encode(), user["password"]):
        return jsonify({"status": "error", "message": "Invalid password"}), 401

    # 🔥 ROLE SECURITY CHECK
    if user.get("role") != role:
        return jsonify({
            "status": "error",
            "message": "Unauthorized role access"
        }), 403

    # success login
    session["user"] = user["email"]
    session["role"] = user["role"]

    return jsonify({
        "status": "success",
        "role": user["role"]
    })


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- CHAT ----------------
@app.route("/ask", methods=["POST"])
def ask():
    msg = request.json.get("message")
    response = get_response(msg)

    # analytics
    try:
        with open(ANALYTICS_FILE, "r+") as f:
            data = json.load(f)
            data["total_queries"] += 1
            intent = response.get("intent", "general")
            if intent in data:
                data[intent] += 1
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    except:
        pass

    return jsonify(response)


# ---------------- SCHOLARSHIP ----------------
@app.route("/recommend_scholarship", methods=["POST"])
def recommend():
    profile = request.json
    results = recommend_scholarships(profile)

    # analytics update
    try:
        with open(ANALYTICS_FILE, "r+") as f:
            data = json.load(f)
            data["total_queries"] += 1
            data["scholarship"] += 1
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    except:
        pass

    return jsonify({"data": results})


# ---------------- ANALYTICS (ADMIN ONLY) ----------------
@app.route("/analytics")
def analytics():
    if session.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    with open(ANALYTICS_FILE) as f:
        return jsonify(json.load(f))


if __name__ == "__main__":
    app.run(debug=True)
