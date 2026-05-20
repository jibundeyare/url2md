# url2md

`url2md` is a python script that takes urls as input and outputs links
in markdown format.

The script accepts a single url, mutiple urls or the name of a text file
containing one or more urls.
In the file, empty lines and lines starting with a sharp symbol are
ignored.
Urls are printed to stdout and errors are printed to stderr.

## Install

```
git clone https://github.com/jibundeyare/url2md
cd url2md
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.lock
# or
pip install -r requirements.txt
```

## Usage

Enable venv:

```
source .venv/bin/activate
```

Get markdown for a single url:

```
$ python url2md.py https://python.org/
[Welcome to Python.org](https://python.org/)
```

Get markdown for multiple urls:

```
$ python url2md.py https://python.org/ https://docs.python.org/ https://realpython.com/
[Welcome to Python.org](https://python.org/)
[3.13.5 Documentation](https://docs.python.org/)
[Python Tutorials – Real Python](https://realpython.com/)
```

Get markdown for multiple urls stored in a text file:

```
$ python url2md.py urls-test.txt
[Welcome to Python.org](https://python.org/)
[3.13.5 Documentation](https://docs.python.org/)
[Python Tutorials – Real Python](https://realpython.com/)
```

Redirect links and errors to a single file:

```
$ python url2md.py urls-test.txt > urls-test.md 2>&1
```

Redirect links to a file and errors to another file:

```
$ python url2md.py urls-test.txt > urls-test.md 2> errors.log
```

