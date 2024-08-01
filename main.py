from PyQt5 import QtWidgets
import sys, os
from core.Context import Context
from database.Connection import Connection
from ui.Login import Login
import resources

# pyqt = os.path.dirname(PyQt5.__file__)
# os.environ['QT_PLUGIN_PATH'] = os.path.join(pyqt, "Qt/plugins")


# Create an instance of QtWidgets.QApplication
app = QtWidgets.QApplication(sys.argv)

context = Context(connection=Connection())

window = Login(context=context)  # Create an instance of our class
app.exec_()  # Start the application
