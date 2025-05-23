from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from openai import OpenAI # Updated import

load_dotenv()

# Initialize the OpenAI client
# It automatically picks up OPENAI_API_KEY from environment variables
client = OpenAI()

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        resp = client.chat.completions.create( # Using the client instance
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"response": resp.choices[0].message.content})
    except Exception as e:
        # Basic error handling for API calls
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) # Railway provides 'PORT'
    app.run(host='0.0.0.0', port=port, debug=False) # Set debug to False for production


