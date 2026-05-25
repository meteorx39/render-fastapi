import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def get_db():
    connection = pymysql.connect(
        host = os.getenv("DB_HOST", "127.0.0.1"),
        port = int(os.getenv("DB_PORT", 4000)),
        user = os.getenv("DB_USER", "root"),
        password = os.getenv("DB_PASSWORD", ""),
        database = os.getenv("DB_NAME", ""),
        charset = "utf8mb4",
        cursorclass = pymysql.cursors.DictCursor,
        ssl = {"ca": None}
    )
    try:
        yield connection
    finally:
        connection.close()