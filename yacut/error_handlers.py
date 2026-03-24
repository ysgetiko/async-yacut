from http import HTTPStatus

from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):

    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        super().__init__()
        self.message = message
        self.status_code = status_code

    # Метод для сериализации переданного сообщения об ошибке.
    def to_dict(self):
        return dict(message=self.message)


# Обработчик кастомного исключения для API.
@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    # Возвращает в ответе текст ошибки и статус-код.
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    return render_template("404.html"), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), HTTPStatus.INTERNAL_SERVER_ERROR
