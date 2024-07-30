from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from datetime import datetime

from core.Context import Context
from helpers import text
from repo.RepoAbsensi import RepoAbsensi
from table_model.ModelAbsensi import ModelAbsensi
from ui.DataAbsensiTambah import DataAbsensiTambah
from ui.DataAbsensiUbah import DataAbsensiUbah
from ui.print.template import get_template
from ui.print.cetak import cetak


class DataAbsensi(QtWidgets.QMainWindow):

    def __init__(self, parent, context: Context):
        super(DataAbsensi, self).__init__(parent)

        uic.loadUi('ui/data_absensi.ui', self)

        self.tambah = DataAbsensiTambah(self, context=context)
        self.ubah = DataAbsensiUbah(self, context=context)

        self.repo = RepoAbsensi(connection=context.get_connectin())

        self.showTable()

        self.cariButton.clicked.connect(self.showTable)
        self.tambahButton.clicked.connect(self.tambahButtonClick)
        self.tutupButton.clicked.connect(self.close)
        self.hapusButton.clicked.connect(self.hapusButtonClick)
        self.ubahButton.clicked.connect(self.ubahButtonClick)
        self.cetakButton.clicked.connect(self.cetakButtonClick)

    def showTable(self):
        search = text(self.searchEdit)
        self.datas = self.repo.all(search)

        self.model = ModelAbsensi(self.datas)
        self.table.setModel(self.model)

        self.table.resizeColumnToContents(2)

    def cetakButtonClick(self):
        html = get_template("data_absensi.html").render(
            datas=self.datas,
            tanggal_indo=datetime.now().strftime("%d %B %Y"),
        )
        cetak(html, "reports/laporan_absensi.pdf")

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
        tanggal = self.model.data(self.model.index(first.row(), 1), Qt.DisplayRole)
        id_karyawan = self.model.data(self.model.index(first.row(), 2), Qt.DisplayRole)
        jam_masuk = self.model.data(self.model.index(first.row(), 3), Qt.DisplayRole)
        jam_pulang = self.model.data(self.model.index(first.row(), 4), Qt.DisplayRole)
        status = self.model.data(self.model.index(first.row(), 5), Qt.DisplayRole)

        self.ubah.show_data(id, tanggal, id_karyawan, jam_masuk, jam_pulang, status)
