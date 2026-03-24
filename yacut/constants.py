import  re
import string


MAX_LENGTH_ORIGINAL = 4000
MAX_LENGTH_SHORT = 16
MAX_ATTEMPTS = 50
MAX_SHORT = 6

CUSTOM_ID_REGEX = re.compile(r"^[a-zA-Z0-9]+$")
ALLOWED_FOR_SHORT = string.ascii_letters + string.digits



class InvalidMessages:
    ERROR_NO_REQUEST_BODY = "Отсутствует тело запроса"
    ERROR_MISSING_REQUIRED_FIELD = '"{field}" является обязательным полем!'
    ERROR_NO_FOUND_ID = "Указанный id не найден"
    CONSTRAINS_SHORT = "Поле может содержать только латинские буквы и цифры"
    CONSTRAINS_NAME = "files"
    INVALID_SHORT = "Указано недопустимое имя для короткой ссылки"
    SHORT_EXISTS = "Предложенный вариант короткой ссылки уже существует."
    ERROR_SHORT_CREATE = "Ошибка создания короткой ссылки для {field}: {field2} error"
    ERROR_RUNTIME = ("Не удалось сгенерировать уникальный короткий "
                     "код после максимального числа попыток {field}."
                     )
    ERROR_DB = "Ошибка при сохранении в БД: {field}"
    ERROR_SHORT_LENGTH = f"Ссылка не должна превышать {MAX_LENGTH_ORIGINAL} символов."
    ERROR_UPLOADS = "Не удалось загрузить файлы на Яндекс.Диск."
    ERROR_UPLOAD = "Ошибка загрузки файла {field}': {field_2}"
    FILE_EXISTS_MESSAGE = "Файл {field} уже существует на диске"
    NOT_EMPTY = "Список файлов не может быть пустым или None"
    CLIENT_ERROR = "Ошибка HTTP при загрузке файла: {field}"
    KEY_ERROR = "Неожиданный формат ответа: отсутствует ключ {field}"
    MISSING_ERROR = "Отсутствует хэдер Location в ответе."


class FormMessages:
    ORIGINAL_LINK_LABEL = 'Длинная ссылка'
    REQUIRED = 'Обязательное поле'
    CUSTOM_ID_LABEL = 'Ваш вариант короткой ссылки'
    SHORT_SUBMIT = 'Добавить'
    FILES_LABEL = 'Выбрать файлы'
    FILES_SUBMIT = 'Загрузить'
