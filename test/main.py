#!/usr/bin/env python3

import sys, os, json
import jackTokenizer

def main(pathData, xmlPath):

  for pd in pathData:
    jackPath = pd["jackPath"]
    filePre = pd["filePre"]
    with open(jackPath) as fp:
      jack = fp.read()

    jackTkizr = jackTokenizer.Tokenizer(jack)
    tmp = jackTkizr.getTokens()
    print(json.dumps(tmp,indent=2))


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
    xmlPath = os.path.join(filePath, filePre + ".xml")
    if fileExt != ".jack":
      raise FileNotFoundError("File must be of type .jack")
    pathData.append({"jackPath": jackPath, "filePre": filePre})
    main(pathData, xmlPath)

  elif os.path.isdir(jackFilePath):
    fullPath = os.path.abspath(jackFilePath)
    xmlPre = os.path.basename(fullPath)
    xmlPath = os.path.join(fullPath, xmlPre + ".xml")
    fileList = os.listdir(fullPath)
    for fileName in fileList:
      filePre, fileExt = os.path.splitext(fileName)
      if fileName.endswith(".jack"):
        jackPath = os.path.join(fullPath, fileName)
        pathData.append({"jackPath": jackPath, "filePre": filePre})
    if len(pathData) == 0:
      raise FileNotFoundError("File must be of type .jack")
    main(pathData, xmlPath)
  else:
    raise FileNotFoundError("File Not Found")
