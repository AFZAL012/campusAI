# 🎓 CampusAI — Your Smart Campus & Scholarship Assistant

CampusAI is an AI-powered web application designed to simplify access to academic and administrative information for college students. It provides instant answers to campus-related queries and personalized scholarship recommendations through a conversational interface.

Built for **SnowFrost Hackathon 2026** under the **Open Innovation & Artificial Intelligence** domain.

## 🚀 Key Features

### 💬 AI Campus Assistant
- Ask questions about **exams, notices, library timings, and announcements**
- Natural language understanding using **NLP (TF-IDF)**
- Real-time conversational responses
- Voice-enabled query support 🎤

### 🎯 Scholarship Recommendation Engine
- Personalized scholarship suggestions
- Input-based filtering:
  - Course
  - Year
  - Category
  - Family Income
- **Explainable AI**: Shows *why* a student qualifies for a scholarship

### 📊 Admin Analytics Dashboard
- Visual analytics of user queries
- Bar chart insights (Exams, Scholarships, Library, Notices)
- Helps administrators understand student needs

### 🌐 Single Page Modern UI
- Home, About, App & Admin sections in one interface
- Responsive, dark-themed professional UI
- Smooth animations and clean layout

## 🧠 Technology Stack

### Frontend
- HTML5
- CSS3 (Custom dark UI)
- JavaScript (Vanilla JS)
- Chart.js (Analytics Visualization)

### Backend
- Python
- Flask
- REST APIs

### AI / ML
- NLP using **TF-IDF Vectorization**
- Cosine Similarity for intent matching
- Rule + ML-based recommendation logic


## 📂 Project Structure

CampusAI/
│
├── app.py
├── requirements.txt
├── readme.md
│
├── data/
│ ├── campus_data.json
│ └── scholarships.json
│
├── nlp/
│ ├── init.py
│ └── processor.py
│
├── templates/
│ └── index.html
│
└── static/
├── css/
│ └── style.css
└── js/
└── script.js

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/AFZAL012/CampusAI.git
cd CampusAI

##install Dependencies
pip install -r requirements.txt

##Run the application
python app.py

##Open in Browser
http://127.0.0.1:5000


🧪 Example Use Cases

“When are MCA exams?”
“Library timing today”
“Scholarships for MCA students with income below ₹50,000”
“Any notices today?”

🏆 Hackathon Relevance

Solves a real student problem
Demonstrates AI + Explainability
Scalable for any university
Lightweight & feasible within hackathon time
Strong demo flow for judges

🔮 Future Enhancements

User authentication (Student/Admin)
Multi-language support
WhatsApp / Mobile app integration
Advanced ML models (BERT / LLMs)
Real-time university data sync

👥 Team

Team Name: NeuroHackers
Project: CampusAI
Domain: Open Innovation & Artificial Intelligence

📜 License
This project is developed for educational and hackathon purposes.

🔥 CampusAI — simplifying campus life with AI
