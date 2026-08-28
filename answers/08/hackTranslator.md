# hackTranslator.py — VM to Hack Assembly Translator

## What this is

`hackTranslator.py` is the VM translator for projects 7 and 8. It reads VM
language commands (a small set of push/pop/arithmetic/branching/function
commands) and emits the equivalent Hack assembly instructions.

## The core idea: faking a stack machine

The Hack CPU (project 5) has no stack. It has an A register, a D register,
a program counter, and RAM — nothing more. There is no `PUSH` or `POP`
instruction in Hack machine language, and no notion of a "function call."

The VM language pretends otherwise: it's a stack-based language where you
push values, pop them, and do arithmetic on "the top of the stack." This
translator's entire job is to *fabricate* that illusion using only the
primitives the Hack CPU actually has: read a memory cell, write a memory
cell, do arithmetic, jump.

The trick: RAM[0] ("SP") holds the address of the next free stack slot, and
RAM[256] onward is treated as the stack purely by convention. Every VM
command becomes a short sequence of ordinary Hack instructions that read or
write through that SP pointer and then move it. For example, three simple
VM commands:

```
push constant 7
push constant 8
add
```

expand into 24 real Hack instructions:

```asm
// push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M+D
@SP
A=M
M=D
@SP
M=M+1
```

Nothing about the underlying machine got smarter here — this is just more
instructions, spelling out "pop, pop, compute, push" as raw memory
operations.

## What each command category does (and where it lives in this file)

| VM commands | What they do | Method(s) |
|---|---|---|
| `push`/`pop` `constant/local/argument/this/that/temp/static/pointer` | Move values between the stack and one of the memory "segments" | `pushpop`, `segPush`/`segPop`, `constantPush`, `tempPush`/`tempPop`, `staticPush`/`staticPop`, `pointerPush`/`pointerPop` |
| `add sub neg eq gt lt and or not` | Arithmetic/logic on the top 1-2 stack values | `AddSubAndOr`, `NegNot`, `EqGtLt` |
| `label` `goto` `if-goto` | Branching within a function | `branch` |
| `function` `call` `return` | Function declaration, calling, and returning | `fnctFunction`, `fnctCall`, `fnctReturn` |

### Memory segments

`local`/`argument`/`this`/`that` are virtual arrays: their *base address* is
stored in a fixed RAM cell (LCL/ARG/THIS/THAT, RAM[1..4]), so `push local 2`
means "go to LCL, add 2, dereference." `temp` is a fixed 8-word block
(RAM[5..12]) needing no indirection. `static` variables are scoped per
`.vm` file — this translator names them `<file>.<index>` and lets the
assembler (project 6) assign them real RAM addresses. `pointer` is the
2-word segment that lets VM code directly change what THIS/THAT point to
(this matters once the Jack compiler starts compiling object methods).

### Function calls: the same trick, one level up

Hack has no `CALL`/`RETURN` instruction either. `fnctCall` fabricates one:
it pushes the caller's LCL/ARG/THIS/THAT onto the *same* stack (so the
"call stack" is just more of the same RAM region), repositions ARG/LCL for
the callee, and does a plain unconditional jump. It also generates a
uniquely-numbered return-address label (`FuncName$ret.N`) and drops that
label right after the jump, so `fnctReturn` — which restores everything and
jumps back — has somewhere to land.

One correctness detail specific to this file: VM labels (`label`/`goto`/
`if-goto`) are only meaningful *within the function they're declared in*,
so this translator mangles them as `<currentFunction>$<label>` to guarantee
they can never collide with an identically-named label declared in a
different function or file. (This was a real bug caught and fixed while
reviewing this file — labels weren't scoped and could silently collide.)

## Where this fits, and what's next

This translator's *input* — push/pop/arithmetic/branching/function-call
commands — isn't something a person writes by hand for real programs. It's
the *output* of the Jack compiler, which comes next in the course:

- **Project 9** — write some actual programs in the Jack language (a small,
  Java-like, object-based language), by hand, just to learn the language.
- **Project 10** — build the front half of a Jack *compiler*: a tokenizer
  and parser that reads `.jack` source and understands its structure, but
  doesn't generate any code yet.
- **Project 11** — finish the compiler: walk the parsed structure and emit
  exactly the VM commands this translator already knows how to consume
  (`push`, `pop`, `add`, `call`, `function`, `label`, ...). This is the
  project currently in progress in `answers/11`.
- **Project 12** — write the Jack *OS* (Math, String, Array, Output,
  Screen, Keyboard, Memory, Sys) — itself just more Jack code, compiled by
  the same project 11 compiler into more VM commands that this same
  translator turns into assembly.

So the full arc is: Jack source → (project 11 compiler) → VM commands →
(this translator) → Hack assembly → (project 6 assembler) → Hack machine
code → runs on the CPU from project 5. Every layer only has to understand
the layer directly below it — the Jack compiler never needs to know
anything about Hack assembly, because this translator already promises to
turn whatever VM commands it emits into working machine code.

One terminology note, since it's an easy mix-up given the similar names:
**"Hack" is the CPU and machine language** (projects 4-6), and **"Jack" is
the high-level language** (projects 9-11) — two different things sitting at
opposite ends of this same toolchain.
