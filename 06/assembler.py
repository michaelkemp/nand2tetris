#!/usr/bin/env python3

import sys, os, re
import asm2hack

def main(asmPath, hackPath):
    asm = []
    with open(asmPath) as fp:
        prog = fp.readlines()
        linecount = 0
        for line in prog:

            ## Strip leading and trailing spaces
            line = line.strip()

            ## Skip blank lines
            if line == "":
                continue
            
            ## Skip comment lines -- lines that begin with //
            if re.match("^\/\/", line) is not None:
                continue

            ## Remove inline comments
            line = line.split("//", 1)[0].strip()

           # Add label
            if line.startswith("("):
                asm2hack.addLabel(line[1:-1], len(asm))
                continue
            
            asm.append(line)
    
    hack = asm2hack.hack(asm)
    with open(hackPath, 'w') as hackFile:
        hackFile.write('\n'.join(hack))
    print("Done")


if __name__ == "__main__":
    
    ## Check if file path was supplied
    if len(sys.argv) != 2:
        print("Usage: assembler.py path/file.asm")
        exit(0)
    
    ## Is supplied path a valid file
    asmFile = sys.argv[1]
    if not os.path.isfile(asmFile):
        print("Cant find file")
        exit(0)

    ## Get absolute path
    asmPath = os.path.abspath(asmFile)

    ## Check if supplied file if of type .asm 
    filePath, fileName = os.path.split(asmPath)
    filePre, fileExt = os.path.splitext(fileName)
    if fileExt != ".asm":
        print("File type must be of type .asm")
        exit(0)
 
    ## Create file path of assembled code
    hackPath = os.path.join(filePath, filePre + ".hack")

    main(asmPath, hackPath)
