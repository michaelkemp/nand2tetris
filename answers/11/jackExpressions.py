
class Expressions:
    def __init__(self):
        self.Expression = []
    
    def getOutput(self):
        final = self.parseExp([])
        print("=========================",final)
    
    def addTerm(self, data, type, child=[]):
        self.Expression.append(
            {
                "data": data,
                "type": type,
                "child": child
             }
        )

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
                    chexp.printExpression(exp["data"], count+2)


    def parseExp(self, final):
        for exp in self.Expression:
            if exp["child"]:
                for chexp in exp["child"]:
                    final = chexp.parseExp(final)
            final.append([exp["data"],exp["type"]])
        print(final)
        #for token, blap in self.shuntingYard(expList):
        #    final.append([token,blap])

        return final


    def shuntingYard(self, expList):

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

        for token,blap in expList:
            if token not in ["+", "-", "*", "/", "&", "|", "<", ">", "=", "~", "(", ")"]:
                outputQueue.append([token,blap])
            if token in ["+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]:
                if (token == "-") and (prevToken is None or prevToken in ["(", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]): ## UNARY MINUS
                    token = "m"
                while ( 
                    operatorStack and 
                    (operatorStack[-1][0] in operators) and
                        (
                            (operators[operatorStack[-1][0]][0] > operators[token][0]) or
                            (
                                operators[operatorStack[-1][0]][0] == operators[token][0] and 
                                operators[operatorStack[-1][0]][1] == "L"
                            )
                        )
                    ):
                    outputQueue.append(operatorStack.pop())
                
                operatorStack.append([token,blap])
            if token == "(":
                operatorStack.append([token,blap])
            if token == ")":
                while operatorStack and operatorStack[-1][0] != '(':
                    outputQueue.append(operatorStack.pop())
                operatorStack.pop()

            prevToken = token

        while operatorStack:
            outputQueue.append(operatorStack.pop())
        
        return outputQueue
