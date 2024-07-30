import os
import cv2
import uuid


class FaceStorage:
    def __init__(self) -> None:
        self.base_path = os.path.realpath(".") + "/images"

    def get(self, id):
        """
        return list image yang di dalam folder id
        """
        res = []
        folder = self.create_folder(id)
        for path in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, path)):
                res.append("%s/%s" % (folder, path))
        return res

    def put(self, id, image):
        """
        save image ke dalam folder id
        """
        folder = self.create_folder(id)
        cv2.imwrite("%s/%s" % (folder, self.generate_random_name()), image)

    def generate_random_name(self):
        return "%s.jpg" % uuid.uuid4().hex

    def create_folder(self, id):
        folder = "%s/%s" % (self.base_path, id)
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder
