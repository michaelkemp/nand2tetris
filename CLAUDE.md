# nand2tetris

Working through [nand2tetris](https://www.nand2tetris.org/) (*The Elements of
Computing Systems*, Nisan & Schocken) — build a general-purpose computer from
NAND gates up through an OS and a compiler, in 13 projects across two parts.

## Course structure

**Part 1 — Hardware (projects 1–6):** boolean logic → ALU → sequential chips
(registers, RAM) → CPU → the Hack machine language → an assembler.

**Part 2 — Software (projects 7–13):** a stack-based VM (arithmetic +
memory-access commands, then program flow + function calls) → the Jack
language (compiler front end: tokenizer + parser, then full code generation)
→ the Jack OS (a standard library written in Jack itself, compiled by your
own compiler). Project 13 is a wrap-up/retrospective, no new build.

| # | Topic |
|---|---|
| 1 | Boolean logic gates (Nand → And, Or, Mux, DMux, ...) |
| 2 | Boolean arithmetic (Half/Full Adder, ALU) |
| 3 | Sequential logic (Bit, Register, RAM8/64/512/2K/4K/16K, PC) |
| 4 | Machine language (Hack assembly: mult.asm, fill.asm) |
| 5 | Computer architecture (Memory, CPU, Computer chip) |
| 6 | Assembler (Hack assembly → binary) |
| 7 | VM I: stack arithmetic + memory access |
| 8 | VM II: program flow (goto/if-goto/label) + function calls |
| 9 | High-level programming in Jack (write a small Jack program) |
| 10 | Jack syntax analyzer (tokenizer + parse tree, no code gen) |
| 11 | **Jack compiler (full code generation to VM code) ← currently here** |
| 12 | Jack OS (Math, String, Array, Output, Screen, Keyboard, Memory, Sys) |
| 13 | Wrap-up |

## Repo layout

- `projects/NN/...` — official course-supplied skeletons and test `.jack` /
  `.vm` / `.asm` files for project NN (untouched course material).
- `answers/NN/...` — my solutions for project NN, mirroring the same
  subfolder names as `projects/NN`.
- `tools/` — the official Java toolchain (nand2tetris "software suite"):
  `Assembler.sh`, `CPUEmulator.sh`, `HardwareSimulator.sh`, `VMEmulator.sh`,
  `JackCompiler.sh` (the reference Jack compiler, used to diff against my
  output), `TextComparer.sh`, and `tools/OS/*.vm` (the pre-built OS library
  used when running compiled Jack programs before project 12 replaces it).
- `README.md` — my own index of course video links per project.
- `grammar.txt` — the full Jack lexical + syntactic grammar (see below).
- `asm.txt`, `boolean.txt` — my scratch notes from the hardware half.
- `tests/` — misc test assets.

## The Jack language

Jack is a simple, Java-like, object-based language (no inheritance, no
interfaces) designed to compile down to the VM language from projects 7–8.

- **Types:** `int`, `char`, `boolean`, `void`, and class names (objects,
  arrays are just `Array`, a built-in class).
- **Class members:** `static` and `field` variables; `constructor`,
  `function` (static method), and `method` (instance method) subroutines.
- **Statements:** `let`, `if`/`else`, `while`, `do`, `return` — that's it,
  no `for`, `switch`, `break`/`continue`.
- **Expressions:** left-to-right with a single precedence level for the
  binary ops `+ - * / & | < > =` (Jack has **no operator precedence** —
  `2 + 3 * 4` parses as `((2+3)*4)`... except this repo's compiler
  deliberately adds real precedence via a Shunting-Yard pass, see below).
  Unary `-` and `~`, keyword constants `true false null this`.
- **No native arrays/strings at the language level** — `Array` and `String`
  are ordinary Jack classes backed by the OS (project 12).
- Full grammar (lexical elements + program structure + statements +
  expressions) lives in `grammar.txt` at repo root — treat it as the
  authoritative spec when in doubt about syntax.

### Jack → VM compiler pipeline (what projects 10–11 build)

1. **Tokenizer** — strip whitespace/comments, emit a flat token stream of
   `{type, value}` where type ∈ keyword/symbol/integerConstant/
   stringConstant/identifier.
2. **CompilationEngine** — recursive-descent parser driven directly by the
   grammar in `grammar.txt`, one `compileX` method per grammar rule.
3. **Code generation (project 11 only)** — while parsing, maintain two
   symbol tables (class-level: `static`/`field`; subroutine-level:
   `argument`/`local`, each with a running index) and emit VM commands.
   VM segment mapping: `static`→`static`, `field`→`this`, `argument`→
   `argument`, `local`→`local`; `this`/`that` pointers via `pointer 0/1`;
   scratch via `temp`. Every `if`/`while` needs uniquely-numbered labels.
   Constructors call `Memory.alloc` for the object's field count and
   `pop pointer 0`; methods receive the object as implicit argument 0 and
   also `pop pointer 0` it; functions do neither.

## Current solution architecture (`answers/11`)

This compiler deviates from the textbook's usual "emit VM code inline while
parsing top-down" approach — **that's an intentional design choice, not a
mistake**, so don't propose collapsing it back to naive inline emission
without reason:

- `jackTokenizer.py` — regex-based tokenizer, same shape as project 10's.
- `jackCompilationEngine.py` — recursive-descent parser. For statements it
  emits VM code directly (`compileLet`/`If`/`While`/`Do`/`Return`). For
  **expressions** it does NOT emit inline; instead each expression is built
  as a tree of `jackExpressions.Expressions` objects (`compileTerm`/
  `compileExpression` just call `.addTerm(...)`).
- `jackExpressions.py` — takes that raw term list and runs a **Shunting-Yard
  algorithm** (`shuntingYard`) to reorder it into proper postfix (RPN) order,
  correctly respecting `* /` > `+ -` > comparisons > `& |` precedence and
  unary minus/not — which the Jack grammar itself doesn't require but this
  implementation adds anyway. `flattenExp` then linearizes the postfix tree
  (depth-first over `child` arrays, e.g. array-index sub-expressions and
  call-argument sub-expressions) into a flat `[[data, type], ...]` list.
- Back in `jackCompilationEngine.py`, `vmExpression()` walks that flat
  postfix list once and appends the actual VM instructions (push
  constant/var, arithmetic ops → `add`/`sub`/`call Math.multiply 2`/etc.,
  keyword constants, subroutine `call`).
- `main.py` — CLI: `main.py file.jack` or `main.py dir/` → prints VM code to
  stdout (redirected to `_Name.vm` by the caller).
- `test.sh` — for each fixture in `Try/`, runs my compiler and the reference
  `../../tools/JackCompiler.sh`, then `diff -w`s the two `.vm` outputs.
  `Try/` holds hand-written mini `.jack` files (`Terms`, `Function`,
  `Array`) plus their expected `.vm` output for fast local iteration,
  separate from the full `projects/11/*` fixtures (Average, Pong, Square,
  ComplexArrays, ConvertToBin, Seven) used for the real project checkpoint.

### Known WIP gaps in code-gen (as of last read-through)

Useful to know before debugging further — none of this is exhaustive, just
what stood out:

- `vmExpression`'s `"call"` case always emits `call {name} 1`, ignoring the
  actual `expList` argument count and not distinguishing function vs. method
  calls (methods need the receiver object pushed as an extra argument and
  the class name resolved from the variable's declared type).
- `"var"` lookup in `vmExpression` only checks `subroutineSymbolTable`; the
  `classSymbolTable` fallback (for fields/statics referenced mid-expression)
  is commented out — `compileLet`'s assignment side does check both tables
  correctly, so the two code paths are currently inconsistent.
- `"constant"` in `vmExpression` treats `stringConstant` the same as
  `integerConstant` (no `String.new`/`String.appendChar` sequence emitted).
- Array-indexed terms (`type == "array"` from `compileTerm`) aren't handled
  in `vmExpression` yet (no `that` pointer setup).
- In `compileSubroutineBody`, both `constructor` and `method` push
  `self.argumentCnt` into `Memory.alloc` — for constructors this should be
  the object's **field count** (`self.fieldCnt`), not its argument count.

## Testing / running

- Compare against the reference compiler: `cd answers/11 && ./test.sh`
  (needs a JVM on PATH for the `tools/*.sh` wrappers).
- To actually execute compiled output, load the produced `.vm` files (plus
  `tools/OS/*.vm` for library calls) into `tools/VMEmulator.sh`.
- Earlier projects follow the same `answers/NN` vs `projects/NN` pattern;
  e.g. the VM translator lives in `answers/07` and `answers/08`.
