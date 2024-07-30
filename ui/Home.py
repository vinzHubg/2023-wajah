from PyQt5 import QtWidgets, uic

from core.Context import Context
from ui.AbsensiWajah import AbsensiWajah
from ui.DataJadwal import DataJadwal
from ui.DataAbsensi import DataAbsensi 
from ui.DataKaryawan import DataKaryawan

class Home(QtWidgets.QMainWindow):

    def __init__(self, context: Context):
        super(Home, self).__init__()

        self.context = context

        uic.loadUi('ui/home.ui', self)

        self.dataKaryawanButton.clicked.connect(self.dataKaryawanButtonClick)
        self.dataJadwalButton.clicked.connect(self.dataJadwalButtonClick)
        self.dataAbsensiButton.clicked.connect(self.dataAbsensiButtonClick)
        self.absensiWajahButton.clicked.connect(self.absensiWajahButtonClick)


    def dataKaryawanButtonClick(self):
        self.data_karyawan = DataKaryawan(self, context=self.context)
        self.data_karyawan.show()

    def dataJadwalButtonClick(self):
        self.data_jadwal = DataJadwal(self, context=self.context)
        self.data_jadwal.show()

    def dataAbsensiButtonClick(self):
        self.data_absensi = DataAbsensi(self, context=self.context)
        self.data_absensi.show()

    def absensiWajahButtonClick(self):
        self.absensi_wajah = AbsensiWajah(self, context=self.context)
        self.absensi_wajah.showFullScreen()
