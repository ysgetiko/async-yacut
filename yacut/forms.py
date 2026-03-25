from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional, Regexp,
                                ValidationError)

from yacut.constants import (CUSTOM_ID_REGEX, MAX_LENGTH_ORIGINAL,
                             MAX_LENGTH_SHORT, FormMessages, InvalidMessages)
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
        FormMessages.CUSTOM_ID_LABEL,
        validators=[
            Length(max=MAX_LENGTH_SHORT),
            Regexp(
                CUSTOM_ID_REGEX,
                message=InvalidMessages.CONSTRAINS_SHORT,
            ),
            Optional(),
        ],
    )
    submit = SubmitField(FormMessages.SHORT_SUBMIT)

    def validate_custom_id(self, field):
        if field.data == InvalidMessages.CONSTRAINS_NAME or URLMap.get(
            field.data
        ):
            raise ValidationError(InvalidMessages.SHORT_EXISTS)


class UploadForm(FlaskForm):
    files = MultipleFileField(
        FormMessages.FILES_LABEL,
        validators=[FileRequired(message=FormMessages.REQUIRED)],
    )
    submit = SubmitField(FormMessages.FILES_SUBMIT)
