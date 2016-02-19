# zerp - a collection of utilities for Z

zerp is a collection of utilities for Z, a toy programming language similar in syntax to Python and Pascal. It targets a virtual machine written in Python that supports a limited instruction set.

For more information on Z, see the [language reference](Z.md).

## Design

zerp is split into two parts: the compiler `zc`, that takes the high-level language
and compiles it into an assembled format, and the virtual machine, `zvm`, which takes
this assembled format and executes it.

### `zc`: the compiler

### `zvm`: the virtual machine
