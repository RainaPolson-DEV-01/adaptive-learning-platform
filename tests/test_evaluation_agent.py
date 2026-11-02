from backend.services.cosmos_service import (
    get_profile,
    get_learning_progress,
    get_learning_path,
    get_assessment,
    save_evaluation
)

from backend.agents.evaluation_agent import (
    evaluate_learner
)

# Get learner profile
profile = get_profile("1001")

# Get progress details
progress = get_learning_progress(
    "1001"
)

# Get learning path
path = get_learning_path(
    "1001"
)

# Get assessment
assessment = get_assessment(
    "1001"
)

# Run evaluation
result = evaluate_learner(
    profile,
    progress,
    path,
    assessment
)

# Add Cosmos metadata
result["id"] = "E1001"
result["userId"] = "1001"

# Save evaluation
save_evaluation(result)

# Print output
print(result)

print(
    "Evaluation Saved Successfully"
)