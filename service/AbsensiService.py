class AbsensiService:

    def __init__(self, repo) -> None:
        self.repo = repo

    def absen(self, tanggal, id_karyawan, jam_masuk, jam_pulang, status):
        self.cek_sudah_absen(id_karyawan, tanggal)
        self.repo.tambah(tanggal, id_karyawan, jam_masuk, jam_pulang, status)

    def cek_sudah_absen(self, id_karyawan, tanggal):
        absen = self.repo.get_absen(id_karyawan, tanggal)
        if absen:
            raise AbsensiServiceException("Sudah melakukan absensi, silahkan gunakan menu edit, jika ingin merubah data")


class AbsensiServiceException(Exception):
    pass
