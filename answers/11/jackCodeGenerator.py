
import json
class CodeGenerator:
    def __init__(self, parseTree):
        self.parseTree = parseTree
        self.vm = []

        ## name (x , y), type (int, char), kind (field, static), number (0, 1, 2...)
        self.classSymbolTable = [] 
        self.subroutineSymbolTable = []
    
        #print(json.dumps(self.parseTree,indent=2))
        self.parseVariables()
        print(self.classSymbolTable)

## VARIABLES
    def parseVariables(self):
        ## classVarDec
        i = self.find("open","classVarDec")
        vkind = ""
        vtype = ""
        vnames = []
        if i >= 0:
            i += 1
            vkind = self.parseTree[i]["value"]
            i += 1
            vtype = self.parseTree[i]["value"]
            i += 1
            vnames.append(self.parseTree[i]["value"])
            i += 1
            while (self.parseTree[i]["value"] == ","):
                i += 1
                vnames.append(self.parseTree[i]["value"])
                i += 1
        self.classSymbolTable.append({"kind":vkind,"type":vtype,"names":vnames})


    def find(self, type, value):
        for i, dic in enumerate(self.parseTree):
            if dic["type"] == type and dic["value"] == value:
                return i
        return -1