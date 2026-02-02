import random
from textblob import TextBlob

class AIEngine:
    def __init__(self):
        self.memory = []
        self.max_memory = 3

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        return {
            "polarity": blob.sentiment.polarity,
            "subjectivity": blob.sentiment.subjectivity
        }

    def detect_emotion_expert(self, text, polarity):
        """
        Expert Logic to detect emotion based on keywords and sentiment.
        """
        text_lower = text.lower()
        
        # 1. Critical Safety Check
        danger_keywords = ["kill myself", "suicide", "hurt myself", "end it all", "die", "death"]
        if any(w in text_lower for w in danger_keywords):
            return "danger"

        # 2. Anger (New)
        anger_keywords = ["hate", "angry", "furious", "mad", "rage", "annoyed", "stupid", "idiot"]
        if any(w in text_lower for w in anger_keywords):
            return "anger"

        # 3. Anxiety
        anxiety_keywords = ["anxious", "scared", "worried", "nervous", "panic", "fear", "terrified", "doom"]
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

        # 7. Fallback based on polarity
        if polarity > 0.2: return "positive"
        if polarity < -0.2: return "sad"
        
        return "neutral"

    def get_expert_response(self, text, emotion):
        """
        Generates formatted HTML response with <strong> tags for emphasis.
        """
        
        # SAFETY FIRST (No Bold, Gentle)
        if emotion == "danger":
            return (
                "I hear that you are in deep pain. Please know you are not alone. "
                "I am an AI, but there are people who care and want to help. "
                "Please reach out to a trusted friend or a crisis helpline immediately."
            )

        # Response Templates with BOLD actions
        responses = {
            "anger": [
                "I hear your frustration. It's valid to feel this way. Try to **take a deep breath** and step away for a moment.",
                "Anger often protects us from other feelings. **Channel this energy** into something physical like a walk or writing it down.",
                "It sounds intense. **Pause for 10 seconds** before you react. You are in control."
            ],
            "anxious": [
                "I sense some anxiety. Let's ground ourselves. **Look at 5 things around you** and name them.",
                "You are safe here. Try to **breathe in for 4 seconds, hold for 7, and exhale for 8**.",
                "Anxiety tells stories that aren't always true. **Focus on just this one moment** right now."
            ],
            "stressed": [
                "You're carrying a lot. Remember, **you can only do one thing at a time**. What is the smallest step you can take?",
                "It's okay to pause. **Rest is productive too**. Give yourself permission to take a break.",
                "Everything feels urgent, but it isn't. **Prioritize just one task** and let the rest accept a delay."
            ],
            "sad": [
                "I'm sorry you're feeling down. **Be gentle with yourself** today. You don't have to 'fix' it immediately.",
                "Sadness is heavy. **Wrap yourself in something warm** or drink some water. Small comforts matter.",
                "It's okay not to be okay. **Allow yourself to feel this** without judgment. It will pass."
            ],
            "positive": [
                "That's wonderful! **Hold onto this feeling**. What was the best part of it?",
                "I love this energy! **Celebrate this win**, no matter how small.",
                "It sounds like things are looking up. **Share this joy** with someone you care about."
            ],
            "neutral": [
                "I'm listening. **Tell me more** about what's on your mind.",
                "I hear you. **Reflect on how your day actually went**—was there a specific moment that stood out?",
                "Just being here is enough. **Take a moment to check in** with your body."
            ]
        }

        # Select a template
        options = responses.get(emotion, responses["neutral"])
        return random.choice(options)

    def process_input(self, text):
        # 1. Analyze
        sentiment = self.analyze_sentiment(text)
        
        # 2. Detect Emotion (Expert Rule-Based)
        emotion = self.detect_emotion_expert(text, sentiment['polarity'])
        
        # 3. Generate Smart Response
        response_text = self.get_expert_response(text, emotion)
        
        # 4. Update Memory
        self.memory.append({
            "user_input": text,
            "response_text": response_text,
            "emotion": emotion
        })
        if len(self.memory) > self.max_memory:
            self.memory.pop(0)

        return {
            "emotion": emotion,
            "confidence": 0.95, # High confidence in our expert rules
            "response_text": response_text
        }
