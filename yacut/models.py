import random
from datetime import datetime
from re import match

from flask import url_for

from yacut import db
from yacut.constants import (
    ALLOWED_FOR_SHORT,
    CUSTOM_ID_REGEX,
    MAX_ATTEMPTS,
    MAX_LENGTH_ORIGINAL,
    MAX_LENGTH_SHORT,
    MAX_SHORT,
    REDIRECT_FOR_SHORT,
    InvalidMessages,
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    @staticmethod
    def get_unique_short():
        """Генерация уникального короткого кода переменной длины"""

        for _ in range(MAX_ATTEMPTS):
            code = "".join(random.choices(ALLOWED_FOR_SHORT, k=MAX_SHORT))

            if (
                code != InvalidMessages.CONSTRAINS_NAME
                or URLMap.get(code) is None
            ):
                return code

        raise RuntimeError(
            InvalidMessages.ERROR_RUNTIME.format(field=MAX_ATTEMPTS)
        )

    @staticmethod
    def create(original, short=None, validation=True):
        if validation:
            if short:
                if (
                    len(short) > MAX_LENGTH_SHORT
                    or not match(CUSTOM_ID_REGEX, short)
                    or short == InvalidMessages.CONSTRAINS_NAME
                ):
                    raise ValueError(InvalidMessages.INVALID_SHORT)
                if URLMap.get(short) is not None:
                    raise ValueError(InvalidMessages.SHORT_EXISTS)
            if len(original) > MAX_LENGTH_ORIGINAL:
                raise ValueError(InvalidMessages.ERROR_SHORT_LENGTH)
        if not short:
            short = URLMap.get_unique_short()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    def get_short_url(self):
        return url_for(REDIRECT_FOR_SHORT, short=self.short, _external=True)
