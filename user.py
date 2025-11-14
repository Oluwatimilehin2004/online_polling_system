from database import Database
class user:
    """User model compatible with the interactive `main.py` flow.

    Usage patterns supported:
    - user = User(); user.authenticate(phone_number)
    - user = User(phone_number, region, age); user.register()
    """

    def __init__(self, phone_number=None, region=None, age=None):
        self.db = Database()
        self.phone_number = phone_number
        self.region = region
        self.age = age
        self.id = None

    def register(self):
        if not self.phone_number:
            raise ValueError("phone_number is required to register")

        # Create a voter record. has_voted defaults to 0
        self.db.execute(
            "INSERT INTO voters (phone_number, region, age, has_voted) VALUES (%s, %s, %s, 0)",
            (self.phone_number, self.region, self.age),
        )
        # retrieve id
        row = self.db.fetch("SELECT id FROM voters WHERE phone_number=%s", (self.phone_number,))
        if row:
            self.id = row[0].get("id")
        print("Registration successful!")

    def authenticate(self, phone_number):
        """Find a voter by phone_number. If found, populate self and return the voter dict; else return None."""
        voter = self.db.fetch("SELECT * FROM voters WHERE phone_number=%s", (phone_number,))
        if voter:
            v = voter[0]
            self.phone_number = v.get("phone_number")
            self.region = v.get("region")
            self.age = v.get("age")
            self.id = v.get("id")
            print("Authentication successful.")
            return v
        return None

    def view_profile(self, voter_id=None):
        if voter_id is None:
            if not self.phone_number:
                print("No user information available.")
                return
            rows = self.db.fetch("SELECT * FROM voters WHERE phone_number=%s", (self.phone_number,))
        else:
            rows = self.db.fetch("SELECT * FROM voters WHERE id=%s", (voter_id,))

        if not rows:
            print("Profile not found.")
            return
        profile = rows[0]
        print(profile)

    def edit_region(self, new_region):
        if not self.phone_number:
            print("No phone number associated with this user.")
            return
        self.db.execute("UPDATE voters SET region=%s WHERE phone_number=%s", (new_region, self.phone_number))
        self.region = new_region
        print("Region updated successfully!")

