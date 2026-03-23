from http import HTTPStatus

from flask import abort, flash, redirect, render_template, request

from . import app
from .forms import UploadForm, URLMapForm
from .models import URLMap
from .yadisk import async_upload_files_to_yadisk


@app.route("/<short>")
def short_url(short):
    url_map = URLMap.get(short)
    if not url_map:
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
                short=form.custom_id.data if form.custom_id.data else None,
            ).get_short_url(),
        )
    except (ValueError, RuntimeError) as e:
        flash(str(e))
        return render_template("index.html", form=form)


@app.route("/files", methods=("GET", "POST"))
async def upload_files_view():
    form = UploadForm()
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                # Загружаем файлы на Яндекс.Диск
                uploaded_files_url = await async_upload_files_to_yadisk(
                    form.files.data
                )

                # Проверяем, что загрузка прошла успешно и есть URL
                if uploaded_files_url is None or not uploaded_files_url:
                    flash(
                        "Не удалось загрузить файлы на Яндекс.Диск.", "error"
                    )
                    return render_template("download_files.html", form=form)

                # Создаём короткие ссылки для каждого файла
                short_for_download = []
                for file, url in zip(form.files.data, uploaded_files_url):
                    try:
                        short_url = URLMap.create(original=url).get_short_url()
                        short_for_download.append(
                            {"filename": file.filename, "short": short_url}
                        )
                    except (ValueError, RuntimeError) as e:
                        flash(
                            "Ошибка создания короткой ссылки для "
                            f"{file.filename}: {str(e)}",
                            "error",
                        )
                        return render_template(
                            "download_files.html", form=form
                        )

                return render_template(
                    "download_files.html",
                    form=form,
                    short_for_download=short_for_download,
                )
            except FileExistsError as e:
                flash(str(e), "error")
                return render_template("download_files.html", form=form)
            except Exception as e:
                flash(
                    "Произошла ошибка при загрузке файлов: " f"{str(e)}",
                    "error",
                )
                return render_template("download_files.html", form=form)
        else:
            # Если валидация не пройдена, показываем форму с ошибками
            return render_template("download_files.html", form=form)
    else:
        # Для GET‑запроса просто показываем форму
        return render_template("download_files.html", form=form)
