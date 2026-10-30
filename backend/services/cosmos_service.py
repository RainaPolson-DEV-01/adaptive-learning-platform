import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient

load_dotenv()

client = CosmosClient(
    os.getenv("COSMOS_ENDPOINT"),
    os.getenv("COSMOS_KEY")
)

database = client.get_database_client(
    "AdaptiveLearning"
)

profile_container = database.get_container_client(
    "LearnerProfiles"
)

assessment_container = database.get_container_client(
    "Assessments"
)


def save_profile(profile):

    profile_container.upsert_item(profile)

    return True


def get_profile(user_id):

    query = """
    SELECT *
    FROM c
    WHERE c.userId = @userId
    """

    items = list(
        profile_container.query_items(
            query=query,
            parameters=[
                {
                    "name": "@userId",
                    "value": user_id
                }
            ],
            enable_cross_partition_query=True
        )
    )

    return items[0] if items else None


def save_assessment(assessment):

    assessment_container.upsert_item(
        assessment
    )

    return True