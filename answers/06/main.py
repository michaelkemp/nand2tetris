#!/usr/bin/env python3

import sys, os
import hackAssembler

def main(pathData):
    for thisFile in pathData:
        asmPath = thisFile["asmPath"]
        hackPath = thisFile["hackPath"]

        ## Initialize Assembler
        hackAss = hackAssembler.Assembler(asmPath)
        hack = hackAss.hack()

        with open(hackPath, 'w') as hackFile:
            hackFile.write('\n'.join(hack))


if __name__ == "__main__":
    
    ## Check if file path was supplied
    if len(sys.argv) != 2:
        print("Usage: main.py path/file.asm")
        exit(0)

    asmFilePath = sys.argv[1]
    pathData = []

    if os.path.isfile(asmFilePath):
        asmPath = os.path.abspath(asmFilePath)
        filePath, fileName = os.path.split(asmPath)
        filePre, fileExt = os.path.splitext(fileName)
        if fileExt != ".asm":
           raise FileNotFoundError("File must be of type .asm")
        hackPath = os.path.join(filePath, "_" + filePre + ".hack")
        pathData.append({"asmPath": asmPath, "hackPath": hackPath})
        main(pathData)
    else:
        raise FileNotFoundError(f"File not found {asmFilePath}")