from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import os
import face_recognition
from PyQt5.QtCore import QTimer, QTime, Qt  

from core.Context import Context
from helpers import text
from repo.RepoAbsensi import RepoAbsensi
from repo.RepoAbsensiWajah import RepoAbsensiWajah
from repo.RepoKaryawan import RepoKaryawan
from service.AbsensiWajahService import (
    AbsensiWajahService,
    AbsensiWajahServiceException,
)



from service.DatasetService import DatasetService
from storage.FaceStorage import FaceStorage
import datetime

THRESHOLD = 0.60

cascPathface = "ui/data/haarcascade_frontalface_alt2.xml"
# load the harcaascade in the cascade classifier
faceCascade = cv2.CascadeClassifier(cascPathface)


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    found_signal = pyqtSignal(tuple)
    kamera_index = 0
    knownNames = []
    knownEncodings = []

    def __init__(self):
        super().__init__()
        self._run_flag = False

    def run(self):
        self._run_flag = True
        print("buka camera")
        cap = cv2.VideoCapture(self.kamera_index, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        print("berhasil buka camera")
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
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (0, 255, 0), 2)

                if len(faces) > 0:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    encodings = face_recognition.face_encodings(rgb)
                    names = []
                    for encoding in encodings:

                        distances = face_recognition.face_distance(
                            self.knownEncodings, encoding)

                        matches = False
                        name = "Unknown"
                        distance = 0
                        for i, face_distance in enumerate(distances):
                            if face_distance > distance:
                                name = self.knownNames[i]
                                distance = face_distance
                                print("{:.2} #{}".format(
                                    face_distance, self.knownNames[i]))

                        matches = face_recognition.compare_faces(
                            self.knownEncodings, encoding
                        )
                        name = "Unknown"
                        if True in matches:
                            matchedIdxs = [
                                i for (i, b) in enumerate(matches) if b]
                            counts = {}
                            for i in matchedIdxs:
                                name = self.knownNames[i]
                                counts[name] = counts.get(name, 0) + 1
                            name = max(counts, key=counts.get)
                            names.append(name)

                        if (name != "Unknown"):
                            karyawan = self.datasets[name]["data"]

                            if distance > THRESHOLD:
                                cv2.putText(
                                    frame,
                                    "{} {:.2f}".format(karyawan[1], distance * 100),
                                    (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.75,
                                    (0, 255, 0),
                                    2,
                                )
                                self.found_signal.emit(karyawan)
                        else:
                            cv2.putText(
                                frame,
                                "Tidak diketahui",
                                (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.75,
                                (0, 255, 0),
                                2,
                            )
                            self.found_signal.emit(())

                        

                        # for ((x, y, w, h), name) in zip(faces, names):
                        #     # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        #     karyawan = self.datasets[name]["data"]
                        #     self.found_signal.emit(karyawan)
                        #     cv2.putText(
                        #         frame,
                        #         "{} {}".format(karyawan[1], distance),
                        #         (x, y),
                        #         cv2.FONT_HERSHEY_SIMPLEX,
                        #         0.75,
                        #         (0, 255, 0),
                        #         2,
                        #     )

                self.change_pixmap_signal.emit(frame)

        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

    def isRun(self):
        return self._run_flag

    def set_service_dataset(self, service: DatasetService):
        knownNames = []
        knownEncodings = []
        for id in service.datasets:
            data = service.datasets[id]
            for imagePath in data["images"]:
                image = cv2.imread(imagePath)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # Use Face_recognition to locate faces
                boxes = face_recognition.face_locations(rgb, model="hog")
                # compute the facial embedding for the face
                encodings = face_recognition.face_encodings(rgb, boxes)
                # loop over the encodings
                for encoding in encodings:
                    knownEncodings.append(encoding)
                    knownNames.append(id)

        self.knownNames = knownNames
        self.knownEncodings = knownEncodings
        self.datasets = service.datasets


class AbsensiWajah(QtWidgets.QMainWindow):

    dataAbsensiButton = QtWidgets.QPushButton
    searchEdit = QtWidgets.QLineEdit

    def __init__(self, parent, context: Context):
        super(AbsensiWajah, self).__init__(parent)

        uic.loadUi("ui/absensi_wajah_masuk.ui", self)

        timerClock = QTimer(self)  
  
        timerClock.timeout.connect(self.displayTime)  
  
        timerClock.start(1000)  

        self.disply_width = 640
        self.display_height = 480
        self.rgb_image = None
        self.karyawans = []
        # self.id = None

        self.repo = RepoAbsensiWajah(connection=context.get_connectin())
        self.repo_karyawan = RepoKaryawan(connection=context.get_connectin())

        # allow only integers
        onlyInt = QtGui.QIntValidator()
        onlyInt.setRange(0, 100)
        self.kameraIndexEdit.setValidator(onlyInt)

        self.tutupButton.clicked.connect(self.close)
        self.mulaiButton.clicked.connect(self.mulaiButtonClick)
        # self.simpanWajahButton.clicked.connect(self.simpanWajahButtonClick)

        self.initVideoThread()

        self.storage = FaceStorage()

        self.service = AbsensiWajahService(repo=self.repo)
        self.service_dataset = DatasetService(
            repo_karyawan=self.repo_karyawan, storage=self.storage
        )
        self.thread.set_service_dataset(self.service_dataset)

    # def simpanWajahButtonClick(self):
    #     if self.id is None and self.rgb_image is None:
    #         QtWidgets.QMessageBox.critical(
    #             self, "Simpan image", "Gagal simpan, image tidak valid"
    #         )
    #         return

    #     self.storage.put(self.id, self.rgb_image)
    #     QtWidgets.QMessageBox.information(self, "Simpan image", "Berhasil disimpan")
    def displayTime(self):  
  
        # get the present time  
        present_time = QTime.currentTime()  
  
        # convert the QTime object into a string  
        time_label = present_time.toString('hh:mm:ss')  
  
        # display text to the label  
        self.jam.setText(time_label) 

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    # def show_data(self, id, nama_lengkap, jenis_kelamin, no_telepon, alamat):
    #     # self.id = id
    #     # self.pesanLabel.setText("{} - {}".format(id, nama_lengkap))
    #     self.show()

    def initVideoThread(self):
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.found_signal.connect(self.found_karyawan)

    def found_karyawan(self, karyawan):


        if len(karyawan) <= 0:
            self.pesanLabel.setText(
                "Tidak dapat melakukan absensi" 
            )
            return

        now = datetime.datetime.today()

        try:
            absen = self.service.hanya_absen_masuk(
                "{}-{}-{}".format(now.year, now.month, now.day), karyawan[0]
            )

            if absen == AbsensiWajahService.ABSEN_MASUK_BERHASIL:
                self.pesanLabel.setText(
                    "%s - %s (%s)" % (karyawan[0], karyawan[1], "Hadir")
                )
            if absen == AbsensiWajahService.ABSEN_MASUK_TERLAMBAT_BERHASIL:
                self.pesanLabel.setText(
                    "%s - %s (%s)" % (karyawan[0], karyawan[1], "Terlambat")
                )
            
        except AbsensiWajahServiceException as e:
            self.pesanLabel.setText("%s - %s (%s)" %
                                    (karyawan[0], karyawan[1], str(e)))

    def mulaiButtonClick(self):
        try:
            print("mulaiButton {}".format(self.thread.isRun))
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
