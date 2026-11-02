from backend.services.cosmos_service import (
    get_profile
)

from backend.services.catalog_service import (
    get_module
)

from backend.agents.tutor_agent import (
    answer_question
)

profile = get_profile("1001")

module = get_module("M001")

response = answer_question(
    profile,
    module,
    "What is OneLake and why is it important?"
)

print(response)