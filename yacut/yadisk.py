import asyncio
from http import HTTPStatus
from typing import List, Optional
from urllib.parse import unquote

import aiohttp
from settings import Config

from . import app

DISK_URL = f"{Config.DISK_HOST}/v1/disk/resources/"
DISK_URL_UPLOAD = f"{DISK_URL}upload"
DISK_URL_DOWNLOAD = f"{DISK_URL}download"
FILE_EXISTS_MESSAGE = "Файл {} уже существует на диске"
AUTH_HEADERS = {"Authorization": f'OAuth {app.config["DISK_TOKEN"]}'}


async def async_upload_files_to_yadisk(
    files: Optional[List] = None,
) -> List[str]:

    if not files:
        raise ValueError("Список файлов не может быть пустым или None")

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(upload_file_and_get_url(session, file))
            for file in files
        ]
        try:
            urls = await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            raise RuntimeError(
                f"Ошибка при выполнении загрузки файлов: {e}"
            ) from e

        valid_urls = []
        for i, result in enumerate(urls):
            if isinstance(result, Exception):
                print(f"Ошибка загрузки файла {files[i].filename}: {result}")
            else:
                valid_urls.append(result)

        return valid_urls


async def upload_file_and_get_url(session: aiohttp.ClientSession, file) -> str:
    """
    Загружает файл на Яндекс Диск и возвращает публичную ссылку для скачивания.
    """
    try:
        # получаем URL для загрузки файла
        upload_url = await _get_upload_url(session, file.filename)

        # загружаем содержимое файла
        file_path = await _upload_file_content(session, upload_url, file)

        # получаем публичную ссылку для скачивания
        download_url = await _get_download_url(session, file_path)

        return download_url

    except aiohttp.ClientError as e:
        raise aiohttp.ClientError(f"HTTP error during file upload: {e}") from e
    except KeyError as e:
        raise ValueError(f"Unexpected response format: missing key {e}") from e


async def _get_upload_url(
    session: aiohttp.ClientSession, filename: str
) -> str:
    """Получает предопределённый URL для загрузки файла."""
    params = {"path": f"app:/{filename}", "fields": "href"}

    async with session.get(
        DISK_URL_UPLOAD, headers=AUTH_HEADERS, params=params
    ) as response:
        if response.status == HTTPStatus.CONFLICT:
            raise FileExistsError(FILE_EXISTS_MESSAGE.format(filename))
        response.raise_for_status()
        data = await response.json()
        return data["href"]


async def _upload_file_content(
    session: aiohttp.ClientSession, upload_url: str, file
) -> str:
    """Выполняет загрузку содержимого файла на указанный URL."""
    file_content = file.read()

    async with session.put(upload_url, data=file_content) as response:
        response.raise_for_status()
        location_header = response.headers.get("Location", "")
        if not location_header:
            raise ValueError("Missing 'Location' header in upload response")
        return unquote(location_header).replace("/disk", "")


async def _get_download_url(
    session: aiohttp.ClientSession, file_path: str
) -> str:
    """Получает публичную ссылку для скачивания файла."""
    params = {"path": file_path, "fields": "href"}

    async with session.get(
        DISK_URL_DOWNLOAD, headers=AUTH_HEADERS, params=params
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return data["href"]
