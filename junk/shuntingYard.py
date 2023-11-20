# 1.  While there are tokens to be read:
# 2.        Read a token
# 3.        If it's a number add it to queue
# 4.        If it's an operator
# 5.               While there's an operator on the top of the stack with greater precedence OR an operator with equal precedence that is LEFT associative:
# 6.                       Pop operators from the stack onto the output queue
# 7.               Push the current operator onto the stack
# 8.        If it's a left bracket push it onto the stack
# 9.        If it's a right bracket 
# 10.            While there's not a left bracket at the top of the stack:
# 11.                     Pop operators from the stack onto the output queue.
# 12.             Pop the left bracket from the stack and discard it
# 13. While there are operators on the stack, pop them to the queue

import re

def parseExp(expList):
    print(expList)

    operators = {
        '+': [2, "L"], 
        '-': [2, "L"], 
        '*': [3, "L"], 
        '/': [3, "L"], 
        '^': [4, "R"],
        'u': [5, "R"] ## unary minus
        }
    
    outputQueue = []
    operatorStack = []
    prevToken = None

    for token in expList:
        if token not in ["+","-","*","/","^","(",")"]:
            outputQueue.append(token)
        if token in ["+","-","*","/","^"]:
            if (token == "-") and (prevToken is None or prevToken in ["(","+","-","*","/","^"]): ## UNARY MINUS
                token = "u"
            while ( 
                operatorStack and 
                (operatorStack[-1] in operators) and
                    (
                        (operators[operatorStack[-1]][0] > operators[token][0]) or
                        (
                            operators[operatorStack[-1]][0] == operators[token][0] and 
                            operators[operatorStack[-1]][1] == "L"
                        )
                    )
                ):
                outputQueue.append(operatorStack.pop())
            
            operatorStack.append(token)
        if token == "(":
            operatorStack.append(token)
        if token == ")":
            while operatorStack and operatorStack[-1] != '(':
                outputQueue.append(operatorStack.pop())
            operatorStack.pop()

        prevToken = token

    while operatorStack:
        outputQueue.append(operatorStack.pop())
    
    print(outputQueue)

    ## test
    stack = []
    for tok in outputQueue:
        if tok == "u":
            a = float(stack.pop())
            val = (-1*a)
            stack.append(val)
        elif tok in ["+","-","*","/","^"]:
            b = float(stack.pop())
            a = float(stack.pop())
            match tok:
                case "+": val = (a+b)
                case "-": val = (a-b)
                case "*": val = (a*b)
                case "/": val = (a/b)
                case "^": val = (a**b)
            stack.append(val)
        else:
            stack.append(tok)
    print(stack)


expLists = [
    "1+2*3*4+5",
    "( ( ( 10 + 5 ) * 3 ) / ( 7 + 23 ) )",
    "((((1))*((2)))+(((3)^(4))/((5))))",
    "3+2*4+5/1*6+5+6+7-1",
    "(3+1) / 5  * 12 * 22 + 8 ^ 2  / 2",
    "5  + 11 * 9 + 7 - 4",
    "3+4*2/(1-5)^2^3",
    "3*-2",
    "(-2 * 45)",
    "-7 - -6",
    "-35 * 12/-4",
    "-2^2"
]

for exp in expLists:
    exp = re.split('([^a-zA-Z0-9])', exp.replace(" ", "") )
    while '' in exp:
        exp.remove('')
    parseExp(exp)

