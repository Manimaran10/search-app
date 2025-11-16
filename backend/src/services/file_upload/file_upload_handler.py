import requests
import re
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
        return self.file.read(), self.file.filename, None



class URLFileSource(FileSource):
    def __init__(self, url):
        self.url = url

    def load(self):
        resp = requests.get(self.url)
        resp.raise_for_status()

        filename = self.url.split("/")[-1]
        return resp.content, filename, self.url



class GoogleDriveFileSource(FileSource):

    def __init__(self, drive_url):
        self.drive_url = drive_url

    def load(self):
        file_id = self.extract_file_id(self.drive_url)
        url = "https://drive.google.com/uc?export=download"
        
        session = requests.Session()
        response = session.get(url, params={"id": file_id}, stream=True)

        # Handle confirmation token
        token = self._get_confirm_token(response)
        if token:
            response = session.get(
                url,
                params={"id": file_id, "confirm": token},
                stream=True
            )

        file_bytes = response.content
        filename = f"{file_id}.file"

        return file_bytes, filename, self.drive_url

    def _get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None

    def extract_file_id(self, url):
        patterns = [
            r"/d/([a-zA-Z0-9_-]+)",                       
            r"id=([a-zA-Z0-9_-]+)",                       
            r"file/d/([a-zA-Z0-9_-]+)",                   
        ]

        for p in patterns:
            match = re.search(p, url)
            if match:
                return match.group(1)

        raise ValueError("Invalid Google Drive link")

class LocalFileSource(FileSource):
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, "rb") as f:
            return f.read(), self.path.split("/")[-1], None



def file_source_factory(request):
    if "files" in request.files:
        return UploadedFileSource(request.files["files"])

    data = request.json or {}

    if "url" in data:
        return URLFileSource(data["url"])

    if "drive_url" in data:
        return GoogleDriveFileSource(data["drive_url"])

    if "local_path" in data:
        return LocalFileSource(data["local_path"])

    raise ValueError("Unsupported file source")