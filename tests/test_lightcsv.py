import unittest
import datetime

from io import StringIO

from lightcsv import LightCSV


class TestLightCSV(unittest.TestCase):
    def test_it_parses_typical_CSV(self):
        input = ('C0,C1,C2,C3,C4,C5,C6\n'
                 ',1,2.5,"a ""String""",2021-02-05,2021-02-05 23:50:12,23:50:12\n')
        with StringIO(input) as f:
            result = list(LightCSV(has_headers=True, strict=False).read(f))

        assert result == [{
            "C0": None,
            "C1": 1,
            "C2": 2.5,
            "C3": 'a "String"',
            "C4": datetime.date(2021, 2, 5),
            "C5": datetime.datetime(2021, 2, 5, 23, 50, 12),
            "C6": datetime.time(23, 50, 12)
        }]


if __name__ == '__main__':
    unittest.main()
