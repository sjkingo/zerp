# Internal design

This document details the internal design of the compiler and virtual machine. It is not
required understanding to use the `zc` and `zvm` programs.

The zerp utilities are split into two parts: the compiler (`zc`), which takes the high-level language Z
and compiles it into a binary format, and the virtual machine (`zvm`), which takes
this binary format and executes it.

## `zc`: the compiler

The Z compiler is a multi-pass compiler that takes the high-level Z code and generates
a binary format ready to be executed by the virtual machine. It builds an abstract syntax tree representing the program.

### Phase 1: lexical analysis

### Phase 2: parsing and AST generation

### Phase 3: reference evaluation 

### Phase 4: semantic analysis

### Phase 5: code generation

## `zvm`: the virtual machine
