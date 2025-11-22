from user import User
from candidate import Candidate
from vote import Vote
import os
import time

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
        dob = input("\n📅 Enter your age: ").strip()
        if dob:
            break
        print_error("Age cannot be empty")
    
    loading_animation("Checking your information")
    
    # Register the user
    result = user.register_user(hobbies, phone_number, national_id, dob, region, age)
    
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
    """Handle the voting process"""
    clear_screen()
    print_header("CAST YOUR VOTE")
    
    candidate = Candidate()
    candidates = candidate.list_candidates()
    
    if not candidates:
        print_error("No candidates available at the moment.")
        input("\nPress Enter to continue...")
        return
    
    # Check if user has already voted
    user_data = user.db.fetch("SELECT id, has_voted FROM Users WHERE phone_number=%s", (user.phone_number,))
    if not user_data:
        print_error("User data not found.")
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
            print(f"{i}. {candidate_info['name']} - {candidate_info['party']}")
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
        print(f"\nYou selected: {selected_candidate['name']} - {selected_candidate['party']}")
        confirm = input("\nAre you sure you want to cast your vote? (y/n): ").lower()
        
        if confirm == 'y':
            loading_animation("Casting your vote")
            vote = Vote()
            vote.cast_vote(user_data['id'], vote_choice)
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
            clear_screen()
            print_header("PROFILE MANAGEMENT")
            
            print("\n👤 Your Profile Information:")
            print("-" * 40)
            user.view_profile()
            print("-" * 40)
            
            edit = input("\n✏️  Do you want to edit your region? (y/n): ").lower()
            if edit == 'y':
                new_region = input("📍 Enter new region: ").strip()
                if new_region:
                    loading_animation("Updating your region")
                    user.edit_region(new_region)
                    print_success("Region updated successfully!")
                else:
                    print_error("Region cannot be empty")
                time.sleep(1)

        elif choice == "4":
            clear_screen()
            print_header("THANK YOU FOR USING VOTEASY")
            print("\n🙏 Thank you for participating in our democratic process!")
            print("🌟 Your vote makes a difference!")
            print("\nExiting the application...")
            time.sleep(2)
            break

        else:
            print_error("Invalid option. Please choose between 1-4.")
            time.sleep(1)

if __name__ == "__main__":
    main()