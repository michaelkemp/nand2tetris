"""
A from-scratch simulator of the actual Hack CPU: the same 16-bit
A/D/PC-register, ALU, fetch-decode-execute machine specified in projects
2-5 of this course, executing real Hack machine instructions (the .hack
files answers/06/hackAssembler.py produces). This is one level lower
than vm_interpreter.py, which instead interprets Jack VM bytecode
directly - this module runs the actual binary this course's own
assembler emits, bit for bit.

Instruction format (matches answers/06/hackAssembler.py's encoding
exactly - verified against it, not assumed):
  A-instruction: 0vvvvvvvvvvvvvvv               (bit 15 = 0)
  C-instruction: 111a cccccc ddd jjj            (bit 15 = 1)
    a:  0 selects A as the ALU's second operand, 1 selects M (RAM[A])
    c1..c6 (zx nx zy ny f no): the 6 ALU control bits
    d1 d2 d3: destination - write result to A, D, M respectively
    j1 j2 j3: jump if the ALU result is <0, =0, >0 respectively
"""

RAM_SIZE = 24577  # 0..24575 general RAM/heap/screen, 24576 = keyboard
KEYBOARD_ADDR = 24576


def to_s16(x):
    x &= 0xFFFF
    return x - 0x10000 if x & 0x8000 else x


class CPU:
    def __init__(self):
        self.rom = []
        self.ram = [0] * RAM_SIZE
        self.a = 0
        self.d = 0
        self.pc = 0
        self.halted = False  # true once PC would run off the end of ROM

    def load_hack(self, path):
        with open(path) as f:
            self.rom = [int(line.strip(), 2) for line in f if line.strip()]

    def _read_m(self, addr):
        if addr < len(self.ram):
            return self.ram[addr]
        return 0  # unmapped RAM above the screen/keyboard - reads as 0

    def _write_m(self, addr, value):
        if addr >= len(self.ram):
            self.ram.extend([0] * (addr - len(self.ram) + 1))
        self.ram[addr] = value

    def step(self):
        if self.pc >= len(self.rom):
            self.halted = True
            return False

        instr = self.rom[self.pc]

        if instr & 0x8000 == 0:
            # A-instruction: A = the 15-bit literal
            self.a = instr & 0x7FFF
            self.pc += 1
            return True

        # C-instruction
        a_bit = (instr >> 12) & 1
        zx = (instr >> 11) & 1
        nx = (instr >> 10) & 1
        zy = (instr >> 9) & 1
        ny = (instr >> 8) & 1
        f = (instr >> 7) & 1
        no = (instr >> 6) & 1
        d_a = (instr >> 5) & 1
        d_d = (instr >> 4) & 1
        d_m = (instr >> 3) & 1
        j_lt = (instr >> 2) & 1
        j_eq = (instr >> 1) & 1
        j_gt = instr & 1

        old_a = self.a  # A is a register: this cycle's M-address and jump
        # target are its value as of the START of the cycle, even if this
        # same instruction also writes a new value into A below.
        x = self.d & 0xFFFF
        y = (self._read_m(old_a) if a_bit else old_a) & 0xFFFF

        if zx:
            x = 0
        if nx:
            x = (~x) & 0xFFFF
        if zy:
            y = 0
        if ny:
            y = (~y) & 0xFFFF
        out = (x + y) & 0xFFFF if f else (x & y) & 0xFFFF
        if no:
            out = (~out) & 0xFFFF

        zr = out == 0
        ng = (out & 0x8000) != 0

        if d_a:
            self.a = out
        if d_d:
            self.d = out
        if d_m:
            self._write_m(old_a, out)

        jump = (ng and j_lt) or (zr and j_eq) or ((not ng and not zr) and j_gt)
        self.pc = old_a if jump else self.pc + 1
        return True

    def run(self, max_steps=None):
        steps = 0
        if max_steps is None:
            while self.step():
                steps += 1
        else:
            while steps < max_steps and self.step():
                steps += 1
        return steps
