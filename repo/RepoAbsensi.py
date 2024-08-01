
from database.Connection import Connection


class RepoAbsensi:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection
    
    def range(self, start_date, end_date):
        cursor = self.connection.cursor()
        sql = """SELECT data_absensi.id, data_absensi.tanggal, CONCAT(data_karyawan.id, " - ", data_karyawan.nama_lengkap), data_absensi.absen_masuk, data_absensi.absen_pulang, data_absensi.status, data_absensi.jadwal_masuk
        FROM data_absensi JOIN data_karyawan ON data_karyawan.id = data_absensi.id_karyawan
        WHERE data_absensi.tanggal BETWEEN %s AND %s"""
        params = (start_date, end_date)
        cursor.execute(sql, params)
        results = cursor.fetchall()
        cursor.close()
        return results

    def all(self, search):
        cursor = self.connection.cursor()
        sql = """SELECT data_absensi.id, data_absensi.tanggal, CONCAT(data_karyawan.id, " - ", data_karyawan.nama_lengkap), data_absensi.absen_masuk, data_absensi.absen_pulang, data_absensi.status, data_absensi.jadwal_masuk
        FROM data_absensi JOIN data_karyawan ON data_karyawan.id = data_absensi.id_karyawan
        WHERE data_karyawan.nama_lengkap
        LIKE %s
        ORDER BY id DESC"""
        params = ("%{}%".format(search),)
        cursor.execute(sql, params)
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_absen(self, id_karyawan, tanggal):
        cursor = self.connection.cursor()
        sql = """SELECT * FROM data_absensi WHERE id_karyawan=%s AND tanggal=%s"""
        params = (id_karyawan, tanggal,)
        cursor.execute(sql, params)
        results = cursor.fetchone()
        return results

    def tambah(self, tanggal, id_karyawan, jam_masuk, jam_pulang, status):
        cursor = self.connection.cursor()
        sql = "INSERT INTO data_absensi (tanggal, id_karyawan, absen_masuk, absen_pulang, status) VALUES (%s, %s, %s, %s, %s)"
        params = (tanggal, id_karyawan, jam_masuk, jam_pulang, status)
        cursor.execute(sql, params)
        self.connection.commit()
        cursor.close()

    def hapus(self, id):
        cursor = self.connection.cursor()
        sql = "DELETE FROM data_absensi WHERE id=%s"
        params = (id,)
        cursor.execute(sql, params)
        self.connection.commit()
        cursor.close()

    def ubah(self, id, tanggal, id_karyawan, jam_masuk, jam_pulang, status):
        cursor = self.connection.cursor()
        sql = "UPDATE data_absensi SET tanggal=%s, id_karyawan=%s, absen_masuk=%s, absen_pulang=%s, status=%s WHERE id=%s" 
        params = (tanggal, id_karyawan, jam_masuk, jam_pulang, status, id,)
        cursor.execute(sql, params)
        self.connection.commit()
        cursor.close()
