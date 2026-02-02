from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_logic import AIEngine
import logging

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend

# Initialize AI Engine
ai_engine = AIEngine()

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "online", "message": "Adaptive AI System Ready"})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        user_input = data.get('text', '')

        if not user_input:
            return jsonify({"error": "No text provided"}), 400

        # Process input through AI Engine
        result = ai_engine.process_input(user_input)

        return jsonify({
            "status": "success",
            "data": result
        })

    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
