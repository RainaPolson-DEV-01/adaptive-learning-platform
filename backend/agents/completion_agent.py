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


def generate_completion_report(
    profile,
    progress,
    path,
    evaluation
):

    base_prompt = load_prompt(
        "completion_prompt.txt"
    )

    prompt = f"""
{base_prompt}

Profile:
{json.dumps(profile, indent=2)}

Progress:
{json.dumps(progress, indent=2)}

Learning Path:
{json.dumps(path, indent=2)}

Evaluation:
{json.dumps(evaluation, indent=2)}
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

    return json.loads(
        response.choices[0].message.content
    )