from database import Database
import getpass
from datetime import datetime

class Admin:
    def __init__(self):
        self.db = Database()
        self.is_authenticated = False

    def authenticate(self, username, password):
        """
        Simple admin authentication
        """
        if username == "admin" and password == "admin123":
            self.is_authenticated = True
            return True
        return False

    def create_poll(self, poll_name, poll_description, start_time, end_time):
        """Create a new poll with voting period"""
        if not self.is_authenticated:
            print("Admin authentication required!")
            return False

        try:
            self.db.execute(
                "INSERT INTO Polls (title, description, start_time, end_time, is_active) VALUES (%s, %s, %s, %s, %s)",
                (poll_name, poll_description, start_time, end_time, True)
            )
            print(f"Poll '{poll_name}' created successfully!")
            print(f"Voting period: {start_time} to {end_time}")
            return True
        except Exception as e:
            print(f"Error creating poll: {e}")
            return False

    def set_voting_period(self, poll_id, end_time):
        """Set or update voting end time for a poll"""
        if not self.is_authenticated:
            print("Admin authentication required!")
            return False

        try:
            self.db.execute(
                "UPDATE Polls SET end_time = %s WHERE poll_id = %s",
                (end_time, poll_id)
            )
            print(f"Voting end time updated to {end_time} for poll ID {poll_id}")
            return True
        except Exception as e:
            print(f"Error updating voting period: {e}")
            return False

    def extend_voting_period(self, poll_id, new_end_time):
        """Extend voting period for ongoing poll"""
        if not self.is_authenticated:
            print("Admin authentication required!")
            return False

        try:
            # Check if poll exists and get current end time
            poll = self.db.fetch("SELECT end_time FROM Polls WHERE poll_id = %s", (poll_id,))
            if not poll:
                print("Poll not found!")
                return False

            current_end = poll[0]['end_time']
            print(f"Current voting end time: {current_end}")
            print(f"New voting end time: {new_end_time}")

            self.db.execute(
                "UPDATE Polls SET end_time = %s WHERE poll_id = %s",
                (new_end_time, poll_id)
            )
            print(f"Voting period extended to {new_end_time}")
            return True
        except Exception as e:
            print(f"Error extending voting period: {e}")
            return False

    def add_candidate(self, candidate_name, political_party, region, poll_id=1):
        """Add candidate to specific poll"""
        if not self.is_authenticated:
            print("Admin authentication required!")
            return False

        try:
            # Check if poll exists and is active
            poll = self.db.fetch("SELECT * FROM Polls WHERE poll_id = %s", (poll_id,))
            if not poll:
                print(f"Poll ID {poll_id} not found!")
                return False

            self.db.execute(
                "INSERT INTO Candidates (cand_name, political_party, region, vote_count, poll_id) VALUES (%s, %s, %s, %s, %s)",
                (candidate_name, political_party, region, 0, poll_id)
            )
            print(f"Candidate '{candidate_name}' added to poll ID {poll_id} successfully!")
            return True
        except Exception as e:
            print(f"Error adding candidate: {e}")
            return False

    def edit_candidate(self, candidate_id, new_name=None, new_party=None, new_region=None):
        """Edit candidate details (cannot edit vote_count)"""
        if not self.is_authenticated:
            print("Admin authentication required!")
            return False

        try:
            updates = []
            params = []
            
            if new_name:
                updates.append("cand_name = %s")
                params.append(new_name)
            if new_party:
                updates.append("political_party = %s")
                params.append(new_party)
            if new_region:
                updates.append("region = %s")
                params.append(new_region)
                
            if not updates:
                print("No changes specified!")
                return False
                
            params.append(candidate_id)
            query = f"UPDATE Candidates SET {', '.join(updates)} WHERE cand_id = %s"
            
            self.db.execute(query, tuple(params))
            print(f"Candidate ID {candidate_id} updated successfully!")
            return True
        except Exception as e:
            print(f"Error editing candidate: {e}")
            return False

    def list_polls(self):
        """List all polls with their status"""
        polls = self.db.fetch("SELECT * FROM Polls ORDER BY poll_id DESC")
        print("\n ALL POLLS:")
        print("=" * 80)
        current_time = datetime.now()
        
        for poll in polls:
            poll_id = poll['poll_id']
            title = poll['title']
            start_time = poll['start_time']
            end_time = poll['end_time']
            is_active = poll.get('is_active', True)
            
            # Determine poll status
            if current_time < start_time:
                status = "🟡 UPCOMING"
            elif current_time <= end_time:
                status = "🟢 ACTIVE"
            else:
                status = "🔴 ENDED"
            
            print(f"ID: {poll_id} | {title} | {start_time} to {end_time} | {status}")
        print("=" * 80)
        return polls

    def list_candidates(self, poll_id=None):
        """List all candidates, optionally filtered by poll"""
        if poll_id:
            candidates = self.db.fetch(
                "SELECT * FROM Candidates WHERE poll_id = %s ORDER BY cand_id", 
                (poll_id,)
            )
            print(f"\n CANDIDATES FOR POLL ID {poll_id}:")
        else:
            candidates = self.db.fetch("SELECT * FROM Candidates ORDER BY poll_id, cand_id")
            print("\n ALL CANDIDATES:")
            
        print("=" * 70)
        for cand in candidates:
            print(f"ID: {cand['cand_id']} | Name: {cand['cand_name']} | Party: {cand['political_party']} | Region: {cand['region']} | Votes: {cand['vote_count']} | Poll: {cand['poll_id']}")
        print("=" * 70)
        return candidates

    def view_results(self, poll_id=None):
        """View election results for specific poll or all polls"""
        if poll_id:
            results = self.db.fetch(
                "SELECT cand_name, political_party, vote_count FROM Candidates WHERE poll_id = %s ORDER BY vote_count DESC",
                (poll_id,)
            )
            print(f"\n ELECTION RESULTS FOR POLL ID {poll_id}:")
        else:
            results = self.db.fetch(
                "SELECT c.cand_name, c.political_party, c.vote_count, p.title as poll_name FROM Candidates c JOIN Polls p ON c.poll_id = p.poll_id ORDER BY c.poll_id, c.vote_count DESC"
            )
            print("\n ELECTION RESULTS (All Polls):")
            
        print("=" * 60)
        for i, r in enumerate(results, 1):
            poll_info = f" | Poll: {r['poll_name']}" if 'poll_name' in r else ""
            print(f"{i}. {r['cand_name']} ({r['political_party']}) - {r.get('vote_count', 0)} votes{poll_info}")
        print("=" * 60)

    def is_voting_active(self, poll_id=1):
        """Check if voting is currently active for a poll"""
        try:
            current_time = datetime.now()
            poll = self.db.fetch(
                "SELECT start_time, end_time FROM Polls WHERE poll_id = %s", 
                (poll_id,)
            )
            
            if not poll:
                return False, "Poll not found!"
                
            start_time = poll[0]['start_time']
            end_time = poll[0]['end_time']
            
            if current_time < start_time:
                return False, f"Voting has not started yet. Starts at: {start_time}"
            elif current_time > end_time:
                return False, f"Voting period has ended. Ended at: {end_time}"
            else:
                return True, "Voting is active"
                
        except Exception as e:
            return False, f"Error checking voting status: {e}"