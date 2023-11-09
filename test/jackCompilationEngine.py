
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
        # expect class
        type,value = self.getNextToken()
        if type == "keyword" and value == "class":
            self.parseTree.append({"type":"open","value":"class"})
            self.parseTree.append({"type":type,"value":value})
            try:
                self.compileClass()
            except SyntaxError as e:
                print(json.dumps(self.parseTree, indent=2))
                print(e)
                exit(0)
            self.parseTree.append({"type":"close","value":"class"})
        else:
            raise SyntaxError("Expected keyword class - {} {}".format(type,value))
        
        return self.parseTree

    def compileClass(self):

        # expect <className>
        type,value = self.getNextToken()
        if type == "identifier":
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected identifier className - {} {}".format(type,value))

        # expect {
        type,value = self.getNextToken()
        if type == "symbol" and value == "{":
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected symbol {{ - {} {}".format(type,value))

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
        type,value = self.getNextToken()
        if type == "symbol" and value == "}":
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected symbol }} - {} {}".format(type,value))


    def compileClassVarDec(self):
        # expect 'static' | 'field' 
        type,value = self.getNextToken()
        if type == "keyword" and (value == "static" or value == "field"):
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected keyword static|field - {} {}".format(type,value))

        ################ TYPE ################
        # expect 'int' | 'char' | 'boolean' | <className>
        type,value = self.getNextToken()
        if (type == "keyword" and (value == "int" or value == "char" or value == "boolean")) or (type == "identifier"):
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected keyword int|char|boolean | identifier - {} {}".format(type,value))

        ################ VARNAME ################
        # expect <varName>
        type,value = self.getNextToken()
        if type == "identifier":
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected identifier - {} {}".format(type,value))

        # maybe more <varName>
        type,value = self.seeNextToken()
        while (type == "symbol" and value == ","):

            # expect ,
            type,value = self.getNextToken()
            if type == "symbol" and value == ",":
                self.parseTree.append({"type":type,"value":value})
            else:
                raise SyntaxError("Expected symbol , - {} {}".format(type,value))

            # expect <varName>
            type,value = self.getNextToken()
            if type == "identifier":
                self.parseTree.append({"type":type,"value":value})
            else:
                raise SyntaxError("Expected identifier - {} {}".format(type,value))

            type,value = self.seeNextToken()

        # expect ;
        type,value = self.getNextToken()
        if type == "symbol" and value == ";":
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected symbol ; - {} {}".format(type,value))


    def compileSubroutineDec(self):
        # expect 'constructor' | 'function' | 'method' 
        type,value = self.getNextToken()
        if type == "keyword" and (value == "constructor" or value == "function" or value == "method"):
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected keyword constructor|function|method - {} {}".format(type,value))

        # expect 'void' | 'int' | 'char' | 'boolean' | <className>
        type,value = self.getNextToken()
        if (type == "keyword" and (value == "void" or value == "int" or value == "char" or value == "boolean")) or (type == "identifier"):
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected keyword void|int|char|boolean | identifier - {} {}".format(type,value))

        ################ SUBROUTINENAME ################
        # expect <subroutineName>
        type,value = self.getNextToken()
        if type == "identifier":
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected identifier - {} {}".format(type,value))

        # expect (
        type,value = self.getNextToken()
        if type == "symbol" and value == "(":
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected symbol ( - {} {}".format(type,value))

        self.parseTree.append({"type":"open","value":"parameterList"})
        self.compileParameterList()
        self.parseTree.append({"type":"close","value":"parameterList"})

        # expect )
        type,value = self.getNextToken()
        if type == "symbol" and value == ")":
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected symbol ) - {} {}".format(type,value))

        self.parseTree.append({"type":"open","value":"subroutineBody"})
        self.compileSubroutineBody()
        self.parseTree.append({"type":"close","value":"subroutineBody"})


    def compileParameterList(self):
        ## No Parameter List
        type,value = self.seeNextToken()
        if type == "symbol" and value == ")":
            return

        while True:
            # expect 'int' | 'char' | 'boolean' | <className>
            type,value = self.getNextToken()
            if (type == "keyword" and (value == "int" or value == "char" or value == "boolean")) or (type == "identifier"):
                self.parseTree.append({"type":type,"value":value})
            else:
                raise SyntaxError("Expected keyword int|char|boolean | identifier - {} {}".format(type,value))

            # expect <varName>
            type,value = self.getNextToken()
            if type == "identifier":
                self.parseTree.append({"type":type,"value":value})
            else:
                raise SyntaxError("Expected identifier - {} {}".format(type,value))

            # maybe more <type> <varName>
            type,value = self.seeNextToken()
            if type == "symbol" and value == ",":
                type,value = self.getNextToken()
                self.parseTree.append({"type":type,"value":value})
            elif type == "symbol" and value == ")":
                return
            else:
                raise SyntaxError("Expected symbol ,|) - {} {}".format(type,value))

#   <subroutineBody>    =>  '{' <varDec>* <statements> '}'

# <varDec>            =>  'var' <type> <varName> (',' <varName>)* ';'


    def compileSubroutineBody(self):
        # expect {
        type,value = self.getNextToken()
        if type == "symbol" and value == "{":
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected symbol {{ - {} {}".format(type,value))

        # expect <varDec>*
        type,value = self.seeNextToken()
        if type == "keyword" and value == "var":
            self.parseTree.append({"type":"open","value":"varDec"})
            self.compileVarDec()
            self.parseTree.append({"type":"close","value":"varDec"})

        # expect <subroutineDec>*
        type,value = self.seeNextToken()    
        while type == "keyword" and (value == "constructor" or value == "function" or value == "method"):
            self.parseTree.append({"type":"open","value":"subroutineDec"})
            self.compileSubroutineDec()
            self.parseTree.append({"type":"close","value":"subroutineDec"})
            type,value = self.seeNextToken()

        # expect }
        type,value = self.getNextToken()
        if type == "symbol" and value == "}":
            self.parseTree.append({"type":type,"value":value})
        else:
            raise SyntaxError("Expected symbol }} - {} {}".format(type,value))




    def compileVarDec(self):
        pass

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

