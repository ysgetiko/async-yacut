from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.constants import InvalidMessages
from yacut.forms import UploadForm, URLMapForm
from yacut.models import URLMap
from yacut.yadisk import async_upload_files_to_yadisk


@app.route("/<short>", endpoint="short_url")
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
        db.session.commit()
        return render_template(
            "index.html",
            form=form,
            short=url_map.get_short_url(),
        )
    except (ValueError, RuntimeError) as e:
        # Откатываем транзакцию при ошибке
        db.session.rollback()
        flash(str(e))
        return render_template("index.html", form=form)


@app.route("/files", methods=("GET", "POST"))
async def upload_files_view():
    form = UploadForm()
    if not form.validate_on_submit():
        return render_template("download_files.html", form=form)

    try:
        # Загружаем файлы на Яндекс.Диск
        uploaded_files_url = await async_upload_files_to_yadisk(
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
                "short": URLMap.create(
                    original=original_link, skip_validation=True
                ).get_short_url(),
            }
            for file, original_link in zip(form.files.data, uploaded_files_url)
        ]
        db.session.commit()
        return render_template(
            "download_files.html",
            form=form,
            short_for_download=shorts_link_for_download,
        )

    except (ValueError, RuntimeError) as e:
        flash(InvalidMessages.ERROR_UPLOAD.format(field=e))
        return render_template("download_files.html", form=form)
