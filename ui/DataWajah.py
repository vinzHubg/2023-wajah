from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import os

from core.Context import Context
from helpers import text
from storage.FaceStorage import FaceStorage

cascPathface = "ui/data/haarcascade_frontalface_alt2.xml"
# load the harcaascade in the cascade classifier
faceCascade = cv2.CascadeClassifier(cascPathface)


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    kamera_index = 0

    def __init__(self):
        super().__init__()
        self._run_flag = False

    def run(self):
        self._run_flag = True
        cap = cv2.VideoCapture(self.kamera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(60, 60),
                    flags=cv2.CASCADE_SCALE_IMAGE,
                )
                for x, y, w, h in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                self.change_pixmap_signal.emit(frame)

        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

    def isRun(self):
        return self._run_flag


class DataWajah(QtWidgets.QMainWindow):

    dataAbsensiButton = QtWidgets.QPushButton
    searchEdit = QtWidgets.QLineEdit

    def __init__(self, parent, context: Context):
        super(DataWajah, self).__init__(parent)

        uic.loadUi("ui/data_wajah.ui", self)

        self.disply_width = 640
        self.display_height = 480
        self.rgb_image = None
        self.id = None

        # allow only integers
        onlyInt = QtGui.QIntValidator()
        onlyInt.setRange(0, 100)
        self.kameraIndexEdit.setValidator(onlyInt)

        self.tutupButton.clicked.connect(self.close)
        self.mulaiButton.clicked.connect(self.mulaiButtonClick)
        self.simpanWajahButton.clicked.connect(self.simpanWajahButtonClick)

        self.initVideoThread()

        self.storage = FaceStorage()

    def simpanWajahButtonClick(self):
        if self.id is None and self.rgb_image is None:
            QtWidgets.QMessageBox.critical(
                self, "Simpan image", "Gagal simpan, image tidak valid"
            )
            return

        self.storage.put(self.id, self.rgb_image)
        QtWidgets.QMessageBox.information(self, "Simpan image", "Berhasil disimpan")

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def show_data(self, id, nama_lengkap, jenis_kelamin, no_telepon, alamat):
        self.id = id
        self.pesanLabel.setText("{} - {}".format(id, nama_lengkap))
        self.show()

    def initVideoThread(self):
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)

    def mulaiButtonClick(self):
        try:
            if self.thread.isRun():
                self.thread.stop()
            else:
                self.thread.kamera_index = int(text(self.kameraIndexEdit))
                self.thread.start()
        except Exception as e:
            self.initVideoThread()
            QtWidgets.QMessageBox.critical(self, "Video error", str(e))

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        self.rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = self.rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            self.rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888
        )
        p = convert_to_Qt_format.scaled(
            self.disply_width, self.display_height, Qt.KeepAspectRatio
        )
        return QPixmap.fromImage(p)
