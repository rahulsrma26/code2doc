# code2doc

![Upload Python Package](https://github.com/rahulsrma26/code2doc/workflows/Upload%20Python%20Package/badge.svg)

A simple documentation utility that takes the docstring from the files, functions and classes and creates markdown files.

---

## Getting Started

Requires: python 3.6+

### Installing

code2doc is available on [PyPi](https://pypi.org/project/code2doc/) and can be easily installed using pip.

```sh
pip install code2doc
```

If you already have code2doc and want to update to a newer version

```sh
pip install -U code2doc
```

You can get the cutting edge version directly from dev branch (this can be unstable)

```sh
pip install git+https://github.com/rahulsrma26/code2doc
```

---

## Running

Assuming you have all the source code in `src/your_module` directory in the current working directory then you can directory build docs using

```sh
code2doc build -m ./src/your_module
```

Build options can be customized using command line or `code2doc.ini` file. To create `code2doc.ini` file in the current working directory use

```sh
code2doc init
```

For additional help see `code2doc.ini` file and use help commands and sub-commands.

```sh
code2doc -h
```