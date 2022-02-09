from abc import abstractmethod
from typing import List

import pikepdf
from pikepdf._qpdf import Pdf

from servel_scraper.data_extractor.person import Person
from servel_scraper.data_extractor.servel_pdf_stream_page import ServelPDFStreamPage, Servel2021PDFStreamPage


class ServelPDFDataExtractor:
    @abstractmethod
    def extract(self, file_path: str) -> List[Person]:
        pass


class Servel2021PDFDataExtractor(ServelPDFDataExtractor):
    
    def extract(self, file_path: str) -> List[Person]:
        pdf: Pdf = pikepdf.open(file_path)
        out_data: List[Person] = []
        for page in pdf.pages:
            page_data = self._extract_people_data_from_page(page)
            out_data.extend(page_data)
        return out_data
    
    @staticmethod
    def _extract_people_data_from_page(page: pikepdf.Page) -> List[Person]:
        page_data_stream: ServelPDFStreamPage = Servel2021PDFStreamPage(page)
        return page_data_stream.extract()
