
from database.Connection import Connection


class RepoKaryawan:
    def __init__(self, connection: Connection) -> None:
        self.db = connection.db

    def all(self, search):
        cursor = self.db.cursor()
        sql = "SELECT * FROM data_karyawan WHERE nama_lengkap LIKE %s"
        params = ("%{}%".format(search),)
        cursor.execute(sql, params)
        results = cursor.fetchall()
        cursor.close()
        return results

    def tambah(self, nama_lengkap, jenis_kelamin, no_telepon, alamat):
        cursor = self.db.cursor()
        sql = "INSERT INTO data_karyawan (nama_lengkap, jenis_kelamin, no_telepon, alamat) VALUES (%s, %s, %s, %s)"
        params = (nama_lengkap, jenis_kelamin, no_telepon, alamat,)
        cursor.execute(sql, params)
        self.db.commit()
        cursor.close()

    def hapus(self, id):
        cursor = self.db.cursor()
        sql = "DELETE FROM data_karyawan WHERE id=%s"
        params = (id,)
        cursor.execute(sql, params)
        self.db.commit()
        cursor.close()

    def ubah(self, id, nama_lengkap, jenis_kelamin, no_telepon, alamat):
        cursor = self.db.cursor()
        sql = "UPDATE data_karyawan SET nama_lengkap=%s, jenis_kelamin=%s, no_telepon=%s, alamat=%s WHERE id=%s" 
        params = (nama_lengkap, jenis_kelamin, no_telepon, alamat, id, )
        cursor.execute(sql, params)
        self.db.commit()
        cursor.close()
