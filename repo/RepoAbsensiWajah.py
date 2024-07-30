from database.Connection import Connection


class RepoAbsensiWajah:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def get_absen(self, id_karyawan, tanggal):
        cursor = self.connection.cursor()
        sql = """SELECT * FROM data_absensi WHERE id_karyawan=%s AND tanggal=%s"""
        params = (
            id_karyawan,
            tanggal,
        )
        cursor.execute(sql, params)
        results = cursor.fetchone()
        return results

    def get_jadwal(self):
        cursor = self.connection.cursor()
        sql = """SELECT jam_masuk, jam_pulang FROM data_jadwal LIMIT 1"""
        cursor.execute(sql)
        results = cursor.fetchone()
        return results

    def absen(self, tanggal, id_karyawan, jam_masuk, jam_pulang, status):
        cursor = self.connection.cursor()
        sql = "INSERT INTO data_absensi (tanggal, id_karyawan, absen_masuk, absen_pulang, status) VALUES (%s, %s, %s, %s, %s)"
        params = (tanggal, id_karyawan, jam_masuk, jam_pulang, status)
        cursor.execute(sql, params)
        self.connection.commit()
        cursor.close()

    def absen_pulang(self, tanggal, id_karyawan, jam_pulang):
        cursor = self.connection.cursor()
        sql = "UPDATE data_absensi SET absen_pulang=%s WHERE tanggal=%s AND id_karyawan=%s"
        params = (jam_pulang, tanggal, id_karyawan)
        cursor.execute(sql, params)
        self.connection.commit()
        cursor.close()
