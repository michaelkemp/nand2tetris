import re

class Translator:
    def __init__(self, pathData):

        self.pathData = pathData

        self.asm = ""
        self.jmpCnt = 0
        self.retCnt = 0

        self.disordat = {'0':'THIS', '1':'THAT'}
        self.segNames = {'local':'LCL', 'argument':'ARG', 'this':'THIS', 'that':'THAT'}

        ## Bootstrap (Set Stack Pointer to 256, call Sys.init)
        self.staticName = "BOOTSTRAP"
        BOOTSTRAP = "//BOOTSTRAP,@256,D=A,@SP,M=D,".replace(",","\n")
        BOOTSTRAP += self.parse(["call Sys.init 0"])
        ADDBSTRAP = False

        for pd in self.pathData:
            self.staticName = pd["filePre"]
            vmPath = pd["vmPath"]
            with open(vmPath) as fp:
                vm = []
                prog = fp.readlines()
                for line in prog:
                    ## Strip leading and trailing spaces
                    line = line.strip()
                    ## Skip blank lines
                    if line == "":
                        continue
                    ## Skip comment lines -- lines that begin with //
                    if re.match("^//", line) is not None:
                        continue
                    ## Remove inline comments
                    line = line.split("//", 1)[0].strip()
                    vm.append(line)
                    if line == "function Sys.init 0":
                        ADDBSTRAP = True

                self.asm += self.parse(vm)

    
        if ADDBSTRAP:
            self.asm = BOOTSTRAP + self.asm


    def getAssembly(self):
        return self.asm
    

    def parse(self, vm):
        ASM = ""
        for expression in vm:

            # Comment asm output with current expression
            ASM += f"\n// {expression}\n"

            command = expression.split(" ", 1)[0].strip()
            match command:
                case "push" | "pop":
                    ASM += self.pushpop(expression)

                case "label" | "goto" | "if-goto":
                    ASM += self.branch(expression)
                
                case "function":
                    ASM += self.fnctFunction(expression)
                case "call":
                    ASM += self.fnctCall(expression)
                case "return":
                    ASM += self.fnctReturn()
                
                case "add":
                    ASM += self.mathAdd()
                case "sub":
                    ASM += self.mathSub()
                case "neg":
                    ASM += self.mathNeg()

                case "eq":
                    ASM += self.mathEQ()
                case "gt":
                    ASM += self.mathGT()
                case "lt":
                    ASM += self.mathLT()

                case "and":
                    ASM += self.logicAnd()
                case "or":
                    ASM += self.logicOr()
                case "not":
                    ASM += self.logicNot()

                case _:
                    raise SyntaxError(f"Unknown expression: {expression}")
            
        return ASM
        

    def pushpop(self, expression):
        command, segment, variable = expression.split(" ")
        match command:
            case "push":
                match segment:
                    case "local" | "argument" | "this" | "that":
                        return self.segPush(segment, variable)
                    case "static":
                        return self.staticPush(variable)
                    case "temp":
                        return self.tempPush(variable)
                    case "pointer":
                        return self.pointerPush(variable)
                    case "constant":
                        return self.constantPush(variable)
                    case _:
                        raise SyntaxError(f"Unknown expression: {expression}")
            case "pop":
                match segment:
                    case "local" | "argument" | "this" | "that":
                        return self.segPop(segment, variable)
                    case "static":
                        return self.staticPop(variable)
                    case "temp":
                        return self.tempPop(variable)
                    case "pointer":
                        return self.pointerPop(variable)
                    case _:
                        raise SyntaxError(f"Unknown expression: {expression}")


    def branch(self, expression):
        command, label = expression.split(" ")
        tmp = ""
        match command:
            case "label":
                # Write Label
                tmp += f"({label}),"
            case "goto":
                # Unconditional Jump
                tmp += f"@{label},0;JMP,"
            case "if-goto":
                # Decrement the Stack Pointer
                tmp += "@SP,M=M-1,"
                # D = *SP
                tmp += "@SP,A=M,D=M,"
                # Jump if D!=0
                tmp += f"@{label},D;JNE,"

        return tmp.replace(",","\n")
    

    def fnctFunction(self, expression):
        command, functionName, nVars = expression.split(" ")
        tmp = ""

        # (functionName)            // declare LABEL for function entry
        tmp += f"({functionName}),"

        # push 0 NVars times        // nVars are the number of local variables, initialize to 0
        for i in range(0, int(nVars)):
            tmp += "@0,D=A,@SP,A=M,M=D,@SP,M=M+1,"

        return tmp.replace(",","\n")
    

    def fnctCall(self, expression):
        command, functionName, nArgs = expression.split(" ")
        tmp = ""

        retAdr = functionName + "$ret." + str(self.retCnt)
        self.retCnt += 1

        # push returnAddress        // using the LABEL declared below eg Foo$ret.1
        tmp += f"@{retAdr},D=A,@SP,A=M,M=D,@SP,M=M+1,"

        # push LCL                  // save LCL of caller
        tmp += "@LCL,D=M,@SP,A=M,M=D,@SP,M=M+1,"

        # push ARG                  // save ARG of caller
        tmp += "@ARG,D=M,@SP,A=M,M=D,@SP,M=M+1,"

        # push THIS                 // save THIS of caller
        tmp += "@THIS,D=M,@SP,A=M,M=D,@SP,M=M+1,"

        # push THAT                 // save THAT of caller
        tmp += "@THAT,D=M,@SP,A=M,M=D,@SP,M=M+1,"

        # ARG = SP - 5 - nArgs      // reposition ARG for callee
        back = int(nArgs) + 5
        tmp += f"@SP,D=M,@{back},D=D-A,@ARG,M=D,"

        # LCL = SP                  // reposition LCL for callee
        tmp += "@SP,D=M,@LCL,M=D,"

        # goto functionName         // transfer controll to the called function
        tmp += f"@{functionName},0;JMP,"

        # (returnAddress)           // Declare lable for the return-address
        tmp += f"({retAdr}),"

        return tmp.replace(",","\n")


    def fnctReturn(self):
        tmp = ""

        # endFrame = LCL            // endFrame is a temporary variable
        tmp += "@LCL,D=M,@endFrame,M=D,"

        # retAddr = *(endFrame -5)  // gets the return address (retAddr another temp var)
        tmp += "@endFrame,D=M,@5,D=D-A,A=D,D=M,@retAddr,M=D,"

        # *ARG = pop()              // put return value into AGR[0]
        tmp += "@SP,M=M-1,@SP,A=M,D=M,@ARG,A=M,M=D,"

        # SP = ARG + 1              // reposition SP
        tmp += "@ARG,D=M+1,@SP,M=D,"

        # THAT = *(endFrame - 1)    // restore THAT to caller
        tmp += "@endFrame,D=M,@1,D=D-A,A=D,D=M,@THAT,M=D,"

        # THIS = *(endFrame - 2)    // restore THIS to caller
        tmp += "@endFrame,D=M,@2,D=D-A,A=D,D=M,@THIS,M=D,"

        # ARG  = *(endFrame - 3)    // restore ARG to caller
        tmp += "@endFrame,D=M,@3,D=D-A,A=D,D=M,@ARG,M=D,"

        # LCL  = *(endFrame - 4)    // restore LCL to caller
        tmp += "@endFrame,D=M,@4,D=D-A,A=D,D=M,@LCL,M=D,"

        # goto retAddr              // jump to return address in callers code 
        tmp += "@retAddr,A=M,0;JMP,"

        return tmp.replace(",","\n")
    

    def mathAdd(self):
        return self.AddSubAndOr("add")

    def mathSub(self):
        return self.AddSubAndOr("sub")
        
    def logicAnd(self):
        return self.AddSubAndOr("and")
        
    def logicOr(self):
        return self.AddSubAndOr("or")

    def mathNeg(self):
        return self.NegNot("neg")
        
    def logicNot(self):
        return self.NegNot("not")
        
    def mathEQ(self):
        return self.EqGtLt("eq")
        
    def mathGT(self):
        return self.EqGtLt("gt")
        
    def mathLT(self):
        return self.EqGtLt("lt")



############################## Helper Functions ##############################

    ############################ MATH & LOGIC ############################

    def EqGtLt(self, func):
        tmp = ""

        # Pop top 2 items off the stack and subtract them: SP--, D = *SP, SP--, D = *SP - D
        tmp += "@SP,M=M-1,@SP,A=M,D=M,@SP,M=M-1,@SP,A=M,D=M-D,"

        match func:
            case "eq": # Jump to (true-i) if D == 0
                tmp += f"@true-{self.jmpCnt},D;JEQ," 
            case "gt":  # Jump to (true-i) if D > 0
                tmp += f"@true-{self.jmpCnt},D;JGT,"
            case "lt": # Jump to (true-i) if D < 0
                tmp += f"@true-{self.jmpCnt},D;JLT,"

        # if NOT true, put 0 on the stack
        tmp += "@SP,A=M,M=0,"

        # goto end-i    
        tmp += f"@end-{self.jmpCnt},0;JMP,"  
            
        # if true, put -1 on stack
        tmp += f"(true-{self.jmpCnt}),@SP,A=M,M=-1,"

        # end-i, Increment SP
        tmp += f"(end-{self.jmpCnt}),@SP,M=M+1,"

        self.jmpCnt += 1

        return tmp.replace(",","\n")


    def AddSubAndOr(self, func):
        tmp = ""

        # Decrement the Stack Pointer
        tmp += "@SP,M=M-1,"

        # D = *SP
        tmp += "@SP,A=M,D=M,"

        # Decrement the Stack Pointer
        tmp += "@SP,M=M-1,"
        
        match func:
            case "add": # D = *SP + D
                tmp += "@SP,A=M,D=M+D,"
            case "sub": # D = *SP - D
                tmp += "@SP,A=M,D=M-D,"
            case "and": # D = *SP & D
                tmp += "@SP,A=M,D=M&D,"
            case "or": # D = *SP | D
                tmp += "@SP,A=M,D=M|D,"

        # *SP = D
        tmp += "@SP,A=M,M=D,"

        # Increment the Stack Pointer
        tmp += "@SP,M=M+1,"

        return tmp.replace(",","\n")


    def NegNot(self, func):
        tmp = ""
    
        # Decrement the Stack Pointer
        tmp += "@SP,M=M-1,"

        # D = *SP
        tmp += "@SP,A=M,D=M,"

        match func:
            case "neg": # *SP = -D
                tmp += "@SP,A=M,M=-D,"
            case "not": # *SP = !D
                tmp += "@SP,A=M,M=!D,"

        # Increment the Stack Pointer
        tmp += "@SP,M=M+1,"

        return tmp.replace(",","\n")



    ############################ PUSH & POP ############################

    def segPush(self, segment, variable): # local, argument, this, that
        tmp = ""

        # addr = segmentPointer+i
        tmp += f"@{self.segNames[segment]},D=M,@{variable},D=D+A,@R13,M=D,"

        # *SP = *addr
        tmp += "@R13,A=M,D=M,@SP,A=M,M=D,"

        # Increment the Stack Pointer
        tmp += "@SP,M=M+1,"

        return tmp.replace(",","\n")

    def segPop(self, segment, variable): # local, argument, this, that
        tmp = ""

        # addr = segmentPointer+i
        tmp += f"@{self.segNames[segment]},D=M,@{variable},D=D+A,@R13,M=D,"

        # Decrement the Stack Pointer
        tmp += "@SP,M=M-1,"

        # *addr = *SP
        tmp += "@SP,A=M,D=M,@R13,A=M,M=D,"

        return tmp.replace(",","\n")


    def staticPush(self, variable): # static -- filename.i
        tmp = ""

        # *SP = *static
        tmp += f"@{self.staticName}.{variable},D=M,@SP,A=M,M=D,"

        # Increment the Stack Pointer
        tmp += "@SP,M=M+1,"

        return tmp.replace(",","\n")

    def staticPop(self, variable): # static -- filename.i
        tmp = ""

        # Decrement the Stack Pointer
        tmp += "@SP,M=M-1,"

        # *static = *SP
        tmp += f"@SP,A=M,D=M,@{self.staticName}.{variable},M=D,"

        return tmp.replace(",","\n")


    def tempPush(self, variable): # temp -- R5 - R12
        tmp = ""

        # addr = R5+i
        tmp += f"@R5,D=A,@{variable},D=D+A,@R13,M=D,"

        # *SP = *addr
        tmp += "@R13,A=M,D=M,@SP,A=M,M=D,"

        # Increment the Stack Pointer
        tmp += "@SP,M=M+1,"

        return tmp.replace(",","\n")

    def tempPop(self, variable): # temp -- R5 - R12
        tmp = ""

        # addr = R5+i
        tmp += f"@R5,D=A,@{variable},D=D+A,@R13,M=D,"

        # Decrement the Stack Pointer
        tmp += "@SP,M=M-1,"

        # *addr = *SP
        tmp += "@SP,A=M,D=M,@R13,A=M,M=D,"

        return tmp.replace(",","\n")


    def pointerPush(self, variable): # pointer -- 0/1 THIS/THAT
        tmp = ""

        # *SP = THIS/THAT
        tmp += f"@{self.disordat[variable]},D=M,@SP,A=M,M=D,"

        # Increment the Stack Pointer
        tmp += "@SP,M=M+1,"

        return tmp.replace(",","\n")

    def pointerPop(self, variable): # pointer -- 0/1 THIS/THAT
        tmp = ""

        # Decrement the Stack Pointer
        tmp += "@SP,M=M-1,"

        # THIS/THAT = *SP
        tmp += f"@SP,A=M,M=D,@{self.disordat[variable]},M=D,"

        return tmp.replace(",","\n")

    def constantPush(self, variable): # constant
        tmp = ""

        # *SP = i
        tmp += f"@{variable},D=A,@SP,A=M,M=D,"

        # Increment the Stack Pointer
        tmp += "@SP,M=M+1,"

        return tmp.replace(",","\n")
    
