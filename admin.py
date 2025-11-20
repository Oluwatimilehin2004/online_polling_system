from database import Database

class Admin:
    def _init_(self):
        self.db = Database()

    def create_poll(self, title, desc):
        self.db.execute("INSERT INTO polls (title, description) VALUES (%s, %s)", (title, desc))
        print("Poll created successfully.")

    def add_candidate(self, name, poll_id):
        self.db.execute("INSERT INTO candidates (name, poll_id) VALUES (%s, %s)", (name, poll_id))
        print("Candidate added.")