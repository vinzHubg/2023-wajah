from PyQt5 import QtWidgets

def text(widget):
    if isinstance(widget, QtWidgets.QTextEdit):
        return widget.toPlainText().encode().decode("utf-8")
    if isinstance(widget, QtWidgets.QComboBox):
        return widget.currentText().encode().decode("utf-8")
    return widget.text().encode().decode("utf-8")

def bulan_indo(num):
    if num == 1:
        return "Januari"
    if num == 2:
        return "Februari"
    if num == 3:
        return "Maret"
    if num == 4:
        return "April"
    if num == 5:
        return "Mei"
    if num == 6:
        return "Juni"
    if num == 7:
        return "Juli"
    if num == 8:
        return "Agustus"
    if num == 9:
        return "September"
    if num == 10:
        return "Oktober"
    if num == 11:
        return "November"
    if num == 12:
        return "Desember"
