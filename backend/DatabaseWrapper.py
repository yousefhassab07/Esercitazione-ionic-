import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseWrapper:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.port = int(os.getenv('DB_PORT', 16366))
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.db_name = os.getenv('DB_NAME')
        self.cursor_class = pymysql.cursors.DictCursor

    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db_name,
            cursorclass=self.cursor_class,
            autocommit=True
        )
    # ... resto del codice uguale ...
