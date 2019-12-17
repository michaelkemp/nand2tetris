#!/usr/bin/env python3

import sys
import os.path
from os import path
import re

staticName = "static"

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
    jmpCnt = 0

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
            asm.append(mathEQ(jmpCnt))
            jmpCnt = jmpCnt + 1
        elif expression == "gt":
            asm.append(mathGT(jmpCnt))
            jmpCnt = jmpCnt + 1
        elif expression == "lt":
            asm.append(mathLT(jmpCnt))
            jmpCnt = jmpCnt + 1
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

def mathAdd():
    return """
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
    """

def mathSub():
    return """
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
    """

def mathNeg():
    return """
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
    """

def mathEQ(jmp):
    return """
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
        @true-{}
        D;JEQ
        
        // *SP = 0
        @SP
        A=M
        M=0

        @end-{}
        0;JMP

        (true-{})
        // *SP = -1
        @SP
        A=M
        M=-1

        (end-{})
        // SP++
        @SP
        M=M+1
    """.format(jmp,jmp,jmp,jmp)

def mathGT(jmp):
    return """
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
        @true-{}
        D;JGT
        
        // *SP = 0
        @SP
        A=M
        M=0

        @end-{}
        0;JMP

        (true-{})
        // *SP = -1
        @SP
        A=M
        M=-1

        (end-{})
        // SP++
        @SP
        M=M+1
    """.format(jmp,jmp,jmp,jmp)

def mathLT(jmp):
    return """
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
        @true-{}
        D;JLT
        
        // *SP = 0
        @SP
        A=M
        M=0

        @end-{}
        0;JMP

        (true-{})
        // *SP = -1
        @SP
        A=M
        M=-1

        (end-{})
        // SP++
        @SP
        M=M+1
    """.format(jmp,jmp,jmp,jmp)


def logicAnd():
    return """
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
    """

def logicOr():
    return """
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
    """

def logicNot():
    return """
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
    """

def branch(command, label):
    return "branch"

def fnctFunction(command, functionName, nVars):
    return "fnctFunction"

def fnctCall(command, functionName, nArgs):
    return "fnctCall"

def returnFC():
    return "return"

def segPush(segment, variable): # local, argument, this, that
    return """
        // addr = segmentPointer+i
        @{}
        D=M
        @{}
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
    """.format(segNames[segment],variable)

def segPop(segment, variable): # local, argument, this, that
    return """
        // addr = segmentPointer+i
        @{}
        D=M
        @{}
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
    """.format(segNames[segment],variable)


def staticPush(variable): # static -- filename.i
    tmp = staticName + "." + variable
    return """
        // *SP = *static
        @{}
        D=M
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    """.format(tmp)

def staticPop(variable): # static -- filename.i
    tmp = staticName + "." + variable
    return """
        // SP--
        @SP
        M=M-1

        // *static = *SP
        @SP
        A=M
        D=M
        @{}
        M=D
    """.format(tmp)

def tempPush(variable): # temp -- R5 - R12
    return """
        // addr = R5+i
        @R5
        D=A
        @{}
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
    """.format(variable)

def tempPop(variable): # temp -- R5 - R12
    return """
        // addr = R5+i
        @R5
        D=A
        @{}
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
    """.format(variable)

def pointerPush(variable): # pointer -- 0/1 THIS/THAT
    return """
        // *SP = THIS/THAT
        @{}
        D=M
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    """.format(disordat[variable])

def pointerPop(variable): # pointer -- 0/1 THIS/THAT
    return """
        // SP--
        @SP
        M=M-1

        // THIS/THAT = *SP
        @SP
        A=M
        M=D
        @{}
        M=D
    """.format(disordat[variable])


def constantPush(variable): # constant
    return """
        // *SP = i
        @{}
        D=A
        @SP
        A=M
        M=D

        // SP++
        @SP
        M=M+1
    """.format(variable)


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