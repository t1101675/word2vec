import numpy as np
import heapq as hq

class HuffmanTreeNode:
    def __init__(self, value, posibility):
        self.posibility = posibility
        self.left = None
        self.right = None
        self.value = value
        self.huffman = ""
        self.parent = None
        self.binary = 0

class HuffmanTree:
    def __init__(self, wordPosiDict, vecLength):
        self.nodeTumpleList = [(wordPosiDict[key], HuffmanTreeNode(key, wordPosiDict[key])) for key in wordPosiDict]
        self.nodeList = [HuffmanTreeNode(key, wordPosiDict[key]) for key in wordPosiDict]
        self.vecLength = vecLength
        self.root = None
        self.wordCodeDict = {}
        self.buildTree()

    def buildTree(self):
        nodeInTree = 0
        sortedNodes = sorted(self.nodeList, key=lambda node:node.posibility, reverse = True)
        # for node in sortedNodes:
            # print node.value, node.posibility
        vocabSize = len(self.nodeList)
        mergedNodes = []
        binary = [0 for i in range(0, vocabSize)]
        pos1 = vocabSize - 1
        pos2 = 0
        for i in range(0, vocabSize - 1):
            if i % 1000 == 0:
                print "[buildTree] node No.", str(i)
            if pos1 >= 0:
                if (pos2 >= len(mergedNodes) or sortedNodes[pos1].posibility < mergedNodes[pos2].posibility):
                    minNode1 = sortedNodes[pos1]
                    pos1 -= 1
                else:
                    minNode1 = mergedNodes[pos2]
                    pos2 += 1
            else:
                minNode1 = mergedNodes[pos2]
                pos2 += 1

            if pos1 >= 0:
                if (pos2 >= len(mergedNodes) or sortedNodes[pos1].posibility < mergedNodes[pos2].posibility):
                    minNode2 = sortedNodes[pos1]
                    pos1 -= 1
                else:
                    minNode2 = mergedNodes[pos2]
                    pos2 += 1
            else:
                minNode2 = mergedNodes[pos2]
                pos2 += 1

            newNode = self.merge(minNode1, minNode2)
            mergedNodes.append(newNode)
        # hq.heapify(self.nodeTumpleList)
        # while (len(self.nodeTumpleList) > 1):
        #     if nodeInTree % 100 == 0:
        #         print "[buildTree] node No.", str(nodeInTree)
        #
        #     minNode1 = hq.heappop(self.nodeTumpleList)[1]
        #     minNode2 = hq.heappop(self.nodeTumpleList)[1]
        #     newNode = self.merge(minNode1, minNode2)
        #     hq.heappush(self.nodeTumpleList, (newNode.posibility, newNode))
        #     nodeInTree += 1
        #
        # self.root = self.nodeTumpleList[0][1]
        print pos2, len(mergedNodes)
        self.root = mergedNodes[pos2]
        print "[buildTree] generating code..."
        self.generateCode(self.root)



        print "[buildTree] generate code done."
        # for node in sortedNodes:
        #     print node.value, self.wordCodeDict[node.value]

    def merge(self, node1, node2):
        # print node1.posibility, node2.posibility
        newNode = HuffmanTreeNode(np.random.rand(self.vecLength), node1.posibility + node2.posibility)
        newNode.value -= np.ones(self.vecLength) * 0.5
        newNode.value /= self.vecLength

        if node1.posibility > node2.posibility:
            newNode.left = node1
            newNode.right = node2
        else:
            newNode.right = node1
            newNode.left = node2

        node1.parent = newNode
        node2.parent = newNode
        return newNode

    def generateCode(self, node):
        # print node.posibility
        if (node.left is None and node.right is None):
            self.wordCodeDict[node.value] = node.huffman

        if node.left:
            node.left.huffman = node.huffman + "1"
            self.generateCode(node.left)

        if node.right:
            node.right.huffman = node.huffman + "0"
            self.generateCode(node.right)
