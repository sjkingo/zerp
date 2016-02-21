# zerp - a collection of utilities for Z

zerp is a collection of utilities for Z, a toy programming language similar in
syntax to Python and Pascal. It targets a virtual machine written in Python
that supports a limited instruction set.

For more information on Z, see the [language reference](docs/Z.md). The internals of
the compiler and virtual machine are discussed in the [design document](docs/DESIGN.md).

zerp targets Python 3.4+ only.

## Dependencies

Before using `zvm`, you must make sure your Python installation contains Tkinter. On Fedora,
this will be:

```
$ sudo dnf install python3-tkinter
```
