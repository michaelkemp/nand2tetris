# Screen.jack — OS Screen Library

## What this is

`Screen.jack` draws to the memory-mapped screen: 512×256 pixels starting at
`RAM[16384]`, 32 sixteen-bit words per row (`screenBase + 32*y + x/16`, bit
`x mod 16` within that word — slide 69). Everything else in this class is
built on that one formula.

## Fields

- `color` — `true` (black) or `false` (white), set by `setColor`, used by
  every draw function.
- `twoToThe` — a private bit-mask table, same idea as `Math`'s own (not
  reused directly since that one is private to `Math`). Sized **17**, not
  16: `twoToThe[16]` is deliberately left to overflow to `0` (doubling
  `twoToThe[15] = -32768` wraps to `0` in 16-bit two's complement). That
  overflow is used on purpose in `drawHorizontal` — see below.
- `screenBase`, `maxX`, `maxY` — named once here instead of repeating the
  literals (`16384`, `511`, `255`) at every call site.

## `clearScreen()`

Always clears to white (`0`), **regardless of the current color** — it
doesn't check `color` at all, it just pokes literal `0` to every one of
the 8192 words that make up the screen. Confirmed this is the intended
behavior, not an oversight: the official reference OS's own `clearScreen`
does exactly the same thing (read directly from `tools/OS/Screen.vm` — no
check against its color flag anywhere in the function). So `setColor(true)`
followed by `clearScreen()` still gives a white screen.

This already operates at word granularity, not pixel granularity — its
loop index walks the 8192 word offsets directly (`screenBase + i`), one
`Memory.poke` per full 16-bit word, same as the reference. There's no
bulk-memory primitive in Jack to do better than one `poke` per word.

## `drawPixel(x, y)` — slide 69

The direct formula: compute the word offset (`x/16`), read that word, set
or clear bit `x mod 16` of it (via `twoToThe[bit]`), write it back through
`updateLocation`. No mod operator in Jack, so `x mod 16` is
`x - (x/16)*16`.

An earlier version of this computed `x/16` **twice** — once inline for the
address, once inline for the bit index — a pure duplicate `Math.divide`
call for the same value. Fixed to compute it once into a local and reuse
it for both, matching the official reference's own `drawPixel` exactly
(confirmed by reading `tools/OS/Screen.vm`: it computes the divide into a
local once too, then reuses it the same way).

## `updateLocation(address, mask)` / `drawHorizontal(y, xa, xb)`

**Why these exist:** filling a horizontal run of pixels by calling
`drawPixel` once per pixel recomputes `32*y` (a `Math.multiply` call) and
`x/16` (a `Math.divide` call) from scratch for *every single pixel*, even
though `y` is constant across the whole run and `x/16` only actually
changes once every 16 pixels. This turned out to be the real cost driver
in this implementation: a filled circle calls `drawLine` once per row, and
each of those calls used to loop `drawPixel` across the row's full width.
Measured directly — a single `drawCircle(255, 127, 35)` (radius 35, one of
the smaller circles the OS can draw) needed on the order of 150-200 million
VM-emulator steps with the naive per-pixel loop, taking ~24 real seconds in
`VMEmulator.sh`, purely from the repeated multiply/divide overhead.

**The fix**, confirmed to be exactly what the official reference OS does
too (`tools/OS/Screen.vm`'s own `Screen.drawHorizontal`, `Screen.
updateLocation` — read directly, not guessed): compute the row's base
address and the two edge bit-masks **once**, then fill whole 16-bit words
at a time instead of one bit at a time:

1. `left`/`right` = the run's two endpoints, sorted (`Math.min`/`max`, so
   callers don't need to pre-sort — `drawLine` doesn't, since its `dx<0`
   case can call this with `xa > xb`).
2. `startWord = left/16`, `endWord = right/16` — one `Math.divide` call
   each, not one per pixel.
3. `leftMask = ~(twoToThe[startBit] - 1)` — bits `startBit..15` set (the
   partial word at the left edge).
4. `rightMask = twoToThe[endBit + 1] - 1` — bits `0..endBit` set (the
   partial word at the right edge). When `endBit = 15` (the run reaches
   the last bit of its word), this needs `twoToThe[16] - 1`, which is
   exactly the overflow case the 17-entry table exists for: `0 - 1 = -1`,
   all 16 bits set, with no special-casing needed.
5. If `startWord = endWord` (the whole run fits in one word), AND the two
   masks together and touch that single word once.
6. Otherwise: set the left edge word with `leftMask`, walk every word
   strictly between the edges setting mask `-1` (a full word, one
   peek/bitop/poke each — no multiply, no divide, just `address + 1`), then
   set the right edge word with `rightMask`.

`updateLocation(address, mask)` is the shared one-line peek/bitop/poke
(`color` ? OR the mask in : AND its complement out) — the same logic
`drawPixel` already had inline, pulled out so `drawHorizontal` doesn't
duplicate it per word.

**Result:** the same `drawCircle(255, 127, 35)` that needed ~200 million
steps now completes in under 5 million (0.7 real seconds) — roughly a 40x
reduction, because a 68-pixel-wide row now costs ~5 word-writes plus two
multiplies and two divides *total*, instead of 68 multiplies and 68
divides.

## `drawLine(x1, y1, x2, y2)` — slides 81-86

The documented algorithm assumes `dx >= 0` and `dy >= 0` ("focus on lines
that go north-east"). Tracing it through shows it actually breaks when
`dx = 0` or `dy = 0` specifically: the tie-break variable starts at `0`,
and the first tie-break always takes the "increment b" branch, which
immediately exceeds a `0` bound on `dy` and cuts a horizontal line off
after one pixel. So those two directions are handled as special cases:

- **`dx = 0`** (vertical line): each pixel is a different word (a
  different row entirely), so there's no run of pixels to batch into
  fewer memory writes the way `drawHorizontal` does. There *is* still
  waste worth removing, though: `x` is the same for every pixel down the
  column, so its word-offset and bit-mask are computed **once** up front
  (instead of via a fresh `drawPixel` call — and its `Math.divide` — every
  single row), and the loop just steps the address by `±32` per row,
  calling `updateLocation` directly with the precomputed mask.
- **`dy = 0`** (horizontal line): delegates straight to
  `Screen.drawHorizontal(y1, x1, x2)` instead of looping `drawPixel`.
- **General diagonal case:** unchanged — walks absolute `dx`/`dy` with a
  running `diff` (Bresenham-style tie-breaking), applying the sign
  (`xStep`/`yStep`) only when computing the actual pixel. Only one pixel
  gets drawn per iteration here, so there's no row/word to batch either.

**A known discrepancy from the official reference, left as-is:** running
this against the real `tools/OS/Screen.vm` on steep/shallow diagonal lines
showed occasional "double-draw" pixels — two pixels landing in the same
row/column at certain transition points. Simulating the literal documented
pseudocode directly in Python reproduced the same behavior, confirming
it's a property of the introductory algorithm as taught, not a bug
introduced in translation. Horizontal, vertical, and 45° lines all match
the reference exactly.

## `drawRectangle(x1, y1, x2, y2)`

Not given its own dedicated algorithm in the slides ("the implementation
of the remaining Screen functions is simple") — every row of a filled
rectangle is exactly the `drawHorizontal` case, so this just validates the
corners once, then loops `y` from `y1` to `y2` handing each row straight
to `Screen.drawHorizontal(y, x1, x2)`. This deliberately bypasses
`drawLine` entirely (rather than looping `drawLine(x1, y, x2, y)`, which
would re-run the `dx`/`dy` branching and the full bounds check on every
single row for no benefit, since every row here is known in advance to be
horizontal and already validated).

Bounds check — `x1 > x2 | y1 > y2 | x1 < 0 | x2 > maxX | y1 < 0 | y2 >
maxY` → `Sys.error(9)` — matches the official reference exactly (read
directly from `tools/OS/Screen.vm`, same six comparisons, same error
code). Verified at runtime: a valid rectangle draws correctly (word-level
pixel patterns checked by hand across multiple rows and word boundaries,
plus a single-word case), and all four invalid-corner variants (`x1>x2`,
`y1>y2`, `x1<0`, `x2` off-screen) halt via `Sys.error(9)` as expected.

## `drawCircle(x, y, r)` — slide 95

The documented algorithm loops `dy` from `-r` to `r`, filling the
horizontal chord at each row from `x - sqrt(r² - dy²)` to
`x + sqrt(r² - dy²)`. This implementation adds one valid optimization on
top of the literal slide pseudocode: `Math.sqrt` is only computed for
`dy = 0..r` and reused for both `y + dy` and `y - dy`, since
`sqrt(r² - dy²) = sqrt(r² - (-dy)²)` — same pixels, half the (non-trivial)
`Math.sqrt` calls. Every chord is drawn via `Screen.drawLine`, which — since
every one of these chords has `dy = 0` by construction (`y+dy` on both
ends) — always lands in `drawHorizontal`'s word-batched path, not the
per-pixel one.

**Bounds checking, verified against the reference by reading
`tools/OS/Screen.vm` directly (not assumed):**

- Center out of screen bounds → `Sys.error(12)`.
- Full bounding box (`x±r`, `y±r`) not entirely on-screen → `Sys.error(13)`
  — confirmed byte-for-byte identical logic in the official reference
  (same four comparisons, same error code). This means a circle can never
  be partially drawn at the screen edge; the whole call is rejected before
  anything is drawn if any part of it would fall off-screen.

**Two size limits, only one of which is actually reachable:**

- **181** is the documented theoretical ceiling: `rSquared = r*r` must fit
  in a 16-bit signed `int` (max `32767`). `181² = 32761` fits; `182² =
  33124` overflows and wraps negative, corrupting every subsequent
  `Math.sqrt` call. Neither this implementation nor the official reference
  actually checks for this at runtime — it's a documented precondition the
  caller is trusted to respect, not something the OS defends against.
- **127** is the real, actually-enforced ceiling: a 256-pixel-tall screen
  means a circle centered vertically can have `y - r >= 0` and
  `y + r <= 255` only up to `r = 127`. Confirmed directly at runtime:
  `drawCircle(255, 127, 127)` draws normally, `drawCircle(255, 127, 128)`
  halts immediately via `Sys.error(13)` in both this implementation and
  the official reference — every time, regardless of where the circle is
  centered, the bounding-box check rejects anything large enough to
  approach the 181 overflow limit long before `rSquared` is ever computed.
  So 181 is a real number, but not one this API can actually be pushed
  into hitting.

**The algorithm itself does not match the official reference's**, and this
was confirmed by reading `tools/OS/Screen.vm`'s `drawCircle` bytecode
directly rather than assumed: the reference doesn't use the slide-95
per-row-sqrt formula at all — it uses an incremental midpoint/Bresenham-style
circle algorithm (`Screen.drawSymetric`, decision-variable comparisons, no
`Math.sqrt` calls whatsoever). Both draw a correctly filled circle of the
requested radius, but the two algorithms' integer decision boundaries land
slightly differently near the diagonal (verified by hand: a radius-3 circle
drawn here produces exactly the `sqrt(r²-dy²)` values row by row, while the
reference's same circle differs at `dy = ±1` and `dy = ±3` specifically).
This mirrors the `drawLine` double-draw situation: the documented algorithm
is followed faithfully here, and the reference's divergence is a separate,
more sophisticated implementation choice, not a translation bug.

## Verified

Same two-part standard as every other OS class:

- **Codegen**: this project's compiler (`answers/11`) produces VM output
  identical to the official `JackCompiler.sh`, line for line, for every
  function in this file.
- **Runtime**: compiled and actually executed in `VMEmulator.sh` (linked
  against the official pre-built OS for classes not yet implemented here).
  Specific checks performed: `drawPixel` bit-level correctness (raw word
  peeks after drawing known pixels); `drawLine` horizontal/vertical/45°
  exact match against the reference, plus the diagonal double-draw
  root-cause above; `drawHorizontal` exercised directly for a single-word
  span (reverse order), a multi-word span (partial + full + partial
  words), and an exact word-aligned span (exercising the `twoToThe[16]`
  overflow case) — all bit patterns checked by hand against the expected
  mask arithmetic; `drawCircle` exact pixel-row verification for a small
  radius (every row's word checked against `sqrt(r²-dy²)` by hand) and the
  127/128/150 boundary behavior confirmed at runtime against both this
  implementation and the official reference; `drawRectangle` exercised for
  a multi-row rectangle spanning several words (pixel patterns checked by
  hand row by row, including that rows outside it stay untouched), a
  single-word rectangle, and all four invalid-corner variants correctly
  halting via `Sys.error(9)`.

This completes every function in `Screen.jack`.
