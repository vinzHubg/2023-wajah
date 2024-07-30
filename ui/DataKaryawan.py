from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt

from core.Context import Context
from helpers import text
from repo.RepoKaryawan import RepoKaryawan
from table_model.ModelKaryawan import ModelKaryawan
from ui.DataKaryawanTambah import DataKaryawanTambah
from ui.DataKaryawanUbah import DataKaryawanUbah
from ui.DataWajah import DataWajah

class DataKaryawan(QtWidgets.QMainWindow):

    def __init__(self, parent, context: Context):
        super(DataKaryawan, self).__init__(parent)

        uic.loadUi('ui/data_karyawan.ui', self)

        self.tambah = DataKaryawanTambah(self, context=context)
        self.ubah = DataKaryawanUbah(self, context=context)
        self.data_wajah = DataWajah(self, context=context)

        self.repo = RepoKaryawan(connection=context.get_connectin())

        self.showTable()

        self.cariButton.clicked.connect(self.showTable)
        self.tambahButton.clicked.connect(self.tambahButtonClick)
        self.tutupButton.clicked.connect(self.close)
        self.hapusButton.clicked.connect(self.hapusButtonClick)
        self.ubahButton.clicked.connect(self.ubahButtonClick)
        self.dataWajahButton.clicked.connect(self.dataWajahButtonClick)

    def dataWajahButtonClick(self):
        selected_rows = sorted(self.table.selectionModel().selectedRows())

        if len(selected_rows) <= 0:
            QtWidgets.QMessageBox.critical(self, "Ubah", "Data belum dipilih")
            return

        first = selected_rows[0]
        id = self.model.data(self.model.index(first.row(), 0), Qt.DisplayRole)
        nama_lengkap = self.model.data(self.model.index(first.row(), 1), Qt.DisplayRole)
        jenis_kelamin = self.model.data(self.model.index(first.row(), 2), Qt.DisplayRole)
        no_telepon = self.model.data(self.model.index(first.row(), 3), Qt.DisplayRole)
        alamat = self.model.data(self.model.index(first.row(), 4), Qt.DisplayRole)

        self.data_wajah.show_data(id, nama_lengkap, jenis_kelamin, no_telepon, alamat)

    def showTable(self):
        search = text(self.searchEdit)
        datas = self.repo.all(search)

        self.model = ModelKaryawan(datas)
        self.table.setModel(self.model)

        self.table.resizeColumnToContents(1)
        self.table.resizeColumnToContents(4)

    def tambahButtonClick(self):
        self.tambah.show()

    def hapusButtonClick(self):
        selected_rows = sorted(self.table.selectionModel().selectedRows())

        if len(selected_rows) <= 0:
            QtWidgets.QMessageBox.critical(self, "Hapus", "Data belum dipilih")
            return

        first = selected_rows[0]
        id = self.model.data(self.model.index(first.row(), 0), Qt.DisplayRole)

        self.repo.hapus(id)

        self.showTable()

    def ubahButtonClick(self):
        selected_rows = sorted(self.table.selectionModel().selectedRows())

        if len(selected_rows) <= 0:
            QtWidgets.QMessageBox.critical(self, "Ubah", "Data belum dipilih")
            return

        first = selected_rows[0]
        id = self.model.data(self.model.index(first.row(), 0), Qt.DisplayRole)
        nama_lengkap = self.model.data(self.model.index(first.row(), 1), Qt.DisplayRole)
        jenis_kelamin = self.model.data(self.model.index(first.row(), 2), Qt.DisplayRole)
        no_telepon = self.model.data(self.model.index(first.row(), 3), Qt.DisplayRole)
        alamat = self.model.data(self.model.index(first.row(), 4), Qt.DisplayRole)

        self.ubah.show_data(id, nama_lengkap, jenis_kelamin, no_telepon, alamat)
