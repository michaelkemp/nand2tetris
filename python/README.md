# A Python Hack Computer

This runs real, compiled Hack machine code — the actual binary that
`answers/06`'s assembler produces — on a from-scratch simulation of the
Hack CPU (the same 16-bit A/D/PC-register, ALU machine specified in
projects 2-5), with a Tkinter window standing in for the physical screen
and keyboard. It's the lowest level this repo's own toolchain reaches:

```
Jack source  --(answers/11, this repo's own compiler)-->  VM bytecode
             --(answers/08, this repo's own VM translator)-->  Hack assembly
             --(answers/06, this repo's own assembler)-->  Hack machine code
             --(python/cpu.py, this file)-->  running program
```

## Files

- `cpu.py` — the CPU simulator: ROM/RAM, the A/D/PC registers, the ALU,
  fetch-decode-execute. No GUI dependency; runs headless.
- `computer.py` — the Tkinter front end: renders `RAM[16384..24575]`
  (the screen memory map) live as an image, and writes real keystrokes
  into `RAM[24576]` (the keyboard register) — exactly the memory-mapped
  I/O contract the real hardware uses.
- `vm_interpreter.py` — a second, independent way to run a compiled
  program: interprets Jack VM bytecode directly, one level *above* real
  machine code (skips the translate-to-assembly and assemble-to-binary
  steps). Kept because it's ~2-3x faster (see "Performance" below) and
  was the first thing built here, before "let's run the actual machine
  code" became the point.
- `build_and_run.sh` — compiles/assembles a program down to `.hack` and
  launches `computer.py` against it. See its own header comment for
  usage; both examples below use it.
- `os/` — copies of this repo's own `answers/12` OS classes.
- `programs/GraphicsDemo/` — a small original program plus a trimmed
  `Sys.jack` (see "The 32K ROM limit" below).
- `programs/Pong/Pong.asm` — the official pre-built Pong assembly from
  `projects/06/pong` (a historical course artifact, not compiled by this
  repo's own toolchain — see below for why).

## Running it

```sh
cd python
./build_and_run.sh jack programs/GraphicsDemo Math Memory Array Screen
./build_and_run.sh asm  programs/Pong/Pong.asm
```

Both open a real window. The graphics demo just draws and sits there;
Pong reads the keyboard for paddle control (arrow keys) the same way any
real Hack program would — press one, move the paddle.

## The 32K ROM limit

The real Hack computer's ROM holds exactly 32,768 (2^15) instructions —
an A-instruction only has 15 bits to address it. This repo's answers/12
OS was written for clarity, not code size, and it turns out **that
matters at this level in a way it never did running through the VM
emulator**: this repo's full 8-class OS plus even a one-line test program
assembles to 45,597 instructions — 12,829 over the limit. The *official*
reference OS is worse (49,927 with the same trivial program), so this
isn't about this repo's OS being unusually large — no complete Jack OS
fits in real Hack ROM alongside a program. `Output`'s font table alone
(building ~90 characters' bitmaps via chained `Array.new` calls) is by
far the biggest single cost.

This is exactly why the course's own VM-level tooling (`tools/
VMEmulator.sh`, and this project's `vm_interpreter.py`) is the normal way
to run Jack programs — interpreting VM bytecode directly has no ROM to
overflow. Trying to run *real machine code* is what surfaces this limit
at all, which is the whole point of building this the hard way rather
than stopping at the VM interpreter.

**`programs/GraphicsDemo`** works around this the honest way: it only
uses `Math`/`Memory`/`Array`/`Screen`, and ships its own trimmed
`Sys.jack` that only initializes those four classes (the real
`answers/12/Sys.jack` also initializes `Output` and `Keyboard`, which
this demo doesn't call). That keeps it at 18,076 instructions — compiled
by this repo's own full toolchain, running correctly on this repo's own
CPU simulator.

**`programs/Pong`** doesn't get the same treatment: Pong needs on-screen
text (score, "Game Over"), which pulls in the expensive `Output` class,
and even with every possible trim (dropping `Keyboard.init`, using this
repo's own leaner classes instead of the official ones) the real total
came to 59,660 instructions — no combination fits. So this demo uses the
pre-built `Pong.asm` already sitting in `projects/06/pong` from earlier
in the course, assembled and run by this repo's own tools rather than
compiled by them. Confirmed correct by rendering a frame to a PNG and
inspecting it directly: "Game Over", the score, the paddle, and the ball
all appear exactly where they should.

## Performance

Pure Python, so neither engine is fast by real-hardware standards:

- `cpu.py` (real machine code): ~1.4M instructions/second.
- `vm_interpreter.py` (VM bytecode directly): ~2.8M instructions/second.

The gap isn't just per-instruction overhead — real Hack code needs
*more instructions to do the same work* than VM bytecode does (a single
`push constant 5` VM command is one interpreter step here, but assembles
to 7 real Hack instructions). Something like a filled `Screen.drawCircle`
that costs a few million VM-level steps can cost tens of millions of
real machine cycles — noticeably slower, not just a constant-factor
slowdown. `build_and_run.sh` runs `steps_per_tick` machine instructions
between each screen redraw (see `computer.py`); graphics-heavy programs
will visibly catch up to the screen in bursts rather than smoothly.

## Bugs found building this

Two real, previously-latent bugs turned up while building and testing
this, both now fixed (with their own commits):

- `vm_interpreter.py`'s own bug, not a pre-existing one: the `function`
  instruction handler never set `LCL = SP` before pushing the zeroed
  locals, so every function's locals pointed at stale memory. Caught by
  `Memory.alloc` looping thousands of times where it should have run
  once.
- `answers/06/hackAssembler.py`: resolving a label address never checked
  it against the 32K ROM limit the way literal `@123` addresses and new
  variable allocation already did — a label past instruction 32767 got
  silently encoded with bit 15 set, which the CPU correctly reads as a
  C-instruction instead of the intended jump, corrupting control flow
  instead of failing loudly. This is what actually surfaced the ROM-size
  discovery above: the assembler now raises a clear error instead.
