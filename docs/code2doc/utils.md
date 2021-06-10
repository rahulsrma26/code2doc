# utils 

## Utility module

Contains different common helper functions.

---

Functions: 
* [read_file](#read_file) 
* [reindent](#reindent) 

---

## read_file 
`read_file (path: str) -> str`

Reads a file and return it's content as a string. 

---

## reindent 
`reindent (s: str, min_spaces: int = 0, trim_lines: bool = True) -> str`

This reindents text by keeping only the minimum level of indentation.

* s: str  
    markdown text which is needed to be reindented.
* min_spaces: int  
    minimum number of spaces to be added as a prefix after reindentation. 

---
