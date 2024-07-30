from PyQt5 import QtWidgets, uic, QtCore

from core.Context import Context
from helpers import text
from repo.RepoJadwal import RepoJadwal

class DataJadwalTambah(QtWidgets.QMainWindow):

    dataJadwalButton = QtWidgets.QPushButton
    searchEdit = QtWidgets.QLineEdit

    def __init__(self, parent, context: Context):
        super(DataJadwalTambah, self).__init__(parent)

        uic.loadUi('ui/data_jadwal_tambah.ui', self)

        self.repo = RepoJadwal(connection=context.get_connectin())

        self.batalButton.clicked.connect(self.close)
        self.simpanButton.clicked.connect(self.simpanButtonClick)


    def simpanButtonClick(self):
        jam_masuk = text(self.jamMasukTimeEdit) 
        jam_pulang = text(self.jamPulangTimeEdit) 

        self.repo.tambah(jam_masuk, jam_pulang)
        
        QtWidgets.QMessageBox.information(self, "Tambah", "Data berhasil disimpan")

        self.close()

