from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Ask AI
@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")

    try:
        response = client.responses.create(
            model="gpt-5",
            input=[
                {"role": "system", "content": "You are a helpful AI assistant"},
                {"role": "user", "content": question}
            ],
            max_output_tokens=300
        )

        answer = response.output[0].content[0].text.strip()

        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Summarize email
@app.route("/summarize", methods=["POST"])
def summarize():
    email = request.form.get("email")

    try:
        response = client.responses.create(
            model="gpt-5",
            input=f"Summarize this email:\n{email}",
            max_output_tokens=200
        )

        summary = response.output[0].content[0].text.strip()

        return jsonify({"response": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)