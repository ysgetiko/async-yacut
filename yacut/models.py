import random
from datetime import datetime
from re import match

from flask import url_for

from yacut import db
from yacut.constants import (ALLOWED_FOR_SHORT, FORBIDDEN_SHORT, MAX_ATTEMPTS,
                             MAX_LENGTH_ORIGINAL, MAX_LENGTH_SHORT, MAX_SHORT,
                             REGEX_FOR_SHORT, InvalidMessages)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    @staticmethod
    def get_unique_short():
        """Генерация уникального короткого кода переменной длины"""

        for _ in range(MAX_ATTEMPTS):
            short = "".join(random.choices(ALLOWED_FOR_SHORT, k=MAX_SHORT))

            if short != FORBIDDEN_SHORT or URLMap.get(short) is None:
                return short

        raise RuntimeError(InvalidMessages.ERROR_RUNTIME)

    @staticmethod
    def create(original, short=None, skip_validation=False):
        if not skip_validation:
            if short:
                if len(short) > MAX_LENGTH_SHORT or not match(
                    REGEX_FOR_SHORT, short
                ):
                    raise ValueError(InvalidMessages.INVALID_SHORT)
                if short == FORBIDDEN_SHORT or URLMap.get(short) is not None:
                    raise ValueError(InvalidMessages.SHORT_EXISTS)
            if len(original) > MAX_LENGTH_ORIGINAL:
                raise ValueError(InvalidMessages.ERROR_SHORT_LENGTH)
        if not short:
            short = URLMap.get_unique_short()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        return url_map

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    def get_short_url(self):
        return url_for("short_url", short=self.short, _external=True)
