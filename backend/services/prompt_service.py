def load_prompt(file_name):

    with open(
        f"backend/prompts/{file_name}",
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()