# String.jack — OS String Library

## What this is

Jack has no native string type — `String` is an ordinary Jack class,
backed by a plain `Array` of character codes plus a couple of bookkeeping
fields. Both `Output.jack` and `Keyboard.jack` were written against this
class's API before it existed (see their own `.md` files); this is what
finally makes `printString`/`readLine`/`readInt` runtime-testable.

## Fields

- `chars` — the character buffer, an `Array`. Only allocated when
  `capacity > 0` (see below).
- `capacity` — the fixed maximum length passed to `new`, never changes.
- `len` — the current length; grows with `appendChar`, shrinks with
  `eraseLastChar`, reset by `setInt`.

`capacity` and `len` are deliberately not called `maxLength`/`length` —
the public API already has a `length()` *method*, and a field can't share
a name with a method in the same class.

## `new(maxLength)` / `dispose()`

`maxLength < 0` → `Sys.error(14)` (this and every other error code below
were confirmed by reading `tools/OS/String.vm` directly, not guessed).
`chars` is only allocated when `maxLength > 0` — a zero-length string
never needs a backing array, and skipping the allocation avoids the
`Memory.alloc` size-must-be-`>=1` restriction other classes already run
into (see `Memory.md`). Because `len` starts at `0`, `charAt`/`setCharAt`
can never actually dereference an unallocated `chars` for such a string —
their own bounds check (`j < len`) would reject every `j` first.

`dispose` mirrors that: only disposes `chars` if `capacity > 0` (checking
`capacity`, not `chars`, for the same reason `new` does — an
unallocated `chars` on a zero-capacity string is unpredictable, and
`capacity` reliably reflects whether an allocation ever happened).

## `length`, `charAt`, `setCharAt`, `appendChar`, `eraseLastChar`

Direct array manipulation, no algorithm beyond bounds-checking:

- `charAt`/`setCharAt`: `j < 0` or `j` not `< len` → `Sys.error(15)` /
  `Sys.error(16)`. Valid range is `0 <= j < len` — note this is length,
  not capacity; you can't read or write past what's actually been
  written, even if there's spare capacity.
- `appendChar`: `len = capacity` (buffer full) → `Sys.error(17)`.
  Otherwise writes at `chars[len]` and increments `len`.
- `eraseLastChar`: `len = 0` (nothing to erase) → `Sys.error(18)`.

One thing worth flagging for anyone used to other languages: Jack has no
`>=`/`<=` operators at all (confirmed the hard way — the reference
compiler rejected `j >= len` outright, while this project's own compiler
silently accepted it and miscompiled it into something else entirely,
since it doesn't validate operator sequences the reference does). `j >=
len` has to be written as `~(j < len)`.

## `intValue()` — the string2Int algorithm

Following the documented algorithm (course slide 135) plus the two
extensions its own worked example implies (round-tripping `setInt`/
`intValue` needs to handle the sign, and the API doc promises stopping
"until a non-digit character is detected", which the bare pseudocode
doesn't show): if the first character is `-`, remember that and start
reading from index `1`. Then walk characters left to right, accumulating
`value = value*10 + digit`, stopping the moment a non-digit is hit (a
`done` flag stands in for `break`, which Jack doesn't have). Negate the
result at the end if the sign was seen.

## `setInt(val)` / `int2String(val)` — the int2String algorithm

The course slide gives this as a **recursive** algorithm: for a
non-negative `val`, recurse on `val/10` first, then append the last
digit's character (`val % 10`, i.e. `val - (val/10)*10` — no mod operator
in Jack). That ordering is exactly what makes it work with a single
growing string rather than needing to build digits in reverse and flip
them afterward: the recursion bottoms out at the *most significant*
digit first (`val < 10`), and each level appends its own digit only
*after* the recursive call returns — so `appendChar` calls happen in
left-to-right order for free.

`setInt` is the public wrapper: rejects a zero-capacity string
(`Sys.error(19)`, matching the reference), resets `len` to `0` (reusing
the same string across repeated `setInt` calls rather than requiring a
fresh one each time), handles the sign by appending `-` before handing
off to the non-negative recursive helper, same pattern `Math.divide` uses
for its own sign handling.

**Deliberately not matching the reference here:** `tools/OS/String.vm`'s
actual `setInt` is considerably more involved — it builds digits into a
scratch buffer in reverse, checks the total digit count against capacity
*before* writing anything (so an overflow fails cleanly with no partial
result), then copies them into the real buffer in the correct order and
disposes the scratch array. That's a real, more defensive design, not
just an optimization — but it isn't what the slide asks for, and this
project's established practice throughout (`Math`, `Memory`, `Screen`) is
to implement the documented algorithm rather than reverse-engineer the
reference's own internal choices. One practical consequence of that
choice: if `setInt` overflows a string's capacity here, it fails
*partway through* (via `appendChar`'s own `Sys.error(17)`, after already
writing however many digits fit) rather than failing cleanly up front.

**Known platform limitation, not specific to this implementation:**
`setInt(-32768)` (the most negative 16-bit value) breaks the same way
`Math.abs` already documents — negating `-32768` overflows back to
`-32768` itself in two's complement, so the sign gets detected correctly
but the digit-recursion still operates on a negative number. Not
special-cased here, consistent with how the same edge case is already
handled (by not being handled) elsewhere in this codebase.

## `newLine()` / `backSpace()` / `doubleQuote()`

Return `128`, `129`, `34` — exactly the hardcoded literals `Output.jack`
and `Keyboard.jack` were already using in place of these calls (see their
own `.md` files for why). Now that this class exists, those two files
could call `String.newLine()`/`String.backSpace()` directly instead — not
done yet, left as a follow-up since it's a pure substitution with no
behavior change.

## Verified

- **Codegen**: matches the official `JackCompiler.sh` exactly, line for
  line (331/331 lines, no diff) — after fixing two real bugs the
  reference compiler caught that this project's own compiler didn't: the
  invalid `>=` operator above, and assigning an arithmetic `int`
  expression to a locally-declared `char` variable (the reference
  compiler type-checks this; this project's own compiler doesn't).
- **Runtime**, linked against this project's own `Math`/`Memory`/`Array`/
  `Screen`/`Output`/`Keyboard` (official `Sys` only, for bootstrapping):
  - Built `"hello"` via repeated `appendChar`, checked `length`/`charAt`
    at both ends, `setCharAt` to change the first character, then
    `eraseLastChar` and re-checked the length.
  - `intValue`: `"314"` → `314`, `"-8"` → `-8`, `"12x3"` → `12` (stops at
    the `x`).
  - `setInt`: `314` → length `3`, characters `'3'`,`'1'`,`'4'`; `-42` on
    the *same* string object afterward → length `3`, `'-'`,`'4'`,`'2'`
    (confirming `len` resets correctly between calls, not just the first
    time); `0` → length `1`, `'0'`.
  - All six error paths (`new(-1)`, `charAt`/`setCharAt` out of bounds in
    both directions, `appendChar` overflow, `eraseLastChar` on empty,
    `setInt` on a zero-capacity string) confirmed to halt via `Sys.error`,
    alongside a matching valid-input control case confirmed to *not*
    halt.
