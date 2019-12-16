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
            @true
            D;JEQ
            
            (false)
            // *SP = 0
            @SP
            A=M
            M=0

            @end
            0;JMP

            (true)
            // *SP = -1
            @SP
            A=M
            M=-1

            (end)
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
            @true
            D;JEQ
            
            (false)
            // *SP = 0
            @SP
            A=M
            M=0

            @end
            0;JMP

            (true)
            // *SP = -1
            @SP
            A=M
            M=-1

            (end)
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
            @true
            D;JEQ
            
            (false)
            // *SP = 0
            @SP
            A=M
            M=0

            @end
            0;JMP

            (true)
            // *SP = -1
            @SP
            A=M
            M=-1

            (end)
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
            @true
            D;JLT
            
            (false)
            // *SP = 0
            @SP
            A=M
            M=0

            @end
            0;JMP

            (true)
            // *SP = -1
            @SP
            A=M
            M=-1

            (end)
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
            @true
            D;JLT
            
            (false)
            // *SP = 0
            @SP
            A=M
            M=0

            @end
            0;JMP

            (true)
            // *SP = -1
            @SP
            A=M
            M=-1

            (end)
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
            @true
            D;JLT
            
            (false)
            // *SP = 0
            @SP
            A=M
            M=0

            @end
            0;JMP

            (true)
            // *SP = -1
            @SP
            A=M
            M=-1

            (end)
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
            @true
            D;JGT
            
            (false)
            // *SP = 0
            @SP
            A=M
            M=0

            @end
            0;JMP

            (true)
            // *SP = -1
            @SP
            A=M
            M=-1

            (end)
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
            @true
            D;JGT
            
            (false)
            // *SP = 0
            @SP
            A=M
            M=0

            @end
            0;JMP

            (true)
            // *SP = -1
            @SP
            A=M
            M=-1

            (end)
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
            @true
            D;JGT
            
            (false)
            // *SP = 0
            @SP
            A=M
            M=0

            @end
            0;JMP

            (true)
            // *SP = -1
            @SP
            A=M
            M=-1

            (end)
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
     //and
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
     //or
// not
     //not