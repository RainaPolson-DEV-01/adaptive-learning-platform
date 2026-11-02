import json


def load_catalog():

    with open(
        "data/contents/learning_catalog.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def get_module(module_id):

    catalog = load_catalog()

    for module in catalog:

        if module["moduleId"] == module_id:
            return module

    return None


def get_module_by_skill(skill):

    catalog = load_catalog()

    for module in catalog:

        if skill in module["skills"]:
            return module

    return None