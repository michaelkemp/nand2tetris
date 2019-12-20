#!/usr/bin/env python3

import sys
import os.path
from os import path
import re

staticName = "static"
jmpCnt = 0

vm = []
asm = []

disordat = {'0':'THIS', '1':'THAT'}

segNames = {
    'local' :       'LCL',
    'argument' :    'ARG',
    'this' :        'THIS',
    'that' :        'THAT'
}

def main(vmFile):
    global staticName

    filePath, fileName = os.path.split(vmFile)
    filePre, fileExt = os.path.splitext(fileName)
    staticName = filePre

    if fileExt != ".vm":
        print("File type must be .vm")
        exit(0)

    with open(vmFile) as fp:
        prog = fp.readlines()
        linecount = 0
        for line in prog:
            
            # remove leading and training space
            line = line.strip()

            # skip blank lines
            if line == "":
                continue

            # skip lines that begin with // [comments]
            if line.startswith("//"):
                continue

            # remove training comments and standardize remaining whitespace
            parts=re.split("//", line)
            line = re.sub("\s+", " ", parts[0]).strip()

            linecount += 1

            vm.append(line)

    for expression in vm:
        # Comment asm output with current expression
        asm.append("// " + expression)

        if expression.startswith("push") or expression.startswith("pop"):
            command, segment, variable = expression.split(" ")
            asm.append(pushpop(command, segment, variable))
        elif expression.startswith("label") or expression.startswith("goto") or expression.startswith("if-goto"):
            command, label = expression.split(" ")
            asm.append(branch(command, label))
        elif expression.startswith("function"):
            command, functionName, nVars = expression.split(" ")
            asm.append(fnctFunction(command, functionName, nVars))
        elif expression.startswith("call"):
            command, functionName, nArgs = expression.split(" ")
            asm.append(fnctCall(command, functionName, nArgs))
        elif expression == "return":
            asm.append(returnFC())
        elif expression == "add":
            asm.append(mathAdd())
        elif expression == "sub":
            asm.append(mathSub())
        elif expression == "neg":
            asm.append(mathNeg())
        elif expression == "eq":
            asm.append(mathEQ())
        elif expression == "gt":
            asm.append(mathGT())
        elif expression == "lt":
            asm.append(mathLT())
        elif expression == "and":
            asm.append(logicAnd())
        elif expression == "or":
            asm.append(logicOr())
        elif expression == "not":
            asm.append(logicNot())
        else:
            print("Unknown command: " + expression)
            exit(0)

    asmPath = os.path.join(filePath, filePre + ".asm")
    with open(asmPath, 'w') as asmFile:
        asmFile.write('\n'.join(asm))
        print("Done")

def pushpop(command, segment, variable):
    if command == 'push' and segment in {'local', 'argument', 'this', 'that'}:
        return segPush(segment, variable)
    elif command == 'pop' and segment in {'local', 'argument', 'this', 'that'}:
        return segPop(segment, variable)
    elif command == 'push' and segment == 'static':
        return staticPush(variable)
    elif command == 'pop' and segment == 'static':
        return staticPop(variable)
    elif command == 'push' and segment == 'temp':
        return tempPush(variable)
    elif command == 'pop' and segment == 'temp':
        return tempPop(variable)
    elif command == 'push' and segment == 'pointer':
        return pointerPush(variable)
    elif command == 'pop' and segment == 'pointer':
        return pointerPop(variable)
    elif command == 'push' and segment == 'constant':
        return constantPush(variable)
    else:
        print("Error: {}, {}, {}".format(command, segment, variable))
        exit(0)

def pop2Funct(funct):
    tmp = ""
    
    # Decrement the Stack Pointer
    tmp += "@SP,M=M-1,"

    # D = *SP
    tmp += "@SP,A=M,D=M,"

    # Decrement the Stack Pointer
    tmp += "@SP,M=M-1,"

    if funct == "add":          # D = *SP + D
        tmp += "@SP,A=M,D=M+D,"
    elif funct == "sub":        # D = *SP - D
        tmp += "@SP,A=M,D=M-D,"
    elif funct == "and":        # D = *SP & D
        tmp += "@SP,A=M,D=M&D,"
    elif funct == "or":         # D = *SP | D
        tmp += "@SP,A=M,D=M|D,"

    # *SP = D
    tmp += "@SP,A=M,M=D,"

    # Increment the Stack Pointer
    tmp += "@SP,M=M+1,"

    return tmp.replace(",","\n")

def mathAdd():
    return pop2Funct("add")

def mathSub():
    return pop2Funct("sub")

def logicAnd():
    return pop2Funct("and")

def logicOr():
    return pop2Funct("or")

def pop1Funct(funct):
    tmp = ""
    
    # Decrement the Stack Pointer
    tmp += "@SP,M=M-1,"

    # D = *SP
    tmp += "@SP,A=M,D=M,"

    if funct == "neg":          # *SP = -D
        tmp += "@SP,A=M,M=-D,"
    elif funct == "not":        # *SP = !D
        tmp += "@SP,A=M,M=!D,"

    # Increment the Stack Pointer
    tmp += "@SP,M=M+1,"

    return tmp.replace(",","\n")

def mathNeg():
    return pop1Funct("neg")

def logicNot():
    return pop1Funct("not")

def pop2Bool(test):
    global jmpCnt
    tmp = ""

    # Pop top 2 items off the stack and subtract them: SP--, D = *SP, SP--, D = *SP - D
    tmp += "@SP,M=M-1,@SP,A=M,D=M,@SP,M=M-1,@SP,A=M,D=M-D,"

    if test == "eq":                # Jump to (true-i) if D == 0
        tmp += "@true-{},D;JEQ,".format(jmpCnt) 
    elif test == "gt":              # Jump to (true-i) if D > 0
        tmp += "@true-{},D;JGT,".format(jmpCnt)
    elif test == "lt":              # Jump to (true-i) if D < 0
        tmp += "@true-{},D;JLT,".format(jmpCnt)

    # if NOT true, put 0 on the stack
    tmp += "@SP,A=M,M=0,"

    # goto end-i    
    tmp += "@end-{},0;JMP,".format(jmpCnt)  
        
    # if true, put -1 on stack
    tmp += "(true-{}),@SP,A=M,M=-1,".format(jmpCnt)

    # end-i, Increment SP
    tmp += "(end-{}),@SP,M=M+1,".format(jmpCnt)

    jmpCnt += 1

    return tmp.replace(",","\n")

def mathEQ():
    return pop2Bool("eq")

def mathGT():
    return pop2Bool("gt")

def mathLT():
    return pop2Bool("lt")

def segPush(segment, variable): # local, argument, this, that
    tmp = ""

    # addr = segmentPointer+i
    tmp += "@{},D=M,@{},D=D+A,@R13,M=D,".format(segNames[segment],variable)

    # *SP = *addr
    tmp += "@R13,A=M,D=M,@SP,A=M,M=D,"

    # Increment the Stack Pointer
    tmp += "@SP,M=M+1,"

    return tmp.replace(",","\n")

def segPop(segment, variable): # local, argument, this, that
    tmp = ""

    # addr = segmentPointer+i
    tmp += "@{},D=M,@{},D=D+A,@R13,M=D,".format(segNames[segment],variable)

    # Decrement the Stack Pointer
    tmp += "@SP,M=M-1,"

    # *addr = *SP
    tmp += "@SP,A=M,D=M,@R13,A=M,M=D,"

    return tmp.replace(",","\n")

def staticPush(variable): # static -- filename.i
    global staticName
    tmp = ""

    # *SP = *static
    tmp += "@{},D=M,@SP,A=M,M=D,".format(staticName + "." + variable)

    # Increment the Stack Pointer
    tmp += "@SP,M=M+1,"

    return tmp.replace(",","\n")

def staticPop(variable): # static -- filename.i
    global staticName
    tmp = ""

    # Decrement the Stack Pointer
    tmp += "@SP,M=M-1,"

    # *static = *SP
    tmp += "@SP,A=M,D=M,@{},M=D,".format(staticName + "." + variable)

    return tmp.replace(",","\n")


def tempPush(variable): # temp -- R5 - R12
    tmp = ""

    # addr = R5+i
    tmp += "@R5,D=A,@{},D=D+A,@R13,M=D,".format(variable)

    # *SP = *addr
    tmp += "@R13,A=M,D=M,@SP,A=M,M=D,"

    # Increment the Stack Pointer
    tmp += "@SP,M=M+1,"

    return tmp.replace(",","\n")

def tempPop(variable): # temp -- R5 - R12
    tmp = ""

    # addr = R5+i
    tmp += "@R5,D=A,@{},D=D+A,@R13,M=D,".format(variable)

    # Decrement the Stack Pointer
    tmp += "@SP,M=M-1,"

    # *addr = *SP
    tmp += "@SP,A=M,D=M,@R13,A=M,M=D,"

    return tmp.replace(",","\n")


def pointerPush(variable): # pointer -- 0/1 THIS/THAT
    tmp = ""

    # *SP = THIS/THAT
    tmp += "@{},D=M,@SP,A=M,M=D,".format(disordat[variable])

    # Increment the Stack Pointer
    tmp += "@SP,M=M+1,"

    return tmp.replace(",","\n")

def pointerPop(variable): # pointer -- 0/1 THIS/THAT
    tmp = ""

    # Decrement the Stack Pointer
    tmp += "@SP,M=M-1,"

    # THIS/THAT = *SP
    tmp += "@SP,A=M,M=D,@{},M=D,".format(disordat[variable])

    return tmp.replace(",","\n")

def constantPush(variable): # constant
    tmp = ""

    # *SP = i
    tmp += "@{},D=A,@SP,A=M,M=D,".format(variable)

    # Increment the Stack Pointer
    tmp += "@SP,M=M+1,"

    return tmp.replace(",","\n")

def branch(command, label):
    tmp = ""
    if command == "label": 
        tmp += "({}),".format(label)
    elif command == "goto":
        tmp += "@{},0;JMP,".format(label)
    elif command == "if-goto":
        # Decrement the Stack Pointer
        tmp += "@SP,M=M-1,"
        # D = *SP
        tmp += "@SP,A=M,D=M,"
        # Jump if D!=0
        tmp += "@{},D;JNE,".format(label)

    return tmp.replace(",","\n")

def fnctCall(command, functionName, nArgs):
    # push returnAddress        // using the LABEL declared below eg Foo$ret.1
    # push LCL                  // save LCL of caller
    # push ARG                  // save ARG of caller
    # push THIS                 // save THIS of caller
    # push THAT                 // save THAT of caller
    # ARG = SP - 5 - nArgs      // reposition ARG for callee
    # LCL = SP                  // reposition LCL for callee
    # goto functionName         // transfer controll to the called function
    # (returnAddress)           // Declare lable for the return-address

    return "fnctCall"

def fnctFunction(command, functionName, nVars):
    # (functionName)            // declare LABEL for function entry
    # push 0 NVars times        // nVars are the number of local variables, initialize to 0

    return "fnctFunction"

def returnFC():
    # endFrame = LCL            // endFrame is a temporary variable
    # retAddr = *(endFrame -5)  // gets the return address (retAddr another temp var)
    # *ARG = pop()              // put return value into AGR[0]
    # SP = ARG + 1              // reposition SP
    # THAT = *(endFrame - 1)    // restore THAT to caller
    # THIS = *(endFrame - 2)    // restore THIS to caller
    # ARG  = *(endFrame - 3)    // restore ARG to caller
    # LCL  = *(endFrame - 4)    // restore LCL to caller
    # goto retAddr              // jump to return address in callers code 
    
    return "return"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: vmtranslator.py path/file.vm")
        exit(0)
    vmFile = sys.argv[1]
    # needs to work with full dir
    if not path.isfile(vmFile):
        print("Cant find file")
        exit(0)
    fullPath = os.path.abspath(vmFile)
    main(fullPath)