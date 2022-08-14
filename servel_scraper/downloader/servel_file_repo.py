import pathlib
from dataclasses import dataclass
from typing import List, Dict

from servel_scraper.downloader.cut import CUT
from servel_scraper.downloader.cut_csv_repo import CUTCSVRepository, CUTField, CUTCSVRepoConfig
from servel_scraper.downloader.file_downloader import FileDownloader
from tqdm import tqdm

CDN_BASE_URL = 'http://cdn.servel.cl/padron'

_DEFAULT_CUT_COLUMNS_CSV: Dict[CUTField, str] = {
    CUTField.NOMBRE_REGION: 'Nombre Región',
    CUTField.NOMBRE_PROVINCIA: 'Nombre Provincia',
    CUTField.NOMBRE_COMUNA: 'Nombre Comuna',
    CUTField.CODIGO_COMUNA: 'Código Comuna 2018',
}

DEFAULT_CUT_CSV_PATH = str(pathlib.Path(__file__).parent.absolute())+'/../../data/codigos_de_comunas.csv'
DEFAULT_DELIMITER = ','

FailReason = str
Url = str


class ServelFilesUrlRepo(object):
    @classmethod
    def get_servel_files_urls(cls, csv_path: str) -> List[str]:
        """
        i.e: [
                "http://cdn.servel.cl/padron/A01107.pdf",
                "http://cdn.servel.cl/padron/A01101.pdf",
                ...
            ]
        """
        url_list = []
        for cut in cls._get_cuts(csv_path):
            url = cls._build_url_from_cut(cut)
            url_list.append(url)
        return url_list
    
    @staticmethod
    def _get_cuts(csv_path: str) -> List[CUT]:
        repo_config = CUTCSVRepoConfig(_DEFAULT_CUT_COLUMNS_CSV, DEFAULT_DELIMITER)
        repo = CUTCSVRepository(csv_path, repo_config)
        return repo.list()
    
    @staticmethod
    def _build_url_from_cut(cut: CUT) -> Url:
        """
        i.e: "http://cdn.servel.cl/padron/A01107.pdf"
        """
        return f"{CDN_BASE_URL}/A{cut.codigo_comuna}.pdf"


@dataclass
class DownloadResult:
    failed: Dict[Url, FailReason]
    success: List[Url]


class ServelFileRepo(object):
    
    @staticmethod
    def download_servel_files(out_path: str, csv_path: str = DEFAULT_CUT_CSV_PATH) -> DownloadResult:
        urls = ServelFilesUrlRepo.get_servel_files_urls(csv_path)
        file_downloader = FileDownloader()
        result = DownloadResult(failed={}, success=[])
        pbar = tqdm(urls)
        for url in pbar:
            pbar.set_description(f"Downloading (Fails: {len(result.failed)}): {url}")
            try:
                file_downloader.download_file(out_path, url)
            except (BaseException, Exception) as e:
                result.failed[url] = str(e)
            result.success.append(url)
        return result
