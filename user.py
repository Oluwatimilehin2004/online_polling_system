from database import db
import bcrypt

class User:
    def __init__(self, phone_number=None, region=None, age=None):
        self.phone_number = phone_number
        self.region = region
        self.age = age
        self.db = db

    def authenticate(self, phone_number):
        query = "SELECT * FROM users WHERE phone_number = %s"
        result = self.db.fetch(query, (phone_number,))
        return bool(result)

    def register(self):
        hashed_pin = bcrypt.hashpw("1234".encode(), bcrypt.gensalt())
        query = "INSERT INTO users (phone_number, region, age, pin, has_voted) VALUES (%s, %s, %s, %s, %s)"
        self.db.execute(query, (self.phone_number, self.region, self.age, hashed_pin, False))
        print("Registration successful!")

    def view_profile(self):
        profile = self.db.fetch("SELECT phone_number, region, age FROM users WHERE phone_number=%s", (self.phone_number,))[0]
        print("\n--- Profile ---")
        print(f"Phone: {profile['phone_number']}")
        print(f"Region: {profile['region']}")
        print(f"Age: {profile['age']}")

    def edit_region(self, new_region):
        self.db.execute("UPDATE users SET region=%s WHERE phone_number=%s", (new_region, self.phone_number))
        self.region = new_region
        print("Region updated!")
