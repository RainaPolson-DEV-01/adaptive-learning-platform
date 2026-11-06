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


def generate_assessment(profile):

    base_prompt = load_prompt(
        "assessment_prompt.txt"
    )

    prompt = f"""
{base_prompt}

Learner Profile:

{json.dumps(profile, indent=2)}

Generate:

1. 10 multiple-choice questions
2. Four options per question
3. One correct answer
4. Associate each question with a skill area
5. Base questions on learner skills from the profile

Return ONLY valid JSON.

Schema:

{{
    "assessment": [
        {{
    "question": "",
    "options": [],
    "answer": "",
    "skill": "",
    "difficulty": ""
}}
    ]
}}
"""
    response = client.chat.completions.create(
        model=model,
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = (
        response
        .choices[0]
        .message
        .content
    )

    return json.loads(
        result
    )