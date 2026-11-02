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


def evaluate_learning_state(
    profile,
    progress,
    learning_path
):

    base_prompt = load_prompt(
        "adaptive_prompt.txt"
    )

    prompt = f"""
{base_prompt}

Learner Profile:

{json.dumps(profile, indent=2)}

Learning Progress:

{json.dumps(progress, indent=2)}

Learning Path:

{json.dumps(learning_path, indent=2)}
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

    result = response.choices[0].message.content

    print("RAW RESPONSE:")
    print(result)

    result = result.replace(
        "```json",
        ""
    )

    result = result.replace(
        "```",
        ""
    )

    result = result.strip()

    try:
        return json.loads(result)

    except Exception as ex:

        print("JSON Parse Failed")
        print(result)

        raise ex