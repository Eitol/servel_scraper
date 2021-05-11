import csv
import enum
from dataclasses import dataclass
from typing import List, Dict, TextIO

from servel_scraper.downloader.cut import CUTRepository, CUT


class CUTField(enum.Enum):
    NOMBRE_REGION = 'NOMBRE_REGION'
    NOMBRE_PROVINCIA = 'NOMBRE_PROVINCIA'
    NOMBRE_COMUNA = 'NOMBRE_COMUNA'
    CODIGO_COMUNA = 'CODIGO_COMUNA'


@dataclass
class CUTCSVRepoConfig:
    columns: Dict[CUTField, str]
    delimiter: str


class CUTCSVRepository(CUTRepository):
    
    def __init__(self, csv_path: str, cfg: CUTCSVRepoConfig):
        self._csv_path = csv_path
        self._delimiter = cfg.delimiter
        self._columns = cfg.columns
    
    def list(self) -> List[CUT]:
        with open(self._csv_path) as f:
            return self._extract_rows(f)
    
    def _extract_rows(self, f: TextIO):
        out_list: List[CUT] = []
        reader = csv.DictReader(f, delimiter=self._delimiter)
        for row in reader:
            cut = self._build_cut_from_row(self._columns, row)
            out_list.append(cut)
        return out_list
    
    @staticmethod
    def _build_cut_from_row(columns_cfg: Dict[CUTField, str], row: Dict[str, str]) -> CUT:
        return CUT(
            nombre_region=row[columns_cfg[CUTField.NOMBRE_REGION]],
            nombre_provincia=row[columns_cfg[CUTField.NOMBRE_PROVINCIA]],
            codigo_comuna=row[columns_cfg[CUTField.CODIGO_COMUNA]],
            nombre_comuna=row[columns_cfg[CUTField.CODIGO_COMUNA]],
        )
