#!/usr/bin/env python3

import sys
import os.path
from os import path
import re

asm = []
hack = []

variables = {   
    'R0'    : 0,
    'R1'    : 1,
    'R2'    : 2,
    'R3'    : 3,
    'R4'    : 4,
    'R5'    : 5,
    'R6'    : 6,
    'R7'    : 7,
    'R8'    : 8,
    'R9'    : 9,
    'R10'   : 10,
    'R11'   : 11,
    'R12'   : 12,
    'R13'   : 13,
    'R14'   : 14,
    'R15'   : 15,
    'SCREEN': 16384,
    'KBD'   : 24576,
    'SP'    : 0,
    'LCL'   : 1,
    'ARG'   : 2,
    'THIS'  : 3,
    'THAT'  : 4,
}

# beginning register of user defined variables
varReg = 16

dest = {
    'null': '000',
    'M'   : '001',  
    'D'   : '010',  
    'MD'  : '011',  
    'DM'  : '011',  
    'A'   : '100',  
    'AM'  : '101',  
    'MA'  : '101',  
    'AD'  : '110',  
    'DA'  : '110',  
    'AMD' : '111',   
    'ADM' : '111',   
    'MDA' : '111',   
    'MAD' : '111',   
    'DMA' : '111',   
    'MAD' : '111',   
}

comp = {
    '0'   : '101010',
    '1'   : '111111',
    '-1'  : '111010',
    'D'   : '001100',
    'A'   : '110000',
    'M'   : '110000',
    '!D'  : '001101',
    '!A'  : '110001',
    '!M'  : '110001',
    '-D'  : '001111',
    '-A'  : '110011',
    '-M'  : '110011',
    'D+1' : '011111',
    'A+1' : '110111',
    'M+1' : '110111',
    'D-1' : '001110',
    'A-1' : '110010',
    'M-1' : '110010',
    'D+A' : '000010',
    'D+M' : '000010',
    'A+D' : '000010',
    'M+D' : '000010',
    'D-A' : '010011',
    'D-M' : '010011',
    'A-D' : '000111',
    'M-D' : '000111',
    'D&A' : '000000',
    'D&M' : '000000',
    'A&D' : '000000',
    'M&D' : '000000',
    'D|A' : '010101',
    'D|M' : '010101',
    'A|D' : '010101',
    'M|D' : '010101',
}

jump = {
    'null' : '000',
    'JGT'  : '001',
    'JEQ'  : '010',
    'JGE'  : '011',
    'JLT'  : '100',
    'JNE'  : '101',
    'JLE'  : '110',
    'JMP'  : '111',
}

def main(asmFile):

    filePath, fileName = os.path.split(asmFile)
    filePre, fileExt = os.path.splitext(fileName)
    if fileExt != ".asm":
        print("File type must be .asm")
        exit(0)

    with open(asmFile) as fp:
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

            # remove training comments and strip all remaining whitespace
            parts=re.split("//", line)
            line = re.sub("\s+", "", parts[0])

            # Add labels to variable dictionary
            if line.startswith("("):
                label = line[line.find("(")+1 : line.find(")")]
                variables[label] = linecount
                continue

            linecount += 1

            asm.append(line)

    for command in asm:
        if command.startswith("@"):
            hack.append(acom(command))
        else:
            hack.append(ccom(command))

    hackPath = os.path.join(filePath, filePre + ".hack")
    with open(hackPath, 'w') as hackFile:
        hackFile.write('\n'.join(hack))
        print("Done")


def acom(command):
    global varReg
    cmd = command[1:]
    try:
        val = int(cmd)
        address = '{0:016b}'.format(val)
    except ValueError:
        if cmd in variables:
            address = '{0:016b}'.format(int(variables[cmd]))
        else:
            variables[cmd] = varReg
            address = '{0:016b}'.format(varReg)
            varReg += 1

    return address

def ccom(command):
    address = "111"
    if "=" not in command:
        command = "null=" + command
    if ";" not in command:
        command = command + ";null"

    d,c,j = re.split('=|;',command)

    if "M" not in c:
        address += "0"
    else:
        address += "1"

    if c in comp:
        address += comp[c]
    else:
        print("Syntax Error: " + command)
        exit(0)
        
    if d in dest:
        address += dest[d]
    else:
        print("Syntax Error: " + command)
        exit(0)

    if j in jump:
        address += jump[j]
    else:
        print("Syntax Error: " + command)
        exit(0)
        
    return address


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: asm.py path/file.asm")
        exit(0)
    asmFile = sys.argv[1]
    if not path.isfile(asmFile):
        print("Cant find file")
        exit(0)
    fullPath = os.path.abspath(asmFile)
    main(fullPath)