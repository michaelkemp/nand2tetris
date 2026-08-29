# Memory.jack — OS Memory Library

## What this is

`Memory.jack` provides two unrelated-looking services that turn out to
share one array: raw RAM access (`peek`/`poke`), and dynamic memory
allocation (`alloc`/`deAlloc`) — the thing every `constructor` you compile
calls (`call Memory.alloc 1`), and what `Array.new`, `String.new`, and
every object's `new` ultimately bottom out in.

This is the class nearly everything else in the OS depends on
(`Array`, `String`, every constructor anywhere), which is why it was
built right after `Math`.

## `peek(address)` / `poke(address, value)` — slides 47-48

The whole trick is one field: `static Array ram;`, set to `0` in `init`.
Jack arrays are just base-address-plus-offset with **no bounds
checking** — `ram[address]` compiles to "dereference `0 + address`", i.e.
directly access `RAM[address]`. So `peek`/`poke` are just:

```
function int peek(int address) {
    return ram[address];
}
function void poke(int address, int value) {
    let ram[address] = value;
    return;
}
```

No loop, no bit manipulation — the "implementation" is really just
declaring `ram` at address 0 and letting Jack's (deliberately unchecked)
array semantics do the rest.

**How this bootstraps without circularity:** `ram` (and `heap`, below)
never go through `Array.new`/`Memory.alloc` at all — `init` just does
`let ram = 0;`, a plain assignment of a literal to an `Array`-typed
variable. This is legal specifically because Jack is weakly typed (slide
48 says so explicitly): every Jack array/object is *always* just a plain
16-bit address under the hood, so pointing an `Array` variable at a
hardcoded, already-known address needs no allocation and no call into
code that doesn't exist yet. `Array.new` itself *does* need `Memory.alloc`
- but `Memory` bootstrapping itself doesn't need `Array.new`. The
dependency only runs one direction.

## The heap: a linked list of free segments

`alloc`/`deAlloc` manage a linked list of free memory blocks starting at
`freeList` (initially `2048`, the base of the heap — everything below that
is reserved for the stack and static/global variables, everything from
`16384` up is the screen/keyboard memory map), addressed through a second
field, `static Array heap;`, based at `2048` - separate from `ram` (based
at `0`), matching the structure in project-12.pdf slide 60 rather than
just using `ram` with absolute addresses everywhere (an earlier version of
this file did the latter; behaviorally identical, since `heap[i]` and
`ram[2048+i]` are the same RAM cell either way, but this matches the
documented structure). Every segment, whether currently free or handed out
to a caller, has a 2-word header sitting at its own base address:

| Offset | Meaning |
|---|---|
| `+0` | `length` — usable words in this segment, **not counting its own header** |
| `+1` | `next` — absolute base address of the next free segment, or `0` for "end of list" |

This layout isn't a guess — it was confirmed by reading `tools/OS/Memory.vm`
(the official pre-built reference OS)'s compiled bytecode directly: its
search loop compares `that 0` (offset `+0`) against the requested size,
then reads `that 1` (offset `+1`) to advance to the next segment. The
error codes (`5` = invalid size, `6` = heap overflow) were confirmed the
same way, by finding the literal constant pushed right before each
`call Sys.error`.

**Why `freeList`/`next` store absolute addresses, not heap-relative
offsets:** using `0` as "end of list" is only safe if no *real* segment
can ever legitimately sit at that value. That's true for absolute
addresses (nothing lives at RAM address `0`) but would **not** be true for
heap-relative offsets, since the very first segment genuinely sits at
heap-relative offset `0` — a `next` field storing `0` would then be
ambiguous between "the first segment" and "nothing." So `freeList` and
every `next` field hold absolute addresses (≥ 2048), and are converted to
a heap-relative offset (`address - 2048`) only at the point of indexing
into `heap[]`. The one exception is the local `previous` variable inside
`alloc`, which is used *only* for indexing (never stored or compared for
nullness against a real segment) and uses `-1`, not `0`, as its own "no
previous yet" sentinel - so it's safe to keep it as a heap-relative offset
throughout and skip the repeated conversion.

**Worth being upfront about:** the reference OS's actual splitting logic
goes deeper than was worth reverse-engineering byte-for-byte from raw VM
instructions. The header layout and error codes above are verified facts;
the specific control flow in `alloc`/`deAlloc` below is this project's own
design built on those facts, not a line-for-line replica of the
reference. It's correct and thoroughly tested (see "Verified" below), but
if you're comparing against a video or another solution that shows a
different splitting strategy (or one that coalesces adjacent free blocks
on `deAlloc`, which this doesn't do), that's an equally valid alternative,
not evidence something here is wrong.

## `init()`

Sets `freeList = 2048` and writes a single header there describing one
giant free segment spanning the entire heap: `length = 14334` (that's
`16384 - 2048 - 2` — the whole heap, minus the 2 words this very header
occupies), `next = 0` (nothing follows it yet).

## `alloc(size)`

First-fit search: walk the linked list from `freeList`, following `next`,
looking for the first segment whose `length >= size`. Once found, one of
two things happens:

- **Enough surplus to split** (`length > size + 1`, i.e. `length >= size +
  2` — enough left over to also fit a valid header for what remains):
  shrink the segment's own `length` in place and carve the requested block
  off its *tail*. The original segment keeps its position in the free
  list (nothing about its address or `next` pointer changes), just with a
  smaller recorded `length`.
- **Not enough surplus to split**: hand over the *whole* segment and
  unlink it from the list (updating either `freeList` itself, if it was
  the head, or the previous segment's `next` field).

Either way, the chosen block's own `length` field gets set to exactly
`size` (its real usable capacity, for `deAlloc` to read back later), and
`block + 2` — the address just past the header — is what's returned to
the caller.

Running off the end of the list (`segment` reaches `0` without finding
anything big enough) means the heap is exhausted: `do Sys.error(6)`,
matching the reference OS's own error code for this case.

## `deAlloc(o)`

Recovers the block's true header address (`o - 2` — undoing the `+2`
`alloc` applied), then prepends it to the front of `freeList`: `next` is
set to whatever `freeList` currently is, then `freeList` becomes this
block. `length` doesn't need to be touched — it's already sitting there
correctly, set back when `alloc` handed this block out and never
disturbed since. No coalescing of adjacent free blocks happens (the
slides call periodic defragmentation an optional extension, not a
requirement for a correct implementation).

## Verified

Two ways, same as every other OS class so far:

- **The actual official `MemoryTest`** (`projects/12/MemoryTest`), run
  end to end through the real VM Emulator — multiple `Array.new` calls of
  different sizes, reads/writes through the allocated memory, and real
  `dispose()`-then-reallocate reuse. `"Comparison ended successfully"`
  against the official `MemoryTest.cmp`.
- **A custom stress test** built specifically to exercise both branches of
  `alloc` together: three blocks carved from one large free segment, the
  middle one freed and exactly reallocated (forcing the "take whole" path
  on an exact-size match), then freed again and reallocated smaller
  (forcing an actual split). The two blocks that were never touched
  stayed intact throughout, and the split-derived block was correct too —
  confirming neither code path corrupts neighboring data.
