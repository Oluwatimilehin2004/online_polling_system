import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="mysql-3755b811-alustudent-042b.f.aivencloud.com",
                user="avnadmin",
                password="AVNS_1Ig0usEEabFmtBB5Rog",
                database="Online_Polling_System",
                port=27197
                # ssl_ca="certs/ca.pem"  # Uncomment if using SSL
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("Connected to the database successfully!")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None
            self.cursor = None

    def fetch(self, query, vals=None):
        if self.cursor:
            self.cursor.execute(query, vals or ())
            return self.cursor.fetchall()
        return []

    def execute(self, query, vals=None):
        if self.cursor:
            self.cursor.execute(query, vals or ())
            self.conn.commit()
            return True
        return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
