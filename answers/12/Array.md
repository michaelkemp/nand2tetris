# Array.jack — OS Array Library

## What this is

The smallest class in this OS by a wide margin, and a direct
consequence of something already covered in `Memory.md`: a Jack array is
just a plain address — `arr[i]` compiles to pure pointer arithmetic
(`push arr`, `push i`, `add`, `pop pointer 1`, `push that 0`), never a
method call — so `Array` itself has almost nothing to do. It exists to
give that raw address a constructor and a destructor, nothing more.

## `new(size)`

`size < 1` → `Sys.error(2)`, matching the official reference OS
(confirmed by reading `tools/OS/Array.vm` directly). Otherwise this is
just `return Memory.alloc(size);` — the returned address *is* the array;
there's no header, no metadata, no initialization of the elements
themselves. Any two-way weak-typing conversion (`Array` in, `int` out of
`Memory.alloc`) is exactly the kind of implicit address reinterpretation
`Memory.md` describes in more depth.

## `dispose()`

`Memory.deAlloc(this)` — the instance's own address, handed back to the
same free-list `Memory.jack` manages. Nothing else to release, since an
array has no other state of its own.

## Verified

- **Codegen**: matches the official `JackCompiler.sh` exactly (22/22
  lines, no diff).
- **Runtime**: the official `ArrayTest` (`projects/12/ArrayTest`) run end
  to end — `"Comparison ended successfully"` — the first test in this
  project where `Array` and `Memory` worked together for real allocation
  and disposal, not just in isolation.
