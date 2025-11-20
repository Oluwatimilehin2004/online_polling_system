from user import User
from candidate import Candidate
from vote import Vote

def main():
    print("Welcome to the Voting App!")
    
    phone_number = input("Enter your phone_number: ")
    
    user = User()
    
    # Check if user already exists (authenticated)
    if not user.authenticate(phone_number):
        print("New user registration:")
        
        hobbie = input("Enter your hobbie: ")
        national_id = input("Enter your national ID: ")
        dob = input("Enter your date of birth (YYYY-MM-DD): ")
        
        # Register the user
        success = user.register_user(hobbie, phone_number, national_id, dob)
        
        if success:
            print("Registration successful! OTP sent to your phone_number.")
        else:
            print("Registration failed. Please try again or check your inputs.")
    else:
        print("User authenticated! You can proceed to vote.")


    while True:
        print("\nMain Menu")
        print("1. Cast your vote")
        print("2. View Notification")
        print("3. View Profile")
        print("4. Exit App")
        choice = input("Choose an option: ")

        if choice == "1":
            candidate = Candidate()
            candidates = candidate.list_candidates()
            choice = int(input("Enter candidate number: "))
            user_data = user.db.fetch("SELECT id, has_voted FROM voters WHERE phone_number = %s", (user.phone_number,))[0]

            if user_data.get('has_voted'):
                print("You have already voted.")
            else:
                vote = Vote()
                vote.cast_vote(user_data['id'], choice)

        elif choice == "2":
            print("\n--- Notifications ---")
            vote = Vote()
            vote.show_results()

        elif choice == "3":
            user.view_profile()
            edit = input("Do you want to edit your region? (y/n): ")
            if edit.lower() == "y":
                new_region = input("Enter new region: ")
                user.edit_region(new_region)

        elif choice == "4":
            print("Exiting app. Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()