import os

from dotenv import load_dotenv
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import (
    CosmosResourceExistsError
)

load_dotenv()

client = CosmosClient(
    os.getenv("COSMOS_ENDPOINT"),
    os.getenv("COSMOS_KEY")
)

database = client.get_database_client(
    "AdaptiveLearning"
)

# ==========================================
# Containers
# ==========================================

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
assessment_result_container = (
    database.get_container_client(
        "AssessmentResults"
    )
)

# ==========================================
# Profile Functions
# ==========================================

def save_profile(profile):

    try:

        profile_container.create_item(
            profile
        )

        return True

    except CosmosResourceExistsError:

        print(
            f"Profile already exists: "
            f"{profile['id']}"
        )

        return False


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


# ==========================================
# Assessment Functions
# ==========================================

def save_assessment(assessment):

    try:

        assessment_container.create_item(
            assessment
        )

        return True

    except CosmosResourceExistsError:

        print(
            f"Assessment already exists: "
            f"{assessment['id']}"
        )

        return False


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


# ==========================================
# Learning Path Functions
# ==========================================

def save_learning_path(path):

    try:

        learning_path_container.create_item(
            path
        )

        return True

    except CosmosResourceExistsError:

        print(
            f"Learning path already exists: "
            f"{path['id']}"
        )

        return False

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


# ==========================================
# Learning Progress Functions
# ==========================================

def save_learning_path(path):

    learning_path_container.upsert_item(
        path
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

            # Progress is expected to change
            learning_progress_container.upsert_item(
                progress
            )

            return progress

    return None


# ==========================================
# Evaluation Functions
# ==========================================

def save_evaluation(evaluation):

    try:

        evaluation_container.create_item(
            evaluation
        )

        return True

    except CosmosResourceExistsError:

        print(
            f"Evaluation already exists: "
            f"{evaluation['id']}"
        )

        return False


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


# ==========================================
# Certificate Functions
# ==========================================

def save_certificate(certificate):

    try:

        certificate_container.create_item(
            certificate
        )

        return True

    except CosmosResourceExistsError:

        print(
            f"Certificate already exists: "
            f"{certificate['id']}"
        )

        return False


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

# ==========================================
# assessment save Functions
# ==========================================


def save_assessment_result(
    result
):

    assessment_result_container.create_item(
        result
    )

    return True
# ==========================================
# Assessment Result Functions
# ==========================================

assessment_result_container = (
    database.get_container_client(
        "AssessmentResults"
    )
)


def save_assessment_result(
    result
):

    assessment_result_container.create_item(
        result
    )

    return True


def get_assessment_result(
    user_id
):

    query = """
    SELECT *
    FROM c
    WHERE c.userId = @userId
    """

    items = list(
        assessment_result_container.query_items(
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