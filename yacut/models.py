import random
import re
from datetime import datetime

from flask import url_for

from yacut import db
from yacut.constants import (
    ALLOWED_FOR_SHORT,
    FORBIDDEN_SHORT,
    MAX_ATTEMPTS,
    MAX_LENGTH_ORIGINAL,
    MAX_LENGTH_SHORT,
    MAX_SHORT,
    REDIRECT_FOR_SHORT,
    SHORT_REGEX,
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
            short = "".join(random.choices(ALLOWED_FOR_SHORT, k=MAX_SHORT))
            if short != FORBIDDEN_SHORT and URLMap.get(short) is None:
                return short
        raise RuntimeError(InvalidMessages.MAX_ATTEMPTS_EXPIRED)

    @staticmethod
    def create(original, short=None, skip_validation=False):
        """Основной метод создания записи"""
        url_map = URLMap._create_internal(original, short, skip_validation)
        db.session.commit()
        return url_map

    @staticmethod
    def create_batch(original, short=None, skip_validation=False):
        """Метод для пакетного создания записи"""
        return URLMap._create_internal(original, short, skip_validation)

    @staticmethod
    def _create_internal(original, short=None, skip_validation=False):
        """Внутренняя логика создания записи"""
        if not skip_validation:
            if len(original) > MAX_LENGTH_ORIGINAL:
                raise ValueError(InvalidMessages.ERROR_SHORT_LENGTH)
            if short:
                if len(short) > MAX_LENGTH_SHORT or not re.match(
                    SHORT_REGEX, short
                ):
                    raise ValueError(InvalidMessages.INVALID_SHORT)
                if short == FORBIDDEN_SHORT or URLMap.get(short) is not None:
                    raise ValueError(InvalidMessages.SHORT_EXISTS)
        url_map = URLMap(
            original=original, short=short or URLMap.get_unique_short()
        )
        db.session.add(url_map)
        return url_map

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    def get_short_url(self):
        return url_for(REDIRECT_FOR_SHORT, short=self.short, _external=True)
