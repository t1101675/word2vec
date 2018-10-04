import numpy as np

class HuffmanTreeNode:
    def __init__(self, value, posibility):
        self.posibility = posibility
        self.left = None
        self.right = None
        self.value = value
        self.huffman = ""

class HuffmanTree:
    def __init__(self, wordList, vecLength):
        self.nodeList = [HuffmanTreeNode(word["value"], word["posibility"]) for word in wordList]
        self.vecLength = vecLength
        self.root = None
        self.buildTree()

    def buildTree(self):
        while (len(nodeList) > 1):
            min1 = 0
            min2 = 1
            for i in range(2, len(nodeList)):
                if nodeList[i].posibility < nodeList[min2].posibility:
                    if nodeList[i].posibility < nodeList[min1].posibility:
                        min2 = min1
                        min1 = i
                    else:
                        min2 = i
            newNode = merge(nodeList[min1], nodeList[min2])
            if (min1 < min2):
                nodeList.pop(min2)
                nodeList.pop(min1)
            elif (min2 < min1):
                nodeList.pop(min1)
                nodeList.pop(min2)
            else:
                raise RuntimeError("min1 = min2")
            nodeList.append(newNode)
        self.root = nodeList[0]

    def merge(self, node1, node2):
        newNode = HuffmanTreeNode(np.zeros(self.vecLength), node1.posibility + node2.posibility)
        if node1.posibility > node2.posibility:
            newNode.left = node1
            newNode.right = node2
        else:
            newNode.right = node1
            newNode.left = node2
        return newNode
