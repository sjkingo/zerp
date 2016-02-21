# `zc` and `zvm` internal design

This document details the internal design of the compiler and virtual machine. It is not
required understanding to use the `zc` and `zvm` programs.

zerp is split into two parts: the compiler `zc`, that takes the high-level language
and compiles it into an assembled format, and the virtual machine, `zvm`, which takes
this assembled format and executes it.

## `zc`: the compiler

The Z compiler is a multi-pass compiler that takes the high-level Z code and generates
an assembled format ready to be executed by the virtual machine.

### Phase 1: lexical analysis

### Phase 2: parsing and AST generation

### Phase 3: reference evaluation 

### Phase 4: semantic analysis

### Phase 5: code generation

## `zvm`: the virtual machine
