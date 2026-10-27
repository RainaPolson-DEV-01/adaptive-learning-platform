import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def generate_profile(resume_text):

    prompt = f"""
    Analyze this resume.

    Extract:
    1. Name
    2. Skills
    3. Career Goals
    4. Experience Summary

    Return ONLY valid JSON.

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model=os.getenv("GPT_DEPLOYMENT"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    # Remove markdown wrappers
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    profile = json.loads(result)

    return profile