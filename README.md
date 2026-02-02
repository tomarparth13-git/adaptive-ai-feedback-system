# Adaptive AI Psychological Feedback System 🧠💙

A supportive, AI-powered web application that adapts to your emotional state.  
*Note: This is a hackathon project acting as a conceptual prototype, NOT a medical tool.*

## 📖 Overview
Mental health support should be accessible and empathetic. This system uses Natural Language Processing (NLP) to analyze user input (journal entries, thoughts) and provides adaptive feedback. It detects emotions like anxiety, stress, or happiness and adjusts its tone to be calming, grounding, or encouraging.

## 🚀 Features
- **Emotion Detection**: Classifies text into states like *Anxious*, *Stressed*, *Sad*, *Positive*, or *Neutral*.
- **Adaptive AI Responses**:
  - *Anxious* → Grounding techniques & calm assurances.
  - *Stressed* → Validation & coping suggestions.
  - *Positive* → Enforcement & celebration.
- **Short-Term Memory**: Remembers context from the last 3 interactions to avoid robotic repetition.
- **Visual Feedback**: The interface changes color psychology based on the detected mood (e.g., Green for positive, Purple for anxious, Blue for sad).
- **Safety First**: Recognizes distress keywords and serves a safety disclaimer.

## 🛠 Tech Stack
- **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JavaScript.
- **Backend**: Python, Flask (REST API).
- **AI Logic**: TextBlob (Sentiment Analysis) + Rule-based Context Engine.

## 📦 How to Run

### Prerequisites
- Python 3.8+ installed.

### 1. Setup Backend
Open a terminal in the project root:
```bash
cd backend
pip install -r requirements.txt
python app.py
```
You should see: `Running on http://127.0.0.1:5000`

### 2. Run Frontend
Simply open the `frontend/index.html` file in your favorite web browser.
*(You can double-click the file or drag it into Chrome/Edge).*

## 🔮 Future Scope
- **LLM Integration**: Replace the logic engine with OpenAI GPT-4 or Llama for deeper conversations.
- **Voice Input**: Allow users to speak their thoughts.
- **Long-term Memory**: Store user journaling history in a database (SQLite/PostgreSQL).
- **Visualization**: Show mood trends over the week.

## ⚠️ Disclaimer
This application is for educational and demonstrative purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.
