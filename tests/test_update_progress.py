from backend.services.cosmos_service import (
    update_learning_progress
)

result = update_learning_progress(
    user_id="1001",
    module_id="M001",
    score=92,
    percent_complete=100,
    status="Completed"
)

print(result)