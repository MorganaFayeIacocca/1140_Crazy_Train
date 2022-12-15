from PLCCompiler import PLCCompiler
from TrackModel import TrackModel, Block

#Wayside Controller class - contains instance of PLCCompiler, TrackModel and CTC
class WaysideController:
    #Initialize WaysideController object
    #Inputs: int[] - list of blocks controlled by the Wayside, TrackModel ptr, bool: default position of switch, int- block number of switch (treated as a dont-care if no switch_
            #int[] - list of blocks containing traffic lights if lights exist, WaysideControllerGroup ptr, String - filename for PLC
            #int[] - list of all blocks in a tunnel if the wayside contains blocks in a tunnel, int - block# of crossbar if it exists
    #Outputs: None
    def __init__(self, blockList, track: TrackModel, defaultPos: bool, switchBlockIndex: int, lightList, groupPtr, filename, tunnelList,crossIndex: int):
        self.groupPtr = groupPtr
        self.defaultPos = defaultPos    #defaultPos is false when straight is default and true when curved is default - defaults were set by Track Model and Wayside controller developers
        self.switchPos = True  #switchPos is true if switch is in default position, false otherwise
        self.switchBlock = switchBlockIndex
        self.cross = crossIndex
        self.lightStatus = {}
        self.tunnelLight = {}
        self.blockOcc = {}
        self.railFail = {}
        self.switchFail = {}
        self.powerFail = {}
        self.circuitFail = {}
        self.maintenanceBlocks = {}
        #Initialize component states based on current track model states
        for x in blockList:
            self.blockOcc[x] = track.getBlock(x).getOccupied()
            self.railFail[x] = track.getBlock(x).getTrackFailure()
            self.switchFail[x] = track.getBlock(x).getSwitchFailure()
            self.powerFail[x] = track.getBlock(x).getPowerFailure()
            self.circuitFail[x] = track.getBlock(x).getCircuitFailure()
            self.maintenanceBlocks[x] = False
            track.getBlock(x).setWayside(self)
        if lightList != None:
            for x in lightList:
                self.lightStatus[x] = track.getBlock(x).getSwitchLight()
        if tunnelList != None:
            for x in tunnelList:
                self.tunnelLight[x] = track.getBlock(x).getLighting()
        self.tunnelList = tunnelList
        if True in self.tunnelLight:
            self.tunnelLightStatus = True
        else:
            self.tunnelLightStatus = False
        self.blockList = blockList
        self.lightList = lightList
        self.suggSpeed = 0
        self.authority = False
        self.heatTracks = False
        self.maintenance = False
        self.compiler = PLCCompiler(self,filename)
        self.trackModel = track
        self.ctc = None

    #update() - updates list of track occupancies and updates track component states based on new occupancy and PLC instructions - called by the controller group update function
    #Inputs: None
    #Outputs:None
    def update(self):
        self.updateOccupancy()
        self.compiler.execFile()

    #updateOccupancy() - updates list of track occupancies to reflect TrackModel occupancies, iterates through all block indexes to update
    #Inputs: None
    #Outputs:None
    def updateOccupancy(self):
        for x in self.blockList:
            occ = self.trackModel.getBlock(x).getOccupied()
            self.blockOcc[x] = occ

    #relayOccupancy() - send updated occupancy to CTC
    #Inputs: int - prevBlock(block index that was but is no longer occupied), int - nextBlock(block index that was not but is now occupied)
    #Outputs: None
    def relayTrackOccupancy(self,prevBlock,newBlock):
        self.groupPtr.ctc.getOccupancy(prevBlock,newBlock)

    #sendErrorToCTC() - sends errors from trackModel to CTC
    #Inputs: int (block number that fails), string (type of error)
    #Outputs: None
    def sendErrorToCTC(self, blockNum, error, status):
        if error == 'Switch Failure':
            self.switchFail[blockNum] = status
        elif error == 'Power Failure':
            self.powerFail[blockNum] = status
        elif error == 'Circuit Failure':
            self.circuitFail[blockNum] = status
        elif error == 'Track Failure':
            self.railFail[blockNum] = status
        self.groupPtr.ctc.getError(blockNum, error, status)

    #setTrackHeating() - called by TrackModel to set the track heating status (ON/OFF)
    #Inputs: Pointer to Block to be heated, bool - True if heat should be ON, False otherwise
    def setTrackHeating(self, block: Block, heat: bool):
        currHeat = block.getHeated()
        if currHeat != heat:
            block.toggleHeated()