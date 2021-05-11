from unittest import TestCase

from servel_scraper.data_extractor.extractor import Servel2021PDFDataExtractor
from servel_scraper.data_extractor.person import Gender

TEST_FILE = '../../test/testdata/tiny.pdf'
EXPECTED_SIZE = 243


class TestServel2021PDFDataExtractor(TestCase):
    def test_extract_with_valid_file__must_be_extract_data(self):
        extractor = Servel2021PDFDataExtractor()
        persons = extractor.extract(file_path=TEST_FILE)
        # Primera persona
        self.assertEqual(persons[0].name, 'ABURTO ARRIAGADA LUIS ALBERTO')
        self.assertEqual(persons[0].gender, Gender.MALE)
        self.assertEqual(persons[0].rut, '13.392.711-5')
        self.assertEqual(persons[0].address, 'ISLA REY JORGE SIN N')
        # Ultima persona
        self.assertEqual(persons[EXPECTED_SIZE - 1].name, 'ZUÑIGA MIRANDA MARIA ELENA')
        self.assertEqual(persons[EXPECTED_SIZE - 1].gender, Gender.FEMALE)
        self.assertEqual(persons[EXPECTED_SIZE - 1].rut, '11.660.676-3')
        self.assertEqual(persons[EXPECTED_SIZE - 1].address, 'BA E FREI')
