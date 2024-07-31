import mysql.connector

class Connection:

    def __init__(self) -> None:
        self.db = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="",
          database="absensi_wajah"
        )

    def cursor(self):
        return self.db.cursor(buffered=True)

    def commit(self):
        return self.db.commit()
