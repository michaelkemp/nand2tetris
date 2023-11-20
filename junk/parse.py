import BinaryTree, re


def buildParseTree(fplist): 

    pStack = []
    eTree = BinaryTree.BinaryTree('')
    pStack.append(eTree)
    currentTree = eTree

    for i in fplist:
        if i == '(':
            currentTree.insertLeft('')
            pStack.append(currentTree)
            currentTree = currentTree.getLeftChild()

        elif i in ['+', '-', '*', '/', '^']:
            if currentTree.getRootVal() != '':
                eTree = BinaryTree.BinaryTree('')
                pStack.append(eTree)
                eTree.setLeftChild(currentTree)
                currentTree = eTree

            currentTree.setRootVal(i)
            currentTree.insertRight('')
            pStack.append(currentTree)
            currentTree = currentTree.getRightChild()
        elif i == ')':
            currentTree = pStack.pop()
        else:
            currentTree.setRootVal(i)
            parent = pStack.pop()
            currentTree = parent

    return eTree


def preorder(tree):
    if tree:
        if tree.getRootVal() != "":
            print("={}=".format(tree.getRootVal()))
        preorder(tree.getLeftChild())
        preorder(tree.getRightChild())

def postorder(tree):
    if tree != None:
        postorder(tree.getLeftChild())
        postorder(tree.getRightChild())
        if tree.getRootVal() != "":
            print(tree.getRootVal())

def inorder(tree):
    if tree != None:
        inorder(tree.getLeftChild())
        if tree.getRootVal() != "":
            print(tree.getRootVal())
        inorder(tree.getRightChild())

def parenthesization(str):
    rstr = "(((("
    for c in str:
        match c:
            case "(" : rstr += "(((("
            case ")" : rstr += "))))"
            case "^" : rstr += ")^("
            case "*" : rstr += "))*(("
            case "/" : rstr += "))/(("
            case "+" : rstr += ")))+((("
            case "-" : rstr += ")))-((("
            case _: rstr += c
    rstr += "))))"
    return rstr


# exp = "( ( ( 10 + 5 ) * 3 ) / ( 7 + 23 ) )"
# pt = buildParseTree(exp)
# print(exp)
# postorder(pt)

# exp = "((((1))*((2)))+(((3)^(4))/((5))))"
# pt = buildParseTree(exp)
# print(exp)
# postorder(pt)

exp = "5  + a * b + 7 - 4".replace(" ", "") 
exp = "(3+1) / 5  * a * b + cd ^ d  / e".replace(" ", "")
# print(exp)
exp = parenthesization(exp)
print(exp)
expList = re.split('([^a-zA-Z0-9])',exp)
while '' in expList:
    expList.remove('')
print(expList)
pt = buildParseTree(expList)

postorder(pt)


# Using the information from above we can define four rules as follows:
#   1. If the current token is a '(', add a new node as the left child of the current node, and descend to the left child.
#   2. If the current token is in the list ['+','-','/','*'], set the root value of the current node to the operator 
#      represented by the current token. Add a new node as the right child of the current node and descend to the right child.
#   3. If the current token is a number, set the root value of the current node to the number and return to the parent.
#   4. If the current token is a ')', go to the parent of the current node.

