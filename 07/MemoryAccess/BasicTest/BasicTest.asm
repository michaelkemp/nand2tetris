// push constant 10

        // *SP = i
        @10
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// pop local 0

        // addr = segmentPointer+i
        @LCL
        D=M
        @0
        D=D+A
        @R13
        M=D

        // SP--
        @SP
        M=M-1

        // *addr = *SP
        @SP
        A=M
        D=M
        @R13
        A=M
        M=D
    
// push constant 21

        // *SP = i
        @21
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 22

        // *SP = i
        @22
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// pop argument 2

        // addr = segmentPointer+i
        @ARG
        D=M
        @2
        D=D+A
        @R13
        M=D

        // SP--
        @SP
        M=M-1

        // *addr = *SP
        @SP
        A=M
        D=M
        @R13
        A=M
        M=D
    
// pop argument 1

        // addr = segmentPointer+i
        @ARG
        D=M
        @1
        D=D+A
        @R13
        M=D

        // SP--
        @SP
        M=M-1

        // *addr = *SP
        @SP
        A=M
        D=M
        @R13
        A=M
        M=D
    
// push constant 36

        // *SP = i
        @36
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// pop this 6

        // addr = segmentPointer+i
        @THIS
        D=M
        @6
        D=D+A
        @R13
        M=D

        // SP--
        @SP
        M=M-1

        // *addr = *SP
        @SP
        A=M
        D=M
        @R13
        A=M
        M=D
    
// push constant 42

        // *SP = i
        @42
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 45

        // *SP = i
        @45
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// pop that 5

        // addr = segmentPointer+i
        @THAT
        D=M
        @5
        D=D+A
        @R13
        M=D

        // SP--
        @SP
        M=M-1

        // *addr = *SP
        @SP
        A=M
        D=M
        @R13
        A=M
        M=D
    
// pop that 2

        // addr = segmentPointer+i
        @THAT
        D=M
        @2
        D=D+A
        @R13
        M=D

        // SP--
        @SP
        M=M-1

        // *addr = *SP
        @SP
        A=M
        D=M
        @R13
        A=M
        M=D
    
// push constant 510

        // *SP = i
        @510
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// pop temp 6

        // addr = R5+i
        @R5
        D=A
        @6
        D=D+A
        @R13
        M=D

        // SP--
        @SP
        M=M-1

        // *addr = *SP
        @SP
        A=M
        D=M
        @R13
        A=M
        M=D
    
// push local 0

        // addr = segmentPointer+i
        @LCL
        D=M
        @0
        D=D+A
        @R13
        M=D

        // *SP = *addr
        @R13
        A=M
        D=M
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push that 5

        // addr = segmentPointer+i
        @THAT
        D=M
        @5
        D=D+A
        @R13
        M=D

        // *SP = *addr
        @R13
        A=M
        D=M
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
        
// push argument 1

        // addr = segmentPointer+i
        @ARG
        D=M
        @1
        D=D+A
        @R13
        M=D

        // *SP = *addr
        @R13
        A=M
        D=M
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
        
// push this 6

        // addr = segmentPointer+i
        @THIS
        D=M
        @6
        D=D+A
        @R13
        M=D

        // *SP = *addr
        @R13
        A=M
        D=M
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push this 6

        // addr = segmentPointer+i
        @THIS
        D=M
        @6
        D=D+A
        @R13
        M=D

        // *SP = *addr
        @R13
        A=M
        D=M
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
        
// push temp 6

        // addr = R5+i
        @R5
        D=A
        @6
        D=D+A
        @R13
        M=D

        // *SP = *addr
        @R13
        A=M
        D=M
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
        