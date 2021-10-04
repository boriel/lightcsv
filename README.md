# LightCSV

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.8](https://img.shields.io/badge/python-3.9-greensvg)](https://www.python.org/downloads/release/python-390/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simple light CSV reader

This CSV reader is implemented in just pure Python. It allows to specify a separator, a quote char and
column titles (or get the first row as titles). Nothing more, nothing else.

## Usage

Usage is pretty straightforward:

```python
from lightcsv import LightCSV

for row in LightCSV().read_file("myfile.csv"):
    print(row)
```

This will open a file named `myfile.csv` and iterate over the CSV file returning each 
row as a key-value dictionary. Line endings can be either `\n` or `\r\n`. The file will be opened
in text-mode with `utf-8` encoding.

You can supply your own stream (i.e. an open file instead of a filename). You can use this, for example,
to open a file with a different encoding, etc.:

```python
from lightcsv import LightCSV

with open("myfile.csv") as f:
    for row in LightCSV().read(f):
        print(row)
```

    NOTE: Blank lines at any point in the file will be ignored

### Parameters

LightCSV can be parametrized during initialization to fine-tune its behaviour.

The following example shows initialization with default parameters:

```python
from lightcsv import LightCSV

myCSV_reader = LightCSV(
    separator=",",
    quote_char='"',
    field_names = None,
    strict=True,
    has_headers=False
)
```

Available settings:

 * `separator`: character used as separator (defaults to `,`)
 * `quote_char`: character used to quote strings (defaults to `"`).<br />
    This char can be escaped by duplicating it.
 * `field_names`: can be any iterable or sequence of `str` (i.e. a list of strings).<br />
    If set, these will be used as column titles (dictionary keys), and also sets the expected number of columns.</br>
 * `strict`: Sets whether the parser runs in _strict mode_ or not.<br />
    In _strict mode_ the parser will raise a `ValueError` exception if a cell cannot be decoded or column
    numbers don't match. In _non-strict mode_ non-recognized cells will be returned as strings. If there are more
    columns than expected they will be ignored. If there are less, the dictionary will contain also fewer values.
 * `has_headers`: whether the first row should be taken as column titles or not.<br />
    If set, `field_names` cannot be specified. If not set, and no field names are specified, dictionary keys will
    be just the column positions of the cells.

 
## Data types recognized

The parser will try to match the following types are recognized in this order:

 * `None` (empty values). Unlike CSV reader, it will return `None` (null) for empty values. <br />
    Empty strings (`""`) are recognized correctly.
 * `str` (strings): Anything that is quoted with the `quotechar`. Default quotechar is `"`. <br />
    If the string contains a quote, it must be escaped duplicating it. i.e. `"HELLO ""WORLD"""` decodes
    to `HELLO "WORLD"` string.
 * `int` (integers): an integer with a preceding optional sign.
 * `float`: any float recognized by Python
 * `datetime`: a datetime in ISO format (with 'T' or whitespace in the middle), like `2022-02-02 22:02:02`
 * `date`: a date in ISO format, like `2022-02-02`
 * `time`: a time in ISO format, like `22:02:02`
 

If all this parsing attempts fails, a string will be returned, unless `strict_mode` is set to `True`. In the latter
case, a `ValueError` exception will be raised.


## Implementing your own type recognizer

You can implement your own deserialization by subclassing `LightCSV` and override the method `parse_obj()`.

For example, suppose we want to recognize hexadecimal integers in the format `0xNNN...`. We can implement it
this way:

```python
import re
from lightcsv import LightCSV

RE_HEXA = re.compile('0[xX][A-Za-z0-9]+$')  # matches 0xNNNN (hexadecimals)


class CSVHexRecognizer(LightCSV):
    def parse_obj(self, lineno: int, chunk: str):
        if RE_HEXA.match(chunk):
            return int(chunk[2:], 16)
        
        return super().parse_obj(lineno, chunk)
```

As you can see, you have to override `parse_obj()`. If your match fails, you have to invoke `super()` (overridden) 
`parse_obj()` method and return its result.


---

## Why

Python built-in CSV module is a bit over-engineered for simple tasks, and one normally doesn't need all bells
and whistles. With `LightCSV` you just open a filename and iterate over its rows.

Decoding `None` for empty cells is needed very often and can be really cumbersome as the standard `csv`
tries hard to cover many corner-cases (if that's your case, this tool might not be suitable for you).
