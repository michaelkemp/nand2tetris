
class Expressions:
    def __init__(self):
        self.Expression = []
    
    def addTerm(self, data, type, child=[]):
        self.Expression.append(
            {
                "data": data,
                "type": type,
                "child": child
             }
        )

    def getExp(self):
        self.parseExp()
        fullExp = self.flattenExp([])
        ## self.printExpression()
        return fullExp

    def flattenExp(self, flat):
        for exp in self.Expression:
            if exp["child"]:
                for chexp in exp["child"]:
                    flat = chexp.flattenExp(flat)
            ## nChild carries the argument count through for "call" terms,
            ## which flattenExp would otherwise discard before it reaches codegen
            flat.append([exp["data"],exp["type"],len(exp["child"])])
        return flat
    
    def parseExp(self):
        self.shuntingYard()
        for exp in self.Expression:
            if exp["child"]:
                for chexp in exp["child"]:
                    chexp.parseExp()

    def printExpression(self, parent=None, count=0):
        print(" " * count, end="")
        if parent == None:
            print("EXP - ",end="")
        else:
            print(f"{parent} - ",end="")

        for exp in self.Expression:
            print(f"{exp['data']}", end="")
        print("")

        for exp in self.Expression:
            if exp["child"]:
                for chexp in exp["child"]:
                    chexp.printExpression(exp["data"], count+5)

    def shuntingYard(self):
        ## Jack's grammar (expression: term (op term)*) has no operator
        ## precedence at all -- every binary op is equal precedence and
        ## strictly left-to-right. All binary ops share one tier here to
        ## match that; unary '~'/'m' still need to bind tighter than any
        ## binary op (so "-x + y" means "(-x) + y", not "-(x+y)").
        operators = {
            '|': [1, "L"],
            '&': [1, "L"],
            '=': [1, "L"],
            '<': [1, "L"],
            '>': [1, "L"],
            '+': [1, "L"],
            '-': [1, "L"],
            '*': [1, "L"],
            '/': [1, "L"],
            '~': [2, "R"], ## UNARY NOT
            'm': [2, "R"]  ## UNARY MINUS
            }
        ## PEMDAS-style precedence (NOT spec-correct for Jack -- every
        ## binary op is actually equal precedence per grammar.txt -- kept
        ## here in case we ever want real C-like precedence instead):
        # operators = {
        #     '|': [2, "L"],
        #     '&': [3, "L"],
        #     '=': [4, "L"],
        #     '<': [5, "L"],
        #     '>': [5, "L"],
        #     '+': [6, "L"],
        #     '-': [6, "L"],
        #     '*': [7, "L"],
        #     '/': [7, "L"],
        #     '~': [8, "R"], ## UNARY NOT
        #     'm': [8, "R"]  ## UNARY MINUS
        #     }

        outputQueue = []
        operatorStack = []
        prevToken = None

        for exp in self.Expression:
            token = exp["data"]
            tokType = exp["type"]
            tokKids = exp["child"]

            if token not in ["+", "-", "*", "/", "&", "|", "<", ">", "=", "~", "(", ")"]:
                outputQueue.append({"data": token, "type": tokType, "child": tokKids})

            if token in ["+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]:
                if (token == "-") and (prevToken is None or prevToken in ["(", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]): ## UNARY MINUS
                    token = "m"
                while ( 
                    operatorStack and 
                    (operatorStack[-1]["data"] in operators) and
                        (
                            (operators[operatorStack[-1]["data"]][0] > operators[token][0]) or
                            (
                                operators[operatorStack[-1]["data"]][0] == operators[token][0] and 
                                operators[operatorStack[-1]["data"]][1] == "L"
                            )
                        )
                    ):
                    outputQueue.append(operatorStack.pop())
                
                operatorStack.append({"data": token, "type": tokType, "child": tokKids})
            if token == "(":
                operatorStack.append({"data": token, "type": tokType, "child": tokKids})
            if token == ")":
                while operatorStack and operatorStack[-1]["data"] != '(':
                    outputQueue.append(operatorStack.pop())
                operatorStack.pop()

            prevToken = token

        while operatorStack:
            outputQueue.append(operatorStack.pop())
        
        self.Expression = outputQueue
