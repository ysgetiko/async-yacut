import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    ValidationError,
)

from yacut.constants import (
    ALLOWED_FOR_SHORT,
    FORBIDDEN_SHORT,
    MAX_LENGTH_ORIGINAL,
    MAX_LENGTH_SHORT,
    FormMessages,
    InvalidMessages,
)
from yacut.models import URLMap


class URLMapForm(FlaskForm):
    original_link = URLField(
        FormMessages.ORIGINAL_LINK_LABEL,
        validators=[
            DataRequired(message=FormMessages.REQUIRED),
            Length(max=MAX_LENGTH_ORIGINAL),
        ],
    )
    custom_id = StringField(
        FormMessages.CUSTOM_SHORT_LABEL,
        validators=[
            Length(max=MAX_LENGTH_SHORT),
            Regexp(
                re.compile(f"^[{re.escape(ALLOWED_FOR_SHORT)}]+$"),
                message=InvalidMessages.CONSTRAINS_SHORT,
            ),
            Optional(),
        ],
    )
    submit = SubmitField(FormMessages.SHORT_SUBMIT)

    def validate_custom_id(self, field):
        if field.data and (
            field.data == FORBIDDEN_SHORT or URLMap.get(field.data)
        ):
            raise ValidationError(InvalidMessages.SHORT_EXISTS)


class UploadForm(FlaskForm):
    files = MultipleFileField(
        FormMessages.FILES_LABEL,
        validators=[FileRequired(message=FormMessages.REQUIRED)],
    )
    submit = SubmitField(FormMessages.FILES_SUBMIT)
