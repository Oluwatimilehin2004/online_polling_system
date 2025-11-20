from database import Database

class Vote:
    def __init__(self):   # <-- FIXED
        self.db = Database()

    def cast_vote(self, voter_id, candidate_id):
        rows = self.db.fetch("SELECT has_voted FROM voters WHERE id=%s", (voter_id,))
        if not rows:
            print("Voter not found.")
            return

        has_voted = rows[0].get("has_voted")
        if has_voted:
            print("You have already voted!")
            return

        # record vote
        try:
            self.db.execute(
                "INSERT INTO voterecords (voter_id, candidate_id) VALUES (%s, %s)",
                (voter_id, candidate_id),
            )
        except Exception:
            pass

        # increment candidate votes
        self.db.execute(
            "UPDATE candidates SET vote_count = vote_count + 1 WHERE id = %s",
            (candidate_id,)
        )

        # mark has_voted = TRUE
        self.db.execute(
            "UPDATE voters SET has_voted = %s WHERE id = %s",
            (1, voter_id)
        )

        print("Vote recorded successfully!")

    def show_results(self, poll_id=None):
        if poll_id is None:
            results = self.db.fetch(
                "SELECT name, vote_count FROM candidates ORDER BY vote_count DESC"
            )
        else:
            results = self.db.fetch(
                "SELECT name, vote_count FROM candidates WHERE poll_id=%s ORDER BY vote_count DESC",
                (poll_id,)
            )

        print("\nResults:")
        for r in results:
            print(f"{r['name']} - {r.get('vote_count', 0)} votes")
