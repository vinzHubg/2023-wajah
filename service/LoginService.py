import hashlib

from repo.RepoLogin import RepoLogin

class LoginService:

    def __init__(self, repo: RepoLogin, username, password) -> None:
        self.repo = repo
        self.username = username
        self.password = password

    def auth(self):
        password = hashlib.md5(self.password).hexdigest()
        login = self.repo.login(self.username, password)
        print(login)
        if login is None:
            raise LoginServiceException("Login gagal! username/password salah")
        return login

class LoginServiceException(Exception):
    pass
