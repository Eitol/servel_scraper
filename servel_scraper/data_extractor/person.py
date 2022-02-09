from dataclasses import dataclass
from enum import Enum

GENDER_MALE_MINIFIED = 'M'
GENDER_FEMALE_MINIFIED = 'F'
GENDER_OTHER_MINIFIED = 'O'


class Gender(Enum):
    OTHER = 0
    MALE = 1
    FEMALE = 2
    UNKNOWN = 3
    
    def __str__(self) -> str:
        if self == Gender.MALE:
            return GENDER_MALE_MINIFIED
        if self == Gender.FEMALE:
            return GENDER_FEMALE_MINIFIED
        return GENDER_OTHER_MINIFIED


@dataclass
class Person:
    name: str
    rut: str
    address: str
    gender: Gender
    district: str
    table: str
    
