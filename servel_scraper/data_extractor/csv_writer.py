import csv
from typing import List, TextIO

from servel_scraper.data_extractor.person import Person

OUT_CSV_DELIMITER = ','
OUT_CSV_QUOTE_CHAR = '"'


class _CSVPersonWriter(object):
    def __init__(self, csv_writer: csv.writer):
        self._csv_writer = csv_writer
    
    def write_rows(self, people: List[Person]):
        for p in people:
            self.write_row(p)
    
    def write_row(self, p: Person):
        self._csv_writer.writerow([p.name, p.district, p.table])


class CSVExporter(object):
    
    def export(self, out_file_name: str, people: List[Person]):
        with open(out_file_name, mode='w') as f:
            w = _CSVPersonWriter(self._new_writer(f))
            w.write_rows(people)
    
    @staticmethod
    def _new_writer(f: TextIO) -> csv.writer:
        return csv.writer(
            f, delimiter=OUT_CSV_DELIMITER, quotechar=OUT_CSV_QUOTE_CHAR, quoting=csv.QUOTE_MINIMAL
        )
