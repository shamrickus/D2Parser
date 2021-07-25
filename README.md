[![D2Parser Tests](https://github.com/shamrickus/D2Parser/actions/workflows/tests.yml/badge.svg)](https://github.com/shamrickus/D2Parser/actions/workflows/tests.yml)

# D2Parser

Takes in Diablo II source files and parses them into Typescript using python. Currently hard coded around the mod 
[Glory of Nephilim](http://gloryofnephilim.org), but should be accurate for vanilla D2.

## Prerequisites 
* Python 3.9

    * Install dependencies `python -m pip install -r requirements.txt` 

## Running
* `python main.py VERSION` 
  * For Glory of Nephilim it is `python main.py gon`
  
## Tests
Tests are written in typescript to allow for easy parsing of the generated ts files. 

### Requirements
* `node.js` 12.x+
* `pnpm` preferred but `npm` works
  

### Running
    pnpm install
  
    pnpm run test` or `npx mocha

## Directory Overview
* /versions `// Contains source files for specific game versions`
* /TS `// Where .ts helper files are as well as tests` 

