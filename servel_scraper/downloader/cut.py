from abc import abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class CUT:
    nombre_region: str
    nombre_provincia: str
    codigo_comuna: str
    nombre_comuna: str


class CUTRepository(object):
    
    @abstractmethod
    def list(self) -> List[CUT]:
        pass


