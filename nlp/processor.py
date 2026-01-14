import json
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- SAFE FILE LOADER ----------------
def load_json(path, default):
    try:
        if not os.path.exists(path):
            return default
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

# ---------------- LOAD CAMPUS DATA ----------------
campus_data = load_json("data/campus_data.json", [])

questions = [item.get("question", "") for item in campus_data if "question" in item]
answers = [item.get("answer", "") for item in campus_data if "answer" in item]

# Prevent crash if dataset empty
if questions:
    vectorizer = TfidfVectorizer(stop_words="english")
    q_vectors = vectorizer.fit_transform(questions)
else:
    vectorizer = None
    q_vectors = None

# ---------------- INTENT DEFINITIONS ----------------
INTENTS = {
    "exam": ["exam", "exams", "test", "tests", "paper", "papers", "date", "form", "forms"],
    "scholarship": ["scholarship", "scholarships", "fee", "fees", "grant", "financial"],
    "library": ["library", "libraries", "book", "books"],
    "notice": ["notice", "notices", "announcement", "announcements"]
}


def detect_intent(query):
    query = query.lower()
    words = re.findall(r"\b\w+\b", query)

    for intent, keywords in INTENTS.items():
        if any(word in words for word in keywords):
            return intent
    return "general"

# ---------------- CHAT RESPONSE ----------------
def get_response(query):
    if not query or not query.strip():
        return {
            "answer": "Please type a valid question.",
            "intent": "unknown",
            "confidence": "Low"
        }

    query = query.lower().strip()
    intent = detect_intent(query)

    canned = {
        "exam": "Exam form deadline is 15th March.",
        "library": "Library timings are 9 AM to 8 PM.",
        "notice": "All notices are available on the university website.",
        "scholarship": "Use the scholarship section below to get personalized recommendations."
    }

    if intent in canned:
        return {
            "answer": canned[intent],
            "intent": intent,
            "confidence": "High"
        }

    # ---- Similarity Search ----
    if vectorizer and q_vectors is not None:
        try:
            user_vec = vectorizer.transform([query])
            similarity = cosine_similarity(user_vec, q_vectors)
            idx = similarity.argmax()

            if similarity[0][idx] > 0.3:
                return {
                    "answer": answers[idx],
                    "intent": "general",
                    "confidence": "Medium"
                }
        except Exception as e:
            print("Similarity Error:", e)

    return {
        "answer": "Sorry, I couldn’t find that information.",
        "intent": "unknown",
        "confidence": "Low"
    }

# ---------------- SCHOLARSHIP ENGINE ----------------
def recommend_scholarships(profile):
    with open("data/scholarships.json", "r") as f:
        scholarships = json.load(f)

    results = []

    course = profile.get("course", "").lower()
    year = int(profile.get("year", 0))
    category = profile.get("category", "").lower()
    income = int(profile.get("income", 0))

    for s in scholarships:
        reasons = []
        eligible = True

        # Course check
        if s["course"] != "any" and s["course"].lower() != course:
            eligible = False
            reasons.append(f"✘ Course not eligible ({course.upper()})")
        else:
            reasons.append(f"✔ Course matched ({course.upper()})")

        # Year check
        if year < s["min_year"]:
            eligible = False
            reasons.append(f"✘ Minimum year required: {s['min_year']}")
        else:
            reasons.append(f"✔ Year eligible ({year})")

        # Category check
        if s["category"] != "any" and s["category"].lower() != category:
            eligible = False
            reasons.append(f"✘ Category mismatch ({category})")
        else:
            reasons.append(f"✔ Category accepted")

        # Income check
        if income > s["max_income"]:
            eligible = False
            reasons.append(f"✘ Income above ₹{s['max_income']}")
        else:
            reasons.append(f"✔ Income below ₹{s['max_income']}")

        probability = 90 if eligible else 20

        results.append({
            "name": s["name"],
            "benefit": s["benefit"],
            "eligible": eligible,
            "probability": f"{probability}%",
            "reasons": reasons
        })

    return results
