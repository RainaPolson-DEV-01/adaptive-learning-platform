from backend.services.resume_reader import read_resume
from backend.agents.profile_agent import generate_profile
from backend.services.cosmos_service import save_profile

# Read resume
resume_text = read_resume(
    "data/resumes/Sample_Azure_Data_Engineer_Resume.pdf"
)

# Generate profile
profile = generate_profile(resume_text)

# Debug
print("Profile Type:", type(profile))
print("Profile Content:", profile)

# Add Cosmos metadata
profile["id"] = "1001"
profile["userId"] = "1001"

# Save to Cosmos DB
save_profile(profile)

print("Profile Saved Successfully")