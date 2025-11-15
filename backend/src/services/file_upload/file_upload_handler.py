import requests

class FileSource:
    def load(self):
        """
        Returns tuple: (file_bytes, filename)
        """
        raise NotImplementedError

class UploadedFileSource(FileSource):
    def __init__(self, file):
        self.file = file

    def load(self):
        return self.file.read(), self.file.filename



class URLFileSource(FileSource):
    def __init__(self, url):
        self.url = url

    def load(self):
        resp = requests.get(self.url)
        resp.raise_for_status()

        filename = self.url.split("/")[-1]
        return resp.content, filename
    

import requests
import re

class GoogleDriveFileSource(FileSource):
    def __init__(self, drive_url):
        self.drive_url = drive_url

    def load(self):
        file_id = self.extract_file_id(self.drive_url)
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        resp = requests.get(download_url)
        resp.raise_for_status()

        filename = file_id + ".download"
        return resp.content, filename

    def extract_file_id(self, url):
        match = re.search(r"/d/([A-Za-z0-9_-]+)", url)
        if match:
            return match.group(1)
        raise ValueError("Invalid Google Drive URL")


class LocalFileSource(FileSource):
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, "rb") as f:
            return f.read(), self.path.split("/")[-1]



def file_source_factory(request):
    if "file" in request.files:
        return UploadedFileSource(request.files["file"])

    data = request.json or {}

    if "url" in data:
        return URLFileSource(data["url"])

    if "drive_url" in data:
        return GoogleDriveFileSource(data["drive_url"])

    if "local_path" in data:
        return LocalFileSource(data["local_path"])

    raise ValueError("Unsupported file source")