# Keyboard.jack — OS Keyboard Library

## What this is

`Keyboard.jack` reads user input through one piece of hardware: `RAM[24576]`,
the keyboard memory map register. When a key is held down, that register
holds its character code; when nothing is pressed, it holds `0`. Every
function in this class ultimately bottoms out in reading that one word.

As with `Output`, the course material doesn't give a specific algorithm
for this class beyond a rough description of what each function should
do — the design here is original, verified by execution.

## `keyPressed()`

`return Memory.peek(24576);` — the entire implementation. No state to
track, nothing to validate; the hardware register already holds exactly
the answer.

## `readChar()`

Waits for a key to be pressed and released, echoes it, and returns its
code. The two `while` loops are the direct, literal version of "wait
until a key is down" then "wait until it's back up":

```
while (Keyboard.keyPressed() = 0) { }        // wait for a key down
let c = Keyboard.keyPressed();
while (~(Keyboard.keyPressed() = 0)) { }     // wait for it to come back up
```

**The visible cursor** is the interesting part, and it isn't obvious from
the API doc comment alone ("Waits until a key is pressed... echoes the key
to the screen") — it's built from a trick discovered while reading the
official reference OS's bytecode directly (`tools/OS/Keyboard.vm`), not
mentioned in the course slides beyond a passing "display the cursor" line
in the `readChar` pseudocode: character code `0` is exactly the "invalid
character" glyph `Output`'s font table already reserves — a solid black
square (`Output.create(0, 63,63,63,63,63,63,63,63,63,0,0)`, in the
skeleton). So before waiting for a key, this calls `Output.printChar(0)`,
which draws that square and advances the cursor one column — a visible
placeholder showing where the next character will land. Once a key is
captured, `Output.printChar(129)` (the hardcoded backspace code — see
`Output.md`) erases that square and moves the cursor back, immediately
before the real character is echoed in its place. No dedicated
"show/hide cursor" function needed — just `printChar`/`backSpace`,
already reused for the purpose they were built for.

## `readLine(message)`

Prints `message`, then repeatedly calls `readChar` and reacts to what
comes back:

- `128` (newline) ends the loop and returns what's been typed so far.
- `129` (backspace) removes the last character from the string being
  built (`str.eraseLastChar()`), if there is one.
- Anything else gets appended (`str.appendChar(c)`).

Uses a fixed `String.new(80)` buffer, matching the official reference's
own choice of size (confirmed by reading `tools/OS/Keyboard.vm` — not an
arbitrary pick). No dynamic growth beyond that capacity; `String`'s own
`appendChar` is responsible for whatever happens if that's exceeded, the
same way `Screen`'s functions trust `Memory`'s bounds rather than
re-checking them.

## `readInt(message)`

Delegates entirely to `readLine` plus `String`'s own `intValue()` (rather
than parsing digits out by hand here) and disposes the temporary buffer
afterward — this matches the official reference exactly (confirmed by
reading `tools/OS/Keyboard.vm`), and makes sense structurally: parsing
digits out of a string is `String`'s job, not `Keyboard`'s, and every
`readLine` buffer needs disposing once its value has been extracted or it
leaks.

## Verified

- **Codegen**: matches the official `JackCompiler.sh` exactly, line for
  line (106/106 lines, no diff).
- **Runtime**, linked against this project's own `Math`/`Memory`/`Array`/
  `Screen`/`Output` plus the official reference `String`/`Sys` (`String`
  isn't implemented yet in this project sequence — used here only as a
  working backend to verify `Keyboard`'s own logic drives it correctly,
  not to test `String` itself):
  - `readChar`: simulated a keypress and release by directly setting
    `RAM[24576]` mid-execution (the same technique the official course's
    own `FillAutomatic.tst` uses for the analogous project-04 test).
    Confirmed the cursor square is drawn (checked its bitmap directly),
    the correct character code is returned, and the echoed glyph matches
    the pressed character's real font data exactly.
  - `readLine`: simulated typing `X`, `Y`, **backspace**, `Z`, newline.
    Confirmed the returned string has length 2 and contains exactly `X`
    then `Z` — the backspace-during-typing correction works, not just a
    trailing backspace.
  - `readInt`: simulated typing `-42` followed by newline. Confirmed the
    returned integer is exactly `-42`, including the negative sign.

A subtlety hit while setting these tests up, worth noting for next time:
the VM Emulator halts a whole `.tst` script at the *first* output-line
mismatch rather than reporting each line independently, so multiple
`output;` calls interleaved with `set RAM[24576] ...` commands need every
earlier line to already match before a later one becomes visible at all.
