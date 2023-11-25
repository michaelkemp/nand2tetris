
class Expressions:
    def __init__(self):
        self.Expression = []

    def addTerm(self, data, type, child=None):
        self.Expression.append(
            {
                "data": data,
                "type": type,
                "child": child,
                "children": None
             }

        )

    def addChildren(self, children):
        self.Expression[-1]["children"] = children

    def printExpression(self, parent=None):
        if parent == None:
            print("EXP - ",end="")
        else:
            print(f"{parent} - ",end="")

        for exp in self.Expression:
            print("{}, ".format(exp["data"]), end="")
        for exp in self.Expression:
            if exp["child"] is not None:
                print("\n")
                exp["child"].printExpression(exp["data"])
            if  exp["children"] is not None:
                for expList in exp["children"]:
                    print("\n")
                    expList.printExpression(exp["data"])
