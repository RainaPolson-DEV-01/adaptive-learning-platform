from backend.services.cosmos_service import (
    get_profile,
    get_learning_progress,
    get_learning_path
)

from backend.agents.adaptive_agent import (
    evaluate_learning_state
)

profile = get_profile("1001")

progress = get_learning_progress(
    "1001"
)

path = get_learning_path(
    "1001"
)

result = evaluate_learning_state(
    profile,
    progress,
    path
)

print(result)