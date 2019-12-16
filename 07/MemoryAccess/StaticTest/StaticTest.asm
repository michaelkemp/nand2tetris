// push constant 111

        // *SP = i
        @111
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 333

        // *SP = i
        @333
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 888

        // *SP = i
        @888
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// pop static 8

        // SP--
        @SP
        M=M-1

        // *static = *SP
        @SP
        A=M
        D=M
        @StaticTest.8
        M=D
    
// pop static 3

        // SP--
        @SP
        M=M-1

        // *static = *SP
        @SP
        A=M
        D=M
        @StaticTest.3
        M=D
    
// pop static 1

        // SP--
        @SP
        M=M-1

        // *static = *SP
        @SP
        A=M
        D=M
        @StaticTest.1
        M=D
    
// push static 3

        // *SP = *static
        @StaticTest.3
        D=M
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push static 1

        // *SP = *static
        @StaticTest.1
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
        
// push static 8

        // *SP = *static
        @StaticTest.8
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
        