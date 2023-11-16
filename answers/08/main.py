#!/usr/bin/env python3

import sys, os, re
import hackTranslator

def main(pathData, asmPath):

    ## Instantiate Translator
    translate = hackTranslator.Translator(pathData)
 
    ASM = translate.getAssembly()

    with open(asmPath, 'w') as asmFile:
        asmFile.write(ASM)


if __name__ == "__main__":
    
    ## Check if file path was supplied
    if len(sys.argv) != 2:
        print("Usage: main.py path/file.vm")
        print("       main.py path")
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
