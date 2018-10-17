import numpy as np
import heapq as hq

class HuffmanTreeNode:
    def __init__(self, value, posibility):
        self.posibility = posibility
        self.left = None
        self.right = None
        self.value = value
        self.huffman = ""

class HuffmanTree:
    def __init__(self, wordPosiDict, vecLength):
        self.nodeTumpleList = [(wordPosiDict[key], HuffmanTreeNode(key, wordPosiDict[key])) for key in wordPosiDict]
        self.vecLength = vecLength
        self.root = None
        self.wordCodeDict = {}
        self.buildTree()

    def buildTree(self):
        nodeInTree = 0
        hq.heapify(self.nodeTumpleList)
        while (len(self.nodeTumpleList) > 1):
            if nodeInTree % 100 == 0:
                print "[buildTree] node No.", str(nodeInTree)

            minNode1 = hq.heappop(self.nodeTumpleList)[1]
            minNode2 = hq.heappop(self.nodeTumpleList)[1]

            # for i in range(2, len(self.nodeList)):
            #     if self.nodeList[i].posibility < self.nodeList[min2].posibility:
            #         if self.nodeList[i].posibility < self.nodeList[min1].posibility:
            #             min2 = min1
            #             min1 = i
            #         else:
            #             min2 = i
            newNode = self.merge(minNode1, minNode2)
            # if (min1 < min2):
            #     self.nodeList.pop(min2)
            #     self.nodeList.pop(min1)
            # elif (min2 < min1):
            #     self.nodeList.pop(min1)
            #     self.nodeList.pop(min2)
            # else:
            #     raise RuntimeError("min1 = min2")
            hq.heappush(self.nodeTumpleList, (newNode.posibility, newNode))
            nodeInTree += 1

        self.root = self.nodeTumpleList[0][1]
        print "[buildTree] generating code..."
        self.generateCode(self.root)
        print "[buildTree] generate code done."

    def merge(self, node1, node2):
        newNode = HuffmanTreeNode(np.random.rand(self.vecLength), node1.posibility + node2.posibility)
        if node1.posibility > node2.posibility:
            newNode.left = node1
            newNode.right = node2
        else:
            newNode.right = node1
            newNode.left = node2
        return newNode

    def generateCode(self, node):
        if (node.left is None and node.right is None):
            self.wordCodeDict[node.value] = node.huffman

        if node.left:
            node.left.huffman = node.huffman + "0"
            self.generateCode(node.left)

        if node.right:
            node.right.huffman = node.huffman + "1"
            self.generateCode(node.right)
