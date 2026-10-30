from backend.services.openai_service import (
    get_client,
    get_model_name
)

client = get_client()

response = client.chat.completions.create(
    model=get_model_name(),
    messages=[
        {
            "role": "user",
            "content": "Hello"
        }
    ]
)

print(response.choices[0].message.content)