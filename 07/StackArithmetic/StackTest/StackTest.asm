// push constant 17

        // *SP = i
        @17
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 17

        // *SP = i
        @17
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// eq

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP - D
        @SP
        A=M
        D=M-D
        @true-0
        D;JEQ
        
        // *SP = 0
        @SP
        A=M
        M=0

        @end-0
        0;JMP

        (true-0)
        // *SP = -1
        @SP
        A=M
        M=-1

        (end-0)
        // SP++
        @SP
        M=M+1
    
// push constant 17

        // *SP = i
        @17
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 16

        // *SP = i
        @16
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// eq

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP - D
        @SP
        A=M
        D=M-D
        @true-1
        D;JEQ
        
        // *SP = 0
        @SP
        A=M
        M=0

        @end-1
        0;JMP

        (true-1)
        // *SP = -1
        @SP
        A=M
        M=-1

        (end-1)
        // SP++
        @SP
        M=M+1
    
// push constant 16

        // *SP = i
        @16
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 17

        // *SP = i
        @17
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// eq

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP - D
        @SP
        A=M
        D=M-D
        @true-2
        D;JEQ
        
        // *SP = 0
        @SP
        A=M
        M=0

        @end-2
        0;JMP

        (true-2)
        // *SP = -1
        @SP
        A=M
        M=-1

        (end-2)
        // SP++
        @SP
        M=M+1
    
// push constant 892

        // *SP = i
        @892
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 891

        // *SP = i
        @891
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// lt

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP - D
        @SP
        A=M
        D=M-D
        @true-3
        D;JLT
        
        // *SP = 0
        @SP
        A=M
        M=0

        @end-3
        0;JMP

        (true-3)
        // *SP = -1
        @SP
        A=M
        M=-1

        (end-3)
        // SP++
        @SP
        M=M+1
    
// push constant 891

        // *SP = i
        @891
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 892

        // *SP = i
        @892
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// lt

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP - D
        @SP
        A=M
        D=M-D
        @true-4
        D;JLT
        
        // *SP = 0
        @SP
        A=M
        M=0

        @end-4
        0;JMP

        (true-4)
        // *SP = -1
        @SP
        A=M
        M=-1

        (end-4)
        // SP++
        @SP
        M=M+1
    
// push constant 891

        // *SP = i
        @891
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 891

        // *SP = i
        @891
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// lt

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP - D
        @SP
        A=M
        D=M-D
        @true-5
        D;JLT
        
        // *SP = 0
        @SP
        A=M
        M=0

        @end-5
        0;JMP

        (true-5)
        // *SP = -1
        @SP
        A=M
        M=-1

        (end-5)
        // SP++
        @SP
        M=M+1
    
// push constant 32767

        // *SP = i
        @32767
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 32766

        // *SP = i
        @32766
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// gt

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP - D
        @SP
        A=M
        D=M-D
        @true-6
        D;JGT
        
        // *SP = 0
        @SP
        A=M
        M=0

        @end-6
        0;JMP

        (true-6)
        // *SP = -1
        @SP
        A=M
        M=-1

        (end-6)
        // SP++
        @SP
        M=M+1
    
// push constant 32766

        // *SP = i
        @32766
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 32767

        // *SP = i
        @32767
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// gt

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP - D
        @SP
        A=M
        D=M-D
        @true-7
        D;JGT
        
        // *SP = 0
        @SP
        A=M
        M=0

        @end-7
        0;JMP

        (true-7)
        // *SP = -1
        @SP
        A=M
        M=-1

        (end-7)
        // SP++
        @SP
        M=M+1
    
// push constant 32766

        // *SP = i
        @32766
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 32766

        // *SP = i
        @32766
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// gt

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP - D
        @SP
        A=M
        D=M-D
        @true-8
        D;JGT
        
        // *SP = 0
        @SP
        A=M
        M=0

        @end-8
        0;JMP

        (true-8)
        // *SP = -1
        @SP
        A=M
        M=-1

        (end-8)
        // SP++
        @SP
        M=M+1
    
// push constant 57

        // *SP = i
        @57
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 31

        // *SP = i
        @31
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 53

        // *SP = i
        @53
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// add

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP + D
        @SP
        A=M
        D=M+D

        // *SP = D
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 112

        // *SP = i
        @112
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// sub

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP - D
        @SP
        A=M
        D=M-D

        // *SP = D
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// neg

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // *SP = D
        @SP
        A=M
        M=-D

        // SP++
        @SP
        M=M+1
    
// and

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP & D
        @SP
        A=M
        D=M&D

        // *SP = D
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 82

        // *SP = i
        @82
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// or

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // SP--
        @SP
        M=M-1

        // D = *SP | D
        @SP
        A=M
        D=M|D

        // *SP = D
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// not

        // SP--
        @SP
        M=M-1

        // D = *SP
        @SP
        A=M
        D=M

        // *SP = !D
        @SP
        A=M
        M=!D

        // SP++
        @SP
        M=M+1
    