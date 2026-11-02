from backend.services.cosmos_service import (
    save_learning_progress,
    get_learning_progress
)

progress = {

    "id": "P1001",

    "userId": "1001",

    "moduleId": "M001",

    "moduleTitle":
        "Microsoft Fabric Fundamentals",

    "status":
        "InProgress",

    "score":
        0,

    "percentComplete":
        0,

    "attempts":
        0
}

save_learning_progress(
    progress
)

result = get_learning_progress(
    "1001"
)

print(result)