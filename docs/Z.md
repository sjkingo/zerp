# Z, a toy programming language

Z is a toy programming language that was designed so the zerp compiler had a
higher-level language to implement. You could say that is the bastard love
child of Python and Pascal, though C might have something to say there as some
of its syntax was borrowed from it too. It evolved out of the need for a
language that is easy to parse, whilst retaining the "feel" of a real language
(unlike PL/0 which is just horrific -- sorry Niklaus).

## A Z program

A Z program is simply a series of constructs present in a .z file. This is the
top-level construct that the compiler knows about. When compiling your program,
you would pass this file to the compiler. Since there is no way to "link"
multiple programs, a .z file will contain the entire routines for a single
program.

## Functions

The only construct that may appear in the top-level Z program is a function, of
which there may be more than one (but certainly not zero!). This means that all
other constructs must live inside a function. To differentiate between
functions, each function must have a globally unique name. One such function
must be named "main" (without the quotes). This is similar to a C/C++ program.
This main function is the entry point for the program -- it is the first thing
the virtual machine jumps to when executing your compiled program.  Execution
flows on from there (hence the term "execution flow").

Inside this execution flow other functions can be called, that is, the
execution jumps to the start of the named function and jumps back to the
original call when finished. This allows a program to be broken up into smaller
procedures that work together to perform a task.

Z does not distinguish between a function definition and a declaration (unlike
C/C++) as (similar to Python) it does not mind if you reference a function
(not a variable -- see below) before it is defined. It is perfectly valid to
write:

```
call foo()
...
# foo() is defined here, after the call
```

(See the 'Calling functions' section for information on the 'call' keyword.)

The grammar rule for a function is given in EBNF:

```ebnf
function = 'begin' ident '(' ')' block 'end'
```

The function name is given by the "ident" non-terminal. An example of a
conforming function could be:

```
begin main()
end
```

Note that since "block" may be empty (see below), the above is still perfectly
valid, although completely useless (as the function does not actually do 
anything but return immediately).

## Built-in functions

Z has some predefined functions that are built in to the language. These 
allow the user to simplify some common tasks, such as printing to the screen.
Since each built-in function's name is a reserved keyword, you cannot reuse it.
This means defining a function called 'print' is an error in the language and
the compiler won't be too happy with you.

## Blocks

A block is simply a list of statements that can appear after each other. It
is just shorthand for writing "list of statements". Written in EBNF, this is:

```ebnf
block = { statement } | e
```

Note a block may be empty (that is, has no statements). This was the form
of the main function example above.

## Statements

A statement is one of the very useful constructs in Z. Without them, a program
would not be able to do anything! A statement is defined as a series of
expressions terminated by a semicolon. This follows the exact same rules that
C/C++ has, where the semicolon is a statement separator.

For instance the following are all statements:

```
1;
2 + 4;
i + 1;
print(i);
```

Note that each statement is terminated by a semicolon. The last line uses the
built-in function 'print' to print the *value* of i (which is assumed to be a
variable, but that is purely semantics) to the screen. Any valid expression
may be used in a statement, which leads us to the most basic syntax:

```ebnf
statement = { expression ';' }
```

We will revisit this later though, as there are more constructs that may
appear in a statement that we haven't defined yet.

## Calling functions

To actually execute a function one must call it. This applies to both 
built-in and user-defined functions, except for main. Recall that the compiler
knows that the function named "main" is the entry point to the program -- it
will call this function for you at the very start. Everything else is up to the
programmer.

Consider the grammar rule for a function call:

```ebnf
function_call = ident '(' [ expression { ',' expression } ] ')'
```

The following are valid function calls (assuming the names they reference
exist):

```
foo()
foo(1)
foo(1, i)
foo(goo(), 1, 2)
foo(goo(1), 2)
```

Note that there is no terminating semicolon at the end -- this is because a
function call is simply an expression, and may be used as such. This means the
following *statement* is perfectly valid:

```
1 + foo(i) + k;
```
