# from database import Database

# class Candidate:
#     def __init__(self):
#         self.db = Database()

#     def list_candidates(self):
#         candidates = self.db.fetch("SELECT * FROM candidates")
#         for c in candidates:
#             print(f"{c['id']}. {c['name']} ({c['vote_count']} votes)")
#         return candidates

#     def update_vote_count(self, candidate_id):
#         self.db.execute(
#             "UPDATE candidates SET vote_count = vote_count + 1 WHERE id = %s",
#             (candidate_id,)
#         )
#         print(f"Vote counted for candidate ID {candidate_id}!")


# if __name__ == "__main__":
#     c = Candidate()
#     print("Listing candidates:")
#     c.list_candidates()          
#     print("Updating vote for candidate ID 1")
#     c.update_vote_count(1)       


from database import Database

class Candidate:
    def __init__(self):
        self.db = Database()

    def list_candidates(self):
        candidates = self.db.fetch("SELECT * FROM Candidates")
        for c in candidates:
            print(f"{c['cand_id']}. {c['cand_name']})")
        return candidates
    
    def list_candidates_after_vote(self):
        candidates = self.db.fetch("SELECT * FROM Candidates")
        for c in candidates:
            print(f"{c['cand_id']}. {c['cand_name']} ({c['vote_count']} votes)")
        return candidates

    def update_vote_count(self, candidate_id):
        self.db.execute("UPDATE Candidates SET vote_count = vote_count + 1 WHERE id = %s", (candidate_id,))