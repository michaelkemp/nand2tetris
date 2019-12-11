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

// Check for keypress
(CHECKKBD)
@KBD
D=M         // id D == 0, no key is pressed
@NOKEY
D;JEQ 

(KEY)       // a key was pressed, set R0 to -1 (paint black)
@R0
M=-1
@PAINT
0;JMP

(NOKEY)     // no key pressed, set R0 to 0 (paint white)
@R0
M=0

(PAINT)
// put BEGIN screen address into screenBEG
@SCREEN
D=A
@screenBEG
M=D

// put END screen address into screenEND
@SCREEN
D=A
@8192
D=D+A
@screenEND
M=D

// load screenBEG into R0
@screenBEG
D=M
@upto
M=D

(COLOR)
@R0         // Get color from R0
D=M
@upto       // get screen location
A=M     
M=D         // set screen location color
@upto       // increment screen location
M=M+1

@upto       // if upto == screenEND finish the loop
D=M
@screenEND  
D=D-M
@CHECKKBD
D;JEQ

@COLOR
0;JMP

