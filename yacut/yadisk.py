import asyncio
from http import HTTPStatus
from typing import List, Optional
from urllib.parse import unquote

import aiohttp
from settings import Config

from yacut import app
from yacut.constants import InvalidMessages

DISK_URL = f"{Config.DISK_HOST}/v1/disk/resources/"
DISK_URL_UPLOAD = f"{DISK_URL}upload"
DISK_URL_DOWNLOAD = f"{DISK_URL}download"
AUTH_HEADERS = {"Authorization": f'OAuth {app.config["DISK_TOKEN"]}'}


async def async_upload_files_to_yadisk(files: Optional[List]):

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(upload_file_and_get_url(session, file))
            for file in files
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)


async def upload_file_and_get_url(session: aiohttp.ClientSession, file) -> str:
    """
    Загружает файл на Яндекс Диск и возвращает публичную ссылку для скачивания.
    """

    # получаем URL для загрузки файла
    upload_url = await _get_upload_url(session, file.filename)

    # загружаем содержимое файла
    file_path = await _upload_file_content(session, upload_url, file)

    return await _get_download_url(session, file_path)


async def _get_upload_url(
    session: aiohttp.ClientSession, filename: str
) -> str:
    """Получает предопределённый URL для загрузки файла."""

    async with session.get(
        DISK_URL_UPLOAD,
        headers=AUTH_HEADERS,
        params={"path": f"app:/{filename}", "fields": "href"},
    ) as response:
        if response.status == HTTPStatus.CONFLICT:
            raise FileExistsError(
                InvalidMessages.FILE_EXISTS_MESSAGE.format(field=filename)
            )
        response.raise_for_status()
        return (await response.json())["href"]


async def _upload_file_content(
    session: aiohttp.ClientSession, upload_url: str, file
) -> str:
    """Выполняет загрузку содержимого файла на указанный URL."""

    async with session.put(upload_url, data=file.read()) as response:
        response.raise_for_status()
        location_header = response.headers.get("Location")
        if not location_header:
            raise ValueError(InvalidMessages.MISSING_HEADER)
        return unquote(location_header).replace("/disk", "")


async def _get_download_url(
    session: aiohttp.ClientSession, file_path: str
) -> str:
    """Получает публичную ссылку для скачивания файла."""

    async with session.get(
        DISK_URL_DOWNLOAD,
        headers=AUTH_HEADERS,
        params={"path": file_path, "fields": "href"},
    ) as response:
        response.raise_for_status()
        return (await response.json())["href"]
