from http import HTTPStatus

from flask import jsonify, request

from yacut import app

from .error_handlers import InvalidAPIUsage
from .models import URLMap


def _validate_request_data(request_obj) -> dict:
    """
    Валидирует входящие данные запроса.
    """
    data = request_obj.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")

    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    return data


@app.route("/api/id/", methods=("POST",))
def create_short():
    """
    Создаёт сокращённую ссылку на основе переданного URL.
    """

    data = _validate_request_data(request)
    original_url = data["url"]
    custom_id = data.get("custom_id")
    try:
        url_map = URLMap.create(original=original_url, short=custom_id)
        short_link = url_map.get_short_url()

        response_data = {"url": original_url, "short_link": short_link}
        return jsonify(response_data), HTTPStatus.CREATED

    except ValueError as e:
        raise InvalidAPIUsage(str(e))
    except RuntimeError as e:
        raise InvalidAPIUsage(str(e), HTTPStatus.CONFLICT)


@app.route("/api/id/<short>/")
def get_url(short):
    if not (url_map := URLMap.get(short)):
        raise InvalidAPIUsage("Указанный id не найден", HTTPStatus.NOT_FOUND)
    return jsonify({"url": url_map.original}), HTTPStatus.OK
