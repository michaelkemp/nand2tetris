# Math.jack — OS Math Library

## What this is

`Math.jack` is the OS class the Jack compiler silently depends on: every
`*` and `/` in a Jack program compiles to `call Math.multiply 2` / `call
Math.divide 2` (you can see this yourself in `answers/11/jackCompilationEngine.py`'s
`vmExpression`), because the Hack ALU has no multiply or divide
instruction at all — only add, sub, and, or, neg, not. This class is what
makes `*` and `/` actually work.

All the algorithms here are the ones taught in `docs/project-12.pdf`
(slides 20-45), not independently invented — each is called out below
with which slides it came from.

## Fields

- `n` — 16, the number of bits in a Hack integer.
- `powersOfTwo` — a precomputed `Array` holding `2^0 .. 2^(n-1)`, built once
  in `init` and reused by every function that needs to test or construct
  individual bits.

## `init()`

Builds `powersOfTwo` by doubling *via addition*, not multiplication —
`multiply` doesn't exist yet at the point `init` runs (it's the thing
`init` is helping to build), so `powersOfTwo[i] = powersOfTwo[i-1] +
powersOfTwo[i-1]` is the only option, and it's exactly correct since
doubling is just adding a number to itself.

## `bit(x, j)`

Not part of the public API slide (it's a private helper, slide 41's
suggested approach) — returns whether bit `j` of `x` is set, by AND-ing
against `powersOfTwo[j]` (which has exactly one bit set) and checking the
result isn't zero. Jack has no `<>` operator, so "is nonzero" is written
as `~(... = 0)`.

## `multiply(x, y)` — slides 23-24, 40-41

"Long multiplication": for each bit `i` of `y` that's set, add `x`
shifted left by `i` places to a running sum. `x` is never actually
shifted with a shift operator (Jack doesn't have one) — instead
`shiftedX` starts at `x` and gets doubled (`shiftedX + shiftedX`) once per
loop iteration, which has the same effect.

This always runs exactly `n` (16) iterations, regardless of how large `y`
is — as opposed to the naive "repeated addition" approach (add `x` to
itself `y` times), which the slides show as the "before" example: correct,
but could take up to 32767 iterations for the largest possible `y`.
Multiply's runtime here is effectively O(1) rather than O(y).

Signed inputs need no special handling here (slide 40): two's complement
arithmetic makes the bit-by-bit shift-and-add algorithm produce the
correct signed result without any extra sign bookkeeping, unlike divide
and sqrt below.

## `divide(x, y)` / `divideNonNeg(x, y)` — slides 36, 42

The public `divide` is a thin wrapper: since the actual division
algorithm (`divideNonNeg`) only works for non-negative operands, `divide`
figures out whether the true answer should be negative (`x` and `y` have
different signs), calls `divideNonNeg` on `|x|` and `|y|`, and negates the
result if needed.

`divideNonNeg` is recursive, based on the identity `x/y = 2*((x/2)/y)`:
it doubles `y` on every recursive call until `y` grows past `x` (the base
case), then unwinds, at each level deciding whether the final quotient's
next bit should be 0 or 1 by checking whether `x - 2*q*y` (the remainder
so far) is still `< y`.

**The overflow case (slide 42, "Handling overflow of y"):** since `y`
doubles every call, it can eventually exceed the largest representable
positive value and wrap around to a negative number in Hack's 16-bit
two's complement representation. The slides' fix — checking `y < 0` as an
*additional* base case, right alongside `y > x` — is exactly what's
implemented here, and it's the specific thing the official `MathTest`'s
`32766 / (-32767)` case exercises (see the "Verified" section below).

**Division by zero** isn't addressed by the slides at all — tracing
`divideNonNeg(x, 0)` shows why it matters: `y > x` is false for any
non-negative `x`, `y < 0` is false (0 isn't negative), so it would recurse
forever doubling 0. `divide` guards this itself with `if (y = 0) { do
Sys.error(3); }`, matching the error code the official reference OS uses
for this exact case (confirmed by reading `tools/OS/Math.vm` directly).
This is currently a placeholder: `Sys.jack` is still an empty stub with no
`return` at all, so right now this call would fall through into whatever
function happens to follow it in memory rather than actually halting.
Not something to exercise until `Sys` is implemented.

## `sqrt(x)` — slides 38, 43

Binary search for the largest `y` such that `y*y <= x`, built one bit of
`y` at a time from the top (`j = n/2 - 1`) down to `0`. `y` only ever
needs `n/2` (8) bits, since `y*y` has to fit back into `n` (16) bits.

**The overflow case (slide 43):** the candidate `(y + 2^j)^2` can itself
overflow and wrap negative for large `x` near the top of the representable
range — a valid square is never negative, so `approxSquared > 0` catches
exactly this case and is checked alongside the `<= x` comparison. Without
it, an overflowed (negative) square would look like it satisfies `<= x`
and get accepted incorrectly.

## `max`/`min`/`abs`

No algorithm needed — direct comparisons. `abs` is also used internally by
`divide`'s sign-handling wrapper.

## Verified

Every function was checked two ways: **codegen** (this project's compiler,
`answers/11`, produces output that matches the official reference
`JackCompiler.sh` exactly, byte for byte) and **runtime** (compiled,
linked against the official pre-built OS for every other class, and
actually executed in the real VM Emulator — not just compared as text).

The full official `MathTest` (`projects/12/MathTest`) passes end to end:
`"Comparison ended successfully"` against its real reference `.cmp` file,
covering every function in this class together, including the exact
overflow-boundary case (`32766 / (-32767)`) the `divide` overflow guard
exists for.
