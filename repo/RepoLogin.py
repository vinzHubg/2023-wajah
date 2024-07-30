
from database.Connection import Connection


class RepoLogin:

    def __init__(self, connection: Connection) -> None:
        self.db = connection.db

    def login(self, username, password):
        cursor = self.db.cursor()
        sql = "SELECT * FROM data_admin WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, password))
        results = cursor.fetchone()
        cursor.close()
        return results
