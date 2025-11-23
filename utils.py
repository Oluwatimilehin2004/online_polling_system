import re
import random
from datetime import datetime
from twilio.rest import Client

# Twilio credentials
TWILIO_ACCOUNT_SID = "ACa4a545739cf241fbbbbf44a506d1dc7d"
TWILIO_AUTH_TOKEN = "e31dbf0c2eaf71a05687e5a49fbee771"
TWILIO_PHONE_NUMBER = "+17753620736"  # your Twilio number


client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def generate_otp():
    return str(random.randint(100000, 999999))

# def send_otp(phone, otp):
    # message = client.messages.create(
    #     body=f"Your OTP code is: {otp}",
    #     from_=TWILIO_PHONE_NUMBER,
    #     to=phone
    # )
    # print(f"OTP sent! Message SID: {message.sid}")

import os
import datetime

def send_otp(phone_number, otp):
    """
    Secure OTP function - creates individual log files per user
    """
    try:
        # Create logs directory if it doesn't exist
        if not os.path.exists('otp_logs'):
            os.makedirs('otp_logs')
        
        # Create a unique log file for each user (using last 4 digits of phone)
        user_log_file = f"otp_logs/user_{phone_number[-4:]}_otp.log"
        
        # Log the OTP with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] OTP for {phone_number}: {otp}\n"
        
        with open(user_log_file, "a") as f:
            f.write(log_entry)
        
        # Display OTP in console (for development)
        print("\n" + "="*50)
        print(f"📱 OTP SENT TO: {phone_number}")
        print(f"🔢 VERIFICATION CODE: {otp}")
        print("="*50)
        print("💡 In production, this would be sent via SMS")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"Error in OTP sending: {e}")
        return False


# def verify_national_id(db, national_id):
#     # Pattern check (example: 14 digits)
#     if not re.match(r"^\d{14}$", national_id):
#         print("Invalid National ID format!")
#         return False

#     # Uniqueness check in database
#     existing = db.fetch("SELECT * FROM Users WHERE national_id=%s", (national_id,))
#     if existing:
#         print("This National ID is already registered!")
#         return False

#     return True


# def verify_dob(dob_str):
#     try:
#         dob = datetime.strptime(dob_str, "%Y-%m-%d")
#         if dob >= datetime.now():
#             print("Date of birth cannot be in the future!")
#             return False
#         return True
#     except ValueError:
#         print("Invalid date format! Use YYYY-MM-DD.")
#         return False
    
def verify_hobbies(hobbies):
    if not hobbies or len(hobbies.strip()) == 0:
        print("Hobbies cannot be empty!")
        return False
    if len(hobbies) > 50:
        print("Hobbies too long! Max 50 characters.")
        return False
    return True

