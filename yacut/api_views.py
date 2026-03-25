from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.constants import InvalidMessages
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap


@app.route("/api/id/", methods=("POST",))
def create_short():
    """
    Создаёт сокращённую ссылку на основе переданного URL.
    """

    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(InvalidMessages.ERROR_NO_REQUEST_BODY)

    if "url" not in data:
        raise InvalidAPIUsage(
            InvalidMessages.ERROR_MISSING_REQUIRED_FIELD.format(field="url")
        )

    try:
        url_map = URLMap.create(
            original=data["url"], short=data.get("custom_id")
        )

        response_data = {
            "url": data["url"],
            "short_link": url_map.get_short_url(),
        }
        return jsonify(response_data), HTTPStatus.CREATED

    except ValueError as e:
        raise InvalidAPIUsage(str(e))
    except RuntimeError as e:
        raise InvalidAPIUsage(str(e), HTTPStatus.CONFLICT)


@app.route("/api/id/<short>/")
def get_url(short):
    if not (url_map := URLMap.get(short)):
        raise InvalidAPIUsage(
            InvalidMessages.ERROR_NO_FOUND_ID, HTTPStatus.NOT_FOUND
        )
    return jsonify({"url": url_map.original}), HTTPStatus.OK
