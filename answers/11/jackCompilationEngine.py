import jackExpressions, json

class CompilationEngine:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenPtr = 0
        self.parseTree = []

        self.vmcode = []
        self.classSymbolTable = [] 
        self.subroutineSymbolTable = []
        self.currentClassName = ""
        self.currentSubroutineName = ""
        self.currentSubroutineType = ""
        self.fieldCnt = 0
        self.staticCnt = 0
        self.argumentCnt = 0
        self.localCnt = 0


    def printClassSymbolTable(self):
        print("CLASS: {}".format(self.currentClassName))
        for symbols in sorted(self.classSymbolTable, key=lambda d: d['kind']):
            print(" {} {} {} {}".format(symbols["kind"],symbols["type"],symbols["name"],symbols["num"]))

    def printSubroutineSymbolTable(self):
        print("SUBROUTINE: {}".format(self.currentSubroutineName))
        for symbols in sorted(self.subroutineSymbolTable, key=lambda d: d['kind']):
            print(" {} {} {} {}".format(symbols["kind"],symbols["type"],symbols["name"],symbols["num"]))


    def getNextToken(self, inc=1):
        if self.tokenPtr < len(self.tokens):
            tkn = self.tokens[self.tokenPtr]
            self.tokenPtr += inc
            return [tkn["type"], tkn["value"]]
        else:
            return ["",""] 
    
    def seeNextToken(self):
        return self.getNextToken(0)

    def seeSubroutineCall(self):
        tmp = ""
        if self.tokenPtr < len(self.tokens):
            tkn = self.tokens[self.tokenPtr]
            if (tkn["type"] == "identifier"):
                tmp += tkn["value"]
            else:
                return None
        if self.tokenPtr+1 < len(self.tokens):
            tkn = self.tokens[self.tokenPtr+1]       
            if (tkn["type"] == "symbol") and (tkn["value"] == "."):
                tmp += tkn["value"]
            elif (tkn["type"] == "symbol") and (tkn["value"] == "("):
                return tmp
            else:
                return None
        if self.tokenPtr+2 < len(self.tokens):
            tkn = self.tokens[self.tokenPtr+2]       
            if (tkn["type"] == "identifier"):
                tmp += tkn["value"]
            else:
                return None
        return tmp
    
    def parseTokens(self):
        self.parseTree.append({"type":"open","value":"class"})
        self.compileClass()
        self.parseTree.append({"type":"close","value":"class"})
        return self.parseTree


    def eat(self, expType, expValues=None):
        TYPE, VALUE = self.getNextToken()
        if (TYPE == expType and expValues is None) or (TYPE == expType and VALUE in expValues):
            self.parseTree.append({"type":TYPE,"value":VALUE})
        else:
            print("----",self.parseTree,"-----")
            raise SyntaxError("Expected [{} {}] Received[{} {}]".format(expType, "|".join(expValues), TYPE, VALUE))


    ## TYPE: 'int'|'char'|'boolean'|className
    def eatType(self, incVoid=False):
        expValues = ["int","char","boolean"]
        if incVoid:
            expValues.append("void")
        TYPE, VALUE = self.getNextToken()
        if (TYPE == "keyword" and VALUE in expValues) or (TYPE == "identifier"):
            self.parseTree.append({"type":TYPE,"value":VALUE})
        else:
            raise SyntaxError("Type Error [{} {}]".format(TYPE, VALUE))
        
        
    ## class: 'class' className '{' classVarDec* subroutineDec* '}'
    def compileClass(self):
        self.eat("keyword", ["class"])
     
        ## GEN -- CLASS NAME
        self.classSymbolTable = [] 
        self.currentClassName = ""
        self.fieldCnt = 0
        self.staticCnt = 0
        ty,va = self.seeNextToken()
        self.currentClassName = va
        ## GEN -- /CLASS NAME

        self.eat("identifier")
        self.eat("symbol", ["{"])

        # expect classVarDec*
        # classVarDec: ('static'|'field') TYPE varName (',' varName)* ';'
        TYPE, VALUE = self.seeNextToken()
        while TYPE == "keyword" and VALUE in["static", "field"]:
            self.parseTree.append({"type":"open","value":"classVarDec"})
            self.compileClassVarDec()
            self.parseTree.append({"type":"close","value":"classVarDec"})
            TYPE, VALUE = self.seeNextToken()

        self.printClassSymbolTable()

        # expect subroutineDec*
        # subroutineDec: ('constructor'|'function'|'method') ('void'|TYPE) subroutineName '(' parameterList ')' subroutineBody
        TYPE, VALUE = self.seeNextToken()    
        while TYPE == "keyword" and VALUE in ["constructor", "function", "method"]:

            ## GEN -- SUBROUTINE NAME
            self.subroutineSymbolTable = []
            self.currentSubroutineName = ""
            self.currentSubroutineType = ""
            self.argumentCnt = 0
            self.localCnt = 0
            ## GEN -- /SUBROUTINE NAME

            self.parseTree.append({"type":"open","value":"subroutineDec"})
            self.compileSubroutineDec()
            self.parseTree.append({"type":"close","value":"subroutineDec"})
            TYPE, VALUE = self.seeNextToken()

            self.printSubroutineSymbolTable()

        self.eat("symbol", ["}"])


    ## classVarDec: ('static'|'field') TYPE varName (',' varName)* ';'
    def compileClassVarDec(self):

        ## GEN -- CLASS VAR KIND
        ty,va = self.seeNextToken()
        classVarKind = va
        ## GEN -- /CLASS VAR KIND

        self.eat("keyword",["static","field"])

        ## GEN -- CLASS VAR TYPE
        ty,va = self.seeNextToken()
        classVarType = va
        ## GEN -- /CLASS VAR TYPE

        self.eatType()

        ## GEN -- CLASS VAR NAME
        classVarNames = []
        ty,va = self.seeNextToken()
        classVarNames.append(va)
        ## GEN -- /CLASS VAR NAME

        self.eat("identifier")

        # (',' varName)*
        TYPE, VALUE = self.seeNextToken()
        while (TYPE == "symbol" and VALUE == ","):
            self.eat("symbol", [","])

            ## GEN -- CLASS VAR NAME
            ty,va = self.seeNextToken()
            classVarNames.append(va)
            ## GEN -- /CLASS VAR NAME

            self.eat("identifier")
            TYPE, VALUE = self.seeNextToken()

        self.eat("symbol", [";"])

        ## GEN -- CLASS SYMBOLTABLE
        for name in classVarNames:
            if classVarKind == "field":
                self.classSymbolTable.append({"kind":classVarKind, "type":classVarType, "name":name, "num":self.fieldCnt})
                self.fieldCnt += 1
            if classVarKind == "static":
                self.classSymbolTable.append({"kind":classVarKind, "type":classVarType, "name":name, "num":self.staticCnt})
                self.staticCnt += 1
        ## GEN -- /CLASS SYMBOLTABLE



    ## subroutineDec: ('constructor'|'function'|'method') ('void'|TYPE) subroutineName '(' parameterList ')' subroutineBody
    def compileSubroutineDec(self):

        ## GEN -- SUBROUTINE TYPE
        ty,va = self.seeNextToken()
        self.currentSubroutineType = va
        ## GEN -- /SUBROUTINE TYPE

        self.eat("keyword",["constructor","function","method"])
        self.eatType(True) ## include Void in Type

        ## GEN -- SUBROUTINE NAME
        ty,va = self.seeNextToken()
        self.currentSubroutineName = va
        ## GEN -- /SUBROUTINE NAME

        self.eat("identifier")

        self.eat("symbol", ["("])
        self.parseTree.append({"type":"open","value":"parameterList"})
        self.compileParameterList()
        self.parseTree.append({"type":"close","value":"parameterList"})
        self.eat("symbol", [")"])

        self.parseTree.append({"type":"open","value":"subroutineBody"})
        self.compileSubroutineBody()
        self.parseTree.append({"type":"close","value":"subroutineBody"})


    ## parameterList: ((TYPE varName) (',' TYPE varName)*)?
    def compileParameterList(self):

        ## GEN -- SUBROUTINE METHOD
        if self.currentSubroutineType == "method":
            self.subroutineSymbolTable.append({"kind":"argument", "type":self.currentClassName, "name":"this", "num":self.argumentCnt})
            self.argumentCnt += 1
        ## GEN -- SUBROUTINE METHOD

        TYPE, VALUE = self.seeNextToken()
        if (TYPE == "keyword" and (VALUE == "int" or VALUE == "char" or VALUE == "boolean")) or (TYPE == "identifier"):
            while True:

                ## GEN -- SUBROUTINE ARG TYPE
                ty,va = self.seeNextToken()
                subVarType = va
                ## GEN -- /SUBROUTINE ARG TYPE

                self.eatType()

                ## GEN -- SUBROUTINE ARG NAME
                ty,va = self.seeNextToken()
                subVarName = va
                ## GEN -- /SUBROUTINE ARG NAME
 
                self.eat("identifier")

                ## GEN -- SUBROUTINE ADD ARG
                self.subroutineSymbolTable.append({"kind":"argument", "type":subVarType, "name":subVarName, "num":self.argumentCnt})
                self.argumentCnt += 1
                ## GEN -- SUBROUTINE ADD ARG

                # (',' TYPE varName)*
                TYPE, VALUE = self.seeNextToken()
                if TYPE == "symbol" and VALUE == ",":
                    self.eat("symbol", [","])
                else:
                    break



    ## subroutineBody: '{' varDec* statements '}'
    def compileSubroutineBody(self):
        self.eat("symbol", ["{"])

        # varDec*
        # varDec: 'var' TYPE varName (',' varName)* ';'
        TYPE, VALUE = self.seeNextToken()
        while TYPE == "keyword" and VALUE == "var":
            self.parseTree.append({"type":"open","value":"varDec"})
            self.compileVarDec()
            self.parseTree.append({"type":"close","value":"varDec"})
            TYPE, VALUE = self.seeNextToken()

        self.parseTree.append({"type":"open","value":"statements"})
        self.compileStatements()
        self.parseTree.append({"type":"close","value":"statements"})
        self.eat("symbol", ["}"])


    ## varDec: 'var' TYPE varName (',' varName)* ';'
    def compileVarDec(self):
        self.eat("keyword", ["var"])

        ## GEN -- SUBROUTINE LOCAL TYPE
        ty,va = self.seeNextToken()
        subVarType = va
        ## GEN -- /SUBROUTINE LOCAL TYPE

        self.eatType()

        while True:

            ## GEN -- SUBROUTINE LOCAL NAME
            ty,va = self.seeNextToken()
            subVarName = va
            ## GEN -- /SUBROUTINE LOCAL NAME

            self.eat("identifier")

            ## GEN -- SUBROUTINE ADD LOCAL
            self.subroutineSymbolTable.append({"kind":"local", "type":subVarType, "name":subVarName, "num":self.localCnt})
            self.localCnt += 1
            ## GEN -- /SUBROUTINE ADD LOCAL

            # (',' varName)*
            TYPE, VALUE = self.seeNextToken()
            if TYPE == "symbol" and VALUE == ",":
                self.eat("symbol", [","])
            else:
                break
        
        self.eat("symbol", [";"])


    ## statements: statement*
    ## statement:  letStatement | ifStatement | whileStatement | doStatement | returnStatement
    def compileStatements(self):
        TYPE, VALUE = self.seeNextToken()
        while TYPE == "keyword" and VALUE in ["let","if","while","do","return"]:
            match VALUE:
                case "let":
                    self.parseTree.append({"type":"open","value":"letStatement"})
                    self.compileLet()
                    self.parseTree.append({"type":"close","value":"letStatement"})
                case "if":
                    self.parseTree.append({"type":"open","value":"ifStatement"})
                    self.compileIf()
                    self.parseTree.append({"type":"close","value":"ifStatement"})
                case "while":
                    self.parseTree.append({"type":"open","value":"whileStatement"})
                    self.compileWhile()
                    self.parseTree.append({"type":"close","value":"whileStatement"})
                case "do":
                    self.parseTree.append({"type":"open","value":"doStatement"})
                    self.compileDo()
                    self.parseTree.append({"type":"close","value":"doStatement"})
                case "return":
                    self.parseTree.append({"type":"open","value":"returnStatement"})
                    self.compileReturn()
                    self.parseTree.append({"type":"close","value":"returnStatement"})
            TYPE, VALUE = self.seeNextToken()


    ## letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    def compileLet(self):
        self.eat("keyword",["let"])
        self.eat("identifier")

        # ('[' expression ']')?
        TYPE, VALUE = self.seeNextToken()
        if TYPE == "symbol" and VALUE == "[":
            self.eat("symbol",["["])
            self.parseTree.append({"type":"open","value":"expression"})

            ## GEN -- EXPRESSION
            letExpression = jackExpressions.Expressions()
            ## GEN -- /EXPRESSION

            self.compileExpression(letExpression)

            ## GEN -- EXPRESSION
            letExpression.printExpression()
            ## GEN -- /EXPRESSION

            self.parseTree.append({"type":"close","value":"expression"})
            self.eat("symbol",["]"])
        

        self.eat("symbol",["="])
        self.parseTree.append({"type":"open","value":"expression"})

        ## GEN -- EXPRESSION
        letExpression = jackExpressions.Expressions()
        ## GEN -- /EXPRESSION

        self.compileExpression(letExpression)

        ## GEN -- EXPRESSION
        letExpression.printExpression()
        ## GEN -- /EXPRESSION

        self.parseTree.append({"type":"close","value":"expression"})
        self.eat("symbol",[";"])
        

    ## ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    def compileIf(self):
        self.eat("keyword",["if"])

        self.eat("symbol",["("])
        self.parseTree.append({"type":"open","value":"expression"})

        ## GEN -- EXPRESSION
        ifExpression = jackExpressions.Expressions()
        ## GEN -- /EXPRESSION

        self.compileExpression(ifExpression)

        ## GEN -- EXPRESSION
        ifExpression.printExpression()
        ## GEN -- /EXPRESSION

        self.parseTree.append({"type":"close","value":"expression"})
        self.eat("symbol",[")"])

        self.eat("symbol",["{"])
        self.parseTree.append({"type":"open","value":"statements"})
        self.compileStatements()
        self.parseTree.append({"type":"close","value":"statements"})
        self.eat("symbol",["}"])

        # ('else' '{' statements '}')?
        TYPE, VALUE = self.seeNextToken()
        if TYPE == "keyword" and VALUE == "else":
            self.eat("keyword",["else"])
            self.eat("symbol",["{"])
            self.parseTree.append({"type":"open","value":"statements"})
            self.compileStatements()
            self.parseTree.append({"type":"close","value":"statements"})
            self.eat("symbol",["}"])



    ## whileStatement: 'while' '(' expression ')' '{' statements '}'
    def compileWhile(self):
        self.eat("keyword",["while"])

        self.eat("symbol",["("])
        self.parseTree.append({"type":"open","value":"expression"})

        ## GEN -- EXPRESSION
        whileExpression = jackExpressions.Expressions()
        ## GEN -- /EXPRESSION

        self.compileExpression(whileExpression)

        ## GEN -- EXPRESSION
        whileExpression.printExpression()
        ## GEN -- /EXPRESSION

        self.parseTree.append({"type":"close","value":"expression"})
        self.eat("symbol",[")"])

        self.eat("symbol",["{"])    
        self.parseTree.append({"type":"open","value":"statements"})
        self.compileStatements()
        self.parseTree.append({"type":"close","value":"statements"})
        self.eat("symbol",["}"])


    ## doStatement: 'do' subroutineCall ';'
    def compileDo(self):
        ## GEN -- EXPRESSION
        doExpression = jackExpressions.Expressions()
        ## GEN -- /EXPRESSION

        self.eat("keyword",["do"])
        self.compileSubroutineCall(True, doExpression)
        self.eat("symbol",[";"])

        ## GEN -- EXPRESSION
        doExpression.printExpression()
        ## GEN -- /EXPRESSION


    ## returnStatement: 'return' expression? ';'
    def compileReturn(self):
        self.eat("keyword",["return"])

        # ;
        TYPE, VALUE = self.seeNextToken()
        if TYPE == "symbol" and VALUE == ";":
            self.eat("symbol",[";"])
        # expression?    
        else:
            self.parseTree.append({"type":"open","value":"expression"})

            ## GEN -- EXPRESSION
            returnExpression = jackExpressions.Expressions()
            ## GEN -- /EXPRESSION

            self.compileExpression(returnExpression)

            ## GEN -- EXPRESSION
            returnExpression.printExpression()
            ## GEN -- /EXPRESSION

            self.parseTree.append({"type":"close","value":"expression"})
            self.eat("symbol",[";"])


    ## term: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOP term
    def compileTerm(self, parent):
        print("==================",type(parent))
        TYPE, VALUE = self.seeNextToken()

        match TYPE:

            # integerConstant | stringConstant
            case "integerConstant" | "stringConstant":
                ## GEN -- TERM
                ty,va = self.seeNextToken()
                parent.addTerm(va,"constant")
                ## GEN -- /TERM

                self.eat(TYPE)

            # keywordConstant
            case "keyword":
                ## GEN -- TERM
                ty,va = self.seeNextToken()
                parent.addTerm(va,"keyword")
                ## GEN -- /TERM

                self.eat("keyword", ['true','false','null','this'])

            case "symbol":
                match VALUE:
                    # '(' expression ')'    
                    case "(":
                        ## GEN -- TERM
                        ty,va = self.seeNextToken()
                        parent.addTerm(va,"symbol")
                        ## GEN -- /TERM

                        self.eat("symbol",["("])

                        self.parseTree.append({"type":"open","value":"expression"})
                        self.compileExpression(parent)
                        self.parseTree.append({"type":"close","value":"expression"})
 
                        ## GEN -- TERM
                        ty,va = self.seeNextToken()
                        parent.addTerm(va,"symbol")
                        ## GEN -- /TERM

                        self.eat("symbol",[")"])

                    # unaryOP term        
                    case "-" | "~":
                        ## GEN -- TERM
                        ty,va = self.seeNextToken()
                        parent.addTerm(va,"unary")
                        ## GEN -- /TERM

                        self.eat("symbol",[VALUE])
                        self.parseTree.append({"type":"open","value":"term"})
                        self.compileTerm(parent)
                        self.parseTree.append({"type":"close","value":"term"})

            case "identifier":
                # varName | varName '[' expression ']' | subroutineCall

                ## GEN -- TERM
                if self.seeSubroutineCall():
                    va = self.seeSubroutineCall()
                    tmp = jackExpressions.Expressions()
                    parent.addTerm(va,"call", tmp)
                else:
                    ty,va = self.seeNextToken()
                    parent.addTerm(va,"var")
                ## GEN -- /TERM

                self.eat("identifier")

                TYPE, VALUE = self.seeNextToken()
                match VALUE:
                    # '[' expression ']'
                    case "[":

                        self.eat("symbol",["["])
                        self.parseTree.append({"type":"open","value":"expression"})
                        self.compileExpression(parent)
                        self.parseTree.append({"type":"close","value":"expression"})
                        self.eat("symbol",["]"])

                    # subroutineCall    
                    case "(" | ".":
                        self.compileSubroutineCall(False, tmp)


    ## expression: term (op term)*
    ## op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    def compileExpression(self, parent):
        self.parseTree.append({"type":"open","value":"term"})
        self.compileTerm(parent)
        self.parseTree.append({"type":"close","value":"term"})

        # (op term)*
        TYPE, VALUE = self.seeNextToken()
        while TYPE == "symbol" and VALUE in ["+","-","*","/","&","|","<",">","="]:

            ## GEN -- TERM
            ty,va = self.seeNextToken()
            parent.addTerm(va,"symbol")
            ## GEN -- /TERM

            self.eat("symbol",[VALUE])

            self.parseTree.append({"type":"open","value":"term"})
            self.compileTerm(parent)
            self.parseTree.append({"type":"close","value":"term"})
            TYPE, VALUE = self.seeNextToken()
 

    ## expressionList: (expression (',' expression)* )?
    def compileExpressionList(self, parent):

        expList = []
        TYPE, VALUE = self.seeNextToken()
        if (TYPE in ["integerConstant","stringConstant","identifier"]) or (TYPE=="keyword" and VALUE in ['true','false','null','this']) or (TYPE == "symbol" and VALUE in ["(","-","~"]):
            self.parseTree.append({"type":"open","value":"expression"})

            tmp = jackExpressions.Expressions()
            expList.append(tmp)
            self.compileExpression(tmp)

            self.parseTree.append({"type":"close","value":"expression"})
            TYPE, VALUE = self.seeNextToken()
            while TYPE == "symbol" and VALUE == ",":
                self.eat("symbol", [","])
                self.parseTree.append({"type":"open","value":"expression"})

                tmp = jackExpressions.Expressions()
                expList.append(tmp)
                self.compileExpression(tmp)

                self.parseTree.append({"type":"close","value":"expression"})
                TYPE, VALUE = self.seeNextToken()

        parent.addChildren(expList)

    ## subroutineCall: subroutineName '(' expressionList ')' | (className|varName)'.'subroutineName '(' expressionList ')'
    def compileSubroutineCall(self, eatName, parent):

        if eatName:
            self.eat("identifier")

        TYPE, VALUE = self.seeNextToken()
        if TYPE == "symbol" and VALUE == ".":
            self.eat("symbol",["."])
            self.eat("identifier")
        
        # '(' expressionList ')'
        self.eat("symbol",["("])    
        self.parseTree.append({"type":"open","value":"expressionList"})
        self.compileExpressionList(parent)
        self.parseTree.append({"type":"close","value":"expressionList"})
        self.eat("symbol",[")"])    
