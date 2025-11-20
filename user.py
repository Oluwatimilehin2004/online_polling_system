import datetime
from database import Database
from utils import *


class User:
    """User model compatible with the interactive flow."""

    def __init__(self, phone_number=None, region=None, age=None):
        self.db = Database()          # Database instance
        self.phone_number = phone_number
        self.region = region
        self.age = age
        self.id = None

    def register_user(self, phone, national_id, dob, hobbies):
        """
        Registers a user with OTP and checks for duplicates.
        """
        # 1️⃣ Check duplicates
        existing_user = self.db.fetch(
            "SELECT * FROM Users WHERE national_id=%s OR phone_number=%s",
            (national_id, phone)
        )
        if existing_user:
            print("User with this national ID or phone already exists!")
            return False

        # 2️⃣ Verify inputs
        # if not verify_dob(dob):
        #     return False
        # if not verify_national_id(self.db, national_id):
        #     return False
        if not verify_hobbies(hobbies):
            return False

        # 3️⃣ Generate OTP
        otp = generate_otp()
        otp_created_at = datetime.now()

        # 4️⃣ Save user with OTP
        self.db.execute("""
            INSERT INTO Users (full_name, phone_number, national_id, date_of_birth, hobbie, otp, otp_created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (phone, national_id, dob, hobbies, otp, otp_created_at))

        # 5️⃣ Send OTP
        send_otp(phone, otp)

        print("User registered! OTP sent to phone.")
        return True



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

    def authenticate(self, phone):
        """
        Check if the user exists and verify OTP.
        Returns True if authenticated, False otherwise.
        """
        # 1️⃣ Fetch user by phone number
        user = self.db.fetch("SELECT * FROM Users WHERE phone_number=%s", (phone,))
        
        if not user:
            # User not found → needs registration
            return False
        
        user = user[0]  # fetch returns a list of dicts
        
        # 2️⃣ Ask for OTP input
        otp_input = input("Enter the OTP sent to your phone: ")
        
        # 3️⃣ Check OTP validity (match and within time, e.g., 5 minutes)
        otp_sent = user['otp']
        otp_time = user['otp_created_at']
        now = datetime.now()
        
        # Check if OTP is within 5 minutes
        if otp_input == otp_sent and (now - otp_time).total_seconds() <= 300:
            print("OTP verified successfully!")
            return True
        else:
            print("Invalid or expired OTP!")
            return False


