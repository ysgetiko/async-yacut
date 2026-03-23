from datetime import datetime
from re import match

from flask import url_for

from yacut import db

from .constants import (MAX_ATTEMPTS, MAX_LENGTH_ORIGINAL, MAX_LENGTH_SHORT,
                        MAX_SHORT)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    @staticmethod
    def get_unique_short_id():
        """Генерация уникального короткого кода переменной длины"""
        import random
        import string

        for _ in range(MAX_ATTEMPTS):
            length = MAX_SHORT
            code = "".join(
                random.choices(string.ascii_letters + string.digits, k=length)
            )

            if URLMap.get(code) is None or code != "files":
                return code

        raise RuntimeError(
            "Не удалось сгенерировать уникальный короткий "
            "код после максимального числа попыток"
        )

    @staticmethod
    def create(original, short=None, validation=True):
        from sqlalchemy.exc import SQLAlchemyError

        if validation:
            if short:
                URLMap._validate_short_code(short)
            URLMap._validate_original_url(original)

        if not short:
            short = URLMap.get_unique_short_id()

        try:
            url_map = URLMap(original=original, short=short)
            db.session.add(url_map)
            db.session.commit()
            return url_map
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Ошибка при сохранении в БД: {str(e)}") from e

    @staticmethod
    def _validate_short_code(short):
        """Валидация короткого кода."""
        if len(short) > MAX_LENGTH_SHORT:
            raise ValueError("Указано недопустимое имя для короткой ссылки")
        if not match(r"^[a-zA-Z0-9]+$", short):
            raise ValueError("Указано недопустимое имя для короткой ссылки")
        if URLMap.get(short) is not None:
            raise ValueError(
                "Предложенный вариант короткой ссылки уже существует."
            )

    @staticmethod
    def _validate_original_url(original):
        """Валидация оригинальной ссылки."""
        if len(original) > MAX_LENGTH_ORIGINAL:
            raise ValueError(
                f"Ссылка не должна превышать {MAX_LENGTH_ORIGINAL} символов."
            )

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    def get_short_url(self):
        print("get_short_url")
        return url_for("short_url", short=self.short, _external=True)
