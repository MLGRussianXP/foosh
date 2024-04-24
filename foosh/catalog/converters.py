from catalog.models import Category


__all__ = [
    "CategoryConverter",
]


class CategoryConverter:
    regex = "|".join([str(category[0]) for category in Category.choices])

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
