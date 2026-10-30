from backend.services.cosmos_service import (
    get_profile,
    save_profile
)

profile = get_profile("1001")

new_profile = {
    "id": profile["id"],
    "userId": profile["userId"],
    "documentType": "learnerProfile",
    "version": 1,
    "status": "Active",

    "name": profile["name"],
    "skills": profile["skills"],
    "careerGoals": profile["careerGoals"],
    "experienceSummary": profile["experienceSummary"]
}

save_profile(new_profile)

print("Profile Schema Updated")