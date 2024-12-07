from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Configure your OpenAI API key
openai.api_key = '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'

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    song = data.get('song')

    if not song:
        return jsonify({'error': 'No song provided'}), 400

    try:
        # Call OpenAI API for recommendations
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Suggest 5 songs similar to '{song}' based on genre and artist.",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        recommendations = response.choices[0].text.strip().split('\n')
        recommendations = [rec.strip('- ') for rec in recommendations if rec.strip()]

        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
