import json

from backend.services.openai_service import (
    get_client,
    get_model_name
)

from backend.services.prompt_service import (
    load_prompt
)

client = get_client()
model = get_model_name()


def generate_profile(resume_text):

    base_prompt = load_prompt(
        "profile_prompt.txt"
    )

    prompt = f"""
{base_prompt}

Resume:

{resume_text}
"""

    response = client.chat.completions.create(
        model=model,
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

    profile = json.loads(result)

    return profile