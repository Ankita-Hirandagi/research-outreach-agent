import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def generate_outreach(data):
    prompt = f"""
You are an expert scientific communication writer.

Write a 3 sentence outreach message:
1. Acknowledge researcher and institution
2. Summarize research insight
3. Explain relevance to health innovators

Keep academic tone. No hype.

Researcher Name: {data['researcher_name']}
Institution: {data['institution']}
Article Title: {data['article_title']}
Article Summary: {data['article_summary']}
Signal Strength: {data['signal_strength']}
Contact Channel: {data['contact_channel']}

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