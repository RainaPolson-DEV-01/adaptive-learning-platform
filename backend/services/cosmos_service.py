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
learning_path_container = database.get_container_client(
    "LearningPaths"
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

def save_learning_path(path):

    learning_path_container.upsert_item(path)

    return True
def get_assessment(user_id):

    query = """
    SELECT *
    FROM c
    WHERE c.userId = @userId
    """

    items = list(
        assessment_container.query_items(
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
