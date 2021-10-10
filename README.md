[![D2Parser Tests](https://github.com/shamrickus/D2Parser/actions/workflows/tests.yml/badge.svg)](https://github.com/shamrickus/D2Parser/actions/workflows/tests.yml)

# D2Parser

Takes in Diablo II source files and parses them into Typescript using python.

## Prerequisites 
* Python 3.9

    * Install dependencies `python -m pip install -r requirements.txt` 

## Running
* `python main.py MOD VERSION` 
  * Glory of Nephilim: `python main.py gon latest`
  * D2LoD (1.14) : `python main.py d2lod 114`
  
## Tests
Tests are written in typescript to allow for easy parsing of the generated ts files. 

### Requirements
* `node.js` 12.x+
* `pnpm` preferred but `npm` works
  

### Running
    pnpm install
    pnpm run test

## Directory Overview
* /versions `// Contains source files for specific game versions`
* /TS `// Where .ts helper files are as well as tests` 

