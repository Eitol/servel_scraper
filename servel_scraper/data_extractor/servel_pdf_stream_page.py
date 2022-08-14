from io import BytesIO, StringIO

from abc import abstractmethod
from typing import List

import pikepdf
from pikepdf._qpdf import Object

from servel_scraper.data_extractor.person import Person, Gender

ROW_START = '1 0 0 1 22'
HEADER_START = '1 0 0 1 22 536 Tm'
FIELD_LINE_START = '('

PDF_SOURCE_RAW_MALE_ID = 'VARON'
PDF_SOURCE_RAW_FEMALE_ID = 'MUJER'

FIELDS_TO_READ_PER_DOC_ROW = 2
FIELD_CONTENT_START_INDEX = 1
FIELD_CONTENT_END_INDEX = -4

PDF_STREAM_ENCODING = 'ISO-8859-1'

RELEVANT_STREAM_PAGE_INDEX = 1

# Field indexes in row
NAME_FIELD_INDEX = 0
DISTRICT_INDEX = 1
TABLE_START_INDEX = 2
TABLE_END_INDEX = 3


class ServelPDFStreamPage(object):
    @abstractmethod
    def extract(self) -> List[Person]:
        pass


class Servel2021PDFStreamPage(ServelPDFStreamPage):
    
    def __init__(self, page: Object):
        self.page = page
    
    def extract(self) -> List[Person]:
        return self._extract_people_data_from_page(self.page)
    
    def _extract_people_data_from_page(self, page: Object) -> List[Person]:
        page_data = []
        page_data_stream = self._get_relevant_data_stream_of_page(page)
        line = page_data_stream.readline()
        while len(line) > 0:
            if self._is_start_of_row(line):
                person_row = self._read_row(page_data_stream)
                page_data.append(person_row)
            line = page_data_stream.readline()
        return page_data
    
    @staticmethod
    def _is_start_of_row(line: str) -> bool:
        """
        Todas las filas inician por "1 0 0 1 22"
        """
        return line.startswith(ROW_START) and not line.startswith(HEADER_START)
    
    @classmethod
    def _read_row(cls, page_data_stream: StringIO) -> Person:
        row_str = cls._extract_row_fields_of_raw_strings(page_data_stream)
        return cls._convert_row_of_strings_to_person(row_str)
    
    @classmethod
    def _extract_row_fields_of_raw_strings(cls, page_data_stream: StringIO) -> List[str]:
        """
        return example:
                     0                           1            2         3                    4      5    6
        [ "ABURTO ARRIAGADA LUIS ALBERTO", "13.392.711-5", "VARON", "ANTARTICA", "SECTOR PUNAHUE", "2", "V"]
        """
        fields_str = []
        field_read_count = 0
        line = page_data_stream.readline()
        while len(line) > 0:
            if field_read_count == FIELDS_TO_READ_PER_DOC_ROW:
                break
            if cls._is_field_line(line):
                row_relevant_val = cls._extract_relevant_text_from_field(line)
                fields_str.append(row_relevant_val)
                field_read_count += 1
            line = page_data_stream.readline()
        return fields_str
    
    @staticmethod
    def _is_field_line(line: str) -> bool:
        return line.startswith(FIELD_LINE_START)
    
    @staticmethod
    def _extract_relevant_text_from_field(field: str) -> str:
        """
        :param field: i.e: "(SECTOR PUNAHUE S/N NELTUME) Tj"
        :return: i.e: "SECTOR PUNAHUE S/N NELTUME"

         1 (start)                  -4 (end)
         |                          |
         v                          v
        "(SECTOR PUNAHUE S/N NELTUME) Tj"
        """
        return field[FIELD_CONTENT_START_INDEX: FIELD_CONTENT_END_INDEX]
    
    @classmethod
    def _convert_row_of_strings_to_person(cls, row: List[str]) -> Person:
        table = " ".join(row[TABLE_START_INDEX:TABLE_END_INDEX + 1])
        return Person(
            name=row[NAME_FIELD_INDEX],
            district=row[DISTRICT_INDEX],
            table=table,
            address="",
            rut="",
            gender=Gender.UNKNOWN
        )
    
    @staticmethod
    def _str_gender_to_gender(str_gender: str) -> Gender:
        if str_gender == PDF_SOURCE_RAW_MALE_ID:
            return Gender.MALE
        if str_gender == PDF_SOURCE_RAW_FEMALE_ID:
            return Gender.FEMALE
        return Gender.OTHER
    
    @staticmethod
    def _get_relevant_data_stream_of_page(page: pikepdf.Page) -> StringIO:
        """
        The servel pdf page (2021) contains two text streams:
        - The first (index 0) contains the background text
        - The second (index 1) contains the important data (this is returned).

        For more context see image:  "doc/pdf_structure.png"
        """
        relevant_page_content: Object = page['/Contents'][RELEVANT_STREAM_PAGE_INDEX]
        buff = relevant_page_content.get_stream_buffer()
        bytes_io = BytesIO(buff)
        byte_str = bytes_io.read()
        # Convert to a "unicode" object
        text_obj = byte_str.decode(PDF_STREAM_ENCODING)
        return StringIO(text_obj)


