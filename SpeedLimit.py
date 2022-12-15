from sqlite3 import connect
from typing import List

class SpeedLimitNode:
    block: int
    speedLimit: int
    connectNodes: List
    switchNodes: List

    def __init__(self, block: int, speedLimit : int) -> None:
        self.block = block
        self.speedLimit = speedLimit
        self.connectNodes = []
        self.switchNodes = []

    def setNextNode(self, nextNode: 'SpeedLimitNode', switch: bool) -> None:
        if(switch):
            self.switchNodes.append(nextNode)
        else:
            self.connectNodes.append(nextNode)
    
    def getBlock(self) -> int:
        return self.block
    
    def getSpeedLimit(self) -> int:
        return self.speedLimit
    
    def getConnectNodes(self) -> List['SpeedLimitNode']:
        return self.connectNodes
    
    def getSwitchNodes(self) -> List['SpeedLimitNode']:
        return self.switchNodes

class SpeedLimit:
    #static variables
    allNodes: List[SpeedLimitNode]
    allNodes = []
    lastNode: SpeedLimitNode
    yardNode: SpeedLimitNode

    #instance variables
    currentNode: SpeedLimitNode
    previousNode: SpeedLimitNode

    def __init__(self) -> None:
        self.currentNode = self.yardNode
        self.previousNode = self.lastNode

    def getNextSpeedLimit(self, beacon: str) -> int:
        nextNode = None
        connectNodes = self.currentNode.getConnectNodes()
        switchNodes = self.currentNode.getSwitchNodes()
        
        node: SpeedLimitNode
        for node in connectNodes:
            if node.getBlock() != self.previousNode.getBlock():
                nextNode = node
        if nextNode is None:
            blockStringLocation = beacon.find("Block:") + len("Block:")
            beaconBlock = int(beacon[blockStringLocation:])
            if switchNodes[0].getBlock() == beaconBlock:
                nextNode = switchNodes[0]
            else:
                nextNode = switchNodes[1]  

        self.previousNode = self.currentNode
        self.currentNode = nextNode
        return self.currentNode.getSpeedLimit()
    
    @staticmethod
    def addNode(nodeNum: int, speedLimit: int) -> None:
        newNode = SpeedLimitNode(nodeNum, speedLimit)
        SpeedLimit.allNodes.append(newNode)

    @staticmethod
    def setNodeConnection(sourceNode: int, nextNode: int, switch: bool) -> None:
        SpeedLimit.allNodes[sourceNode].setNextNode(SpeedLimit.allNodes[nextNode], switch)
    
    @staticmethod
    def setInitialNode(firstBlock: int) -> None:
        SpeedLimit.yardNode = SpeedLimit.allNodes[0]
        node: SpeedLimitNode
        for node in SpeedLimit.yardNode.connectNodes:
            if node.block != firstBlock:
                SpeedLimit.lastNode = node
        if not hasattr(SpeedLimit, "lastNode"):
            SpeedLimit.lastNode = SpeedLimit.yardNode