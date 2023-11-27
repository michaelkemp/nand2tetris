
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

    def printExpression(self, parent=None):
        if parent == None:
            print("EXP - ",end="")
        else:
            print(f"{parent} - ",end="")

        for exp in self.Expression:
            print("{}, ".format(exp["data"]), end="")

        for exp in self.Expression:
            if exp["child"]:
                for chexp in exp["child"]:
                    print("\n")
                    chexp.printExpression(exp["data"])
