### Как запустить проект Yacut:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ysgetiko/async-yacut.git

cd async-yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать в директории проекта файл .env с четыремя переменными окружения:

```
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key
DB=sqlite:///db.sqlite3
```

Создать базу данных и применить миграции:

```
flask db upgrade
```

Запустить проект:

```
flask run
```
## Эндпоинты
[http://127.0.0.1:5000/](http://127.0.0.1:5000/) - создание короткой ссылки

[http://127.0.0.1:5000/files/](http://127.0.0.1:5000/files/) - загрузка файлов на диск

### API
POST [http://127.0.0.1:5000/api/id/](http://127.0.0.1:5000/api/id/) - создание короткой ссылки


GET [http://127.0.0.1:5000/api/id/<short>/](http://127.0.0.1:5000/api/id/<short>/) - получение оригинальной ссылки

### API Docs (Swagger): http://localhost/api/docs/

## Технологии

* **Python**
* **Flask**
* **SQLAlchemy**
* **asyncio**/**aiohttp**
* **Яндекс.Диск REST API**

### Контакты
Автор: Евгений Гетиков

Email: zenia777@yandex.ru

Репозиторий: [https://github.com/ysgetiko](https://github.com/ysgetiko)