import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="polluser",
            password="PollPass123",
            database="polling_system"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def fetch(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()
