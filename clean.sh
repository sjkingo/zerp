#!/bin/bash
find . -name \*.orig -exec rm {} \;
find . -name \*.pyc -exec rm {} \;
find . -name z.out -exec rm {} \;
rm -f compiler/parser.out compiler/parsetab.py
