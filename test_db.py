from database import Database

db = Database()
results = db.fetch("SELECT NOW() as current_time")
print(results)
