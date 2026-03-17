from flask import Flask, request, render_template, send_file
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)

# DeepSeek client setup
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# Home route
@app.route('/')
def home():
    return render_template("index.html")


# Generate route
@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get uploaded file
        file = request.files.get('file')

        if not file:
            return "❌ No file uploaded"

        # Read CSV
        df = pd.read_csv(file)

        # Validate required columns
        required_columns = ["name", "email", "topic", "notes"]
        for col in required_columns:
            if col not in df.columns:
                return f"❌ Missing column: {col}"

        outputs = []

        # Loop through rows
        for _, row in df.iterrows():
            name = row.get("name", "")
            topic = row.get("topic", "")
            notes = row.get("notes", "")

            prompt = f"""
Write a short, personalized research outreach email.

Name: {name}
Topic: {topic}
Notes: {notes}

Make it professional, concise, and engaging.
"""

            # DeepSeek API call
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}]
            )

            message = response.choices[0].message.content
            outputs.append(message)

        # Add output column
        df["generated_message"] = outputs

        # Save file
        output_file = "output.csv"
        df.to_csv(output_file, index=False)

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return f"❌ Error: {str(e)}"


# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)