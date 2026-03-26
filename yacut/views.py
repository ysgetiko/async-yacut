from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.constants import REDIRECT_FOR_SHORT, InvalidMessages
from yacut.forms import UploadForm, URLMapForm
from yacut.models import URLMap
from yacut.yadisk import async_upload_files_to_yadisk


@app.route("/<short>", endpoint=REDIRECT_FOR_SHORT)
def short_url(short):
    if not (url_map := URLMap.get(short)):
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)


@app.route("/", methods=("GET", "POST"))
def short_url_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    try:
        url_map = URLMap.create(
            original=form.original_link.data,
            short=form.custom_id.data,
            skip_validation=True,
        )
        return render_template(
            "index.html",
            form=form,
            short=url_map.get_short_url(),
        )
    except (ValueError, RuntimeError) as e:
        # Откатываем транзакцию при ошибке
        flash(str(e))
        return render_template("index.html", form=form)


@app.route("/files", methods=("GET", "POST"))
async def upload_files_view():
    form = UploadForm()
    if not form.validate_on_submit():
        return render_template("download_files.html", form=form)

    try:
        # Загружаем файлы на Яндекс.Диск
        urls_for_upload_files = await async_upload_files_to_yadisk(
            form.files.data
        )
    except Exception as e:
        flash(str(e))
        return render_template("download_files.html", form=form)

    try:
        # Создаём короткие ссылки для каждого файла
        shorts_link_for_download = [
            {
                "filename": file.filename,
                "short": URLMap.create(original=original_link).get_short_url(),
            }
            for file, original_link in zip(
                form.files.data, urls_for_upload_files
            )
        ]
        return render_template(
            "download_files.html",
            form=form,
            short_for_download=shorts_link_for_download,
        )

    except (ValueError, RuntimeError) as e:
        flash(InvalidMessages.ERROR_UPLOAD.format(field=e))
        return render_template("download_files.html", form=form)
