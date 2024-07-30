from PyQt5 import QtWidgets, uic, QtCore

from core.Context import Context
from helpers import text
from repo.RepoAbsensi import RepoAbsensi
from repo.RepoKaryawan import RepoKaryawan
from service.AbsensiService import AbsensiService, AbsensiServiceException

class DataAbsensiTambah(QtWidgets.QMainWindow):

    dataAbsensiButton = QtWidgets.QPushButton
    searchEdit = QtWidgets.QLineEdit

    def __init__(self, parent, context: Context):
        super(DataAbsensiTambah, self).__init__(parent)

        uic.loadUi('ui/data_absensi_tambah.ui', self)

        self.repo = RepoAbsensi(connection=context.get_connectin())
        self.repo_karyawan = RepoKaryawan(connection=context.get_connectin())

        self.service = AbsensiService(self.repo)

        self.batalButton.clicked.connect(self.close)
        self.simpanButton.clicked.connect(self.simpanButtonClick)

        self.statusComboBox.addItem("Hadir")
        self.statusComboBox.addItem("Terlambat")
        self.statusComboBox.addItem("Izin")

        self.init_combobox_karyawan()


    def init_combobox_karyawan(self):
        karyawans = self.repo_karyawan.all("")
        self.karyawans = {}
        for karyawan in karyawans:
            key = "{} - {}".format(karyawan[0], karyawan[1])
            self.karyawans[key] = karyawan
            self.namaKaryawanComboBox.addItem(key)

    def simpanButtonClick(self):
        tanggal = self.tanggalDateEdit.date() 
        tanggal = '{0}-{1}-{2}'.format(tanggal.year(), tanggal.month(), tanggal.day())
        nama_karyawan = text(self.namaKaryawanComboBox) 
        id_karyawan = self.karyawans.get(nama_karyawan)[0]
        jam_masuk = text(self.jamMasukTimeEdit)
        jam_pulang = text(self.jamPulangTimeEdit)
        status = text(self.statusComboBox)

        try:
            self.service.absen(tanggal, id_karyawan, jam_masuk, jam_pulang, status)
            QtWidgets.QMessageBox.information(self, "Tambah", "Data berhasil disimpan")
        except AbsensiServiceException as e:
            QtWidgets.QMessageBox.critical(self, "Tambah", str(e))

        self.close()

