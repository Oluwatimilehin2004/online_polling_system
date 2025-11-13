#!/usr/bin/python3
import pymysql as mysql

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = "mysql-3755b811-alustudent-042b.f.aivencloud.com",
            user = "root",
            password = "yourpassword",
            database = "Online_Polling_System"
        )
        self.cursor = self.conn.cursor(dictionary= True)

    def execute(self, query, values=None):
        self.cursor.execute(query, values or ())                                                                                    
        self.conn.commit()

    def fetch(self, query, values=None):
        self.cursor.execute(query, values or ())
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()
