import os
from json import load


def check_if_has_cursed_words(words):
    try:
        with open(
            os.path.join(
                os.getcwd(), "universities", "static", "universities", "curseWords.json"
            )
        ) as file:
            data = load(file)
            if "pl" in data and isinstance(data["pl"], list):
                pl_elements = data["pl"]
                for word in words:
                    if any(
                        isinstance(element, str)
                        and (word.lower() == element or element in word.lower())
                        for element in pl_elements
                    ):
                        return True
        return False
    except FileNotFoundError:
        return False
