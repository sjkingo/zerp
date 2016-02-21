# zerp - a collection of utilities for Z

zerp is a collection of utilities for Z, a toy programming language similar in
syntax to Python and Pascal. It targets a virtual machine written in Python
that supports a limited instruction set.

For more information on Z, see the [language reference](Z.md).

zerp targets Python 3.4+ only.

## Dependencies

Before using `zvm`, you must make sure your Python installation contains Tkinter. On Fedora,
this will be:

```
$ sudo dnf install python3-tkinter
```

## Design

zerp is split into two parts: the compiler `zc`, that takes the high-level language
and compiles it into an assembled format, and the virtual machine, `zvm`, which takes
this assembled format and executes it.

### `zc`: the compiler

The Z compiler is a multi-pass compiler that takes the high-level Z code and generates
an assembled format ready to be executed by the virtual machine.

#### Phase 1: lexical analysis

#### Phase 2: parsing and AST generation

#### Phase 3: reference evaluation 

#### Phase 4: semantic analysis

#### Phase 5: code generation

### `zvm`: the virtual machine
