from json import load
from os import path

from unirecka.settings import BASE_DIR


def check_if_has_cursed_words(words):
    try:
        with open(
            path.join(BASE_DIR, "universities\\static\\universities\\curseWords.json")
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
