from backend.services.openai_service import (
    get_client,
    get_model_name
)

from backend.services.prompt_service import (
    load_prompt
)

client = get_client()
model = get_model_name()


def answer_question(
    learner_profile,
    module,
    question
):

    base_prompt = load_prompt(
        "tutor_prompt.txt"
    )

    prompt = f"""
{base_prompt}

Learner Background:

{learner_profile["experienceSummary"]}

Current Module:

{module["title"]}

Difficulty:

{module["difficulty"]}

Learning Objectives:

{module["learningObjectives"]}

Module Summary:

{module["summary"]}

Question:

{question}
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

    return (
        response
        .choices[0]
        .message
        .content
    )