// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// LOAD 8192 into screenPointer
@8191
D=A
@screenPointer
M=D

(TOP)

@SCREEN
D=A
@screenPointer
A=D+M           // Address of SCREEN + ScreenPointer
M=-1            // Set this Memory address to -1 (black)

@screenPointer  
MD=M-1          // reduce the value of ScreenPointer by 1

@END
D;JLT           // Stop if ScreenPointer is less than 0

@TOP
0;JMP

(END)
@END
0;JMP