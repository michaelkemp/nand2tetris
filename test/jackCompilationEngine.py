
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

class CompliationEngine:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenPtr = 0
        self.currentToken = self.tokens[self.tokenPtr]["value"]
        self.parseTree = []

    def getNextToken(self, inc=1):
        self.tokenPtr += inc
        try:
            return [self.tokens[self.tokenPtr-inc]["type"],self.tokens[self.tokenPtr-inc]["value"]]
        except:
            return ["",""] 
    
    def seeNextToken(self):
        return self.getNextToken(0)


def parser():
    global parseTree

    # expect class
    type,value = getNextToken()
    if type == "keyword" and value == "class":
        parseTree.append({"type":"open","value":"class"})
        parseTree.append({"type":type,"value":value})
        compileClass()
        parseTree.append({"type":"close","value":"class"})
    else:
        print("Error in parser(): {} {}".format(type,value))
        exit(0)


    def parseTokens(self):
        # expect class
        type,value = getNextToken()
        if type == "keyword" and value == "class":
            parseTree.append({"type":"open","value":"class"})
            parseTree.append({"type":type,"value":value})
            compileClass()
            parseTree.append({"type":"close","value":"class"})
        else:
            print("Error in parser(): {} {}".format(type,value))
            exit(0)
            
    def compileClass(self):
        pass

    def compileClassVarDec(self):
        pass

    def compileSubroutine(self):
        pass

    def compileParameterList(self):
        pass

    def compileSubroutineBody(self):
        pass

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

