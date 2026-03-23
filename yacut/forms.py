from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional, Regexp,
                                ValidationError)

from .constants import MAX_LENGTH_ORIGINAL, MAX_LENGTH_SHORT
from .models import URLMap


class URLMapForm(FlaskForm):
    original_link = URLField(
        "Длинная ссылка",
        validators=[
            DataRequired(message="Обязательное поле"),
            Length(1, MAX_LENGTH_ORIGINAL),
        ],
    )
    custom_id = StringField(
        "Ваш вариант короткой ссылки",
        validators=[
            Length(max=MAX_LENGTH_SHORT),
            Regexp(
                r"^[a-zA-Z0-9]+$",
                message="Поле может содержать только латинские буквы и цифры",
            ),
            Optional(),
        ],
    )
    submit = SubmitField("Добавить")

    def validate_custom_id(self, field):
        if field.data:
            if URLMap.get(field.data) or field.data == "files":
                raise ValidationError(
                    "Предложенный вариант короткой ссылки уже существует."
                )


class UploadForm(FlaskForm):
    files = MultipleFileField(
        "Выбрать файлы", validators=[FileRequired(message="Обязательное поле")]
    )
    submit = SubmitField("Загрузить")
