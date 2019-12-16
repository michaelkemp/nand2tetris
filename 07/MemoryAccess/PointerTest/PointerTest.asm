// push constant 3030

        // *SP = i
        @3030
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// pop pointer 0

        // SP--
        @SP
        M=M-1

        // THIS/THAT = *SP
        @SP
        A=M
        M=D
        @THIS
        M=D
    
// push constant 3040

        // *SP = i
        @3040
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// pop pointer 1

        // SP--
        @SP
        M=M-1

        // THIS/THAT = *SP
        @SP
        A=M
        M=D
        @THAT
        M=D
    
// push constant 32

        // *SP = i
        @32
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// pop this 2

        // addr = segmentPointer+i
        @THIS
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
    
// push constant 46

        // *SP = i
        @46
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// pop that 6

        // addr = segmentPointer+i
        @THAT
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
    
// push pointer 0

        // *SP = THIS/THAT
        @THIS
        D=M
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push pointer 1

        // *SP = THIS/THAT
        @THAT
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
        
// push this 2

        // addr = segmentPointer+i
        @THIS
        D=M
        @2
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
        
// push that 6

        // addr = segmentPointer+i
        @THAT
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
        