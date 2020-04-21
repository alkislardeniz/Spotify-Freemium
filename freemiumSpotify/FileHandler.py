import pickle
from pathlib import Path


class FileHandler:
    @staticmethod
    def save_obj(obj, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_obj(file_name):
        with open(file_name, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def create_download_directory(path):
        p = Path(path)
        p.mkdir(exist_ok=True)
