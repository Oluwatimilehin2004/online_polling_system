import datetime
from datetime import datetime, timedelta
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
        self.is_authenticated = False

    def register_user(self, hobbies, phone, national_id, dob, region, age):
        """
        Registers a user and adds the information into the database.
        Returns: 
            - True if registration AND OTP verification successful
            - False if registration failed or OTP verification failed
            - "EXISTING_USER" if user already exists
        """
        try:
            # 1️⃣ Check duplicates
            existing_user = self.db.fetch(
                "SELECT * FROM Users WHERE national_id=%s OR phone_number=%s",
                (national_id, phone)
            )
            if existing_user:
                print("User with this national ID or phone already exists!")
                return "EXISTING_USER"

            # 2️⃣ Verify inputs
            if not verify_hobbies(hobbies):
                return False

            # 3️⃣ Generate OTP
            otp = generate_otp()
            otp_created_at = datetime.now()

            # 4️⃣ Save user with OTP
            self.db.execute("""
                INSERT INTO Users (phone_number, national_id, date_of_birth, hobbie, otp, otp_created_at, region, age)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (phone, national_id, dob, hobbies, otp, otp_created_at, region, age))

            # 5️⃣ Send OTP
            send_otp(phone, otp)

            print("User registered! OTP sent to phone.")
            self.phone_number = phone
            
            # 6️⃣ IMMEDIATE OTP VERIFICATION - User must type OTP right after registration
            new_user_otp = input("Enter the OTP sent to you: ")
            if new_user_otp == otp:
                print("OTP Verified! Registration completed successfully!")
                self.is_authenticated = True
                return True
            else: 
                print("Invalid OTP! Registration failed.")
                return False
                
        except Exception as e:
            print(f"Registration error: {e}")
            return False

    def authenticate(self, phone):
        """
        Check if the user exists and verify OTP.
        Returns True if authenticated, False otherwise.
        """
        try:
            # 1️⃣ Fetch user by phone number
            user = self.db.fetch("SELECT * FROM Users WHERE phone_number=%s", (phone,))
            
            if not user:
                # User not found → needs registration
                return False
            
            user = user[0]  # fetch returns a list of dicts
            
            # 2️⃣ Check if OTP has expired (5 minutes)
            otp_time = user['otp_created_at']
            now = datetime.now()
            otp_expiry_time = otp_time + timedelta(minutes=5)
            
            if now > otp_expiry_time:
                print("OTP has expired! Generating new OTP...")
                # Generate new OTP
                new_otp = generate_otp()
                self.db.execute(
                    "UPDATE Users SET otp=%s, otp_created_at=%s WHERE phone_number=%s",
                    (new_otp, now, phone)
                )
                send_otp(phone, new_otp)
                print("New OTP sent to your phone!")
            
            # 3️⃣ Ask for OTP input
            otp_input = input("Enter the OTP sent to your phone: ")
            
            # 4️⃣ Verify OTP
            current_user = self.db.fetch("SELECT * FROM Users WHERE phone_number=%s", (phone,))[0]
            if otp_input == current_user['otp']:
                print("OTP verified successfully!")
                self.phone_number = phone
                self.is_authenticated = True
                return True
            else:
                print("Invalid OTP!")
                return False
                
        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    def resend_otp(self, phone):
        """Resend OTP to user"""
        try:
            new_otp = generate_otp()
            now = datetime.now()
            
            self.db.execute(
                "UPDATE Users SET otp=%s, otp_created_at=%s WHERE phone_number=%s",
                (new_otp, now, phone)
            )
            
            send_otp(phone, new_otp)
            print("New OTP sent to your phone!")
            return True
            
        except Exception as e:
            print(f"Error resending OTP: {e}")
            return False

    def view_profile(self, voter_id=None):
        try:
            if voter_id is None:
                if not self.phone_number:
                    print("No user information available.")
                    return
                rows = self.db.fetch("SELECT * FROM Users WHERE phone_number=%s", (self.phone_number,))
            else:
                rows = self.db.fetch("SELECT * FROM Users WHERE id=%s", (voter_id,))

            if not rows:
                print("Profile not found.")
                return
                
            profile = rows[0]
            print("\n--- Your Profile ---")
            print(f"Phone: {profile.get('phone_number', 'N/A')}")
            print(f"National ID: {profile.get('national_id', 'N/A')}")
            print(f"Date of Birth: {profile.get('date_of_birth', 'N/A')}")
            print(f"Hobbies: {profile.get('hobbies', 'N/A')}")
            print(f"Region: {profile.get('region', 'N/A')}")
            
        except Exception as e:
            print(f"Error viewing profile: {e}")

    def edit_region(self, new_region):
        try:
            if not self.phone_number:
                print("No phone number associated with this user.")
                return False
                
            self.db.execute("UPDATE Users SET region=%s WHERE phone_number=%s", (new_region, self.phone_number))
            self.region = new_region
            print("Region updated successfully!")
            return True
            
        except Exception as e:
            print(f"Error updating region: {e}")
            return False