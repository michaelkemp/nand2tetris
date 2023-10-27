// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

    @R2
    M=0     // Zero R2

    @R0
    D=M
    @END
    D;JEQ   // END IF R0 == 0

    @R1
    D=M
    @END
    D;JEQ   // END IF R1 == 0

    (LOOP)
        @R0
        D=M     // put value of R0 in D
        @R2
        M=D+M   // Add R2 = R2 + D
        @R1
        MD=M-1  // Reduce R1 by 1
        @END
        D;JEQ   // Goto END if R1 is 0
        @LOOP
        0;JMP   // Goto LOOP

    (END)
        @END
        0;JMP
