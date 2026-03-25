from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from yacut import app
from yacut.constants import InvalidMessages
from yacut.forms import UploadForm, URLMapForm
from yacut.models import URLMap
from yacut.yadisk import async_upload_files_to_yadisk


@app.route("/<short>")
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
        return render_template(
            "index.html",
            form=form,
            short=URLMap.create(
                original=form.original_link.data,
                short=form.custom_id.data,
            ).get_short_url(),
        )
    except (ValueError, RuntimeError) as e:
        flash(str(e))
        return render_template("index.html", form=form)


@app.route("/files", methods=("GET", "POST"))
async def upload_files_view():
    form = UploadForm()
    if not form.validate_on_submit():
        return render_template("download_files.html", form=form)
    try:
        try:
            # Загружаем файлы на Яндекс.Диск
            uploaded_files_url = await async_upload_files_to_yadisk(
                form.files.data
            )
        except FileExistsError as e:
            flash(str(e), "error")
            return render_template("download_files.html", form=form)

        # Создаём короткие ссылки для каждого файла
        short_for_download = [
            {
                "filename": file.filename,
                "short": URLMap.create(original=original_link).get_short_url(),
            }
            for file, original_link in zip(form.files.data, uploaded_files_url)
        ]
        return render_template(
            "download_files.html",
            form=form,
            short_for_download=short_for_download,
        )

    except Exception:
        flash(
            InvalidMessages.ERROR_UPLOAD,
            "error",
        )
        return render_template("download_files.html", form=form)
