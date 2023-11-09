#!/usr/bin/env python3

import sys, os, re
import vm2asm

def main(pathData, asmPath):

    ## Instantiate Translator
    translate = vm2asm.Translator()
 
    ## Bootstrap (Set Stack Pointer to 256, call Sys.init)
    BOOTSTRAP = "//BOOTSTRAP,@256,D=A,@SP,M=D,".replace(",","\n")
    BOOTSTRAP += translate.parse(["call Sys.init 0"], "BOOTSTRAP")
    ADDBSTRAP = False

    ASM = ""
    for pd in pathData:
        vm = []
        vmPath = pd["vmPath"]
        filePre = pd["filePre"]
        with open(vmPath) as fp:
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

            ASM += translate.parse(vm, filePre)
    
    if ADDBSTRAP:
        ASM = BOOTSTRAP + ASM

    with open(asmPath, 'w') as asmFile:
        asmFile.write(ASM)
    print("Done")



if __name__ == "__main__":
    
    ## Check if file path was supplied
    if len(sys.argv) != 2:
        print("Usage: vmtranslator.py path/file.vm")
        print("       vmtranslator.py path")
        exit(0)

    vmFilePath = sys.argv[1]
    pathData = []

    if os.path.isfile(vmFilePath):
        vmPath = os.path.abspath(vmFilePath)
        filePath, fileName = os.path.split(vmPath)
        filePre, fileExt = os.path.splitext(fileName)
        asmPath = os.path.join(filePath, filePre + ".asm")
        if fileExt != ".vm":
            raise FileNotFoundError("File must be of type .vm")
        pathData.append({"vmPath": vmPath, "filePre": filePre})
        main(pathData, asmPath)

    elif os.path.isdir(vmFilePath):
        fullPath = os.path.abspath(vmFilePath)
        asmPre = os.path.basename(fullPath)
        asmPath = os.path.join(fullPath, asmPre + ".asm")
        fileList = os.listdir(fullPath)
        for fileName in fileList:
            filePre, fileExt = os.path.splitext(fileName)
            if fileName.endswith(".vm"):
                vmPath = os.path.join(fullPath, fileName)
                pathData.append({"vmPath": vmPath, "filePre": filePre})
        if len(pathData) == 0:
            raise FileNotFoundError("File must be of type .vm")
        main(pathData, asmPath)
    else:
        raise FileNotFoundError("File Not Found")