"""
A from-scratch interpreter for the Hack VM bytecode that project 11's Jack
compiler produces. No GUI, no dependency on the rest of this package -
just: load a directory of .vm files, run them, and expose the RAM array
(where the screen memory map and keyboard register live) for a front end
to read/write.

This re-implements the standard Hack VM call convention directly against
a flat RAM array, rather than going through Hack assembly/machine code -
one level lower than tools/VMEmulator.sh's "bytecoded" abstraction, same
level as this repo's own answers/08/hackTranslator.py, just interpreted
instead of translated to assembly.
"""

import os


RAM_SIZE = 24577          # 0..24575 = general RAM/heap/screen, 24576 = keyboard
STACK_BASE = 256
STATIC_BASE = 16


def to_u16(x):
    return x & 0xFFFF


def to_s16(x):
    x &= 0xFFFF
    return x - 0x10000 if x & 0x8000 else x


class VMError(Exception):
    pass


class Instr:
    __slots__ = ("op", "a", "b")

    def __init__(self, op, a=None, b=None):
        self.op = op
        self.a = a
        self.b = b

    def __repr__(self):
        return f"Instr({self.op!r}, {self.a!r}, {self.b!r})"


ARITH_UNARY = {"neg", "not"}
ARITH_BINARY = {"add", "sub", "and", "or"}
COMPARE = {"eq", "gt", "lt"}


class VM:
    def __init__(self):
        self.ram = [0] * RAM_SIZE
        self.instructions = []          # flat list of Instr, all files concatenated
        self.function_index = {}        # "Class.func" -> index of its Instr("function", ...)
        self.label_index = {}           # "Class.func$label" -> index of the instruction after the label
        self._static_addr = {}          # (classname, index) -> ram address
        self._next_static = STATIC_BASE
        self.pc = 0
        self.call_depth = 0             # for a runaway-recursion guard, not part of the real hardware
        self.halted = False
        self.on_error = None            # optional callback(errorCode) when Sys.error halts

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load_dir(self, path):
        for name in sorted(os.listdir(path)):
            if name.endswith(".vm"):
                self.load_file(os.path.join(path, name))

    def load_file(self, path):
        classname = os.path.splitext(os.path.basename(path))[0]
        current_function = None
        with open(path) as f:
            for raw_line in f:
                line = raw_line.split("//", 1)[0].strip()
                if not line:
                    continue
                parts = line.split()
                op = parts[0]

                if op == "function":
                    name, nlocals = parts[1], int(parts[2])
                    current_function = name
                    self.function_index[name] = len(self.instructions)
                    self.instructions.append(Instr("function", name, nlocals))

                elif op == "call":
                    name, nargs = parts[1], int(parts[2])
                    self.instructions.append(Instr("call", name, nargs))

                elif op == "return":
                    self.instructions.append(Instr("return"))

                elif op == "label":
                    label = f"{current_function}${parts[1]}"
                    self.label_index[label] = len(self.instructions)
                    self.instructions.append(Instr("label", label))

                elif op == "goto":
                    label = f"{current_function}${parts[1]}"
                    self.instructions.append(Instr("goto", label))

                elif op == "if-goto":
                    label = f"{current_function}${parts[1]}"
                    self.instructions.append(Instr("if-goto", label))

                elif op in ("push", "pop"):
                    seg, idx = parts[1], int(parts[2])
                    if seg == "static":
                        key = (classname, idx)
                        addr = self._static_addr.get(key)
                        if addr is None:
                            addr = self._next_static
                            self._next_static += 1
                            self._static_addr[key] = addr
                        self.instructions.append(Instr(op, "addr", addr))
                    else:
                        self.instructions.append(Instr(op, seg, idx))

                elif op in ARITH_UNARY or op in ARITH_BINARY or op in COMPARE:
                    self.instructions.append(Instr(op))

                else:
                    raise VMError(f"Unknown VM command {line!r} in {path}")

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def bootstrap(self):
        """Mirrors the real VM contract: SP=256; call Sys.init 0."""
        self.ram[0] = STACK_BASE
        self._push_frame(return_pc=-1, nargs=0)  # -1: Sys.init should never actually return
        self.pc = self.function_index["Sys.init"]

    def _push(self, value):
        sp = self.ram[0]
        if sp >= len(self.ram):
            self.ram.extend([0] * (sp - len(self.ram) + 1024))
        self.ram[sp] = value
        self.ram[0] = sp + 1

    def _pop(self):
        sp = self.ram[0] - 1
        self.ram[0] = sp
        return self.ram[sp]

    def _push_frame(self, return_pc, nargs):
        ram = self.ram
        sp = ram[0]
        self._push(return_pc)
        self._push(ram[1])  # LCL
        self._push(ram[2])  # ARG
        self._push(ram[3])  # THIS
        self._push(ram[4])  # THAT
        ram[2] = sp - nargs  # new ARG

    def _segment_addr(self, seg, idx):
        ram = self.ram
        if seg == "local":
            return ram[1] + idx
        if seg == "argument":
            return ram[2] + idx
        if seg == "this":
            return ram[3] + idx
        if seg == "that":
            return ram[4] + idx
        if seg == "pointer":
            return 3 + idx
        if seg == "temp":
            return 5 + idx
        if seg == "addr":  # pre-resolved static
            return idx
        raise VMError(f"Bad segment {seg!r}")

    def step(self):
        """Executes exactly one instruction. Returns False once halted."""
        if self.halted:
            return False

        instr = self.instructions[self.pc]
        op = instr.op
        ram = self.ram

        if op == "push":
            if instr.a == "constant":
                self._push(instr.b)
            else:
                self._push(ram[self._segment_addr(instr.a, instr.b)])
            self.pc += 1

        elif op == "pop":
            addr = self._segment_addr(instr.a, instr.b)
            ram[addr] = self._pop()
            self.pc += 1

        elif op in ARITH_BINARY:
            b = self._pop()
            a = self._pop()
            if op == "add":
                self._push(to_s16(a + b))
            elif op == "sub":
                self._push(to_s16(a - b))
            elif op == "and":
                self._push(to_s16(a & b))
            elif op == "or":
                self._push(to_s16(a | b))
            self.pc += 1

        elif op in ARITH_UNARY:
            a = self._pop()
            if op == "neg":
                self._push(to_s16(-a))
            elif op == "not":
                self._push(to_s16(~a))
            self.pc += 1

        elif op in COMPARE:
            b = self._pop()
            a = self._pop()
            if op == "eq":
                result = a == b
            elif op == "gt":
                result = a > b
            else:
                result = a < b
            self._push(-1 if result else 0)
            self.pc += 1

        elif op == "label":
            self.pc += 1

        elif op == "goto":
            self.pc = self.label_index[instr.a]

        elif op == "if-goto":
            self.pc = self.label_index[instr.a] if self._pop() != 0 else self.pc + 1

        elif op == "function":
            ram[1] = ram[0]  # LCL = SP: this is where the new locals begin
            for _ in range(instr.b):
                self._push(0)
            self.pc += 1

        elif op == "call":
            target = self.function_index.get(instr.a)
            if target is None:
                raise VMError(f"Call to undefined function {instr.a!r}")
            self._push_frame(return_pc=self.pc + 1, nargs=instr.b)
            self.pc = target
            self.call_depth += 1

        elif op == "return":
            frame = ram[1]  # LCL
            return_pc = ram[frame - 5]
            return_value = self._pop()
            new_sp = ram[2] + 1
            that_ = ram[frame - 1]
            this_ = ram[frame - 2]
            arg_ = ram[frame - 3]
            lcl_ = ram[frame - 4]
            ram[ram[2]] = return_value
            ram[0] = new_sp
            ram[4] = that_
            ram[3] = this_
            ram[2] = arg_
            ram[1] = lcl_
            self.call_depth -= 1
            if return_pc == -1:
                self.halted = True
                return False
            self.pc = return_pc

        else:
            raise VMError(f"Unhandled instruction {instr!r}")

        return True

    def run(self, max_steps=None):
        """Runs until halted or max_steps executed (whichever first).
        Returns the number of steps actually executed."""
        steps = 0
        if max_steps is None:
            while self.step():
                steps += 1
        else:
            while steps < max_steps and self.step():
                steps += 1
        return steps
