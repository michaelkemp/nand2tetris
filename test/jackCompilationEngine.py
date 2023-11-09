
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

##
## compileClass
## compileClassVarDec
## compileSubroutine
## compileParameterList
## compileSubroutineBody
## compileVarDec
## compileStatements
## compileLet
## compileIf
## compileWhile
## compileDo
## compileReturn
## compileExpression
## compileTerm
## compileExpressionList
##
## type, className, subroutineName, varName, statement, subroutineCall

class CompliationEngine:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pointer = 0
        self.currentToken = self.tokens[self.pointer]["value"];

    def parseTokens(self):
        print(self.tokens[self.pointer]["type"], self.tokens[self.pointer]["value"])

    def compileStatements(self):
        pass

    def compileIfStatement(self):
        pass

    def compileLetStatement(self):
        pass

    def compileWhileStatement(self):
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

    def compileTerm(self):
        # varName | constant
        pass

    def compileExpression(self):
        ## term (op term)?
        pass
    
    def eat(self, string):
        if (self.currentToken != string):
            raise SyntaxError("Expecting {}, received {}".format(string,self.currentToken))
        else:
            self.advanceToken()
    
    def advanceToken(self):
        self.pointer += 1
        self.currentToken = self.tokens[self.pointer]["value"];
