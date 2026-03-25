import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///db.sqlite3")
    SECRET_KEY = os.getenv("SECRET_KEY", "YOUR_SECRET_KEY")
    DISK_TOKEN = os.getenv("DISK_TOKEN")
    DISK_HOST = "https://cloud-api.yandex.net"
