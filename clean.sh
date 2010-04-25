#!/bin/bash
find . -name \*.orig -exec rm {} \;
find . -name \*.pyc -exec rm {} \;
rm -f compiler/parser.out compiler/out/*
