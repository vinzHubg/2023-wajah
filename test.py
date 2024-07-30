
from database.Connection import Connection
from repo.RepoAbsensiWajah import RepoAbsensiWajah
from service.AbsensiWajahService import AbsensiWajahService


if __name__ == "__main__":
    connection = Connection()
    repo = RepoAbsensiWajah(connection=connection)
    absensi = AbsensiWajahService(repo=repo)
    print(absensi.absen("2000-12-21", "2"))
