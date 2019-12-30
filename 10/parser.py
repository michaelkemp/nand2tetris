#!/usr/bin/env python3

import sys
import os.path
from os import path
import re

tokens = []
tokenPtr = 0

def seeNextToken():
    return getNextToken(0)

def getNextToken(inc=1):
    global tokenPtr
    tokenPtr += inc
    try:
        return [tokens[tokenPtr-inc]["type"],tokens[tokenPtr-inc]["value"]]
    except:
        return ["",""] 

def tokenizer(jack):
    global tokens
    global tokenPtr
    tokens = []
    tokenPtr = 0

    keywords = ["class","constructor","function","method","field","static","var","int","char","boolean","void","true","false","null","this","let","do","if","else","while","return"]
    symbols = ["{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~"]

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
#   <subroutineCall>    =>  <subroutineName> '(' <expressionList> ')' | (<className>|<varName>) '.' <subroutineName> '(' <expressionList> ')' 
#   <expressionList>    =>  ( <expression> (',' <expression>)* )?
#   <op>                =>  '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
#   <unaryOp>           =>  '-' | '~'
#   <keywordConstant>   =>  'true' | 'false' | 'null' | 'this'

def compileClass():

    # expect <className>
    type,value = getNextToken()
    if type == "identifier":
        parseTree.append({"type":type,"value":value})
    else:
        print("Error in compileClass(): {} {}".format(type,value))
        exit(0)

    # expect {
    type,value = getNextToken()
    if type == "symbol" and value == "{":
        parseTree.append({"type":type,"value":value})
    else:
        print("Error in compileClass(): {} {}".format(type,value))
        exit(0)

    # check <classVarDec> OR <subroutineDec>
    type,value = seeNextToken()
    while type == "keyword" and (value == "static" or value == "field"):
        parseTree.append({"type":"open","value":"classVarDec"})
        compileClassVarDec()
        parseTree.append({"type":"close","value":"classVarDec"})
        type,value = seeNextToken()

    print("\n\n ---------------- {} ------------- {}\n\n".format(type,value) )

    type,value = seeNextToken()    
    while type == "keyword" and (value == "constructor" or value == "function" or value == "method"):
        parseTree.append({"type":"open","value":"subroutineDec"})
        compileSubroutineDec()
        parseTree.append({"type":"close","value":"subroutineDec"})
        type,value = seeNextToken()

    # expect }
    type,value = getNextToken()
    if type == "symbol" and value == "}":
        parseTree.append({"type":type,"value":value})
    else:
        print("Error in compileClass(): {} {}".format(type,value))
        return #exit(0)



def compileClassVarDec():

    # expect 'static' | 'field' 
    type,value = getNextToken()
    if type == "keyword" and (value == "static" or value == "field"):
        parseTree.append({"type":type,"value":value})
    else:
        print("Error in compileClassVarDec(): {} {}".format(type,value))
        exit(0)

    # expect 'int' | 'char' | 'boolean' | <className>
    type,value = getNextToken()
    if (type == "keyword" and (value == "int" or value == "char" or value == "boolean")) or (type == "identifier"):
        parseTree.append({"type":type,"value":value})
    else:
        print("Error in compileClassVarDec(): {} {}".format(type,value))
        exit(0)

    # expect <varName>
    type,value = getNextToken()
    if type == "identifier":
        parseTree.append({"type":type,"value":value})
    else:
        print("Error in compileClassVarDec(): {} {}".format(type,value))
        exit(0)

    # maybe more <varName>
    type,value = seeNextToken()
    while (type == "symbol" and value == ","):

        # expect ,
        type,value = getNextToken()
        if type == "symbol" and value == ",":
            parseTree.append({"type":type,"value":value})
        else:
            print("Error in compileClassVarDec(): {} {}".format(type,value))
            exit(0)

        # expect <varName>
        type,value = getNextToken()
        if type == "identifier":
            parseTree.append({"type":type,"value":value})
        else:
            print("Error in compileClassVarDec(): {} {}".format(type,value))
            exit(0)

        type,value = seeNextToken()

    # expect ;
    type,value = getNextToken()
    if type == "symbol" and value == ";":
        parseTree.append({"type":type,"value":value})
    else:
        print("Error in compileClassVarDec(): {} {}".format(type,value))
        exit(0)



def compileSubroutineDec():

    # expect 'constructor' | 'function' | 'method' 
    type,value = getNextToken()
    if type == "keyword" and (value == "constructor" or value == "function" or value == "method"):
        parseTree.append({"type":type,"value":value})
    else:
        print("Error in compileSubroutineDec(): {} {}".format(type,value))
        exit(0)

    # expect 'void' | 'int' | 'char' | 'boolean' | <className>
    type,value = getNextToken()
    if (type == "keyword" and (value == "void" or value == "int" or value == "char" or value == "boolean")) or (type == "identifier"):
        parseTree.append({"type":type,"value":value})
    else:
        print("Error in compileSubroutineDec(): {} {}".format(type,value))
        exit(0)

    # expect <subroutineName>
    type,value = getNextToken()
    if type == "identifier":
        parseTree.append({"type":type,"value":value})
    else:
        print("Error in compileSubroutineDec(): {} {}".format(type,value))
        exit(0)

    # expect (
    type,value = getNextToken()
    if type == "symbol" and value == "(":
        parseTree.append({"type":type,"value":value})
    else:
        print("Error in compileSubroutineDec(): {} {}".format(type,value))
        exit(0)

    parseTree.append({"type":"open","value":"parameterList"})
    compileParameterList()
    parseTree.append({"type":"close","value":"parameterList"})

    # expect )
    type,value = getNextToken()
    if type == "symbol" and value == ")":
        parseTree.append({"type":type,"value":value})
    else:
        print("Error in compileSubroutineDec(): {} {}".format(type,value))
        exit(0)

    parseTree.append({"type":"open","value":"subroutineBody"})
    compileSubroutineBody()
    parseTree.append({"type":"close","value":"subroutineBody"})


def compileParameterList():

    type,value = seeNextToken()
    if type == "symbol" and value == ")":
        return

    while True:
        # expect 'int' | 'char' | 'boolean' | <className>
        type,value = getNextToken()
        if (type == "keyword" and (value == "int" or value == "char" or value == "boolean")) or (type == "identifier"):
            parseTree.append({"type":type,"value":value})
        else:
            print("Error in compileParameterList(): {} {}".format(type,value))
            exit(0)

        # expect <varName>
        type,value = getNextToken()
        if type == "identifier":
            parseTree.append({"type":type,"value":value})
        else:
            print("Error in compileParameterList(): {} {}".format(type,value))
            exit(0)

        # maybe more <type> <varName>
        type,value = seeNextToken()
        if type == "symbol" and value == ",":
            type,value = getNextToken()
            parseTree.append({"type":type,"value":value})
        elif type == "symbol" and value == ")":
            return
        else:
            print("Error in compileParameterList(): {} {}".format(type,value))
            exit(0)


def compileSubroutineBody():
    print(getNextToken())
    return
def compileVarDec():
    print(getNextToken())
    return
def compileStatements():
    print(getNextToken())
    return
def compileLet():
    print(getNextToken())
    return
def compileIf():
    print(getNextToken())
    return
def compileWhile():
    print(getNextToken())
    return
def compileDo():
    print(getNextToken())
    return
def compileReturn():
    print(getNextToken())
    return
def compileExpression():
    print(getNextToken())
    return
def compileTerm(): # look ahead for '[', '(', or '.' -- array, variable, subroutine call
    print(getNextToken())
    return
def compileExpressionList():
    print(getNextToken())
    return

## simple rules with no corresponding functions - type, className, subroutineName, varName, statement, subroutineCall    

parseTree = []

def parser():
    global parseTree

    # expect class
    type,value = getNextToken()
    if type == "keyword" and value == "class":
        parseTree.append({"type":"open","value":"class"})
        parseTree.append({"type":type,"value":value})
        compileClass()
        parseTree.append({"type":"close","value":"class"})
    else:
        print("Error in parser(): {} {}".format(type,value))
        exit(0)


def main(jackFile):
    global parseTree
    parseTree = []
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

    tokenizer(clean)
    parser()
    print(parseTree)
    return xmled(parseTree)

def xmled(parseTreeList):
    tabCount = 0
    tabSpaces = 2
    str = ""
    for i in range(len(parseTreeList)):
        type = parseTreeList[i]["type"]
        value = parseTreeList[i]["value"].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
        if type == "open":
            str += " "*tabCount
            str += "<{}>\n".format(value)
            tabCount += tabSpaces
        elif type == "close":
            tabCount -= tabSpaces
            str += " "*tabCount
            str += "</{}>\n".format(value)
        else:
            str += " "*tabCount
            str += "<{}> {} </{}>\n".format(type,value,type)
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
                print("\n--{}".format(fileName))
                filePath = os.path.join(fullPath, fileName)
                output = main(filePath)

                xmlPath = os.path.join(fullPath, "_" + filePre + ".xml")
                with open(xmlPath, 'w') as xmlFile:
                    xmlFile.write(output)

        print("Done")

    else:
        print("Cant find file")
        exit(0)
