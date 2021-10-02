# SimpleCSV

Simple CSV reader

This CSV reader is implemented in just pure Python. It allows to specify a separator, a quote char and
column titles (or get the first row as titles). Nothing more, nothing else.

## Usage

Usage is pretty straightforward:

```python
from simplecsv import SimpleCSV

for row in SimpleCSV().read_file("myfile.csv"):
    print(row)
```

This will open a file named `myfile.csv` and iterate over the CSV file returning each 
row as a key-value dictionary.

You can supply your own stream (i.e. an open file instead of a filename):
```python
from simplecsv import SimpleCSV

with open("myfile.csv") as f:
    for row in SimpleCSV().read(f):
        print(row)
```

 
## Data types recognized

The following types are recognized:

 * `None` (empty values). Unlike CSV reader, it will return `None` (null) for empty values. <br />
    Empty strings (`""`) are recognized correctly. Read below
 * `str` (strings): Anything that is quoted with the `quotechar`. Default quotechar is `"`. <br />
    If the string contains a quote, it must be escaped duplicating it. i.e. `"HELLO ""WORLD"""` decodes
    to `HELLO "WORLD"` string.
 * `int` (integers): an integer with a preceding optional sign.
 * `float`: any float recognized by Python
 * `datetime`: a datetime in ISO format (with 'T' or whitespace in the middle), like `2022-02-02 22:02:02`
 * `date`: a date in ISO format, like `2022-02-02`
 * `time`: a time in ISO format, like `22:02:02`
 

---

## Why

Python built-in CSV module is a bit over-engineered for simple tasks,
and one normally doesn't need all bell and whistles. Just open a filename and iterate over its rows.
