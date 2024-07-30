from repo.RepoKaryawan import RepoKaryawan
from storage.FaceStorage import FaceStorage


class DatasetService:

    def __init__(self, repo_karyawan: RepoKaryawan, storage: FaceStorage) -> None:
        self.repo_karyawan = repo_karyawan
        self.storage = storage
        self.karyawans = []
    
        self.init_dataset_images()

    def init_dataset_images(self):
        self.karyawans = self.repo_karyawan.all("")
        self.datasets = {}
        for karyawan in self.karyawans:
            list_images = self.storage.get(karyawan[0])
            self.datasets[karyawan[0]] = {"data": karyawan, "images": list_images}
