
## Terminal Element -- keyword, symbol, integerConstant, StringConstant, identifier
##  eg.. <keyword> method </keyword>

## NON Terminal Element 
## -- class dec, class var dec, subroutine dec, param list, subrotuine body, var dec, statements, let (if, while, do, return) stmt, expression, term, expression list
## eg return x;
# <returnStatement>
#   <keyword>
#       return
#   </keyword>
#   <expression>
#       <term>
#           <identifier> x </identifier>
#       </term>
#   </expression>
#   <symbol> ; </symbol>
# </returnStatement>

## Shallow Rule -- type, className, subroutineName, varName, statement, subroutineCall
## eg let x = 17;
# <letStatement>
#   <keyword> let </keyword>
#   <identifier> x </identifier> <--- varName creates no markup
#   <symbol> = </symbol>    

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

## x? 0 or 1 time -- x* 0 or more times

## type, className, subroutineName, varName, statement, subroutineCall

import json

class CompliationEngine:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenPtr = 0
        self.currentToken = self.tokens[self.tokenPtr]["value"]
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
        if type == expType and expValues is None:
            self.parseTree.append({"type":type,"value":value})
        elif type == expType and value in expValues:
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected [{} {}] Received[{} {}]".format(expType, "|".join(expValues), type, value))

    ## <type> => 'int' | 'char' | 'boolean' | <className>
    def eatType(self, incVoid=False):
        expValues = ["int","char","boolean"]
        if incVoid:
            expValues.append("void")
        type,value = self.getNextToken()
        if (type == "keyword" and value in expValues) or (type == "identifier"):
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Type Error [{} {}]".format(type,value))
        
    ## <className> => identifier
    ## <subroutineName> => identifier
    ## <varName> => identifier    
    def eatName(self):
        type,value = self.getNextToken()
        if type == "identifier":
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Name Error [{} {}]".format(type,value))
        
    
    ## <class> => 'class' <className> '{' <classVarDec>* <subroutineDec>* '}'
    def compileClass(self):

        # expect 'class'
        self.eat("keyword", ["class"])

        # expect <className>
        self.eat("identifier")

        # expect {
        self.eat("symbol", ["{"])
        type,value = self.getNextToken()

        # expect <classVarDec>*
        type,value = self.seeNextToken()
        while type == "keyword" and (value == "static" or value == "field"):
            self.parseTree.append({"type":"open","value":"classVarDec"})
            self.compileClassVarDec()
            self.parseTree.append({"type":"close","value":"classVarDec"})
            type,value = self.seeNextToken()

        # expect <subroutineDec>*
        type,value = self.seeNextToken()    
        while type == "keyword" and (value == "constructor" or value == "function" or value == "method"):
            self.parseTree.append({"type":"open","value":"subroutineDec"})
            self.compileSubroutineDec()
            self.parseTree.append({"type":"close","value":"subroutineDec"})
            type,value = self.seeNextToken()

        # expect }
        self.eat("symbol", ["}"])


    ## <classVarDec> => ('static' | 'field') <type> <varName> (',' <varName>)* ';'
    def compileClassVarDec(self):

        # expect 'static' | 'field' 
        self.eat("keyword",["static","field"])

        # expect <type>
        self.eatType()

        # expect <varName>
        self.eatName()

        # maybe more <varName>
        type,value = self.seeNextToken()
        while (type == "symbol" and value == ","):
            # expect ,
            self.eat("symbol", [","])
            # expect <varName>
            self.eatName()
            type,value = self.seeNextToken()

        # expect ;
        self.eat("symbol", [";"])


    ## <subroutineDec> => ('constructor' | 'function' | 'method') ('void' | <type>) <subroutineName> '(' <parameterList> ')' <subroutineBody>
    def compileSubroutineDec(self):
        # expect 'constructor' | 'function' | 'method'
        self.eat("keyword",["constructor","function","method"])
 
        # expect 'void' | <type>
        self.eatType(True) ## invVoid

        # expect <subroutineName>
        self.eatName()

        # expect (
        self.eat("symbol", ["("])

        self.parseTree.append({"type":"open","value":"parameterList"})
        self.compileParameterList()
        self.parseTree.append({"type":"close","value":"parameterList"})

        # expect )
        self.eat("symbol", [")"])

        self.parseTree.append({"type":"open","value":"subroutineBody"})
        self.compileSubroutineBody()
        self.parseTree.append({"type":"close","value":"subroutineBody"})


    ## <parameterList> => (<type> <varName> (',' <type> <varName>)* )?
    def compileParameterList(self):
        type,value = self.seeNextToken()
        if (type == "keyword" and (value == "int" or value == "char" or value == "boolean")) or (type == "identifier"):
            while True:
                # expect <type>
                self.eatType()

                # expect <varName>
                self.eatName()

                # maybe more <type> <varName>
                type,value = self.seeNextToken()
                if type == "symbol" and value == ",":
                    self.eat("symbol", [","])
                else:
                    return

    ## <subroutineBody> => '{' <varDec>* <statements> '}'
    def compileSubroutineBody(self):
        # expect {
        self.eat("symbol", ["{"])

        # expect <varDec>*
        type,value = self.seeNextToken()
        while type == "keyword" and value == "var":
            self.parseTree.append({"type":"open","value":"varDec"})
            self.compileVarDec()
            self.parseTree.append({"type":"close","value":"varDec"})
            type,value = self.seeNextToken()

        # expect <subroutineDec>*
        type,value = self.seeNextToken()    
        while type == "keyword" and (value == "constructor" or value == "function" or value == "method"):
            self.parseTree.append({"type":"open","value":"subroutineDec"})
            self.compileSubroutineDec()
            self.parseTree.append({"type":"close","value":"subroutineDec"})
            type,value = self.seeNextToken()

        # expect }
        self.eat("symbol", ["}"])


    ## <varDec> => 'var' <type> <varName> (',' <varName>)* ';'
    def compileVarDec(self):
        # expect 'var'
        self.eat("keyword", ["var"])

        # expect <type>
        self.eatType()

        while True:
            # expect <varName>
            self.eatName()

            # maybe more <varName>
            type,value = self.seeNextToken()
            if type == "symbol" and value == ",":
                self.eat("symbol", [","])
            else:
                return


    def compileStatements(self):
        pass

    def compileLet(self):
        pass

    def compileIf(self):
        pass

    def compileWhile(self):
        ## follow RHS of rule and parse accordingly
        ## 'while' '(' expression ')' '{' statements '}'
        self.eat("while") ## handle while
        self.eat("(") ## handle (
        self.compileExpression()
        self.eat(")") ## handle )
        self.eat("{") ## handle {
        self.compileStatements()
        self.eat("{") ## handle }
        pass

    def compileDo(self):
        pass

    def compileReturn(self):
        pass

    def compileExpression(self):
        ## term (op term)?
        pass

    def compileTerm(self):
        # varName | constant
        pass

    def compileExpressionList(self):
        pass

