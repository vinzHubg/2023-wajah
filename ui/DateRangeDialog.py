from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QPushButton
from PyQt5.QtCore import QDate

class DateRangeDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Pilih Rentang Tanggal')

        layout = QVBoxLayout()

        # Date range selection
        start_layout = QHBoxLayout()
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        start_layout.addWidget(QLabel('Tanggal Mulai:'))
        start_layout.addWidget(self.start_date_edit)

        end_layout = QHBoxLayout()
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        end_layout.addWidget(QLabel('Tanggal Akhir:'))
        end_layout.addWidget(self.end_date_edit)

        # Confirm button
        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton('OK')
        self.confirm_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(self.confirm_button)

        # Add layouts to the main layout
        layout.addLayout(start_layout)
        layout.addLayout(end_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_date_range(self):
        start_date = self.start_date_edit.date().toString('yyyy-MM-dd')
        end_date = self.end_date_edit.date().toString('yyyy-MM-dd')
        return start_date, end_date