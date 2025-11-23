import getpass
import os
import time
from vote import Vote
from user import User
from admin import Admin
from admin import Admin
from candidate import Candidate


def clear_screen():
    """Clear the terminal screen for better readability"""
    os.system('cls' if os.name == 'nt' else 'clear')

def delayed_clear_screen(delay_seconds):
    """Wait for specified seconds then clear screen"""
    time.sleep(delay_seconds)
    clear_screen()

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🗳️  {title:^52} 🗳️")
    print("="*60)

def print_success(message):
    """Print success messages in green"""
    print(f"\n✅ \033[92m{message}\033[0m")

def print_error(message):
    """Print error messages in red"""
    print(f"\n❌ \033[91m{message}\033[0m")

def print_info(message):
    """Print info messages in blue"""
    print(f"\nℹ️  \033[94m{message}\033[0m")

def loading_animation(message, duration=2):
    """Show a loading animation"""
    print(f"\n⏳ {message}", end="", flush=True)
    for _ in range(duration):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print()

def get_phone_number():
    """Get and validate phone number"""
    while True:
        phone_number = input("\n📱 Enter your phone number: ").strip()
        if phone_number and any(char.isdigit() for char in phone_number):
            return phone_number
        print_error("Please enter a valid phone number")

def register_new_user(user, phone_number):
    """Handle new user registration"""
    print_header("NEW USER REGISTRATION")
    print("\nLet's get you registered! Please provide the following details:")
    
    # Get registration details
    while True:
        hobbies = input("\n🎨 Enter your hobbies: ").strip()
        if hobbies:
            break
        print_error("Hobbies cannot be empty")

    while True:
        region = input("\n🎨 Enter your region: ").strip()
        if region:
            break
        print_error("Region cannot be empty")
    
    while True:
        national_id = input("\n🆔 Enter your national ID: ").strip()
        if national_id:
            break
        print_error("National ID cannot be empty")
    
    while True:
        dob = input("\n📅 Enter your date of birth (YYYY-MM-DD): ").strip()
        if dob:
            break
        print_error("Date of birth cannot be empty")

    while True:
        age = input("\n📅 Enter your age: ").strip()
        if dob:
            break
        print_error("Age cannot be empty")

    loading_animation("Checking your information")
    
    # Register the user
    result = user.register_user(hobbies, phone_number, national_id, dob, region, age, has_voted=False)
    
    if result == True:
        print_success("Registration successful! OTP has been sent to your phone.")
        return True
    elif result == "EXISTING_USER":
        print_info("It looks like you already have an account!")
        print("Please login with your existing account.")
        
        # Guide them to login
        login_choice = input("\nDo you want to login now? (y/n): ").lower()
        if login_choice == 'y':
            auth_success = authenticate_user(user, phone_number)
            if auth_success:
                print("Registration Sucessful!")
                return True
            else:
                print_error("Login failed. Please try again later.")
                return False
        else:
            print_info("You can try registration again with different information.")
            return False
    else:
        print_error("Registration failed. Please check your information and try again.")
        return False

def authenticate_user(user, phone_number):
    """Handle user authentication with OTP"""
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        success = user.authenticate(phone_number)
        
        if success:
            return True
        else:
            attempts += 1
            remaining_attempts = max_attempts - attempts
            if remaining_attempts > 0:
                print_error(f"Authentication failed. {remaining_attempts} attempts remaining.")
                retry = input("Do you want to try again? (y/n): ").lower()
                if retry != 'y':
                    break
                # Option to resend OTP
                resend = input("Do you want a new OTP? (y/n): ").lower()
                if resend == 'y':
                    user.resend_otp(phone_number)
            else:
                print_error("Maximum authentication attempts reached. Please try again later.")
                return False
    
    return False

def handle_voting(user):
    """Handle the voting process with voting period check"""
    clear_screen()
    print_header("CAST YOUR VOTE")
    
    # Check if voting is active for the default poll (poll_id=1)
    from admin import Admin
    admin_check = Admin()
    is_active, message = admin_check.is_voting_active(poll_id=1)
    
    if not is_active:
        print_error("Voting Period Information:")
        print_info(message)
        input("\nPress Enter to return to main menu...")
        return
    
    candidate = Candidate()
    candidates = candidate.list_candidates()
    
    if not candidates:
        print_error("No candidates available at the moment.")
        input("\nPress Enter to continue...")
        return
    
    # Check if user has already voted
    user_data = user.db.fetch("SELECT usr_id, has_voted FROM Users WHERE phone_number=%s", (user.phone_number,))
    if not user_data:
        print_error("User record not found.")
        input("\nPress Enter to continue...")
        return
        
    user_data = user_data[0]

    if user_data.get('has_voted'):
        print_error("You have already voted in this election.")
        print_info("Each voter can only cast one vote.")
        input("\nPress Enter to continue...")
    else:
        print("\nAvailable Candidates:")
        print("-" * 40)
        for i, candidate_info in enumerate(candidates, 1):
            print(f"{i}. {candidate_info['cand_name']} - {candidate_info['political_party']}")
        print("-" * 40)
        
        while True:
            try:
                vote_choice = int(input(f"\n👉 Enter candidate number (1-{len(candidates)}): "))
                if 1 <= vote_choice <= len(candidates):
                    break
                else:
                    print_error(f"Please enter a number between 1 and {len(candidates)}")
            except ValueError:
                print_error("Please enter a valid number")
        
        # Confirm vote
        selected_candidate = candidates[vote_choice-1]
        print(f"\nYou selected: {selected_candidate['cand_name']} - {selected_candidate['political_party']}")
        confirm = input("\nAre you sure you want to cast your vote? (y/n): ").lower()
        
        if confirm == 'y':
            loading_animation("Casting your vote")
            vote = Vote()
            vote.cast_vote(user_data['usr_id'], vote_choice)
            print_success("Your vote has been cast successfully! Thank you for participating.")
            print_info("You can view the results in the notifications section.")
            time.sleep(3)
        else:
            print_info("Vote cancelled. Returning to main menu.")
            time.sleep(1)

def main():
    clear_screen()
    print_header("WELCOME TO VOTEASY - SECURE VOTING PLATFORM")
    
    print("\n🌟 Welcome to Voteasy! Your voice matters! 🌟")
    print("\nPlease have your National ID ready for verification.")
    
    # Get phone number
    phone_number = get_phone_number()
    
    user = User()
    
    # First, check if user exists to determine the flow
    user_exists = user.db.fetch("SELECT * FROM Users WHERE phone_number=%s", (phone_number,))
    
    if not user_exists:
        # New user - go through registration flow
        print_info("New phone number detected. Registration required.")
        
        while True:
            registration_success = register_new_user(user, phone_number)
            
            if registration_success:
                break  # Registration and authentication successful
            else:
                retry = input("\nDo you want to try registration again? (y/n): ").lower()
                if retry != 'y':
                    print_error("Registration cancelled. Cannot access the application.")
                    return
    else:
        # Existing user - go directly to authentication
        print_success("Welcome back! Existing user detected.")
        auth_success = authenticate_user(user, phone_number)
        
        if not auth_success:
            print_error("Authentication failed. Cannot access the application.")
            return

    # Main application loop (only reached if authenticated)
    print_success("Authentication successful! Welcome to Voteasy!")
    time.sleep(1)

    while True:
        clear_screen()
        print_header("MAIN MENU")
        
        print("\nPlease choose an option:")
        print("1. 🗳️  Cast Your Vote")
        print("2. 📢 View Notifications & Results")
        print("3. 👤 View & Edit Profile")
        print("4. 🚪 Exit Application")
        print("5. 🔧 Admin Panel")
        
        choice = input("\n👉 Enter your choice (1-4): ").strip()

        if choice == "1":
            handle_voting(user)
            
        elif choice == "2":
            clear_screen()
            print_header("NOTIFICATIONS & RESULTS")
            
            vote = Vote()
            print("\n📊 Current Election Results:")
            print("=" * 50)
            vote.show_results()
            print("=" * 50)
            
            input("\nPress Enter to continue...")

        elif choice == "3":
            delayed_clear_screen(5)
            print_header("PROFILE MANAGEMENT")
            
            print("\n👤 Your Profile Information:")
            print("-" * 40)
            user.view_profile()
            print("-" * 40)
            
            print("\n📝 Edit Options:")
            print("1. Edit Region")
            print("2. Edit Age") 
            print("3. Back to Main Menu")
            
            edit_choice = input("\n👉 Choose an option (1-3): ").strip()
            
            if edit_choice == "1":
                new_region = input("📍 Enter new region: ").strip()
                if new_region:
                    loading_animation("Updating your region")
                    if user.edit_region(new_region):
                        print_success("Region updated successfully!")
                    else:
                        print_error("Failed to update region.")
                else:
                    print_error("Region cannot be empty")
                time.sleep(1)
                
            elif edit_choice == "2":
                new_age = input("🎂 Enter new age: ").strip()
                if new_age:
                    loading_animation("Updating your age")
                    if user.edit_age(new_age):
                        print_success("Age updated successfully!")
                    else:
                        print_error("Failed to update age. Please enter a valid positive number.")
                else:
                    print_error("Age cannot be empty")
                time.sleep(1)

            elif edit_choice == "3":
                print_info("Returning to main menu...")
                time.sleep(1)
            else:
                print_error("Invalid option. Returning to main menu.")
                time.sleep(1)
        
        elif choice == "4":
            clear_screen()
            print_header("THANK YOU FOR USING VOTEASY")
            print("\n🙏 Thank you for participating in our democratic process!")
            print("🌟 Your vote makes a difference!")
            print("\nExiting the application...")
            time.sleep(2)
            break

        elif choice == "5":
            admin = admin_login()
            if admin:
                admin_menu(admin)

        else:
            print_error("Invalid option. Please choose between 1-4.")
            time.sleep(1)
    

# Admin Interface
def admin_login():
    """Admin authentication"""
    clear_screen()
    print_header("ADMIN LOGIN")
    
    username = input("👤 Admin Username: ")
    password = getpass.getpass("🔒 Admin Password: ")
    
    admin = Admin()
    if admin.authenticate(username, password):
        print_success("Admin login successful!")
        return admin
    else:
        print_error("Invalid admin credentials!")
        return None

def admin_menu(admin):
    """Admin management interface"""
    while True:
        clear_screen()
        print_header("ADMIN PANEL")
        
        print("1. 📋 List All Polls")
        print("2. 📊 View Election Results") 
        print("3. 👥 List All Candidates")
        print("4. ➕ Add New Candidate")
        print("5. ✏️  Edit Candidate")
        print("6. 📝 Create New Poll")
        print("7. ⏰ Set/Extend Voting Period")
        print("8. 🚪 Exit Admin Panel")
        
        choice = input("\n👉 Choose an option (1-8): ").strip()
        
        if choice == "1":
            admin.list_polls()
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            poll_id = input("Enter Poll ID (or press Enter for all polls): ").strip()
            if poll_id:
                admin.view_results(int(poll_id))
            else:
                admin.view_results()
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            poll_id = input("Enter Poll ID to filter (or press Enter for all): ").strip()
            if poll_id:
                admin.list_candidates(int(poll_id))
            else:
                admin.list_candidates()
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            clear_screen()
            print_header("ADD NEW CANDIDATE")
            admin.list_polls()
            poll_id = input("\nEnter Poll ID: ") or 1
            name = input("Candidate Name: ")
            party = input("Political Party: ")
            region = input("Region: ")
            if admin.add_candidate(name, party, region, int(poll_id)):
                print_success("Candidate added successfully!")
            time.sleep(2)
            
        elif choice == "5":
            clear_screen()
            print_header("EDIT CANDIDATE")
            admin.list_candidates()
            try:
                cand_id = int(input("\nEnter Candidate ID to edit: "))
                new_name = input("New Name (press Enter to skip): ") or None
                new_party = input("New Party (press Enter to skip): ") or None
                new_region = input("New Region (press Enter to skip): ") or None
                
                if admin.edit_candidate(cand_id, new_name, new_party, new_region):
                    print_success("Candidate updated successfully!")
                else:
                    print_error("Failed to update candidate!")
            except ValueError:
                print_error("Invalid Candidate ID!")
            time.sleep(2)
            
        elif choice == "6":
            clear_screen()
            print_header("CREATE NEW POLL")
            poll_name = input("Poll Name: ")
            poll_desc = input("Poll Description: ")
            start_time = input("Start Time (YYYY-MM-DD HH:MM:SS): ")
            end_time = input("End Time (YYYY-MM-DD HH:MM:SS): ")
            if admin.create_poll(poll_name, poll_desc, start_time, end_time):
                print_success("Poll created successfully!")
            time.sleep(2)
            
        elif choice == "7":
            clear_screen()
            print_header("SET VOTING PERIOD")
            admin.list_polls()
            try:
                poll_id = int(input("\nEnter Poll ID: "))
                new_end_time = input("New End Time (YYYY-MM-DD HH:MM:SS): ")
                if admin.extend_voting_period(poll_id, new_end_time):
                    print_success("Voting period updated successfully!")
                else:
                    print_error("Failed to update voting period!")
            except ValueError:
                print_error("Invalid Poll ID!")
            time.sleep(2)
            
        elif choice == "8":
            print_info("Exiting admin panel...")
            break
            
        else:
            print_error("Invalid option!")
            time.sleep(1)

if __name__ == "__main__":
    main()