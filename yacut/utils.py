import random
import string

from yacut.models import URLMap


def get_unique_short_id():
    """Формирование коротких идентификаторов."""
    while True:
        short_id = ''.join(
            random.choices(string.ascii_letters, k=6)
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
