
// function Sys.init 0
(Sys.init)

// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Class1.set 2
@Class1.set$ret.0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@7
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(Class1.set$ret.0)

// pop temp 0
@R5
D=A
@0
D=D+A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D

// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Class2.set 2
@Class2.set$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@7
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(Class2.set$ret.1)

// pop temp 0
@R5
D=A
@0
D=D+A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D

// call Class1.get 0
@Class1.get$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(Class1.get$ret.2)

// call Class2.get 0
@Class2.get$ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(Class2.get$ret.3)

// label WHILE
(WHILE)

// goto WHILE
@WHILE
0;JMP

// function Class2.set 0
(Class2.set)

// push argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop static 0
@SP
M=M-1
@SP
A=M
D=M
@Class2.0
M=D

// push argument 1
@ARG
D=M
@1
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop static 1
@SP
M=M-1
@SP
A=M
D=M
@Class2.1
M=D

// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// return
@LCL
D=M
@endFrame
M=D
@endFrame
D=M
@5
D=D-A
A=D
D=M
@retAddr
M=D
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@endFrame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@endFrame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@endFrame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@endFrame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@retAddr
A=M
0;JMP

// function Class2.get 0
(Class2.get)

// push static 0
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1

// push static 1
@Class2.1
D=M
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1

// return
@LCL
D=M
@endFrame
M=D
@endFrame
D=M
@5
D=D-A
A=D
D=M
@retAddr
M=D
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@endFrame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@endFrame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@endFrame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@endFrame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@retAddr
A=M
0;JMP

// function Class1.set 0
(Class1.set)

// push argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop static 0
@SP
M=M-1
@SP
A=M
D=M
@Class1.0
M=D

// push argument 1
@ARG
D=M
@1
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop static 1
@SP
M=M-1
@SP
A=M
D=M
@Class1.1
M=D

// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// return
@LCL
D=M
@endFrame
M=D
@endFrame
D=M
@5
D=D-A
A=D
D=M
@retAddr
M=D
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@endFrame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@endFrame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@endFrame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@endFrame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@retAddr
A=M
0;JMP

// function Class1.get 0
(Class1.get)

// push static 0
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1

// push static 1
@Class1.1
D=M
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1

// return
@LCL
D=M
@endFrame
M=D
@endFrame
D=M
@5
D=D-A
A=D
D=M
@retAddr
M=D
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@endFrame
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@endFrame
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@endFrame
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@endFrame
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@retAddr
A=M
0;JMP
