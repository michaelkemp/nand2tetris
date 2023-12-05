import jackExpressions, json

class CompilationEngine:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenPtr = 0

        self.vmCode = []
        self.classSymbolTable = [] 
        self.subroutineSymbolTable = []
        self.currentClassName = ""
        self.currentSubroutineName = ""
        self.currentSubroutineReturn = ""
        self.currentSubroutineType = ""
        self.fieldCnt = 0
        self.staticCnt = 0
        self.argumentCnt = 0
        self.localCnt = 0

        self.IF = 0
        self.WHILE = 0


    def printClassSymbolTable(self):
        print(f"CLASS: {self.currentClassName}")
        for symbols in sorted(self.classSymbolTable, key=lambda d: d['kind']):
            print(f" {symbols['kind']} {symbols['type']} {symbols['name']} {symbols['num']}")

    def printSubroutineSymbolTable(self):
        print(f"SUBROUTINE: {self.currentSubroutineName}")
        for symbols in sorted(self.subroutineSymbolTable, key=lambda d: d['kind']):
            print(f" {symbols['kind']} {symbols['type']} {symbols['name']} {symbols['num']}")


    def getNextToken(self):
        if self.tokenPtr < len(self.tokens):
            tkn = self.tokens[self.tokenPtr]
            self.tokenPtr += 1
            return [tkn["type"], tkn["value"]]
        else:
            return ["",""] 
    
    def seeNextToken(self):
        if self.tokenPtr < len(self.tokens):
            tkn = self.tokens[self.tokenPtr]
            return [tkn["type"], tkn["value"]]
        else:
            return ["",""] 

    def valNextToken(self):
        if self.tokenPtr < len(self.tokens):
            tkn = self.tokens[self.tokenPtr]
            return tkn["value"]
        else:
            return "" 

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
        self.compileClass()
        return self.vmCode


    def eat(self, expType, expValues=None):
        TYPE, VALUE = self.getNextToken()
        if (TYPE == expType and expValues is None) or (TYPE == expType and VALUE in expValues):
            pass
        else:
            raise SyntaxError(f"Expected [{expType} {'|'.join(expValues)}] Received[{TYPE} {VALUE}]")


    ## TYPE: 'int'|'char'|'boolean'|className
    def eatType(self, incVoid=False):
        expValues = ["int","char","boolean"]
        if incVoid:
            expValues.append("void")
        TYPE, VALUE = self.getNextToken()
        if (TYPE == "keyword" and VALUE in expValues) or (TYPE == "identifier"):
            pass
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
        self.currentClassName = self.valNextToken()
        ## GEN -- /CLASS NAME

        self.eat("identifier")
        self.eat("symbol", ["{"])

        # expect classVarDec*
        # classVarDec: ('static'|'field') TYPE varName (',' varName)* ';'
        TYPE, VALUE = self.seeNextToken()
        while TYPE == "keyword" and VALUE in["static", "field"]:
            self.compileClassVarDec()
            TYPE, VALUE = self.seeNextToken()

        ## self.printClassSymbolTable()

        # expect subroutineDec*
        # subroutineDec: ('constructor'|'function'|'method') ('void'|TYPE) subroutineName '(' parameterList ')' subroutineBody
        TYPE, VALUE = self.seeNextToken()    
        while TYPE == "keyword" and VALUE in ["constructor", "function", "method"]:

            ## GEN -- SUBROUTINE NAME
            self.subroutineSymbolTable = []
            self.currentSubroutineName = ""
            self.currentSubroutineReturn = ""
            self.currentSubroutineType = ""
            self.argumentCnt = 0
            self.localCnt = 0
            ## GEN -- /SUBROUTINE NAME

            self.compileSubroutineDec()
            TYPE, VALUE = self.seeNextToken()

            ## self.printSubroutineSymbolTable()

        self.eat("symbol", ["}"])


    ## classVarDec: ('static'|'field') TYPE varName (',' varName)* ';'
    def compileClassVarDec(self):

        ## GEN -- CLASS VAR KIND
        classVarKind = self.valNextToken()
        ## GEN -- /CLASS VAR KIND

        self.eat("keyword",["static","field"])

        ## GEN -- CLASS VAR TYPE
        classVarType = self.valNextToken()
        ## GEN -- /CLASS VAR TYPE

        self.eatType()

        ## GEN -- CLASS VAR NAME
        classVarNames = []
        classVarNames.append(self.valNextToken())
        ## GEN -- /CLASS VAR NAME

        self.eat("identifier")

        # (',' varName)*
        TYPE, VALUE = self.seeNextToken()
        while (TYPE == "symbol" and VALUE == ","):
            self.eat("symbol", [","])

            ## GEN -- CLASS VAR NAME
            classVarNames.append(self.valNextToken())
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
        self.currentSubroutineType = self.valNextToken()
        ## GEN -- /SUBROUTINE TYPE

        self.eat("keyword",["constructor","function","method"])

        ## GEN -- SUBROUTINE RETURN
        self.currentSubroutineReturn = self.valNextToken()
        ## GEN -- /SUBROUTINE RETURN

        self.eatType(True) ## include Void in Type

        ## GEN -- SUBROUTINE NAME
        self.currentSubroutineName = self.valNextToken()
        ## GEN -- /SUBROUTINE NAME

        self.eat("identifier")

        self.eat("symbol", ["("])
        self.compileParameterList()
        self.eat("symbol", [")"])

        self.compileSubroutineBody()


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
                subVarType = self.valNextToken()
                ## GEN -- /SUBROUTINE ARG TYPE

                self.eatType()

                ## GEN -- SUBROUTINE ARG NAME
                subVarName = self.valNextToken()
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
            self.compileVarDec()
            TYPE, VALUE = self.seeNextToken()

        ######## SUBROUTINES ########
        #print(self.currentSubroutineType, self.currentSubroutineReturn, self.currentSubroutineName, self.subroutineSymbolTable)

        match self.currentSubroutineType:
            case "constructor":
                self.vmCode.append(f"function {self.currentClassName}.{self.currentSubroutineName} {self.localCnt}")
                self.vmCode.append(f"push constant {self.argumentCnt}")
                self.vmCode.append("call Memory.alloc 1")
                self.vmCode.append("pop pointer 0")
            case "method":
                self.vmCode.append(f"function {self.currentClassName}.{self.currentSubroutineName} {self.localCnt}")
                self.vmCode.append(f"push constant {self.argumentCnt}")
                self.vmCode.append("call Memory.alloc 1")
                self.vmCode.append("pop pointer 0")
            case "function":
                self.vmCode.append(f"function {self.currentClassName}.{self.currentSubroutineName} {self.localCnt}")
                #self.vmCode.append("push argument 0")

        self.compileStatements()
        self.eat("symbol", ["}"])


    ## varDec: 'var' TYPE varName (',' varName)* ';'
    def compileVarDec(self):
        self.eat("keyword", ["var"])

        ## GEN -- SUBROUTINE LOCAL TYPE
        subVarType = self.valNextToken()
        ## GEN -- /SUBROUTINE LOCAL TYPE

        self.eatType()

        while True:

            ## GEN -- SUBROUTINE LOCAL NAME
            subVarName = self.valNextToken()
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
                    self.compileLet()
                case "if":
                    self.compileIf()
                case "while":
                    self.compileWhile()
                case "do":
                    self.compileDo()
                case "return":
                    self.compileReturn()
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

            ## GEN -- EXPRESSION
            rawExpression = jackExpressions.Expressions()
            ## GEN -- /EXPRESSION

            self.compileExpression(rawExpression)

            ## GEN -- EXPRESSION
            parsedExpression = rawExpression.getExp()
            self.vmExpression(parsedExpression)
            ## GEN -- /EXPRESSION

            self.eat("symbol",["]"])
        

        self.eat("symbol",["="])

        ## GEN -- EXPRESSION
        rawExpression = jackExpressions.Expressions()
        ## GEN -- /EXPRESSION

        self.compileExpression(rawExpression)

        ## GEN -- EXPRESSION
        parsedExpression = rawExpression.getExp()
        self.vmExpression(parsedExpression)
        notFound = True
        for symbols in self.subroutineSymbolTable:
            if notFound and identifier["value"] == symbols["name"]:
                self.vmCode.append(f"pop {symbols['kind']} {symbols['num']}")
                notFound = False
        for symbols in self.classSymbolTable:
            if notFound and identifier["value"] == symbols["name"]:
                if (symbols["kind"] == "field"):    
                    self.vmCode.append(f"pop this {symbols['num']}")
                    notFound = False
                else:
                    self.vmCode.append(f"pop {symbols['kind']} {symbols['num']}")
                    notFound = False
        ## GEN -- /EXPRESSION

        self.eat("symbol",[";"])
        

    ## ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    def compileIf(self):
        ifcnt = self.IF
        self.IF += 1
        self.eat("keyword",["if"])

        self.eat("symbol",["("])

        ## GEN -- EXPRESSION
        rawExpression = jackExpressions.Expressions()
        ## GEN -- /EXPRESSION

        self.compileExpression(rawExpression)

        ## GEN -- EXPRESSION
        parsedExpression = rawExpression.getExp()
        self.vmExpression(parsedExpression)
        self.vmCode.append(f"if-goto IF_TRUE{ifcnt}")
        self.vmCode.append(f"goto IF_FALSE{ifcnt}")
        self.vmCode.append(f"label IF_TRUE{ifcnt}")
        ## GEN -- /EXPRESSION

        self.eat("symbol",[")"])

        self.eat("symbol",["{"])
        self.compileStatements()
        self.eat("symbol",["}"])

        # ('else' '{' statements '}')?
        TYPE, VALUE = self.seeNextToken()
        noElse = True
        if TYPE == "keyword" and VALUE == "else":

            ## GEN -- STATEMENTS
            self.vmCode.append(f"goto IF_END{ifcnt}")
            self.vmCode.append(f"label IF_FALSE{ifcnt}")
            noElse = False
            ## GEN -- /STATEMENTS

            self.eat("keyword",["else"])
            self.eat("symbol",["{"])
            self.compileStatements()

            self.eat("symbol",["}"])
        ## GEN -- STATEMENTS
        if noElse:
            self.vmCode.append(f"label IF_FALSE{ifcnt}")
        else:
            self.vmCode.append(f"label IF_END{ifcnt}")
        ## GEN -- /STATEMENTS



    ## whileStatement: 'while' '(' expression ')' '{' statements '}'
    def compileWhile(self):
        whilecnt = self.WHILE
        self.WHILE += 1

        self.eat("keyword",["while"])

        self.eat("symbol",["("])

        ## GEN -- EXPRESSION
        rawExpression = jackExpressions.Expressions()
        ## GEN -- /EXPRESSION

        self.compileExpression(rawExpression)

        ## GEN -- EXPRESSION
        parsedExpression = rawExpression.getExp()
        self.vmCode.append(f"label WHILE_EXP{whilecnt}")
        self.vmExpression(parsedExpression)
        self.vmCode.append("not")
        self.vmCode.append(f"if-goto WHILE_END{whilecnt}")
        ## GEN -- /EXPRESSION

        self.eat("symbol",[")"])

        self.eat("symbol",["{"])    
        self.compileStatements()
        ## GEN -- STATEMENTS
        self.vmCode.append(f"goto WHILE_EXP{whilecnt}")
        self.vmCode.append(f"label WHILE_END{whilecnt}")
        ## GEN -- /STATEMENTS
        self.eat("symbol",["}"])


    ## doStatement: 'do' subroutineCall ';'
    def compileDo(self):

        ## GEN -- EXPRESSION
        rawExpression = jackExpressions.Expressions()
        ## GEN -- /EXPRESSION

        self.eat("keyword",["do"])
        va = self.seeSubroutineCall()
        self.compileSubroutineCall(True, va, rawExpression)
        self.eat("symbol",[";"])

        ## GEN -- EXPRESSION
        parsedExpression = rawExpression.getExp()
        self.vmExpression(parsedExpression)
        self.vmCode.append("pop temp 0")
        ## GEN -- /EXPRESSION


    ## returnStatement: 'return' expression? ';'
    def compileReturn(self):

        self.eat("keyword",["return"])

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

            ## GEN -- EXPRESSION
            rawExpression = jackExpressions.Expressions()
            ## GEN -- /EXPRESSION

            self.compileExpression(rawExpression)

            ## GEN -- EXPRESSION
            parsedExpression = rawExpression.getExp()
            self.vmExpression(parsedExpression)
            self.vmCode.append("return")
            ## GEN -- /EXPRESSION

            self.eat("symbol",[";"])


    ## term: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOP term
    def compileTerm(self, parent):
        TYPE, VALUE = self.seeNextToken()

        match TYPE:

            # integerConstant | stringConstant
            case "integerConstant" | "stringConstant":
                ## GEN -- TERM
                parent.addTerm(self.valNextToken(),"constant")
                ## GEN -- /TERM

                self.eat(TYPE)

            # keywordConstant
            case "keyword":
                ## GEN -- TERM
                parent.addTerm(self.valNextToken(),"keyword")
                ## GEN -- /TERM

                self.eat("keyword", ['true','false','null','this'])

            case "symbol":
                match VALUE:
                    # '(' expression ')'    
                    case "(":
                        ## GEN -- TERM
                        parent.addTerm(self.valNextToken(),"symbol")
                        ## GEN -- /TERM

                        self.eat("symbol",["("])

                        self.compileExpression(parent)
 
                        ## GEN -- TERM
                        parent.addTerm(self.valNextToken(),"symbol")
                        ## GEN -- /TERM

                        self.eat("symbol",[")"])

                    # unaryOP term        
                    case "-" | "~":
                        ## GEN -- TERM
                        parent.addTerm(self.valNextToken(),"unary")
                        ## GEN -- /TERM

                        self.eat("symbol",[VALUE])
                        self.compileTerm(parent)

            case "identifier":
                # varName | varName '[' expression ']' | subroutineCall

                ## GEN -- TERM
                if self.seeSubroutineCall():
                    va = self.seeSubroutineCall()
                else:
                    va = self.valNextToken()
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
                        child = jackExpressions.Expressions()
                        parent.addTerm(va,"array", [child])
                        self.compileExpression(child)
                        self.eat("symbol",["]"])

                    # Simple Variable
                    case _: 
                        parent.addTerm(va,"var")

    ## expression: term (op term)*
    ## op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    def compileExpression(self, parent):
        self.compileTerm(parent)

        # (op term)*
        TYPE, VALUE = self.seeNextToken()
        while TYPE == "symbol" and VALUE in ["+","-","*","/","&","|","<",">","="]:

            ## GEN -- TERM
            parent.addTerm(self.valNextToken(),"symbol")
            ## GEN -- /TERM

            self.eat("symbol",[VALUE])

            self.compileTerm(parent)
            TYPE, VALUE = self.seeNextToken()
 

    ## expressionList: (expression (',' expression)* )?
    def compileExpressionList(self):

        expList = []
        TYPE, VALUE = self.seeNextToken()
        if (TYPE in ["integerConstant","stringConstant","identifier"]) or (TYPE=="keyword" and VALUE in ['true','false','null','this']) or (TYPE == "symbol" and VALUE in ["(","-","~"]):

            tmp = jackExpressions.Expressions()
            expList.append(tmp)
            self.compileExpression(tmp)

            TYPE, VALUE = self.seeNextToken()
            while TYPE == "symbol" and VALUE == ",":
                self.eat("symbol", [","])

                tmp = jackExpressions.Expressions()
                expList.append(tmp)
                self.compileExpression(tmp)

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
        expList = self.compileExpressionList()
        self.eat("symbol",[")"]) 
        parent.addTerm(fullName, "call", expList)   


    def vmExpression(self, expression):
        #print(expression)
        for exp,typ in expression:
            match typ:
                case "var":
                    for symbols in self.subroutineSymbolTable:
                        if exp == symbols["name"]:
                            self.vmCode.append(f"push {symbols['kind']} {symbols['num']}")
                    # for symbols in self.classSymbolTable:
                    #     if exp == symbols["name"]:
                    #         if (symbols["kind"] == "field"):    
                    #             self.vmCode.append(f"push this {symbols['num']}")
                    #         else:
                    #             self.vmCode.append(f"push {symbols['kind']} {symbols['num']}")

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

                case "call":
                    self.vmCode.append(f"call {exp} 1")

                case "symbol":
                    match exp:
                        case "+": self.vmCode.append("add")
                        case "-": self.vmCode.append("sub")
                        case "*": self.vmCode.append("call Math.multiply 2")
                        case "/": self.vmCode.append("call Math.divide 2")
                        case "&": self.vmCode.append("and")
                        case "|": self.vmCode.append("or")
                        case "<": self.vmCode.append("lt")
                        case ">": self.vmCode.append("gt")
                        case "=": self.vmCode.append("eq")

                case "unary":
                    match exp:
                        case "m": self.vmCode.append("neg")
                        case "~": self.vmCode.append("not")

