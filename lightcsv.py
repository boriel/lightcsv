import datetime
import re

from typing import Dict, Iterable, List, TextIO, Union


class SimpleCSVInvalidOptionError(Exception):
    """Bad parameters error"""

    pass


CellType = Union[None, int, float, str, datetime.datetime, datetime.date, datetime.time]
RE_INT = re.compile(r"[-+]?[0-9]+$")


class LightCSV:
    def __init__(
        self, separator=",", quote_char='"', field_names: Iterable[str] = None, strict=True, has_headers=False
    ):
        self.separator = separator
        self.quote_char = quote_char
        self.field_names: List[Union[str, int]] = list(field_names or [])
        self.strict = strict
        self.has_headers = has_headers

        qch = re.escape(quote_char)
        sep = re.escape(separator)
        self.re = re.compile(rf"(?:\s*)((?:{qch}(?:[^{qch}]|{qch}{qch})*{qch})|[^{sep}]*)?\s*[{sep}]?")
        self.first_line = True

        if self.field_names and has_headers:
            raise SimpleCSVInvalidOptionError("Cannot use field_names if has_headers is True")

    def read(self, stream: TextIO) -> Iterable[Dict[Union[str, int], CellType]]:
        self.first_line = True

        for lineno, line in enumerate(stream):
            line = line.strip()
            if not line:
                continue  # skip empty lines

            parsed_line = self._parse(lineno, line)
            if self.first_line:
                self.first_line = False

                if self.has_headers:
                    self.field_names = [str(x) for x in parsed_line]
                    continue
                else:
                    self.field_names = list(range(len(parsed_line)))

            if self.strict and len(self.field_names) != len(parsed_line):
                raise ValueError(f"Line {lineno} has {len(parsed_line)} values. Expected {len(self.field_names)}")

            yield {x: y for x, y in zip(self.field_names, parsed_line)}

    def read_file(self, filename: str) -> Iterable[Dict[Union[str, int], CellType]]:
        with open(filename, "rt", encoding="utf-8") as f:
            yield from self.read(f)

    def _parse(self, lineno: int, line: str) -> List[CellType]:
        result: List[CellType] = []

        while True:
            match = self.re.match(line)

            if not match:
                if self.strict:
                    raise ValueError(f"Cannot parse line {lineno}")
                else:
                    result.append(None)
                    break

            chunk = match.groups()[0]

            result.append(self.parse_obj(lineno, chunk))
            line = line[match.end() :]
            if not match.group().endswith(self.separator):
                break

        return result

    def _is_null(self, s: str) -> bool:
        return not s.strip()

    def _is_int(self, s: str) -> bool:
        global RE_INT

        return RE_INT.match(s) is not None

    def _is_float(self, s: str) -> bool:
        try:
            float(s)
        except ValueError:
            return False
        return True

    def _is_string(self, s: str) -> bool:
        return len(s) > 1 and s[0] == s[-1] == self.quote_char

    def _is_datetime(self, s: str) -> bool:
        try:
            datetime.datetime.fromisoformat(s)
        except ValueError:
            return False

        return True

    def _is_date(self, s: str) -> bool:
        try:
            datetime.date.fromisoformat(s)
        except ValueError:
            return False

        return True

    def _is_time(self, s: str) -> bool:
        try:
            datetime.time.fromisoformat(s)
        except ValueError:
            return False

        return True

    def parse_obj(self, lineno: int, chunk: str) -> CellType:
        """If you want to add more types to the parser (i.e. to deserialize your own
        object from a string), subclass LightCSV and override this method. Then, either
        return your object or, if you can't deserialize it, return super().parse_obj(lineno, chunk).
        """
        chunk = chunk.strip()
        if self._is_null(chunk):
            return None

        if self._is_int(chunk):
            return int(chunk)

        if self._is_float(chunk):
            return float(chunk)

        if self._is_string(chunk):
            return chunk[1:-1].replace('""', '"')

        if self._is_date(chunk):
            return datetime.date.fromisoformat(chunk)

        if self._is_datetime(chunk):
            return datetime.datetime.fromisoformat(chunk)

        if self._is_time(chunk):
            return datetime.time.fromisoformat(chunk)

        if self.strict:
            raise ValueError(f"Cannot parse '{chunk} in line {lineno}")

        return chunk  # non-strict mode. Return it "as is"
