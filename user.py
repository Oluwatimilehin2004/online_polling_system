from database import Database
import hashlib

class User:
    def __init__(self):
        self.db = Database()

    def register(self, email, pin, region):
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
        self.db.execute("INSERT INTO voters (email, pin, region) VALUES (%s, %s, %s)", 
                        (email, hashed_pin, region))
        print("Registration successful!")

    def authenticate(self, email, pin):
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
        voter = self.db.fetch("SELECT * FROM voters WHERE email=%s AND pin=%s", (email, hashed_pin))
        if voter:
            print("Authentication successful.")
            return voter[0]
        print("Invalid credentials.")
        return None

    def view_profile(self, voter_id):
        profile = self.db.fetch("SELECT * FROM voters WHERE id=%s", (voter_id,))
        print(profile[0])

    def edit_region(self, voter_id, new_region):
        self.db.execute("UPDATE voters SET region=%s WHERE id=%s", (new_region, voter_id))
        print("Region updated successfully!")
