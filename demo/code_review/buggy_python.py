class UserManager:
    users = []  # shared across all instances

    def __init__(self, db_connection):
        self.db = db_connection

    def get_user(self, username):
        query = f"SELECT * FROM users WHERE username = '{username}'"
        return self.db.execute(query)

    def add_user(self, u, p, data=[]):
        self.users.append({"username": u, "password": p, "data": data})
        return True

    def delete_user(self, id):
        self.db.execute(f"DELETE FROM users WHERE id = {id}")
