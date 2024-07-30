from database.Connection import Connection
from repo.RepoAbsensiWajah import RepoAbsensiWajah
import datetime


class Absen:
    def __init__(self, absen) -> None:
        self.absen = absen

    def belum_absen_masuk(self):
        return self.absen is None

    def belum_absen_pulang(self):
        return not self.absen[4]

"""
Kelas AbsensiWajahService digunakan untuk menyediakan layanan absensi berbasis wajah untuk aplikasi. Kelas ini digunakan untuk mengelola aktivitas absensi seperti absen masuk, absen pulang, dan mengecek status absensi.
ABSEN_MASUK_BERHASIL, ABSEN_PULANG_BERHASIL, SUDAH_ABSEN, ABSEN_MASUK_TERLAMBAT_BERHASIL adalah konstanta yang digunakan untuk memberikan informasi kembali ke aplikasi tentang hasil dari aktivitas absensi.
def __init__(self, repo) -> None: adalah konstruktor dari kelas ini yang digunakan untuk menginisialisasi objek kelas. Parameter repo digunakan untuk menyediakan akses ke objek repository yang digunakan untuk mengakses data absensi dari aplikasi.
self.repo = repo digunakan untuk menyimpan referensi objek repository yang diterima dari konstruktor ke dalam atribut kelas.
"""
class AbsensiWajahService:
    ABSEN_MASUK_BERHASIL = 1
    ABSEN_PULANG_BERHASIL = 2
    SUDAH_ABSEN = 3
    ABSEN_MASUK_TERLAMBAT_BERHASIL = 4

    def __init__(self, repo) -> None:
        self.repo = repo

    """
    untuk mengelola aktivitas absensi berdasarkan tanggal dan id_karyawan yang diterima.
    self.tanggal = tanggal dan self.id_karyawan = id_karyawan digunakan untuk menyimpan tanggal dan id_karyawan yang diterima dari parameter ke dalam atribut kelas.
    absen = Absen(absen=self.repo.get_absen(id_karyawan, tanggal)) digunakan untuk mengambil data absensi dari objek repository dan menyimpannya dalam objek Absen.
    if absen.belum_absen_masuk(): digunakan untuk mengecek apakah karyawan belum melakukan absen masuk pada tanggal yang ditentukan.
    return self.absen_masuk() digunakan untuk mengeksekusi metode absen_masuk() jika karyawan belum melakukan absen masuk.
    elif absen.belum_absen_pulang(): digunakan untuk mengecek apakah karyawan belum melakukan absen pulang pada tanggal yang ditentukan.
    return self.absen_pulang() digunakan untuk mengeksekusi metode absen_pulang() jika karyawan belum melakukan absen pulang.
    raise AbsensiWajahServiceException("Sudah melakukan absen masuk dan pulang") digunakan untuk melemparkan exception jika karyawan sudah melakukan absen masuk dan pulang pada tanggal yang ditentukan.
    Metode absen_masuk() dan absen_pulang() akan ditangani oleh kelas ini atau kelas turunannya, yang akan mengeksekusi aktivitas absen masuk dan pulang sesuai dengan logika yang ditentukan.
    """
    def absen(self, tanggal, id_karyawan):
        self.tanggal = tanggal
        self.id_karyawan = id_karyawan

        absen = Absen(absen=self.repo.get_absen(id_karyawan, tanggal))
        if absen.belum_absen_masuk():
            return self.absen_masuk()
        elif absen.belum_absen_pulang():
            return self.absen_pulang()
        raise AbsensiWajahServiceException("Sudah melakukan absen masuk dan pulang")

    """
    digunakan untuk mengeksekusi aktivitas absen masuk.
    jam_masuk = datetime.datetime.now().time() digunakan untuk mengambil jam saat ini sebagai jam absen masuk.
    jadwal = self.get_jadwal_masuk() digunakan untuk mengambil jadwal masuk dari karyawan yang bersangkutan.
    if jam_masuk > jadwal: digunakan untuk memeriksa apakah karyawan terlambat dari jadwal masuk yang ditentukan.
    status = "Terlambat" digunakan untuk memberikan status "Terlambat" jika karyawan terlambat dari jadwal masuk.
    status = "Hadir" digunakan untuk memberikan status "Hadir" jika karyawan tidak terlambat dari jadwal masuk.
    self.repo.absen(self.tanggal, self.id_karyawan, "{}:{}".format(jam_masuk.hour, jam_masuk.minute), "00:00", status) digunakan untuk menyimpan data absen masuk ke repository.
    if status == "Terlambat": digunakan untuk memeriksa apakah karyawan terlambat dari jadwal masuk.
    return self.ABSEN_MASUK_TERLAMBAT_BERHASIL digunakan untuk mengembalikan konstanta ABSEN_MASUK_TERLAMBAT_BERHASIL jika karyawan terlambat dari jadwal masuk.
    return self.ABSEN_PULANG_BERHASIL digunakan untuk mengembalikan konstanta ABSEN_PULANG_BERHASIL jika karyawan tidak terlambat dari jadwal masuk.
    Metode ini akan menyimpan data absen masuk dan mengembalikan konstanta yang sesuai dengan hasil absen masuk yang dilakukan.
    """
    def absen_masuk(self):
        jam_masuk = datetime.datetime.now().time()
        jadwal = self.get_jadwal_masuk()
        if jam_masuk > jadwal:
            status = "Terlambat"
        else:
            status = "Hadir"
        self.repo.absen(
            self.tanggal,
            self.id_karyawan,
            "{}:{}".format(jam_masuk.hour, jam_masuk.minute),
            "00:00",
            status,
        )
        if status == "Terlambat":
            return self.ABSEN_MASUK_TERLAMBAT_BERHASIL
        return self.ABSEN_PULANG_BERHASIL

    """
    digunakan untuk mengambil jadwal masuk dari karyawan yang bersangkutan.
    jadwal = self.repo.get_jadwal() digunakan untuk mengambil jadwal masuk dari repository.
    td = jadwal[0] digunakan untuk mengambil jadwal dari hasil yang diterima dari repository.
    days, hours, minutes = td.days, td.seconds // 3600, td.seconds // 60 % 60 digunakan untuk mengkonversi jadwal yang diterima dari repository dari format timedelta menjadi format jam, menit.
    return datetime.time(hours, minutes, 0) digunakan untuk mengubah format jam, menit menjadi format waktu yang dapat digunakan.
    Metode ini akan mengembalikan jadwal masuk dari karyawan yang bersangkutan dalam format waktu yang dapat digunakan.
    """
    def get_jadwal_masuk(self):
        jadwal = self.repo.get_jadwal()
        td = jadwal[0]
        days, hours, minutes = td.days, td.seconds // 3600, td.seconds // 60 % 60
        return datetime.time(hours, minutes, 0)

    """
    digunakan untuk mengambil jadwal pulang dari karyawan yang bersangkutan.
    jadwal = self.repo.get_jadwal() digunakan untuk mengambil jadwal pulang dari repository.
    td = jadwal[1] digunakan untuk mengambil jadwal dari hasil yang diterima dari repository.
    days, hours, minutes = td.days, td.seconds // 3600, td.seconds // 60 % 60 digunakan untuk mengkonversi jadwal yang diterima dari repository dari format timedelta menjadi format jam, menit.
    return datetime.time(hours, minutes, 0) digunakan untuk mengubah format jam, menit menjadi format waktu yang dapat digunakan.
    Metode ini akan mengembalikan jadwal pulang dari karyawan yang bersangkutan dalam format waktu yang dapat digunakan.
    """
    def get_jadwal_pulang(self):
        jadwal = self.repo.get_jadwal()
        td = jadwal[1]
        days, hours, minutes = td.days, td.seconds // 3600, td.seconds // 60 % 60
        return datetime.time(hours, minutes, 0)

    def absen_pulang(self):
        jam_pulang = datetime.datetime.now().time()
        jadwal = self.get_jadwal_pulang()
        if jam_pulang < jadwal:
            raise AbsensiWajahServiceException("Belum bisa absen pulang!")
        self.repo.absen_pulang(
            self.tanggal,
            self.id_karyawan,
            "{}:{}".format(jam_pulang.hour, jam_pulang.minute),
        )
        return self.ABSEN_PULANG_BERHASIL


class AbsensiWajahServiceException(Exception):
    pass
