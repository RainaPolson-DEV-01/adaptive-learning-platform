from backend.services.cosmos_service import (
    get_profile,
    get_learning_progress,
    get_learning_path,
    get_evaluation,
    save_certificate
)

from backend.agents.completion_agent import (
    generate_completion_report
)

profile = get_profile("1001")

progress = get_learning_progress(
    "1001"
)

path = get_learning_path(
    "1001"
)

evaluation = get_evaluation(
    "1001"
)

result = generate_completion_report(
    profile,
    progress,
    path,
    evaluation
)

result["id"] = "C1001"
result["userId"] = "1001"

save_certificate(result)

print(result)

print(
    "Certificate Record Saved Successfully"
)