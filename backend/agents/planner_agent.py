import json

from backend.services.openai_service import (
    get_client,
    get_model_name
)

client = get_client()
model = get_model_name()


def generate_learning_path(
        profile,
        assessment_result
):

    skill_gaps = assessment_result.get(
        "skillGaps",
        []
    )

    learner_level = assessment_result.get(
        "learnerLevel",
        "Beginner"
    )

    prompt = f"""
You are an Adaptive Learning Path Agent.

Create a personalized learning roadmap.

Learner Profile:

{json.dumps(profile, indent=2)}

Assessment Information:

Level: {learner_level}

Identified Skill Gaps:

{json.dumps(skill_gaps, indent=2)}

IMPORTANT RULES:

1. Create modules ONLY for the identified skill gaps.
2. Do NOT create modules for skills the learner already knows.
3. Arrange modules from beginner to advanced.
4. Each module must directly address one skill gap.
5. Include learning objectives.
6. Include estimated duration.
7. Include hands-on exercises.
8. Include expected outcome.
9. Return ONLY valid JSON.

Schema:

{{
    "learningPath": [
        {{
            "moduleTitle": "",
            "skill": "",
            "duration": "",
            "objective": "",
            "exercise": "",
            "outcome": ""
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

    content = (
        response
        .choices[0]
        .message
        .content
    )

    return json.loads(
        content
    )