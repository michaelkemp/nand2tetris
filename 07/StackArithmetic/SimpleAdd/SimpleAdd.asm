// push constant 7

        // *SP = i
        @7
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    
// push constant 8

        // *SP = i
        @8
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
        