
class CompilationEngine:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenPtr = 0
        self.parseTree = []

    def getNextToken(self, inc=1):
        if self.tokenPtr < len(self.tokens):
            tkn = self.tokens[self.tokenPtr]
            self.tokenPtr += inc
            return [tkn["type"], tkn["value"]]
        else:
            return ["",""] 
    
    def seeNextToken(self):
        return self.getNextToken(0)


    def parseTokens(self):
        self.parseTree.append({"type":"open","value":"class"})
        self.compileClass()
        self.parseTree.append({"type":"close","value":"class"})
        return self.parseTree


    def eat(self, expType, expValues=None):
        type,value = self.getNextToken()
        if (type == expType and expValues is None) or (type == expType and value in expValues):
            self.parseTree.append({"type":type,"value":value})
        else:
            print("----",self.parseTree,"-----")
            raise SyntaxError(f"Expected [{expType} {'|'.join(expValues)}] Received[{type} {value}]")


    ## type: 'int'|'char'|'boolean'|className
    def eatType(self, incVoid=False):
        expValues = ["int","char","boolean"]
        if incVoid:
            expValues.append("void")
        type,value = self.getNextToken()
        if (type == "keyword" and value in expValues) or (type == "identifier"):
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError(f"Type Error [{type} {value}]")
        
        
    ## class: 'class' className '{' classVarDec* subroutineDec* '}'
    def compileClass(self):
        self.eat("keyword", ["class"])
        self.eat("identifier")
        self.eat("symbol", ["{"])

        # expect classVarDec*
        # classVarDec: ('static'|'field') type varName (',' varName)* ';'
        type,value = self.seeNextToken()
        while type == "keyword" and value in["static", "field"]:
            self.parseTree.append({"type":"open","value":"classVarDec"})
            self.compileClassVarDec()
            self.parseTree.append({"type":"close","value":"classVarDec"})
            type,value = self.seeNextToken()

        # expect subroutineDec*
        # subroutineDec: ('constructor'|'function'|'method') ('void'|type) subroutineName '(' parameterList ')' subroutineBody
        type,value = self.seeNextToken()    
        while type == "keyword" and value in ["constructor", "function", "method"]:
            self.parseTree.append({"type":"open","value":"subroutineDec"})
            self.compileSubroutineDec()
            self.parseTree.append({"type":"close","value":"subroutineDec"})
            type,value = self.seeNextToken()

        self.eat("symbol", ["}"])


    ## classVarDec: ('static'|'field') type varName (',' varName)* ';'
    def compileClassVarDec(self):
        self.eat("keyword",["static","field"])
        self.eatType()
        self.eat("identifier")

        # (',' varName)*
        type,value = self.seeNextToken()
        while (type == "symbol" and value == ","):
            self.eat("symbol", [","])
            self.eat("identifier")
            type,value = self.seeNextToken()

        self.eat("symbol", [";"])


    ## subroutineDec: ('constructor'|'function'|'method') ('void'|type) subroutineName '(' parameterList ')' subroutineBody
    def compileSubroutineDec(self):
        self.eat("keyword",["constructor","function","method"])
        self.eatType(True) ## include Void in Type
        self.eat("identifier")

        self.eat("symbol", ["("])
        self.parseTree.append({"type":"open","value":"parameterList"})
        self.compileParameterList()
        self.parseTree.append({"type":"close","value":"parameterList"})
        self.eat("symbol", [")"])

        self.parseTree.append({"type":"open","value":"subroutineBody"})
        self.compileSubroutineBody()
        self.parseTree.append({"type":"close","value":"subroutineBody"})


    ## parameterList: ((type varName) (',' type varName)*)?
    def compileParameterList(self):
        type,value = self.seeNextToken()
        if (type == "keyword" and (value == "int" or value == "char" or value == "boolean")) or (type == "identifier"):
            while True:
                self.eatType()
                self.eat("identifier")

                # (',' type varName)*
                type,value = self.seeNextToken()
                if type == "symbol" and value == ",":
                    self.eat("symbol", [","])
                else:
                    break

    ## subroutineBody: '{' varDec* statements '}'
    def compileSubroutineBody(self):
        self.eat("symbol", ["{"])

        # varDec*
        # varDec: 'var' type varName (',' varName)* ';'
        type,value = self.seeNextToken()
        while type == "keyword" and value == "var":
            self.parseTree.append({"type":"open","value":"varDec"})
            self.compileVarDec()
            self.parseTree.append({"type":"close","value":"varDec"})
            type,value = self.seeNextToken()

        self.parseTree.append({"type":"open","value":"statements"})
        self.compileStatements()
        self.parseTree.append({"type":"close","value":"statements"})
        self.eat("symbol", ["}"])


    ## varDec: 'var' type varName (',' varName)* ';'
    def compileVarDec(self):
        self.eat("keyword", ["var"])
        self.eatType()

        while True:
            self.eat("identifier")

            # (',' varName)*
            type,value = self.seeNextToken()
            if type == "symbol" and value == ",":
                self.eat("symbol", [","])
            else:
                break
        
        self.eat("symbol", [";"])



    ## statements: statement*
    ## statement:  letStatement | ifStatement | whileStatement | doStatement | returnStatement
    def compileStatements(self):
        type,value = self.seeNextToken()
        while type == "keyword" and value in ["let","if","while","do","return"]:
            match value:
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
            type,value = self.seeNextToken()


    ## letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    def compileLet(self):
        self.eat("keyword",["let"])
        self.eat("identifier")

        # ('[' expression ']')?
        type,value = self.seeNextToken()
        if type == "symbol" and value == "[":
            self.eat("symbol",["["])
            self.parseTree.append({"type":"open","value":"expression"})
            self.compileExpression()
            self.parseTree.append({"type":"close","value":"expression"})
            self.eat("symbol",["]"])
        

        self.eat("symbol",["="])
        self.parseTree.append({"type":"open","value":"expression"})
        self.compileExpression()
        self.parseTree.append({"type":"close","value":"expression"})
        self.eat("symbol",[";"])
        

    ## ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    def compileIf(self):
        self.eat("keyword",["if"])

        self.eat("symbol",["("])
        self.parseTree.append({"type":"open","value":"expression"})
        self.compileExpression()
        self.parseTree.append({"type":"close","value":"expression"})
        self.eat("symbol",[")"])

        self.eat("symbol",["{"])
        self.parseTree.append({"type":"open","value":"statements"})
        self.compileStatements()
        self.parseTree.append({"type":"close","value":"statements"})
        self.eat("symbol",["}"])

        # ('else' '{' statements '}')?
        type,value = self.seeNextToken()
        if type == "keyword" and value == "else":
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
        self.compileExpression()
        self.parseTree.append({"type":"close","value":"expression"})
        self.eat("symbol",[")"])

        self.eat("symbol",["{"])    
        self.parseTree.append({"type":"open","value":"statements"})
        self.compileStatements()
        self.parseTree.append({"type":"close","value":"statements"})
        self.eat("symbol",["}"])


    ## doStatement: 'do' subroutineCall ';'
    def compileDo(self):
        self.eat("keyword",["do"])
        self.compileSubroutineCall()
        self.eat("symbol",[";"])


    ## returnStatement: 'return' expression? ';'
    def compileReturn(self):
        self.eat("keyword",["return"])

        # ;
        type,value = self.seeNextToken()
        if type == "symbol" and value == ";":
            self.eat("symbol",[";"])
        # expression?    
        else:
            self.parseTree.append({"type":"open","value":"expression"})
            self.compileExpression()
            self.parseTree.append({"type":"close","value":"expression"})
            self.eat("symbol",[";"])


    ## term: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOP term
    def compileTerm(self):
        type,value = self.seeNextToken()
        match type:
            # integerConstant | stringConstant
            case "integerConstant" | "stringConstant":
                self.eat(type)
            # keywordConstant
            case "keyword":
                self.eat("keyword", ['true','false','null','this'])
            case "symbol":
                match value:
                    # '(' expression ')'    
                    case "(":
                        self.eat("symbol",["("])
                        self.parseTree.append({"type":"open","value":"expression"})
                        self.compileExpression()
                        self.parseTree.append({"type":"close","value":"expression"})
                        self.eat("symbol",[")"])
                    # unaryOP term        
                    case "-" | "~":
                        self.eat("symbol",[value])
                        self.parseTree.append({"type":"open","value":"term"})
                        self.compileTerm()
                        self.parseTree.append({"type":"close","value":"term"})
            case "identifier":
                # varName | varName '[' expression ']' | subroutineCall
                self.eat("identifier")
                type,value = self.seeNextToken()
                match value:
                    # '[' expression ']'
                    case "[":
                        self.eat("symbol",["["])
                        self.parseTree.append({"type":"open","value":"expression"})
                        self.compileExpression()
                        self.parseTree.append({"type":"close","value":"expression"})
                        self.eat("symbol",["]"])
                    # subroutineCall    
                    case "(" | ".":
                        self.compileSubroutineCall(False)

    ## expression: term (op term)*
    ## op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    def compileExpression(self):
        self.parseTree.append({"type":"open","value":"term"})
        self.compileTerm()
        self.parseTree.append({"type":"close","value":"term"})

        # (op term)*
        type,value = self.seeNextToken()
        while type == "symbol" and value in ["+","-","*","/","&","|","<",">","="]:
            self.eat("symbol",[value])
            self.parseTree.append({"type":"open","value":"term"})
            self.compileTerm()
            self.parseTree.append({"type":"close","value":"term"})
            type,value = self.seeNextToken()
 

    ## expressionList: (expression (',' expression)* )?
    def compileExpressionList(self):
        type,value = self.seeNextToken()
        if (type in ["integerConstant","stringConstant","identifier"]) or (type=="keyword" and value in ['true','false','null','this']) or (type == "symbol" and value in ["(","-","~"]):
            self.parseTree.append({"type":"open","value":"expression"})
            self.compileExpression()
            self.parseTree.append({"type":"close","value":"expression"})
            type,value = self.seeNextToken()
            while type == "symbol" and value == ",":
                self.eat("symbol", [","])
                self.parseTree.append({"type":"open","value":"expression"})
                self.compileExpression()
                self.parseTree.append({"type":"close","value":"expression"})
                type,value = self.seeNextToken()


    ## subroutineCall: subroutineName '(' expressionList ')' | (className|varName)'.'subroutineName '(' expressionList ')'
    def compileSubroutineCall(self, eatName = True):
        if eatName:
            self.eat("identifier")

        type,value = self.seeNextToken()
        if type == "symbol" and value == ".":
            self.eat("symbol",["."])
            self.eat("identifier")
        
        # '(' expressionList ')'
        self.eat("symbol",["("])    
        self.parseTree.append({"type":"open","value":"expressionList"})
        self.compileExpressionList()
        self.parseTree.append({"type":"close","value":"expressionList"})
        self.eat("symbol",[")"])    
