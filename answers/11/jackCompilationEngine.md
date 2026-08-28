# jackCompilationEngine.py / jackExpressions.py — Jack Compiler Back End

## What this is

`jackCompilationEngine.py` is the second half of the Jack compiler: a
recursive-descent parser that walks the token stream `jackTokenizer.py`
produced and, in a single pass, both *validates the program's structure*
against the grammar in `grammar.txt` and *emits VM code* for it — one
`compileX` method per grammar rule (`compileClass`, `compileClassVarDec`,
`compileExpression`, `compileTerm`, ...), the same shape as project 10's
parser but generating VM commands instead of XML tags.

`jackExpressions.py` is a small helper class used only for expressions —
see "How expressions actually turn into code" below for why it exists
separately.

The end-to-end pipeline (see `answers/08/hackTranslator.md` for what
happens after this): **Jack source → tokens → this file's parse-and-codegen
pass → a flat list of VM commands → `hackTranslator.py` (projects 7/8) →
Hack assembly → the assembler (project 6) → machine code.**

## Symbol tables

Two symbol tables track every variable, each entry storing `kind`, `type`,
`name`, and a running index:

- **`classSymbolTable`** — `field`s and `static`s, reset at the start of
  every class (`compileClass`).
- **`subroutineSymbolTable`** — `argument`s and `local`s, reset at the
  start of every subroutine (`compileClass`'s subroutine loop). For a
  `method`, `compileParameterList` injects an implicit `argument 0` named
  `"this"` before the declared parameters — that's how a method receives
  the object it's operating on.

`lookupVar(name)` checks the subroutine table first (so a local shadows a
field of the same name), then the class table, and returns the VM
"segment index" text to push/pop that variable — `field`s are translated
to `this N` since that's the VM segment fields actually live in.
`lookupVarType(name)` does the same search but returns the variable's
declared *type* instead — used only to resolve method calls (below).

## Subroutine prologues

Three different setups, all in `compileSubroutineBody`, matching what
each kind of subroutine needs before its own statements can run:

| Kind | Prologue | Why |
|---|---|---|
| `constructor` | `push constant {fieldCnt}` / `call Memory.alloc 1` / `pop pointer 0` | allocate a new object sized to hold its fields, point `this` at it |
| `method` | `push argument 0` / `pop pointer 0` | point `this` at the object the *caller* already passed in — no allocation |
| `function` | (nothing extra) | no object involved at all |

## Statements

- **`let`** — for a plain variable, evaluates the RHS then pops it
  straight into that variable's segment (`lookupVar`, with the same
  subroutine-then-class fallback). For `let arr[i] = value`, it computes
  the target address first (`push {index}; push {arr}; add`), evaluates
  the RHS, then does the standard `pop temp 0 / pop pointer 1 / push temp
  0 / pop that 0` dance — stashing the value in `temp` *before*
  repointing `THAT` matters whenever the RHS itself reads through another
  array access, which would otherwise clobber `pointer 1` before the
  target address gets used.
- **`if`/`while`** — straightforward label-based branching.
  `self.IF`/`self.WHILE` counters are reset to 0 at the start of every
  subroutine (matching the reference compiler's numbering), and every
  label gets used exactly once per branch, so there's no risk of a label
  colliding with another one in the *same* function. Different functions
  reusing the same numbers (e.g. every subroutine's first `if` being
  `IF_TRUE0`) is fine — VM labels are function-scoped, and
  `hackTranslator.py`'s label-scoping fix (see its own `.md`) already
  guarantees uniqueness across functions regardless of what raw number a
  Jack compiler happens to pick.
- **`do`** — compiles the subroutine call, then discards its return value
  (`pop temp 0`) since `do` never uses one.
- **`return`** — pushes `constant 0` for a bare `return;` (every Jack
  subroutine must return *something*, even `void` ones), or the actual
  expression's value otherwise.

## How expressions actually turn into code

This is the part that looks different from the rest of the file, and
it's worth understanding *why* it's structured this way.

Jack's grammar treats every binary operator as equal precedence,
evaluated strictly left to right (`expression: term (op term)*`, no
precedence tiers at all) — but that's not simply "stream tokens out in
the order you parsed them," because of parentheses: an operator can
textually precede its second operand when that operand is a parenthesized
sub-expression (e.g. `2 * (3 + 4)` — the `*` appears before the `+` even
gets evaluated). A stack machine needs both operands pushed before the
operator runs, so something has to genuinely reorder tokens into postfix,
not just replay them.

That's `jackExpressions.Expressions`, built while `compileTerm`/
`compileExpression` parse: each term (`addTerm`) gets appended to a flat
list *in parse order*, including literal `(`/`)` tokens. Once a whole
expression is parsed, `getExp()` runs:

1. **`shuntingYard()`** — the classic infix-to-postfix algorithm,
   converting that flat parse-order list into true postfix order. All
   binary operators share one precedence tier here (matching Jack's
   actual no-precedence grammar); unary `-`/`~` (internally `m`/`~`) sit
   at a higher tier so `-x + y` means `(-x) + y`. *(A real PEMDAS-style
   tiered table is kept commented out directly above the active one, in
   case C-like precedence is ever wanted instead of Jack's actual
   semantics.)*
2. **`flattenExp()`** — walks that postfix list depth-first: any term
   with children (an array index expression, or a call's argument list)
   gets its children's code emitted *first*, recursively, before the term
   itself. This also threads `len(child)` through as `nChild` for every
   entry — needed so a `"call"` term's actual argument count survives all
   the way to code generation instead of being silently dropped.

`vmExpression()` then walks that final flat `[data, type, nChild]` list
once and emits the real VM instructions — this is the only place that
actually knows what a `+` or a `call` *means* in VM terms; everything
before it is purely about getting the terms into the right order.

## Term types

| Term type | Meaning | Codegen |
|---|---|---|
| `constant` | integer literal | `push constant N` |
| `string` | string literal | `String.new(len)` then one `String.appendChar(code)` per character, chaining off the object reference each call leaves on the stack |
| `keyword` | `true`/`false`/`null`/`this` | `true`→`push constant 0 / not` (both push `-1`), `false`/`null`→`push constant 0`, `this`→`push pointer 0` |
| `var` | a plain variable reference | `push {lookupVar(name)}` |
| `array` | `varName[expr]` used as a *value* | index is already on the stack (parsed before this term, per the flattening order above) — push the base, `add`, `pop pointer 1`, `push that 0` |
| `unary` | `-`/`~` | `neg`/`not` |
| `symbol` | binary operator | `add`/`sub`/`Math.multiply`/`Math.divide`/`and`/`or`/`lt`/`gt`/`eq` |
| `call` | a subroutine call | see below |

## Method-call resolution

`subroutineCall` in the grammar allows three forms, and `
compileSubroutineCall` has to tell them apart *before* it can decide what
VM code to emit — this is the part of the file that took the most work to
get right:

- **`subroutineName(...)`** (no dot at all) is *always* a method call on
  the current object — `this` isn't in scope any other way, so Jack
  defines a bare call as shorthand for calling one of the current class's
  own methods. Emits `push pointer 0` as an implicit first argument, then
  calls `CurrentClass.subroutineName`.
- **`varName.subroutineName(...)`** where `varName` is a *known* declared
  variable (`lookupVarType` finds it) is a method call on that object —
  pushes the variable itself as the implicit first argument, and calls
  `{declared type}.subroutineName`.
- **`className.subroutineName(...)`** where the leading name *isn't* a
  declared variable is a plain function or constructor call — no implicit
  argument, calls `className.subroutineName` exactly as written.

The implicit-argument push is implemented by **prepending a synthetic
one-term `Expressions` object** (`this` or the variable) to the call's own
`expList`, rather than special-casing it in `vmExpression` — that way the
existing `nChild`-from-`len(expList)` machinery automatically produces the
right argument count with no separate code path.

## Verification

Every one of the above pieces has been checked against the official
reference `JackCompiler.sh`, not just against this file's own logic:
individually via isolated test cases (constructors, methods of all three
call forms, array reads/writes, nested array-to-array assignment, string
constants, `a + b * c`-style precedence), and as a whole — the full
official project 11 test suite (`Average`, `ComplexArrays`,
`ConvertToBin`, `Pong` — 4 classes, `Seven`, `Square` — 3 classes, 11
class files total) compiles to output that matches the reference compiler
**exactly, byte for byte**, as does the hand-written `Try/` suite
(`Terms`, `Function`, `Array`) this project's own `test.sh` runs.

### Bugs found and fixed getting here

For reference, since none of these were obvious from a first read of the
code — each one is here because it was actually caught by tracing through
generated VM code against the reference compiler's, not by inspection
alone:

- `call` always emitted argument count `1` regardless of the actual
  argument list (root cause: `flattenExp` discarding the count).
- Array-indexed terms weren't handled in `vmExpression` at all.
- `var` lookups only checked `subroutineSymbolTable`, so a bare field
  reference inside an expression silently produced no code.
- Real PEMDAS-style operator precedence, when Jack's grammar defines
  none — `a + b * c` computed the wrong number entirely (`a+(b*c)`
  instead of `(a+b)*c`).
- `method`'s prologue was copy-pasted from `constructor` (allocated a
  brand new object instead of using the one passed in).
- `constructor`'s `Memory.alloc` size used the parameter count instead of
  the field count.
- Method calls weren't resolved at all — no receiver pushed, wrong
  (unqualified) call target.
- `let arr[i] = value` computed the index and then ignored it, popping
  the value straight into `arr` itself and destroying the array
  reference.
- String constants were treated identically to integer constants,
  emitting `push constant <the literal text>` — not valid VM code.
