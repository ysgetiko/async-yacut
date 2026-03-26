import re
import string

MAX_LENGTH_ORIGINAL = 4000
MAX_LENGTH_SHORT = 16
MAX_ATTEMPTS = 50
MAX_SHORT = 6

ALLOWED_FOR_SHORT = string.ascii_letters + string.digits
FORBIDDEN_SHORT = "files"
REDIRECT_FOR_SHORT = "short_url"


class InvalidMessages:
    ERROR_NO_REQUEST_BODY = "Отсутствует тело запроса"
    ERROR_MISSING_REQUIRED_FIELD = '"{field}" является обязательным полем!'
    ERROR_NO_FOUND_SHORT = "Указанный id не найден"
    CONSTRAINS_SHORT = "Поле может содержать только латинские буквы и цифры"
    INVALID_SHORT = "Указано недопустимое имя для короткой ссылки"
    SHORT_EXISTS = "Предложенный вариант короткой ссылки уже существует."
    ERROR_SHORT_CREATE = (
        "Ошибка создания короткой ссылки для {field}: {field2} error"
    )
    MAX_ATTEMPTS_EXPIRED = (
        "Не удалось сгенерировать уникальный короткий "
        f"код после максимального числа попыток {MAX_ATTEMPTS}."
    )
    ERROR_SHORT_LENGTH = (
        f"Ссылка не должна превышать {MAX_LENGTH_ORIGINAL} символов."
    )
    ERROR_UPLOADS = "Не удалось загрузить файлы на Яндекс.Диск."
    ERROR_UPLOAD = "Ошибка загрузки файла {field}': {field_2}"
    FILE_EXISTS_MESSAGE = "Файл {field} уже существует на диске"
    CLIENT_ERROR = "Ошибка HTTP при загрузке файла: {field}"
    KEY_ERROR = "Неожиданный формат ответа: отсутствует ключ {field}"
    MISSING_HEADER = "Отсутствует хэдер Location в ответе."


class FormMessages:
    ORIGINAL_LINK_LABEL = "Длинная ссылка"
    REQUIRED = "Обязательное поле"
    CUSTOM_SHORT_LABEL = "Ваш вариант короткой ссылки"
    SHORT_SUBMIT = "Добавить"
    FILES_LABEL = "Выбрать файлы"
    FILES_SUBMIT = "Загрузить"
