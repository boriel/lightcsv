import unittest
import datetime

from io import StringIO

from lightcsv import LightCSV


class TestLightCSV(unittest.TestCase):
    def test_it_parses_typical_CSV(self):
        input = "C0,C1,C2,C3,C4,C5,C6\n" ',1,2.5,"a ""String""",2021-02-05,2021-02-05 23:50:12,23:50:12\n'
        with StringIO(input) as f:
            result = list(LightCSV(has_headers=True, strict=False).read(f))

        assert result == [
            {
                "C0": None,
                "C1": 1,
                "C2": 2.5,
                "C3": 'a "String"',
                "C4": datetime.date(2021, 2, 5),
                "C5": datetime.datetime(2021, 2, 5, 23, 50, 12),
                "C6": datetime.time(23, 50, 12),
            }
        ]

    def test_it_parses_with_no_column(self):
        input = "C0,C1,C2,C3,C4,C5,C6\n" ',1,2.5,"a ""String""",2021-02-05,2021-02-05 23:50:12,23:50:12\n'
        with StringIO(input) as f:
            result = list(LightCSV(strict=False).read(f))

        assert result == [
            {0: "C0", 1: "C1", 2: "C2", 3: "C3", 4: "C4", 5: "C5", 6: "C6"},
            {
                0: None,
                1: 1,
                2: 2.5,
                3: 'a "String"',
                4: datetime.date(2021, 2, 5),
                5: datetime.datetime(2021, 2, 5, 23, 50, 12),
                6: datetime.time(23, 50, 12),
            },
        ]


if __name__ == "__main__":
    unittest.main()
