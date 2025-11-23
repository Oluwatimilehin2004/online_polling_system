from database import Database

class Vote:
    def __init__(self):
        self.db = Database()

    def cast_vote(self, user_id, candidate_id):
        # FIXED: Check Users table for has_voted
        rows = self.db.fetch("SELECT has_voted FROM Users WHERE usr_id=%s", (user_id,))
        if not rows:
            print("User not found.")
            return

        has_voted = rows[0].get("has_voted")
        if has_voted:
            print("You have already voted!")
            return

        # record vote
        try:
            self.db.execute(
                "INSERT INTO Vote_records (usr_id, cand_id) VALUES (%s, %s)",
                (user_id, candidate_id),
            )
        except Exception as e:
            print(f"Error recording vote: {e}")
            return

        # DEBUG: Check current vote count before update
        current_count = self.db.fetch("SELECT vote_count FROM Candidates WHERE cand_id=%s", (candidate_id,))
        if current_count:
            print(f"DEBUG: Current vote count for candidate {candidate_id}: {current_count[0]['vote_count']}")

        # increment candidate votes - FIXED: Ensure it increments by 1
        result = self.db.execute(
            "UPDATE Candidates SET vote_count = vote_count + 1 WHERE cand_id = %s",
            (candidate_id,)
        )
        
        if not result:
            print("Error: Failed to update candidate vote count")
            return

        # DEBUG: Check vote count after update
        updated_count = self.db.fetch("SELECT vote_count FROM Candidates WHERE cand_id=%s", (candidate_id,))
        if updated_count:
            print(f"DEBUG: Updated vote count for candidate {candidate_id}: {updated_count[0]['vote_count']}")

        # mark has_voted = TRUE in Users table
        self.db.execute(
            "UPDATE Users SET has_voted = %s WHERE usr_id = %s",
            (1, user_id)
        )

        print("Vote recorded successfully!")

    def show_results(self):
        # Get results from Candidates table
        results = self.db.fetch(
            "SELECT cand_name, political_party, vote_count FROM Candidates ORDER BY vote_count DESC"
        )

        print("\n📊 ELECTION RESULTS:")
        print("=" * 50)
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['cand_name']} ({r['political_party']}) - {r.get('vote_count', 0)} votes")
        print("=" * 50)