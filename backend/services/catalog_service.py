import json


def load_catalog():

    with open(
        "data/contents/learning_catalog.json",
        "r"
    ) as file:

        return json.load(file)