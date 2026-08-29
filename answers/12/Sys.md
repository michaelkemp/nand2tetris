# Sys.jack — OS System Services

## What this is

`Sys.jack` is the piece that turns seven independently-built classes into
one coherent, bootstrapped OS. Every Hack program starts the same way,
per the "VM contract" the course documentation spells out: the VM's own
built-in bootstrap code sets `SP = 256` and calls `Sys.init` — nothing
else. Everything from there on is `Sys.init`'s job.

## `init()`

The exact call order is given directly in the course documentation
(unlike most of the other OS classes, which just say "do it"), and this
follows it verbatim:

```
Memory.init();
Math.init();
Screen.init();
Output.init();
Keyboard.init();
Main.main();   // the actual program
Sys.halt();    // Hack has no OS-level "exit" - park here forever
```

**Why this particular order matters, traced through the actual
dependencies** (not just because the slide says so):

- `Memory` has to come first because almost everything else allocates
  through it — `Screen.init`'s bit-mask table and `Output.init`'s ~90
  character bitmaps are both built via `Array.new`, which is
  `Memory.alloc` under the hood.
- `Math` and `Memory` don't actually depend on each other (`Math.init`
  only does repeated addition, no allocation), so their relative order
  here doesn't matter — it's just the order the slide happens to list.
- `Output` doesn't depend on `Screen` either, despite both touching the
  same screen memory — `Output.drawGlyph` writes to the screen directly
  via `Memory.peek`/`poke` (see `Output.md`), never calling into `Screen`
  at all.
- `Keyboard.init` is a genuine no-op (confirmed reading its own bytecode
  while building it — see `Keyboard.md`), so its position is irrelevant.
- `Array` and `String` are absent from this list entirely: neither has
  an `init` function, because neither has any static/class-level state —
  `Array` is a thin `Memory.alloc` wrapper, and `String`'s fields are all
  per-instance, set up in its own `constructor`.

**This is also the function that makes every `Sys.error(...)` call
elsewhere in this OS actually do something.** Every one of them —
`Memory.alloc`'s heap-overflow check, `Array.new`'s size check,
`Screen`'s bounds checks, `String`'s six error codes — was written and
committed as a "placeholder until `Sys` exists" (see each class's own
`.md`), meaning until this file existed those calls fell through into
whatever function happened to follow them in memory rather than actually
halting. Implementing `Sys.jack` is what finally closes every one of
those loose ends at once.

## `halt()`

`while (true) { }` — the documented approach (the implementation notes
say exactly this: "use an infinite loop"). Hack has no operating-system
concept of a process exiting, so parking forever is the only sensible
"done" state, for both a program that finishes normally and one that
called `Sys.error`.

## `wait(duration)`

The slides deliberately don't give a fixed algorithm here — the
implementation notes just say "use a loop, hardware-specific," since the
right calibration depends on how fast the actual machine (or emulator)
executes instructions. Rather than inventing an untested constant, this
uses the same one the official reference OS settled on (read directly
from `tools/OS/Sys.vm`): a nested loop, counting an inner variable down
from `50` to `0` once per millisecond of the requested duration. Negative
durations halt via `Sys.error(1)`, matching the reference's own error
code for this case.

## `error(errorCode)`

Builds the literal string `"ERR"` via three `appendChar` calls (`69`,
`82`, `82`), prints it, prints the error code as a plain integer right
after it with no separator (so `Sys.error(42)` shows `"ERR42"`), then
halts. Confirmed by reading `tools/OS/Sys.vm` directly, not guessed from
the API doc's `"ERR<errorCode>"` format string alone.

## Verified

- **Codegen**: matches the official `JackCompiler.sh` exactly, line for
  line (92/92 lines, no diff).
- **Runtime — the real milestone here**: for the first time, ran a
  program using **all eight of this project's own OS classes together
  and zero reference files** (`Math`, `Memory`, `Array`, `Screen`,
  `Output`, `Keyboard`, `String`, `Sys`). A `Main.jack` with no manual
  init calls at all — relying entirely on the VM's standard bootstrap
  calling this project's own `Sys.init` — successfully:
  - Drew a circle and confirmed its topmost pixel bit-exact.
  - Printed a literal string (`"Hello, OS!"`) and an integer via
    `Output.printString`/`printInt`, confirmed bit-exact against the
    known font data — including correctly accounting for two
    consecutive characters sharing one screen word (column 10's `H` and
    column 11's `e` both land in the same 16-bit word, OR'd together, as
    `Output.md` describes).
  - Reached a final `Memory.poke` placed as the last statement of
    `Main.main`, proving execution genuinely completed rather than
    stalling somewhere in the bootstrap chain.
  - `Sys.wait(-1)` confirmed to halt via `Sys.error(1)`; `Sys.wait(5)`
    confirmed to complete normally.
  - `Sys.error(42)` confirmed to render `"ERR42"` on screen bit-exact,
    checked word by word (again correctly accounting for shared-word
    character pairs) — the whole `String`/`Output` pipeline working
    correctly when driven by `Sys.error` itself, not just by hand-written
    test code.

This completes every class in `answers/12` — the full Jack OS, written
and self-verified from `Math` through `Sys`, using only this project's
own implementations of every piece.
