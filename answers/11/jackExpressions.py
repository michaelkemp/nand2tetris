import json

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
