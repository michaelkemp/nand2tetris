
class BinaryTree:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def getLeftChild(self):
        return self.left

    def setLeftChild(self, tree):
        self.left = tree

    def getRightChild(self):
        return self.right

    def setRightChild(self, tree):
        self.right = tree

    def getRootVal(self):
        return self.data

    def setRootVal(self, data):
        self.data = data

    def insertLeft(self, data):
        if self.left is None:
            self.left = BinaryTree(data)
        else:
            self.left.insertLeft(data)

    def insertRight(self, data):
        if self.right is None:
            self.right = BinaryTree(data)
        else:
            self.right.insertRight(data)

    def insert(self, data):
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data
