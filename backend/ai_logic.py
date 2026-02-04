import os
import random
import logging
import google.generativeai as genai
from textblob import TextBlob
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

class AIEngine:
    def __init__(self):
        self.memory = []
        self.max_memory = 5 # Context for Gemini
        
        # Initialize Gemini API
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("DEBUG: Gemini API Initialized.")
        else:
            self.model = None
            print("DEBUG: Gemini API Key not found!")

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        return {
            "polarity": blob.sentiment.polarity,
            "subjectivity": blob.sentiment.subjectivity
        }

    def detect_emotion_expert(self, text, polarity):
        """
        Expert Logic to detect emotion based on keywords and sentiment.
        Determines the UI color.
        """
        text_lower = text.lower()
        
        # 1. Critical Safety Check
        danger_keywords = ["kill myself", "suicide", "hurt myself", "end it all", "die", "death"]
        if any(w in text_lower for w in danger_keywords):
            return "danger"

        # 2. Anger
        anger_keywords = ["hate", "angry", "furious", "mad", "rage", "annoyed", "stupid", "idiot", "pissed", "frustrated"]
        if any(w in text_lower for w in anger_keywords):
            return "anger"

        # 3. Anxiety
        anxiety_keywords = ["anxious", "scared", "worried", "nervous", "panic", "fear", "terrified", "doom", "stress"]
        if any(w in text_lower for w in anxiety_keywords):
            return "anxious"

        # 4. Stress
        stress_keywords = ["stressed", "busy", "overwhelmed", "tired", "exhausted", "pressure", "deadline"]
        if any(w in text_lower for w in stress_keywords):
            return "stressed"

        # 5. Sadness
        sad_keywords = ["sad", "cry", "lonely", "depressed", "blue", "down", "hopeless", "grief"]
        if any(w in text_lower for w in sad_keywords):
            return "sad"

        # 6. Happiness
        happy_keywords = ["happy", "good", "great", "joy", "excited", "love", "wonderful", "amazing"]
        if any(w in text_lower for w in happy_keywords):
            return "positive"

        # 7. Inspiration
        inspired_keywords = ["inspired", "creative", "wonder", "awe", "motivated", "vision", "goal", "dream"]
        if any(w in text_lower for w in inspired_keywords):
            return "inspired"

        # Fallback based on polarity
        if polarity > 0.2: return "positive"
        if polarity < -0.2: return "sad"
        
        return "neutral"

    def generate_gemini_response(self, text, emotion):
        """
        Calls Gemini to create a deep, empathetic response.
        Enforces bolding and persona.
        """
        if not self.model:
            return None

        try:
            # Build memory context
            history = ""
            for mem in self.memory:
                history += f"User: {mem['user_input']}\nAI: {mem['response_text']}\n"

            prompt = (
                f"You are 'Adaptive', a deeply empathetic and supportive AI friend. "
                f"The user is currently feeling: {emotion}. "
                f"Your goal is to provide profound psychological support and grounding. "
                f"RULES:\n"
                f"1. Be warm, human, and conversational.\n"
                f"2. Use **bold text** for key advice or supportive actions.\n"
                f"3. Keep it to 2-3 impactful sentences.\n"
                f"4. If {emotion} is 'danger', be extremely gentle and DO NOT use bold text. Direct them to help.\n"
                f"5. Reference the context if it helps.\n\n"
                f"Context:\n{history}\n"
                f"User's latest thought: {text}\n"
                f"Adaptive:"
            )

            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            print(f"DEBUG: Gemini Error: {e}")
            return None

    def get_fallback_expert_response(self, text, emotion):
        """Expert system fallback if API fails"""
        if emotion == "danger":
            return "I hear that you are in deep pain. Please know you are not alone. Reach out to a trusted friend or a crisis helpline immediately."

        # Simplified bold logic for fallback
        responses = {
            "anger": "I hear your frustration. **Take a deep breath** right now. You are valid, and I am here.",
            "anxious": "You are safe. Try to **focus on your breathing** for a moment. This will pass.",
            "sad": "I am so sorry you feel this way. **Be gentle with yourself** today. You are not alone.",
            "positive": "That's amazing! **Hold onto this joy** as long as you can!",
            "inspired": "This is a powerful moment! **Keep this momentum** and see where it takes you.",
            "neutral": "I am listening. **Tell me more** about how you are feeling."
        }
        return responses.get(emotion, "I am here for you. **Tell me more**.")

    def process_input(self, text):
        sentiment = self.analyze_sentiment(text)
        emotion = self.detect_emotion_expert(text, sentiment['polarity'])
        
        # Try Gemini First
        response_text = self.generate_gemini_response(text, emotion)
        
        # Fallback if Gemini fails
        if not response_text:
            response_text = self.get_fallback_expert_response(text, emotion)
        
        # Update Memory
        self.memory.append({
            "user_input": text,
            "response_text": response_text,
            "emotion": emotion
        })
        if len(self.memory) > self.max_memory:
            self.memory.pop(0)

        return {
            "emotion": emotion,
            "confidence": 1.0,
            "response_text": response_text
        }
