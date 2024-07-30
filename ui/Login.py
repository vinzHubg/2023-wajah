from PyQt5 import QtWidgets, uic

from core.Context import Context
from repo.RepoLogin import RepoLogin
from service.LoginService import LoginService, LoginServiceException
from ui.Home import Home


class Login(QtWidgets.QMainWindow):

    batalButton = QtWidgets.QPushButton
    loginButton = QtWidgets.QPushButton

    def __init__(self, context: Context):
        super(Login, self).__init__()

        uic.loadUi('ui/login.ui', self)

        self.context = context

        self.repo = RepoLogin(connection= context.get_connectin())

        self.batalButton.clicked.connect(self.batalButtonClick)
        self.loginButton.clicked.connect(self.loginButtonClick)

        self.show()

    def batalButtonClick(self):
        self.close()

    def loginButtonClick(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        login = LoginService(repo= self.repo, username=username.encode(), password=password.encode())
        try:
            admin = login.auth()
            QtWidgets.QMessageBox.information(self, "Login berhasil", "Selamat datang kembali {}".format(admin[1]))
            self.home = Home(context=self.context)
            self.home.show()
            self.close()
        except LoginServiceException as e:
            QtWidgets.QMessageBox.critical(self, "Login gagal", str(e))
