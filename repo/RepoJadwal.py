from database.Connection import Connection
from datetime import datetime


class RepoJadwal:
    def __init__(self, connection: Connection) -> None:
        self.db = connection.db

    def all(self, search):
        cursor = self.db.cursor()
        sql = "SELECT * FROM data_jadwal WHERE jam_masuk LIKE %s OR jam_pulang LIKE %s"
        params = ("%{}%".format(search),"%{}%".format(search),)
        cursor.execute(sql, params)
        results = cursor.fetchall()
        cursor.close()
        return results

    def tambah(self, jam_masuk_str, jam_pulang_str):

        jam_masuk = datetime.strptime(jam_masuk_str.replace(".", ":"), '%H:%M').time()
        jam_pulang = datetime.strptime(jam_pulang_str.replace(".", ":"), '%H:%M').time()

        cursor = self.db.cursor()
        sql = "INSERT INTO data_jadwal (jam_masuk, jam_pulang) VALUES (%s, %s)"
        params = (jam_masuk, jam_pulang,)
        cursor.execute(sql, params)
        self.db.commit()
        cursor.close()

    def hapus(self, id):
        cursor = self.db.cursor()
        sql = "DELETE FROM data_jadwal WHERE id=%s"
        params = (id,)
        cursor.execute(sql, params)
        self.db.commit()
        cursor.close()

    def ubah(self, id, jam_masuk_str, jam_pulang_str):

        jam_masuk = datetime.strptime(jam_masuk_str.replace(".", ":"), '%H:%M').time()
        jam_pulang = datetime.strptime(jam_pulang_str.replace(".", ":"), '%H:%M').time()

        cursor = self.db.cursor()
        sql = "UPDATE data_jadwal SET jam_masuk=%s, jam_pulang=%s WHERE id=%s" 

        params = (jam_masuk, jam_pulang, id,)
        cursor.execute(sql, params)
        self.db.commit()
        cursor.close()
