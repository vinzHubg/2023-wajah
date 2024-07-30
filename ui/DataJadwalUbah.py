from PyQt5 import QtWidgets, uic, QtCore
from datetime import datetime

from core.Context import Context
from helpers import text
from repo.RepoJadwal import RepoJadwal

class DataJadwalUbah(QtWidgets.QMainWindow):

    dataJadwalButton = QtWidgets.QPushButton
    searchEdit = QtWidgets.QLineEdit

    def __init__(self, parent, context: Context):
        super(DataJadwalUbah, self).__init__(parent)

        uic.loadUi('ui/data_jadwal_ubah.ui', self)

        self.repo = RepoJadwal(connection=context.get_connectin())

        self.batalButton.clicked.connect(self.close)
        self.simpanButton.clicked.connect(self.simpanButtonClick)


    def simpanButtonClick(self):
        jam_masuk = text(self.jamMasukTimeEdit) 
        jam_pulang = text(self.jamPulangTimeEdit)

        self.repo.ubah(self.id, jam_masuk, jam_pulang)
        
        QtWidgets.QMessageBox.information(self, "Ubah", "Data berhasil disimpan")

        self.close()

    def show_data(self, id, jam_masuk, jam_pulang):
        self.id = id

        jam_masuk = datetime.strptime(jam_masuk, '%H:%M:%S').time()
        jam_pulang = datetime.strptime(jam_pulang, '%H:%M:%S').time()

        self.jamMasukTimeEdit.setTime(QtCore.QTime(jam_masuk.hour, jam_masuk.minute))
        self.jamPulangTimeEdit.setTime(QtCore.QTime(jam_pulang.hour, jam_pulang.minute))

        self.show()

