from backend.services.cosmos_service import (
    get_learning_path
)

path = get_learning_path("1001")

print(path)