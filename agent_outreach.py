import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def generate_outreach():
    prompt = """
You are an expert scientific communication writer.

Write a 3 sentence outreach message:

1. Acknowledge researcher and institution
2. Summarize research insight
3. Explain relevance to health innovators

Keep academic tone. No hype.

Input:
Researcher Name: Dr. Sarah Chen
Institution: Harvard Medical School
Article Title: AI-driven early detection of cardiovascular disease
Article Summary: A machine learning model predicts cardiovascular risk using biomarkers.
Signal Strength: High
Contact Channel: Email

Return only the final message.
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a precise academic writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


result = generate_outreach()

print("\nGenerated Outreach Message:\n")
print(result)