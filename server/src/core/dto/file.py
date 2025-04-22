from tempfile import SpooledTemporaryFile

class FileDTO:
    def __init__(self,
            download_name: str,
            file: SpooledTemporaryFile,
            size: int,
            real_name: str = None
        ):
        self.download_name = download_name
        self.file = file
        self.size = size
        self.real_name = real_name

    def to_dict(self) -> dict:
        return {
            "real_name": self.real_name,
            "download_name": self.download_name,
            "file": self.file,
            "size": self.size,
        }
