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

# =========================
# Containers
# =========================

profile_container = database.get_container_client(
    "LearnerProfiles"
)

assessment_container = database.get_container_client(
    "Assessments"
)

learning_path_container = database.get_container_client(
    "LearningPaths"
)

learning_progress_container = database.get_container_client(
    "LearningProgress"
)

evaluation_container = database.get_container_client(
    "Evaluations"
)

certificate_container = database.get_container_client(
    "Certificates"
)

# =========================
# Profile Functions
# =========================

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


# =========================
# Assessment Functions
# =========================

def save_assessment(assessment):

    assessment_container.upsert_item(
        assessment
    )

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


# =========================
# Learning Path Functions
# =========================

def save_learning_path(path):

    learning_path_container.upsert_item(
        path
    )

    return True


def get_learning_path(user_id):

    query = """
    SELECT *
    FROM c
    WHERE c.userId = @userId
    """

    items = list(
        learning_path_container.query_items(
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


# =========================
# Learning Progress Functions
# =========================

def save_learning_progress(progress):

    learning_progress_container.upsert_item(
        progress
    )

    return True


def get_learning_progress(user_id):

    query = """
    SELECT *
    FROM c
    WHERE c.userId = @userId
    """

    items = list(
        learning_progress_container.query_items(
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

    return items


def update_learning_progress(
    user_id,
    module_id,
    score,
    percent_complete,
    status
):

    progress_list = get_learning_progress(
        user_id
    )

    for progress in progress_list:

        if progress["moduleId"] == module_id:

            progress["score"] = score

            progress["percentComplete"] = (
                percent_complete
            )

            progress["status"] = status

            learning_progress_container.upsert_item(
                progress
            )

            return progress

    return None


# =========================
# Evaluation Functions
# =========================

def save_evaluation(evaluation):

    evaluation_container.upsert_item(
        evaluation
    )

    return True


def get_evaluation(user_id):

    query = """
    SELECT *
    FROM c
    WHERE c.userId = @userId
    """

    items = list(
        evaluation_container.query_items(
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


# =========================
# Certificate Functions
# =========================

def save_certificate(certificate):

    certificate_container.upsert_item(
        certificate
    )

    return True


def get_certificate(user_id):

    query = """
    SELECT *
    FROM c
    WHERE c.userId = @userId
    """

    items = list(
        certificate_container.query_items(
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