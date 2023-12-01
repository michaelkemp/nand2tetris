import jackExpressions, json

class CompilationEngine:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenPtr = 0
        self.parseTree = []

        self.vmCode = []
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
        print(f"CLASS: {self.currentClassName}")
        for symbols in sorted(self.classSymbolTable, key=lambda d: d['kind']):
            print(f" {symbols['kind']} {symbols['type']} {symbols['name']} {symbols['num']}")

    def printSubroutineSymbolTable(self):
        print(f"SUBROUTINE: {self.currentSubroutineName}")
        for symbols in sorted(self.subroutineSymbolTable, key=lambda d: d['kind']):
            print(f" {symbols['kind']} {symbols['type']} {symbols['name']} {symbols['num']}")


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
        return self.vmCode


    def eat(self, expType, expValues=None):
        TYPE, VALUE = self.getNextToken()
        if (TYPE == expType and expValues is None) or (TYPE == expType and VALUE in expValues):
            self.parseTree.append({"type":TYPE,"value":VALUE})
        else:
            print("----",self.parseTree,"----")
            raise SyntaxError(f"Expected [{expType} {'|'.join(expValues)}] Received[{TYPE} {VALUE}]")


    ## TYPE: 'int'|'char'|'boolean'|className
    def eatType(self, incVoid=False):
        expValues = ["int","char","boolean"]
        if incVoid:
            expValues.append("void")
        TYPE, VALUE = self.getNextToken()
        if (TYPE == "keyword" and VALUE in expValues) or (TYPE == "identifier"):
            self.parseTree.append({"type":TYPE,"value":VALUE})
        else:
            raise SyntaxError(f"Type Error [{TYPE} {VALUE}]")
        
        
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

        TYPE, VALUE = self.seeNextToken()
        identifier = {"type":"let", "value":VALUE}

        self.eat("identifier")

        # ('[' expression ']')?
        TYPE, VALUE = self.seeNextToken()
        if TYPE == "symbol" and VALUE == "[":
            self.eat("symbol",["["])
            self.parseTree.append({"type":"open","value":"expression"})

            ## GEN -- EXPRESSION
            rawExpression = jackExpressions.Expressions()
            ## GEN -- /EXPRESSION

            self.compileExpression(rawExpression)

            ## GEN -- EXPRESSION
            parsedExpression = rawExpression.getExp()
            self.vmExpression(parsedExpression)
            ## GEN -- /EXPRESSION

            self.parseTree.append({"type":"close","value":"expression"})
            self.eat("symbol",["]"])
        

        self.eat("symbol",["="])
        self.parseTree.append({"type":"open","value":"expression"})

        ## GEN -- EXPRESSION
        rawExpression = jackExpressions.Expressions()
        ## GEN -- /EXPRESSION

        self.compileExpression(rawExpression)

        ## GEN -- EXPRESSION
        parsedExpression = rawExpression.getExp()
        self.vmExpression(parsedExpression)
        for symbols in self.subroutineSymbolTable:
            if identifier["value"] == symbols["name"]:
                self.vmCode.append(f"pop {symbols['kind']} {symbols['num']}")
        for symbols in self.classSymbolTable:
            if identifier["value"] == symbols["name"]:
                if (symbols["kind"] == "field"):    
                    self.vmCode.append(f"pop this {symbols['num']}")
                else:
                    self.vmCode.append(f"pop {symbols['kind']} {symbols['num']}")
        ## GEN -- /EXPRESSION

        self.parseTree.append({"type":"close","value":"expression"})
        self.eat("symbol",[";"])
        

    ## ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    def compileIf(self):
        self.eat("keyword",["if"])

        self.eat("symbol",["("])
        self.parseTree.append({"type":"open","value":"expression"})

        ## GEN -- EXPRESSION
        rawExpression = jackExpressions.Expressions()
        ## GEN -- /EXPRESSION

        self.compileExpression(rawExpression)

        ## GEN -- EXPRESSION
        parsedExpression = rawExpression.getExp()
        self.vmExpression(parsedExpression)
        self.vmCode.append("not")
        self.vmCode.append("if-goto L1")
        ## GEN -- /EXPRESSION

        self.parseTree.append({"type":"close","value":"expression"})
        self.eat("symbol",[")"])

        self.eat("symbol",["{"])
        self.parseTree.append({"type":"open","value":"statements"})
        self.compileStatements()
        ## GEN -- STATEMENTS
        self.vmCode.append("goto L2")
        self.vmCode.append("label L2")
        ## GEN -- /STATEMENTS
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
        ## GEN -- STATEMENTS
        self.vmCode.append("label L1")
        ## GEN -- /STATEMENTS



    ## whileStatement: 'while' '(' expression ')' '{' statements '}'
    def compileWhile(self):
        self.eat("keyword",["while"])

        self.eat("symbol",["("])
        self.parseTree.append({"type":"open","value":"expression"})

        ## GEN -- EXPRESSION
        rawExpression = jackExpressions.Expressions()
        ## GEN -- /EXPRESSION

        self.compileExpression(rawExpression)

        ## GEN -- EXPRESSION
        parsedExpression = rawExpression.getExp()
        self.vmCode.append("label L1")
        self.vmExpression(parsedExpression)
        self.vmCode.append("not")
        self.vmCode.append("if-goto L2")
        ## GEN -- /EXPRESSION

        self.parseTree.append({"type":"close","value":"expression"})
        self.eat("symbol",[")"])

        self.eat("symbol",["{"])    
        self.parseTree.append({"type":"open","value":"statements"})
        self.compileStatements()
        ## GEN -- STATEMENTS
        self.vmCode.append("goto L1")
        self.vmCode.append("label L2")
        ## GEN -- /STATEMENTS
        self.parseTree.append({"type":"close","value":"statements"})
        self.eat("symbol",["}"])


    ## doStatement: 'do' subroutineCall ';'
    def compileDo(self):
        ## GEN -- EXPRESSION
        rawExpression = jackExpressions.Expressions()
        ## GEN -- /EXPRESSION

        self.eat("keyword",["do"])
        self.compileSubroutineCall(True, "crap", rawExpression)
        self.eat("symbol",[";"])

        ## GEN -- EXPRESSION
        parsedExpression = rawExpression.getExp()
        self.vmExpression(parsedExpression)
        self.vmCode.append("pop temp 0")
        ## GEN -- /EXPRESSION


    ## returnStatement: 'return' expression? ';'
    def compileReturn(self):

        self.eat("keyword",["return"])

        TYPE, VALUE = self.seeNextToken()
        identifier = {"type":TYPE, "value":VALUE}

        # ;
        TYPE, VALUE = self.seeNextToken()
        if TYPE == "symbol" and VALUE == ";":
            self.eat("symbol",[";"])
            ## GEN -- EXPRESSION
            self.vmCode.append("push constant 0")
            self.vmCode.append("return")
            ## GEN -- /EXPRESSION
        # expression?    
        else:
            self.parseTree.append({"type":"open","value":"expression"})

            ## GEN -- EXPRESSION
            rawExpression = jackExpressions.Expressions()
            ## GEN -- /EXPRESSION

            self.compileExpression(rawExpression)

            ## GEN -- EXPRESSION
            parsedExpression = rawExpression.getExp()
            self.vmExpression(parsedExpression, identifier)
            self.vmCode.append("return")
            ## GEN -- /EXPRESSION

            self.parseTree.append({"type":"close","value":"expression"})
            self.eat("symbol",[";"])


    ## term: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOP term
    def compileTerm(self, parent):
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
                else:
                    ty,va = self.seeNextToken()
                ## GEN -- /TERM

                self.eat("identifier")

                TYPE, VALUE = self.seeNextToken()
                match VALUE:
                    # subroutineCall    
                    case "(" | ".":
                        self.compileSubroutineCall(False, va, parent)

                    # '[' expression ']'
                    case "[":

                        self.eat("symbol",["["])
                        self.parseTree.append({"type":"open","value":"expression"})
                        child = jackExpressions.Expressions()
                        parent.addTerm(va,"array", [child])
                        self.compileExpression(child)
                        self.parseTree.append({"type":"close","value":"expression"})
                        self.eat("symbol",["]"])

                    # Simple Variable
                    case _: 
                        parent.addTerm(va,"var")

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
    def compileExpressionList(self):

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

        return expList


    ## subroutineCall: subroutineName '(' expressionList ')' | (className|varName)'.'subroutineName '(' expressionList ')'
    def compileSubroutineCall(self, eatName, fullName, parent):

        if eatName:
            self.eat("identifier")

        TYPE, VALUE = self.seeNextToken()
        if TYPE == "symbol" and VALUE == ".":
            self.eat("symbol",["."])
            self.eat("identifier")
        
        # '(' expressionList ')'
        self.eat("symbol",["("])    
        self.parseTree.append({"type":"open","value":"expressionList"})
        expList = self.compileExpressionList()
        self.parseTree.append({"type":"close","value":"expressionList"})
        self.eat("symbol",[")"]) 
        parent.addTerm(fullName,"call", expList)   


    def vmExpression(self, expression, identifier={}):

        for exp,typ in expression:
            match typ:
                case "var":
                    for symbols in self.subroutineSymbolTable:
                        if exp == symbols["name"]:
                            self.vmCode.append(f"push {symbols['kind']} {symbols['num']}")
                    for symbols in self.classSymbolTable:
                        if exp == symbols["name"]:
                            if (symbols["kind"] == "field"):    
                                self.vmCode.append(f"push this {symbols['num']}")
                            else:
                                self.vmCode.append(f"push {symbols['kind']} {symbols['num']}")

                case "keyword":
                    match exp:
                        case "true":
                            self.vmCode.append("push constant 1")
                            self.vmCode.append("neg")
                        case "false":
                            self.vmCode.append("push constant 0")
                        case "null":
                            self.vmCode.append("push constant 0")
                        case "this":
                            self.vmCode.append("push pointer 0")


                case "constant":
                    self.vmCode.append(f"push constant {exp}")

                case "symbol":
                    match exp:
                        case "+": self.vmCode.append("add")
                        case "-": self.vmCode.append("neg")
                        case "*": self.vmCode.append("call Math.multiply 2")
                        case "/": self.vmCode.append("call Math.divide 2")
                        case "&": self.vmCode.append("call Math.AND 2")
                        case "|": self.vmCode.append("call Math.OR 2")
                        case "<": self.vmCode.append("lt")
                        case ">": self.vmCode.append("gt")
                        case "=": self.vmCode.append("call Math.EQ 2")

                case "unary":
                    match exp:
                        case "m": self.vmCode.append("neg")
                        case "~": self.vmCode.append("call Math.NOT 1")

