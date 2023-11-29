
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
            flat.append([exp["data"],exp["type"]])
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
            print("{}".format(exp["data"]), end="")
        print("")

        for exp in self.Expression:
            if exp["child"]:
                for chexp in exp["child"]:
                    chexp.printExpression(exp["data"], count+5)

    def shuntingYard(self):
        operators = {
            '|': [2, "L"], 
            '&': [3, "L"], 
            '=': [4, "L"],
            '<': [5, "L"], 
            '>': [5, "L"], 
            '+': [6, "L"], 
            '-': [6, "L"], 
            '*': [7, "L"], 
            '/': [7, "L"], 
            '~': [8, "R"], ## UNARY NOT
            'm': [8, "R"]  ## UNARY MINUS
            }

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
                while operatorStack and operatorStack[-1][0] != '(':
                    outputQueue.append(operatorStack.pop())
                operatorStack.pop()

            prevToken = token

        while operatorStack:
            outputQueue.append(operatorStack.pop())
        
        self.Expression = outputQueue
