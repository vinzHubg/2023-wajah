from PyQt5 import QtWidgets, uic, QtCore
from datetime import datetime

from core.Context import Context
from helpers import text
from repo.RepoAbsensi import RepoAbsensi
from repo.RepoKaryawan import RepoKaryawan

class DataAbsensiUbah(QtWidgets.QMainWindow):

    dataAbsensiButton = QtWidgets.QPushButton
    searchEdit = QtWidgets.QLineEdit

    def __init__(self, parent, context: Context):
        super(DataAbsensiUbah, self).__init__(parent)

        uic.loadUi('ui/data_absensi_ubah.ui', self)

        self.repo = RepoAbsensi(connection=context.get_connectin())
        self.repo_karyawan = RepoKaryawan(connection=context.get_connectin())

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
        # tanggal = text(self.tanggalDateEdit) 
        tanggal = self.tanggalDateEdit.date() 
        tanggal = '{0}-{1}-{2}'.format(tanggal.year(), tanggal.month(), tanggal.day())

        id_karyawan = text(self.namaKaryawanComboBox) 
        jam_masuk = text(self.jamMasukTimeEdit) 
        jam_pulang = text(self.jamPulangTimeEdit)
        status = text(self.statusComboBox)

        id_karyawan = self.karyawans.get(id_karyawan)[0]
        self.repo.ubah(self.id, tanggal, id_karyawan, jam_masuk, jam_pulang, status)
        
        QtWidgets.QMessageBox.information(self, "Ubah", "Data berhasil disimpan")

        self.close()

    def show_data(self, id, tanggal, id_karyawan, jam_masuk, jam_pulang, status):
        self.id = id

        jam_masuk = datetime.strptime(jam_masuk, '%H:%M:%S').time()
        jam_pulang = datetime.strptime(jam_pulang, '%H:%M:%S').time()

        self.jamMasukTimeEdit.setTime(QtCore.QTime(jam_masuk.hour, jam_masuk.minute))
        self.jamPulangTimeEdit.setTime(QtCore.QTime(jam_pulang.hour, jam_pulang.minute))

        index = self.statusComboBox.findText(status, QtCore.Qt.MatchFixedString)
        if index >= 0:
             self.statusComboBox.setCurrentIndex(index)


        self.show()

