# jackTokenizer.py — Jack Lexical Analyzer

## What this is

`jackTokenizer.py` is the first stage of the Jack compiler: it reads raw
`.jack` source text and turns it into a flat stream of tokens, each
classified as one of the 5 lexical categories the Jack grammar defines:
`keyword`, `symbol`, `identifier`, `integerConstant`, `stringConstant`. It
does no parsing and no code generation — its only job is "what are the
individual words and symbols in this file, and what kind is each one."

This file is byte-for-byte identical to `answers/10/jackTokenizer.py`.
That's not an oversight — project 11's compiler is built directly on top
of project 10's syntax analyzer, and tokenizing doesn't change at all
between "just parse it" (project 10) and "parse it and generate code"
(project 11), so there was never a reason for the two copies to diverge.
Because they're separate files rather than a shared import, though, a fix
made to one (like the regex cleanups below) has to be applied to both by
hand.

## How it works

The whole tokenizer is one loop (`parseTokens`) that repeatedly looks at
the *front* of the remaining source text and tries each token pattern in
turn, in this order:

1. **Whitespace** — stripped silently, not emitted as a token.
2. **`// ...` inline comments** and **`/* ... */` multi-line comments** —
   also stripped, not emitted.
3. **String constants** — `"..."` up to the next `"` or newline (Jack
   strings can't contain a literal newline or an escaped quote).
4. **Identifiers and keywords** — one letter/underscore followed by any
   number of word characters; the tokenizer checks the matched text
   against Jack's fixed keyword list to decide which of the two it is.
5. **Symbols** — the fixed set of single-character symbols Jack defines
   (`{ } ( ) [ ] . , ; + - * / & | < > = ~`).
6. **Integers** — one or more digits, range-checked against Jack's
   0–32767 limit (raises `OverflowError` outside that range).
7. Anything left over that matched none of the above is a syntax error.

Each successful match consumes that much text off the front of
`self.jack` and appends a `{"type": ..., "value": ...}` dict to
`self.tokens`. There's no lookahead or backtracking — whichever pattern
matches first at the current position wins, and the loop just keeps
eating characters until the file is empty.

## The `r"..."` raw-string fix

Every regex pattern in this file is written as a **raw string**
(`r"..."` or `r'...'`). This matters because regex uses backslash for its
own purposes (`\d` = digit, `\s` = whitespace, `\w` = word character) that
aren't valid Python string escapes — without the `r` prefix, Python
would warn about "invalid escape sequence" and (for genuinely ambiguous
cases) potentially not do what was intended. `r"..."` tells Python "don't
touch backslashes in this string at all, pass it through exactly as
typed" — which is what you want, since it's `re`'s job to interpret the
backslashes, not Python's.

The one pattern that stays single-quoted
(`r'^(")([^\n]*)(")'`, matching a string constant) is a deliberate
exception, not an inconsistency: that pattern needs to contain a literal
`"` character, and using the *other* quote style to hold a string that
contains the first one is the standard way to avoid escaping it.

## Verification

Both copies of this file (`answers/10` and `answers/11`) are exercised by
their respective `test10.sh`/`test.sh` (via `answers/11`'s own
`test.sh`) — the token stream feeds directly into `_ClassNameT.xml` in
project 10's case, and this file's output is what
`jackCompilationEngine.py` consumes as input in project 11's. Project 10's
suite (`ArrayTest`, `ExpressionLessSquare`, `Square`) matches the official
reference token/parse-tree XML exactly, confirming the tokenizer handles
every lexical construct in those programs correctly.
