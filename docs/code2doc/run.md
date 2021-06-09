# run 

This is the entry point for the commands. Currently, it supports three sub-commands: init, build, and clean.

---

Dependencies: 
* from build_config import BUILD_CONFIG, Options 
* from builder import DocBuilder 
* from renderer.renderer import MdRenderer 
* from generator import Generator 

Functions: 
* [build](#build) 
* [clean](#clean) 
* [get_config_path](#get_config_path) 
* [init](#init) 
* [main](#main) 

---

## build 
`build (args)`

Build the docs by generating markdown files. Options can be passed
via command-line args or by code2doc.ini file.

Preference is:  
command-line args > code2doc.ini > default command-line args 

---

## clean 
`clean (args)`

Removes all the doc file(s) created by the config file. It also remove
all the empty folders in its sub-directories. 

---

## get_config_path 
`get_config_path ()`

Helper function that returns the config-file path in the present working directory. 

---

## init 
`init (args)`

This will create default code2doc.ini file in the present working directory. 

---

## main 
`main ()`

Entry function for the module. Create arg-parser and all of the sub-parsers. 

---
