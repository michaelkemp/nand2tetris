#!/usr/bin/env python3

import sys, os, re
import vm2asm

def main(vmPath, asmPath, filePre):
    vm = []
    with open(vmPath) as fp:
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

            vm.append(line)
    
    translate = vm2asm.Translator(vm, filePre)
    asm = translate.parse()
    
    with open(asmPath, 'w') as asmFile:
        asmFile.write('\n'.join(asm))
    print("Done")



if __name__ == "__main__":
    
    ## Check if file path was supplied
    if len(sys.argv) != 2:
        print("Usage: translator.py path/file.vm")
        exit(0)
    
    ## Is supplied path a valid file
    vmFile = sys.argv[1]
    if not os.path.isfile(vmFile):
        print("Cant find file")
        exit(0)

    ## Get absolute path
    vmPath = os.path.abspath(vmFile)

    ## Check if supplied file if of type .asm 
    filePath, fileName = os.path.split(vmPath)
    filePre, fileExt = os.path.splitext(fileName)
    if fileExt != ".vm":
        print("File type must be of type .vm")
        exit(0)
 
    ## Create file path of assembly code
    asmPath = os.path.join(filePath, filePre + ".asm2")

    main(vmPath, asmPath, filePre)
