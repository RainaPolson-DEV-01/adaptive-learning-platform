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

def generate_assessment(profile):

    skills = profile.get(
        "Skills",
        profile.get("skills", [])
    )

    prompt = f"""
    Create an assessment for this learner.

    Skills:
    {skills}

    Requirements:
    - 10 Multiple Choice Questions
    - 5 Beginner
    - 5 Intermediate
    - 4 options per question
    - Include correct answer
    - Include related skill

    Return JSON only.

    {{
      "questions":[
        {{
          "skill":"",
          "difficulty":"",
          "question":"",
          "options":[],
          "answer":""
        }}
      ]
    }}
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

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    return json.loads(result)
