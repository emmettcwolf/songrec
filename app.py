from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Simple GET route for testing
@app.route('/test', methods=['GET'])
def test_api():
    return jsonify({"message": "API is working!"})

@app.route('/recommend', methods=['POST'])
def recommend_songs():
    data = request.get_json()

    # Check if the 'song' key exists in the request data
    if 'song' not in data:
        return jsonify({"error": "Song name is required"}), 400

    song = data['song']

    try:
        # Use OpenAI API to generate song recommendations
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the appropriate model
            prompt=f"Suggest songs similar to {song} based on genre and artist.",
            max_tokens=100,
            temperature=0.7
        )

        recommendations = response['choices'][0]['text'].strip()
        return jsonify({"recommendations": recommendations})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
