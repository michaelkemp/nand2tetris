#!/usr/bin/env python3

import sys
import os.path
from os import path
import re

keywords = ["class","constructor","function","method","field","static","var","int","char","boolean","void","true","false","null","this","let","do","if","else","while","return"]
symbols = ["{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~"]

def main(jackFIle):
    clean = ""
    tokens = []

    # clean up comments and white space
    with open(jackFIle) as fp:
        jack = fp.read()

        inStr = False

        i = 0
        while i < len(jack):

            comment = False

            if jack[i] == '"':
                inStr = not inStr

            if jack[i] == "\n":
                inStr = False
            
            if i < len(jack):
                if not inStr and jack[i] == "/" and jack[i+1] == "*":
                    comment = True
                    while i < len(jack) - 1:
                        if jack[i] == "*" and jack[i+1] == "/":
                            i += 1
                            break
                        else:
                            i += 1

                if not inStr and jack[i] == "/" and jack[i+1] == "/":
                    comment = True
                    while i < len(jack) and jack[i] != "\n":
                        i += 1

            if not comment:
                clean += jack[i]

            i += 1

    # tokenize
    while len(clean) > 0:
    
        type = ""
        value = ""

        # whitespace
        while re.search("^\s", clean):
            clean = clean[1:]

        # string
        if re.search('^(")([^\n]*)(")', clean):
            string = re.match('^(")([^\n]*)(")', clean).group(0)
            clean = clean[len(string):]
            type = "stringConst"
            value = string

        if type == "":
            # identifier
            if re.search("^([a-zA-Z]|_(\w))", clean):
                ident = re.match("^([a-zA-Z]+|_+)(\w)*", clean).group(0)
                clean = clean[len(ident):]
                if ident in keywords:
                    type = "keyword"
                    value = ident
                else:
                    type = "identifier"    
                    value = ident


        if type == "":
            # symbols        
            for sym in symbols:
                if re.search("^\\"+sym, clean):
                    clean = clean[1:]
                    type = "symbol"
                    value = sym

        if type == "":
            # integers
            if re.search("^\d+", clean):
                ints = re.match("^\d+", clean).group(0)
                clean = clean[len(ints):]
                type = "intConst"
                value = ints

        if len(clean) > 0 and type == "":
            print("Syntax Error: {}".format(clean))
            exit(0)

        if type != "":
            tokens.append("<{}> {} </{}>".format(type,value,type))

    return "\n".join(tokens)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: tokenizer.py path/file.jack")
        print("       tokenizer.py path")
        exit(0)

    jackFilePath = sys.argv[1]

    if path.isfile(jackFilePath):
        fullPath = os.path.abspath(jackFilePath)
        filePath, fileName = os.path.split(fullPath)
        filePre, fileExt = os.path.splitext(fileName)
        output = main(fullPath)
        print("\n\n===============================\n\n")
        print(output)

        # asmPath = os.path.join(filePath, filePre + ".asm")
        # with open(asmPath, 'w') as asmFile:
        #     asmFile.write(output)
        #     print("Done")

    elif path.isdir(jackFilePath):
        fullPath = os.path.abspath(jackFilePath)
        fileList = os.listdir(fullPath)
        for fileName in fileList:
            filePre, fileExt = os.path.splitext(fileName)
            if fileName.endswith(".jack"):
                filePath = os.path.join(fullPath, fileName)
                output = main(filePath)
                print("\n\n===============================\n\n")
                print(output)

        # filePre = os.path.basename(fullPath)
        # asmPath = os.path.join(fullPath, filePre + ".asm")
        # with open(asmPath, 'w') as asmFile:
        #     asmFile.write(output)
        #     print("Done")

    else:
        print("Cant find file")
        exit(0)
