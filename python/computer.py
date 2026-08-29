"""
A Tkinter front end for cpu.CPU: renders the screen memory map
(RAM[16384..24575]) live as an image, and feeds real keystrokes into the
keyboard register (RAM[24576]) - the same memory-mapped I/O contract the
real Hack computer uses, just with a real window standing in for the
physical screen and keyboard. This runs actual Hack machine code (a
.hack file), not an intermediate representation.
"""

import sys
import tkinter as tk

import numpy as np
from PIL import Image, ImageTk

from cpu import CPU

SCREEN_W, SCREEN_H = 512, 256
SCREEN_BASE = 16384
KEYBOARD_ADDR = 24576

# From Keyboard.jack's own doc comment - the non-ASCII key codes this OS recognizes.
KEYSYM_TO_CODE = {
    "Return": 128,
    "KP_Enter": 128,
    "BackSpace": 129,
    "Left": 130,
    "Up": 131,
    "Right": 132,
    "Down": 133,
    "Home": 134,
    "End": 135,
    "Prior": 136,  # Page Up
    "Next": 137,   # Page Down
    "Insert": 138,
    "Delete": 139,
    "Escape": 140,
}
for _i in range(1, 13):
    KEYSYM_TO_CODE[f"F{_i}"] = 140 + _i


def render_screen_array(ram):
    """Converts RAM[16384..24575] into a 256x512 uint8 array (0=black,
    255=white), matching Screen.jack's bit convention: bit j of a word is
    pixel (wordCol*16 + j) - i.e. bit 0 (LSB) is the leftmost pixel of
    that word, bit 15 (MSB) the rightmost."""
    words = np.array(ram[SCREEN_BASE:SCREEN_BASE + 8192], dtype=np.uint16)
    byte_pairs = words.view(np.uint8).reshape(-1, 2)  # [low_byte, high_byte] per word (little-endian)
    bits = np.unpackbits(byte_pairs, axis=1, bitorder="little")  # (8192, 16), left-to-right per word
    pixels = bits.reshape(SCREEN_H, SCREEN_W)
    return np.where(pixels != 0, 0, 255).astype(np.uint8)


class Computer:
    def __init__(self, hack_path, scale=2, steps_per_tick=300_000, fps=30):
        self.cpu = CPU()
        self.cpu.load_hack(hack_path)

        self.scale = scale
        self.steps_per_tick = steps_per_tick
        self.frame_delay_ms = max(1, int(1000 / fps))
        self.running = True

        self.root = tk.Tk()
        self.root.title("Hack Computer")
        self.label = tk.Label(self.root)
        self.label.pack()
        self.photo = None  # keep a reference so Tk doesn't garbage-collect it

        self.root.bind("<KeyPress>", self._on_key_press)
        self.root.bind("<KeyRelease>", self._on_key_release)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _key_code(self, event):
        if event.keysym in KEYSYM_TO_CODE:
            return KEYSYM_TO_CODE[event.keysym]
        ch = event.char
        if ch and 0 < ord(ch) < 256:
            return ord(ch)
        return None

    def _on_key_press(self, event):
        code = self._key_code(event)
        if code is not None:
            self.cpu.ram[KEYBOARD_ADDR] = code

    def _on_key_release(self, event):
        self.cpu.ram[KEYBOARD_ADDR] = 0

    def _on_close(self):
        self.running = False
        self.root.destroy()

    def _render(self):
        arr = render_screen_array(self.cpu.ram)
        img = Image.fromarray(arr, mode="L")
        if self.scale != 1:
            img = img.resize((SCREEN_W * self.scale, SCREEN_H * self.scale), Image.NEAREST)
        self.photo = ImageTk.PhotoImage(img)
        self.label.configure(image=self.photo)

    def _tick(self):
        if not self.running:
            return
        if not self.cpu.halted:
            try:
                self.cpu.run(max_steps=self.steps_per_tick)
            except Exception as exc:  # surface simulator bugs without killing the window
                print(f"CPU error: {exc}", file=sys.stderr)
                self.cpu.halted = True
        self._render()
        self.root.after(self.frame_delay_ms, self._tick)

    def start(self):
        self.root.after(0, self._tick)
        self.root.mainloop()


def main():
    if len(sys.argv) != 2:
        print("usage: computer.py <path-to-.hack-file>", file=sys.stderr)
        sys.exit(1)
    Computer(sys.argv[1]).start()


if __name__ == "__main__":
    main()
