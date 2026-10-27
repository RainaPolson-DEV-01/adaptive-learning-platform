import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient

load_dotenv()

client = CosmosClient(
    os.getenv("COSMOS_ENDPOINT"),
    credential=os.getenv("COSMOS_KEY")
)

database = client.get_database_client(
    "AdaptiveLearning"
)

container = database.get_container_client(
    "LearnerProfiles"
)


def save_profile(profile):

    container.upsert_item(profile)

    return True