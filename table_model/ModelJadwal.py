from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import datetime


class ModelJadwal(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(ModelJadwal, self).__init__()
        self._data = data
        self._headers = ['ID', 'Jam Masuk', 'Jam Keluar']

    def data(self, index, role):
        if role == Qt.DisplayRole:
            item = self._data[index.row()][index.column()]
            if isinstance(item, datetime.timedelta):
                return str(item) 
            return item

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._headers)
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._headers[section])

