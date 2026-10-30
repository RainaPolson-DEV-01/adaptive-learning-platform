from backend.services.cosmos_service import (
    get_profile,
    save_assessment
)

from backend.agents.assessment_agent import (
    generate_assessment
)

profile = get_profile("1001")

assessment = generate_assessment(
    profile
)

print(assessment)

assessment["id"] = "A1001"
assessment["userId"] = "1001"

save_assessment(
    assessment
)

print("Assessment Saved Successfully")