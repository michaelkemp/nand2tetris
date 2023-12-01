#!/usr/bin/env python3

import sys, os
import jackTokenizer, jackCompilationEngine

def main(pathData):

    for thisFile in pathData:
        jackPath = thisFile["jackPath"]
        xmlPath = thisFile["xmlPath"]
        xmlTPath = thisFile["xmlTPath"]

        ## Initialize Tokenizer
        jackTkizr = jackTokenizer.Tokenizer(jackPath)
        tokens = jackTkizr.getTokens()

        ## Initialize CompilationEngine
        jackCmpEng = jackCompilationEngine.CompilationEngine(tokens)
        vmCode = jackCmpEng.parseTokens()
        print("\n".join(vmCode))

if __name__ == "__main__":
    
    ## Check if file path was supplied
    if len(sys.argv) != 2:
        print("Usage: main.py path/file.jack")
        print("       main.py path")
        exit(0)

    jackFilePath = sys.argv[1]
    pathData = []

    if os.path.isfile(jackFilePath):
        jackPath = os.path.abspath(jackFilePath)
        filePath, fileName = os.path.split(jackPath)
        filePre, fileExt = os.path.splitext(fileName)
        if fileExt != ".jack":
            raise FileNotFoundError("File must be of type .jack")
        xmlPath = os.path.join(filePath, "_" + filePre + ".xml")
        xmlTPath = os.path.join(filePath, "_" + filePre + "T.xml")
        pathData.append({"jackPath": jackPath, "xmlPath": xmlPath, "xmlTPath": xmlTPath})
        main(pathData)

    elif os.path.isdir(jackFilePath):
        fullPath = os.path.abspath(jackFilePath)
        xmlPre = os.path.basename(fullPath)
        xmlPath = os.path.join(fullPath, xmlPre + ".xml")
        fileList = os.listdir(fullPath)
        for fileName in fileList:
            filePre, fileExt = os.path.splitext(fileName)
            if fileName.endswith(".jack"):
                jackPath = os.path.join(fullPath, fileName)
                xmlPath = os.path.join(fullPath, "_" + filePre + ".xml")
                xmlTPath = os.path.join(fullPath, "_" + filePre + "T.xml")
                pathData.append({"jackPath": jackPath, "xmlPath": xmlPath, "xmlTPath": xmlTPath})
        if len(pathData) == 0:
            raise FileNotFoundError("File must be of type .jack")
        main(pathData)
    else:
        raise FileNotFoundError("File Not Found")
