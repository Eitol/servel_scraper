import enum
import os
from typing import List

from tqdm import tqdm

from servel_scraper.data_extractor.extractor import Servel2021PDFDataExtractor
from servel_scraper.data_extractor.csv_writer import CSVExporter
from servel_scraper.downloader.servel_file_repo import ServelFileRepo, DownloadResult


class _PipelineLogger(object):
    @staticmethod
    def log_download_result(download_result: DownloadResult):
        if len(download_result.failed) > 0:
            print(f"\n\nLas siguientes descargas han fallado:")
            for faliled_url in download_result.failed:
                print(faliled_url)
        else:
            print(f"\n\nTodas las descargas fueron exitosas!")


class PipelineStage(enum.Enum):
    DOWNLOAD_PDFS = 'DOWNLOAD_PDFS'
    EXTRACT_CSV_FROM_PDF = 'EXTRACT_CSV_FROM_PDF'


class ServelPipeline(object):
    DEFAULT_STAGES = [
        PipelineStage.DOWNLOAD_PDFS,
        PipelineStage.EXTRACT_CSV_FROM_PDF
    ]
    
    def __init__(self, out_path: str, out_csv_path: str):
        self.pdf_path = out_path
        self.out_csv_path = out_csv_path
    
    def run_pipeline(self, stages: List[PipelineStage] = None):
        if stages is None:
            stages = ServelPipeline.DEFAULT_STAGES
        if PipelineStage.DOWNLOAD_PDFS in stages:
            self._download_servel_pdfs()
        if PipelineStage.EXTRACT_CSV_FROM_PDF in stages:
            self._extract_csv_from_servel_pdfs()
    
    def _download_servel_pdfs(self):
        download_result = ServelFileRepo.download_servel_files(self.pdf_path)
        _PipelineLogger.log_download_result(download_result)
    
    def __get_pdf_files(self) -> List[str]:
        return [x for x in os.listdir(self.pdf_path) if x.endswith(".pdf")]
    
    def _extract_csv_from_servel_pdfs(self):
        exporter = CSVExporter()
        extractor = Servel2021PDFDataExtractor()
        pdf_files = self.__get_pdf_files()
        pbar = tqdm(pdf_files)
        for pdf_file_name in pbar:
            pbar.set_description(f"Processing: {pdf_file_name}")
            people = extractor.extract(file_path=os.path.join(self.pdf_path, pdf_file_name))
            out_file_name = os.path.join(self.out_csv_path, pdf_file_name) + '.csv'
            exporter.export(out_file_name, people)
