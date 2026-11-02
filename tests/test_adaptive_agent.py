from backend.agents.adaptive_agent import (
    evaluate_progress
)

progress = {
    "score": 45
}

result = evaluate_progress(
    progress
)

print(result)