from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class ModelKaryawan(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(ModelKaryawan, self).__init__()
        self._data = data
        self._headers = ['ID', 'Nama Lengkap', 'Jenis Kelamin', 'No Telepon', 'Alamat']

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

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

