from rest_framework.exceptions import ValidationError
from pathlib import Path


class ForbiddenWordValidator:
    """
    Валидатор для проверки текста на запрещенные слова
    """

    def __init__(self, announcement_title=None, announcement_description=None, review_text=None):
        self.announcement_title = announcement_title
        self.announcement_description = announcement_description
        self.review_text = review_text

    def __call__(self, value):

        announcement_title_field = value.get(self.announcement_title)
        announcement_description_field = value.get(self.announcement_description)
        review_text_field = value.get(self.review_text)

        with open(Path(__file__).parent.joinpath("forbidden_words.txt"), "r", encoding="utf-8") as file:
            forbidden_words = file.read().splitlines()

        for word in forbidden_words:
            try:
                if word in announcement_title_field or word in announcement_description_field:
                    raise ValidationError(f"Имеется запрещенное слово в тексте")
            except TypeError:
                pass
            try:
                if word in review_text_field:
                    raise ValidationError(f"Имеется запрещенное слово в тексте")
            except TypeError:
                pass




