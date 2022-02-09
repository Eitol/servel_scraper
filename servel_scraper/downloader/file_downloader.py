import os
import urllib.request


class FileDownloader(object):
    
    def download_file(self, out_path: str, url: str):
        file_data = self._read_url_data(url)
        out_file_path = self._build_path_to_save_file(url, out_path)
        self._write_file(out_file_path, file_data)
    
    @staticmethod
    def _build_path_to_save_file(url: str, out_path: str) -> str:
        filename = os.path.basename(url)
        return os.path.join(out_path, filename)
    
    @staticmethod
    def _read_url_data(url: str):
        response = urllib.request.urlopen(url)
        return response.read()
    
    @staticmethod
    def _write_file(out_file_path: str, file_data):
        with open(out_file_path, "wb") as f:
            f.write(file_data)
