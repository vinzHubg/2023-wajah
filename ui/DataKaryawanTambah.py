from PyQt5 import QtWidgets, uic, QtCore

from core.Context import Context
from helpers import text
from repo.RepoKaryawan import RepoKaryawan

class DataKaryawanTambah(QtWidgets.QMainWindow):

    dataKaryawanButton = QtWidgets.QPushButton
    searchEdit = QtWidgets.QLineEdit

    def __init__(self, parent, context: Context):
        super(DataKaryawanTambah, self).__init__(parent)

        uic.loadUi('ui/data_karyawan_tambah.ui', self)

        self.repo = RepoKaryawan(connection=context.get_connectin())

        self.batalButton.clicked.connect(self.close)
        self.simpanButton.clicked.connect(self.simpanButtonClick)

        self.jenisKelaminComboBox.addItem("Laki-laki")
        self.jenisKelaminComboBox.addItem("Perempuan")

    def simpanButtonClick(self):
        nama_lengkap = text(self.namaLengkapLineEdit) 
        jenis_kelamin = text(self.jenisKelaminComboBox)
        no_telepon = text(self.noTeleponLineEdit) 
        alamat = text(self.alamatEdit) 

        self.repo.tambah(nama_lengkap, jenis_kelamin, no_telepon, alamat)
        
        QtWidgets.QMessageBox.information(self, "Tambah", "Data berhasil disimpan")

        self.close()

