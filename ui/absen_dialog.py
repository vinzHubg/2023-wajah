import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel
# from ui.AbsensiWajah import AbsensiWajah
from ui import absensi_wajah_masuk
from ui import absensi_wajah_pulang

class AbsenDialog(QDialog):
    def __init__(self, context):
        super().__init__()

        self.context = context

        self.setWindowTitle("Absen Kehadiran")

        # Layout utama
        layout = QVBoxLayout()

        # Label judul
        self.label = QLabel("Pilih opsi absen Anda:", self)
        layout.addWidget(self.label)

        # Tombol Absen Masuk
        self.btn_absen_masuk = QPushButton("Absen Masuk", self)
        self.btn_absen_masuk.clicked.connect(self.absen_masuk)
        layout.addWidget(self.btn_absen_masuk)

        # Tombol Absen Pulang
        self.btn_absen_pulang = QPushButton("Absen Pulang", self)
        self.btn_absen_pulang.clicked.connect(self.absen_pulang)
        layout.addWidget(self.btn_absen_pulang)

        # Set layout ke dialog
        self.setLayout(layout)

    def absen_masuk(self):
        self.absensi_wajah = absensi_wajah_masuk.AbsensiWajah(self, context=self.context)
        self.absensi_wajah.showFullScreen()

    def absen_pulang(self):
        self.absensi_wajah = absensi_wajah_pulang.AbsensiWajah(self, context=self.context)
        self.absensi_wajah.showFullScreen()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = AbsenDialog()
    dialog.show()

    sys.exit(app.exec_())
