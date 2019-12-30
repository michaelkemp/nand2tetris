#!/usr/bin/env python3

import sys
import os.path
from os import path
import re

def tokenizer(jack):
    keywords = ["class","constructor","function","method","field","static","var","int","char","boolean","void","true","false","null","this","let","do","if","else","while","return"]
    symbols = ["{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~"]
    tokens = []

    # tokenize
    while len(jack) > 0:
    
        found = False

        # whitespace
        while re.search("^\s", jack):
            jack = jack[1:]

        # string
        if re.search('^(")([^\n]*)(")', jack):
            string = re.match('^(")([^\n]*)(")', jack).group(0)
            jack = jack[len(string):]
            type = "stringConstant"
            value = string.strip('"')
            tokens.append({"type":type,"value":value})
            found = True

        # identifier
        if re.search("^([a-zA-Z]+|_+)(\w)*", jack):
            ident = re.match("^([a-zA-Z]+|_+)(\w)*", jack).group(0)
            jack = jack[len(ident):]
            if ident in keywords:
                type = "keyword"
                value = ident
                tokens.append({"type":type,"value":value})
                found = True
            else:
                type = "identifier"    
                value = ident
                tokens.append({"type":type,"value":value})
                found = True
            

        # symbols        
        for sym in symbols:
            if re.search("^\\"+sym, jack):
                jack = jack[1:]
                type = "symbol"
                value = sym
                tokens.append({"type":type,"value":value})
                found = True

        # integers
        if re.search("^\d+", jack):
            ints = re.match("^\d+", jack).group(0)
            jack = jack[len(ints):]
            type = "integerConstant"
            value = ints
            if int(value) < 0 or int(value) > 32767:
                print("Integer out of range: {}".format(value))
                exit(0)
            tokens.append({"type":type,"value":value})
            found = True

        # error
        if len(jack) > 0 and not found:
            print("Syntax Error: {}".format(jack))
            exit(0)
            
    return tokens

# ============================= GRAMMAR =============================
# Structure
#   <class>             =>  'class' <className> '{' <classVarDec>* <subroutineDec>* '}'
#   <classVarDec>       =>  ('static' | 'field') <type> <varName> (',' <varName>)* ';'
#   <type>              =>  'int' | 'char' | 'boolean' | <className>
#   <subroutineDec>     =>  ('constructor' | 'function' | 'method') ('void' | <type>) <subroutineName> '(' <parameterList> ')' <subroutineBody>
#   <parameterList>     =>  (<type> <varName> (',' <type> <varName>)* )?
#   <subroutineBody>    =>  '{' <varDec>* <statements> '}'
#   <varDec>            =>  'var' <type> <varName> (',' <varName>)* ';'
#   <className>         =>  identifier
#   <subroutineName>    =>  identifier
#   <varName>           =>  identifier
# Statements
#   <statements>        =>  <statement>*
#   <statement>         =>  <letStatement> | <ifStatement> | <whileStatement> | <doStatement> | <returnStatement>
#   <letStatement>      =>  'let' <varName> ('[' <expression> ']')? '=' <expression> ';'
#   <ifStatement>       =>  'if' '(' <expression> ')' '{' <statements> '}' ('else' '{' statements> '}')?
#   <whileStatement>    =>  'while' '(' <expression> ')' '{' <statements> '}'
#   <doStatement>       =>  'do' <subroutineCall> ';'
#   <returnStatement>   =>  'return' <expression>? ';'
# Expressions
#   <expression>        =>  <term> (<op> <term>)*
#   <term>              =>  integerConstant | stringConstant | keywordConstant | <varName> | <varName> '[' <expression> ']' | <subroutineCall> | '(' <expression> ')' | unaryOp <term>
#   <subroutineCall>    =>  <subroutineName> '(' <expressionList> ')' | (<className>|<varName>) '.' <subroutineName> '(' <expressionList> ')' <expressionList> => (<expression> (',' <expression>)* )?
#   <expressionList>    =>  ( <expression> (',' <expression>)* )?
#   <op>                =>  '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
#   <unaryOp>           =>  '-' | '~'
#   <keywordConstant>   =>  'true' | 'false' | 'null' | 'this'


def parser(tokens):
    parseTree = []

    return parseTree

def main(jackFile):
    clean = ""

    # clean up comments and white space
    with open(jackFile) as fp:
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

    tokens = tokenizer(clean)    
    return xmled(tokens)

def xmled(tokenList):
    str = "<tokens>\n"
    for i in range(len(tokenList)):
        type = tokenList[i]["type"]
        value = tokenList[i]["value"].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
        str += "<{}> {} </{}>\n".format(type,value,type)

    str += "</tokens>\n"
    return str

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: parser.py path/file.jack")
        print("       parser.py path")
        exit(0)

    jackFilePath = sys.argv[1]

    if path.isfile(jackFilePath):
        fullPath = os.path.abspath(jackFilePath)
        filePath, fileName = os.path.split(fullPath)
        filePre, fileExt = os.path.splitext(fileName)
        if fileName.endswith(".jack"):
            output = main(fullPath)

            xmlPath = os.path.join(fullPath, "_" + filePre + ".xml")
            with open(xmlPath, 'w') as xmlFile:
                xmlFile.write(output)

    elif path.isdir(jackFilePath):
        fullPath = os.path.abspath(jackFilePath)
        fileList = os.listdir(fullPath)
        for fileName in fileList:
            filePre, fileExt = os.path.splitext(fileName)
            if fileName.endswith(".jack"):
                filePath = os.path.join(fullPath, fileName)
                output = main(filePath)

                xmlPath = os.path.join(fullPath, "_" + filePre + ".xml")
                with open(xmlPath, 'w') as xmlFile:
                    xmlFile.write(output)

        print("Done")

    else:
        print("Cant find file")
        exit(0)
