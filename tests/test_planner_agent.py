from backend.services.cosmos_service import (
    get_profile,
    get_assessment,
    save_learning_path
)

from backend.services.catalog_service import (
    load_catalog
)

from backend.agents.planner_agent import (
    generate_learning_path
)

profile = get_profile("1001")

assessment = get_assessment("1001")

catalog = load_catalog()

path = generate_learning_path(
    profile,
    assessment,
    catalog
)

print(path)

path["id"] = "LP1001"
path["userId"] = "1001"

save_learning_path(path)

print("Learning Path Saved")