#!/usr/bin/python3
import os
import sqlite3

try:
    import importlib
    mysql = importlib.import_module("pymysql")
except Exception:
    mysql = None


class Database:
    

    def __init__(self):
        self.backend = None
        self.conn = None
        self.cursor = None

        use_sqlite = os.getenv("USE_SQLITE", "0") == "1"

        if not use_sqlite and mysql is not None:
            try:
                self.conn = mysql.connector.connect(
                    host=os.getenv("DB_HOST", "mysql-3755b811-alustudent-042b.f.aivencloud.com"),
                    user=os.getenv("DB_USER", "avnadmin"),
                    password=os.getenv("DB_PASSWORD", "AVNS_1Ig0usEEabFmtBB5Rog"),
                    database=os.getenv("DB_NAME", "defaultdb"),
                    port=27197,
                    ssl_ca="certs/ca.pem",
                )
                self.cursor = self.conn.cursor(dictionary=True)
                self.backend = "mysql"
                print("✓ Connected to MySQL database.")
            except Exception as e:
                print("❌ Failed to connect to MySQL:", e)
                raise  # Stop here instead of falling back to SQLite

        if self.conn is None:
            local_db_path = os.path.join(os.path.dirname(__file__), "local.db")
            self.conn = sqlite3.connect(local_db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            self.backend = "sqlite"

    def __translate_query(self, query: str) -> str:
        if self.backend == "sqlite":
            return query.replace("%s", "?")
        return query

    def execute(self, query, values=None):
        q = self.__translate_query(query)
        vals = values or ()
        self.cursor.execute(q, vals)
        self.conn.commit()

    def fetch(self, query, values=None):
        q = self.__translate_query(query)
        vals = values or ()
        self.cursor.execute(q, vals)
        if self.backend == "mysql":
            return self.cursor.fetchall()
        rows = self.cursor.fetchall()
        return [dict(r) for r in rows]

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass