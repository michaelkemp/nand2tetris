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

    ## Write Tokens to XML T File
    xml = "<tokens>\n"
    for token in tokens:
        tp = token["type"]
        vl = token["value"].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quote;')
        xml += "<{}> {} </{}>\n".format(tp, vl, tp)
    xml += "</tokens>\n"
    with open(xmlTPath, 'w') as xmlFile:
        xmlFile.write(xml)


    ## Initialize CompliationEngine
    jackCmpEng = jackCompilationEngine.CompliationEngine(tokens)
    compiled = jackCmpEng.parseTokens()
    xml = xmled(compiled)
    with open(xmlPath, 'w') as xmlFile:
      xmlFile.write(xml)
    print("done")

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
