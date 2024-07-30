from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt

from core.Context import Context
from helpers import text
from repo.RepoJadwal import RepoJadwal
from table_model.ModelJadwal import ModelJadwal
from ui.DataJadwalTambah import DataJadwalTambah
from ui.DataJadwalUbah import DataJadwalUbah

class DataJadwal(QtWidgets.QMainWindow):

    def __init__(self, parent, context: Context):
        super(DataJadwal, self).__init__(parent)

        uic.loadUi('ui/data_jadwal.ui', self)

        self.tambah = DataJadwalTambah(self, context=context)
        self.ubah = DataJadwalUbah(self, context=context)

        self.repo = RepoJadwal(connection=context.get_connectin())

        self.showTable()

        self.cariButton.clicked.connect(self.showTable)
        self.tambahButton.clicked.connect(self.tambahButtonClick)
        self.tutupButton.clicked.connect(self.close)
        self.hapusButton.clicked.connect(self.hapusButtonClick)
        self.ubahButton.clicked.connect(self.ubahButtonClick)

    def showTable(self):
        search = text(self.searchEdit)
        self.datas = self.repo.all(search)

        self.model = ModelJadwal(self.datas)
        self.table.setModel(self.model)

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
        jam_masuk = self.model.data(self.model.index(first.row(), 1), Qt.DisplayRole)
        jam_pulang = self.model.data(self.model.index(first.row(), 2), Qt.DisplayRole)

        self.ubah.show_data(id, jam_masuk, jam_pulang)
