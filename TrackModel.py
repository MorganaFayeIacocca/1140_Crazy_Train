import os
import json
from random import randrange
from typing import List
from time import sleep
from PyQt5 import QtWidgets, QtGui, QtCore
from SpeedLimit import SpeedLimit

GreenConfigFilePath = "TrackModelModule/greenConfig.json"
RedConfigFilePath = "TrackModelModule/redConfig.json"
checkImage = "TrackModelModule/Check.jpg"
redXImage = "TrackModelModule/redX.jpg"
redLight = "TrackModelModule/redLight.jpg"
greenLight = "TrackModelModule/greenLight.jpg"

class TrackModel:
    blocks: List['Block']
    map: str
    line: str

    #__init__ initializes the trackModel object
    #Inputs: line: a string indicating which block should be used for this simulation
    #Return: No return values
    def __init__(self, line: str) -> None:
        self.line = line
        if self.line == "RED":
            with open(RedConfigFilePath, "r") as in_file:
                data = json.load(in_file)
        elif self.line == "GREEN":
            with open(GreenConfigFilePath, "r") as in_file:
                data = json.load(in_file)
        else:
            print("Error: Attempted to initialize Track Model with \"{}\" which does not exist".format(line))
            os._exit()

        self.map = data['picture']
        
        blocksData = data['blocks']
        self.blocks = []
        for blockData in blocksData:
            newBlock = Block(blockData, self)
            self.blocks.append(newBlock)
            SpeedLimit.addNode(newBlock.getBlockNum(), newBlock.getSpeedLimit())
        
        block: Block
        for block in self.blocks:
            for connection in block.connections:
                SpeedLimit.setNodeConnection(block.getBlockNum(), connection[0], connection[1] == "switch")
        SpeedLimit.setInitialNode(self.blocks[0].defaultConnection)    

    #getBlock returns a pointer to a specific block from the track model
    #Inputs: index: integer index of the block to be returned
    #Return: a pointer to the block located at the given index
    def getBlock(self, index : int) -> 'Block':
        if index >= len(self.blocks):
            self.errorSignal.emit("Error: Attempted to access block {}.\nThere are only {} blocks on this line.".format(index, len(self.blocks) - 1))
        return self.blocks[index]
    
    #setTrainModelInterface allows the system controller to assign the train model interface to the track model and its blocks after initialization
    #Inputs: trainModel: train model interface pointer to be connected
    #Return: No return values
    def setTrainModelInterface(self, trainModel: 'TrainModelInterface'):
        for block in self.blocks:
            block.setTrainModel(trainModel)
    
    #setErrorSignal allows the system controller to assign the errorSignal widget to the track model after initialization
    #Inputs: errorSignal: the PyQt signal to be connected to the track model
    #Return: No return values
    def setErrorSignal(self, errorSignal: QtCore.pyqtSignal):
        self.errorSignal = errorSignal

    #update updates the track model and any blocks attached to it to represent the passage of time
    #Inputs: No inputs
    #Return: No return values
    def update(self) -> None:
        for block in self.blocks:
            block.update()
    
    #setSuggestedSpeed realys the suggested speed received from the Wayside Group to the correct block
    #Inputs: blockNum: integer indicating which block the signal is intended for
    #        speed: int indicating the speed to be sent
    #Return: No return values
    def setSuggestedSpeed(self, blockNum: int, speed: int) -> None:
        self.blocks[blockNum].setSuggestedSpeed(speed)
    
    #setAuthority relays the authority received from the Wayside Group to the correct block
    #Inputs: blockNum: integer indicating which block the signal is intended for
    #        authority: boolean indicating the authority to be sent
    #Return: No return values
    def setAuthority(self, blockNum: int, authority: bool) -> None:
        self.blocks[blockNum].setAuthority(authority)

class Block:
    #Test Inputs
    inputs: 'Input'

    #Other modules/classes
    trackModel: TrackModel
    wayside: 'WaysideController'
    trainModel: 'TrainModelInterface'

    #Constants
    blockNum: int
    length: float
    elevation: float
    grade: float
    speedLimit: int

    #connected blocks
    #connections are of the form ("block number" (int), "type"(switch or connection), "current block connected"(bool), "other block connected"(bool))
    connections: List
    #Next block expected on route. Ignored in most cases
    defaultConnection: int

    #status
    lighting: bool
    heated: bool
    crossLights: bool

    #Train currently occupying the block or None
    occupied: 'Train'

    #Color of the switch light ("RED", "YELLOW", or "GREEN") or "NONE"
    switchLight: str
    #beacon = "Station:StationName:NextStation:NextStation:Underground:Block:BlockNum"
    #beacon = "Station:StationName:Side:Left:"
    #beacon = "Underground:Block:BlockNum"
    beacon: str

    #Temperature of the track
    temperature: int

    #Current values of the failures
    powerFailure: bool
    trackFailure: bool
    circuitFailure: bool
    switchFailure: bool

    #Station pointer or None
    station: 'Station'

    #last updated values
    authority: bool
    suggestedSpeed: int
    #format "0b" + {1} "Circuit Failure" + {3} "Authority" + {8} "Speed"
    trackCircuit: bytes

    #Gui Widgets that need updated
    connectedWidget: QtWidgets.QLabel
    adjacentWidget: QtWidgets.QLabel
    occupiedWidget: QtWidgets.QLabel
    lightingWidget: QtWidgets.QLabel
    crossingWidget: QtWidgets.QLabel
    heatingWidget: QtWidgets.QLabel
    switchLightWidget: QtWidgets.QLabel
    powerFailureWidget: QtWidgets.QPushButton
    trackFailureWidget: QtWidgets.QPushButton
    circuitFailureWidget: QtWidgets.QPushButton
    switchFailureWidget: QtWidgets.QPushButton
    authorityWidget: QtWidgets.QLabel
    speedWidget: QtWidgets.QLabel
    binaryWidget: QtWidgets.QLabel

    #__init__ initializes the block object
    #Inputs: block: a dictionary describing the block from the configuration file
    #        trackModel: a pointer to the trackModel this block is a part of
    #Return: No return values
    def __init__(self, block : dict, trackModel : TrackModel) -> None:
        #initialize pointer
        self.trackModel = trackModel

        #initalize test inputs object
        self.inputs = Input(self)

        #initialize instance variables from configuration dictionary and default values
        self.blockNum = block['num']
        self.length = block['length']
        self.elevation = block['elevation']
        self.grade = block['grade']
        self.speedLimit = block['speedLimit']

        self.connections = block['adjacent']
        self.defaultConnection = block['defaultConnection']

        self.lighting = False
        self.heated = False
        self.crossLights = False

        self.occupied = None

        self.switchLight = block['switchLight']
        self.beacon = block['beacon']

        self.temperature = block['temperature']
        self.heaterTemperature = 37

        self.powerFailure = False
        self.trackFailure = False
        self.circuitFailure = False
        self.switchFailure = False

        #only create a station if there is a station on this block
        if 'station' in block.keys():
            self.station = Station(block['station'], self)
        else:
            self.station = None
        
        #initialize default values
        self.authority = False
        self.suggestedSpeed = 0
        self.trackCircuit = "     ".encode()

        #initialize the dynamic GUI widgets
        self.connectedWidget = QtWidgets.QLabel()
        self.adjacentWidget = QtWidgets.QLabel()
        self.occupiedWidget = QtWidgets.QLabel("No")
        self.lightingWidget = QtWidgets.QLabel("Off")
        self.crossingWidget = QtWidgets.QLabel("Off")
        self.heatingWidget = QtWidgets.QLabel("Off")
        self.switchLightWidget = QtWidgets.QLabel()
        self.powerFailureWidget = QtWidgets.QPushButton()
        self.trackFailureWidget = QtWidgets.QPushButton()
        self.circuitFailureWidget = QtWidgets.QPushButton()
        self.switchFailureWidget = QtWidgets.QPushButton()
        self.authorityWidget = QtWidgets.QLabel()
        self.speedWidget = QtWidgets.QLabel()
        self.binaryWidget = QtWidgets.QLabel()

        self.setConnectionWidgets()
        self.setSwitchLight(self.switchLight)
        self.powerFailureWidget.setIcon(QtGui.QIcon(checkImage))
        self.trackFailureWidget.setIcon(QtGui.QIcon(checkImage))
        self.circuitFailureWidget.setIcon(QtGui.QIcon(checkImage))
        self.switchFailureWidget.setIcon(QtGui.QIcon(checkImage))
        self.powerFailureWidget.clicked.connect(self.togglePowerFailure)
        self.trackFailureWidget.clicked.connect(self.toggleTrackFailure)
        self.circuitFailureWidget.clicked.connect(self.toggleCircuitFailure)
        self.switchFailureWidget.clicked.connect(self.toggleSwitchFailure)
    
    #setWayside connects the block to an instance of the Wayside Controller after the block is created
    #Inputs: wayside: the instance of WaysideController to connect to this block
    #Return: No return values
    def setWayside(self, wayside: 'WaysideController') -> None:
        self.wayside = wayside
    
    #setTrainModel connects the block to an instance of the Train Model Interface after the block is created
    #Inputs: trainModel: the instance of TrainModelInterface to connect to this block
    #Return: No return values
    def setTrainModel(self, trainModel: 'TrainModelInterface') -> None:
        self.trainModel = trainModel
    
    #switch changes the state of the switch on this block if there is a switch hosted on this block
    #Inputs: No inputs
    #Return: boolean indicating success of the action.
    #        The action fails for the following reasons:
    #           Power Failure
    #           Switch Failure
    #           There is no switch hosted on this block
    #        The action succeeds otherwise
    def switch(self) -> bool:
        if self.switchFailure or self.powerFailure:
            return False
        changes = 0
        for connection in self.connections:
            if connection[1] == 'switch':
                changes += 1
                connection[2] = not connection[2]
                self.trackModel.getBlock(connection[0]).changeConnection(self.blockNum)
        self.setConnectionWidgets()
        return changes > 0
        
    
    #hasSwitch determines whether a switch is hosted on this block or not
    #Inputs: No inputs
    #Return: boolean indicating that there is a switch hosted on this block
    def hasSwitch(self) -> bool:
        for connection in self.connections:
            if connection[1] == "switch":
                return True
        return False

    #changeConnection is called when a switch hosted on another block disconnects from or connects to this one
    #Inputs: switchBlock: the block number of the block that hosts the switch
    #Return: No return values
    def changeConnection(self, switchBlock : int) -> None:
        for connection in self.connections:
            if connection[0] == switchBlock:
                connection[3] = not connection[3]
        self.setConnectionWidgets()
    
    #setConnectionWidgets recalculates the values of the two connection widgets
    #Inputs: No inputs
    #Return: No return values
    def setConnectionWidgets(self) -> None:
        connected = ""
        adjacent = ""
        for c in self.connections:
            if c[0] == 0:
                connectionName = "Yard"
            else:
                connectionName = str(c[0])
            adjacent = adjacent + " " + connectionName
            if c[2] and c[3]:
                connected = connected + " " + connectionName
        if connected == "":
            connected = "None"
        
        self.connectedWidget.setText(connected)
        self.adjacentWidget.setText(adjacent)
    
    #toggleLighting toggles the value of lighting
    #Inputs: No inputs
    #Return: No return values
    def toggleLighting(self) -> None:
        self.lighting = not self.lighting
        #Update GUI
        if self.lighting:
            self.lightingWidget.setText("On")
        else:
            self.lightingWidget.setText("Off")
    
    #toggleHeated toggles the value of heated
    #Inputs: No inputs
    #Return: No return values
    def toggleHeated(self) -> None:
        self.heated = not self.heated
        #Update GUI
        if self.heated:
            self.heatingWidget.setText("On")
        else:
            self.heatingWidget.setText("Off")
    
    #toggleCrossLights toggles the value of crossLights
    #Inputs: No inputs
    #Return: No return values
    def toggleCrossLights(self) -> None:
        self.crossLights = not self.crossLights
        #Update GUI
        if self.crossLights:
            self.crossingWidget.setText("On")
        else:
            self.crossingWidget.setText("Off")
    
    #setSwitchLight sets the value of switchLight to the given input
    #Inputs: color: string representing new light value
    #Return: No return values
    def setSwitchLight(self, color: str) -> None:
        #Set system variable
        self.switchLight = color
        #update GUI
        if color == "RED":
            pixmap1101 = QtGui.QPixmap(redLight)
            self.switchLightWidget.setPixmap(pixmap1101)
        elif color == "YELLOW":
            pass
        elif color == "GREEN":
            pixmap1101 = QtGui.QPixmap(greenLight)
            self.switchLightWidget.setPixmap(pixmap1101)

    #lowerTemperature lowers the temperature by 1 degree and notifies the wayside controller
    #Inputs: No inputs
    #Return: No return values
    def lowerTemperature(self) -> None:
        self.temperature = self.temperature - 1
        self.wayside.setTrackHeating(self, self.temperature < self.heaterTemperature)
    
    #raiseTemperature raises the temperature by 1 degree and notifies the wayside controller
    #Inputs: No inputs
    #Return: No return values
    def raiseTemperature(self) -> None:
        self.temperature = self.temperature + 1
        self.wayside.setTrackHeating(self, self.temperature < self.heaterTemperature)

    #togglePowerFailure toggles the value of powerFailure and notifies the CTC office
    #Inputs: No inputs
    #Return: No return values
    def togglePowerFailure(self) -> None:
        self.powerFailure = not self.powerFailure
        self.wayside.sendErrorToCTC(self.blockNum, "Power Failure", self.powerFailure)
        #Update GUI
        if self.powerFailure:
            self.powerFailureWidget.setIcon(QtGui.QIcon(redXImage))
        else:
            self.powerFailureWidget.setIcon(QtGui.QIcon(checkImage))

    #toggleTrackFailure toggles the value of trackFailure and notifies the CTC office
    #Inputs: No inputs
    #Return: No return values
    def toggleTrackFailure(self) -> None:
        self.trackFailure = not self.trackFailure
        self.wayside.sendErrorToCTC(self.blockNum, "Track Failure", self.trackFailure)
        #Update GUI
        if self.trackFailure:
            self.trackFailureWidget.setIcon(QtGui.QIcon(redXImage))
        else:
            self.trackFailureWidget.setIcon(QtGui.QIcon(checkImage))

    #toggleCircuitFailure toggles the value of circuitFailure and notifies the CTC office
    #Inputs: No inputs
    #Return: No return values
    def toggleCircuitFailure(self) -> None:
        self.circuitFailure = not self.circuitFailure
        self.wayside.sendErrorToCTC(self.blockNum, "Circuit Failure", self.circuitFailure)
        #Update GUI
        if self.circuitFailure:
            self.circuitFailureWidget.setIcon(QtGui.QIcon(redXImage))
        else:
            self.circuitFailureWidget.setIcon(QtGui.QIcon(checkImage))

    #toggleSwitchFailure toggles the value of switchFailure and notifies the CTC office
    #Inputs: No inputs
    #Return: No return values
    def toggleSwitchFailure(self) -> None:
        #Update Model
        self.switchFailure = not self.switchFailure
        if self.hasSwitch():
            self.wayside.sendErrorToCTC(self.blockNum, "Switch Failure", self.switchFailure)
        #Update GUI
        if self.switchFailure:
            self.switchFailureWidget.setIcon(QtGui.QIcon(redXImage))
        else:
            self.switchFailureWidget.setIcon(QtGui.QIcon(checkImage))

    #setSuggestedSpeed updates the stored value of suggestedSpeed of the block
    #Inputs: suggestedSpeed: int indicating the suggested speed of the block
    #Return: No return value
    def setSuggestedSpeed(self, suggestedSpeed: int) -> None:
        self.suggestedSpeed = suggestedSpeed
    
    #setAuthority updates the stored value of authority of the block
    #Inputs: authority: boolean indicating the authority of the block
    #Return: No return value
    def setAuthority(self, authority: bool) -> None:
        self.authority = authority
    
    #updateTrackCircuit updates the value of the track circuit based on new authority and suggested speed
    #Inputs: No inputs
    #Return: No return value
    def updateTrackCircuit(self) -> None:
        #if power failure, floor all values
        if self.powerFailure:
            authority = False
            speed = 0
            circuit = "0b000000000000"
        #If track circuit failure, random values
        elif self.circuitFailure:
            authority = False
            speed = randrange(0,127)
            circuit = format(randrange(0,1023), '#014b')
        #Else funcitoning correctly
        else:
            authority = self.authority
            speed = self.suggestedSpeed
            circuit = "0b1"
            if authority:
                circuit = circuit + "111"
            else:
                circuit = circuit + "000"
            circuit = circuit + format(speed, '08b')
        
        self.trackCircuit = circuit.encode()
        
        #Update GUI
        self.authorityWidget.setText(str(authority))
        self.speedWidget.setText("{} = {:.2f} mph".format(speed, speed*0.621371))
        self.binaryWidget.setText(circuit)

    #getNextBlock updates the Track Model and the Train Model any time a train leaves a block
    #Inputs: train: a pointer to the train object that is leaving the block
    #Return: No return value
    def getNextBlock(self, train: 'Train') -> None:
        #find the next block that the train is going to
        previous = train.get("lastBlock")
        #nextBlock = self.defaultConnection
        for block in self.connections:
            if block[2] and block[3] and (block[0] != previous):
                nextBlock = block[0]
                break
        
        #If no available connenction exists, force quit
        if not "nextBlock" in locals():
            self.trackModel.errorSignal.emit("Track Connenction Error: a train attempted to leave block {} after entering from block {}.\nNo block was connected, so the train was unable to continue.\nThere are many reasons why this may occur.\nPlease see section 4.6 of the User Manual for possible reasons.".format(self.blockNum, previous))
            while(True): sleep(1)

        
        #update wayside and block occupancies
        self.occupied = None
        if self.station is not None:
            self.station.departing()

        self.wayside.relayTrackOccupancy(self.blockNum, nextBlock)
        train.set("currentBlock", nextBlock)
        train.set("lastBlock", self.blockNum)
        #update using next block's values
        self.trackModel.getBlock(nextBlock).addOccupancy(train)

        #update GUI Widgets
        self.occupiedWidget.setText("No")
    
    #addOccupancy updates the Track Model and Train Model any time that a train enters a new block
    #Inputs: train: a pointer to the train object that is now occupying this block of track
    #Return: No return values
    def addOccupancy(self, train: 'Train') -> None:
        #update block values
        self.occupied = train
        if self.station is not None:
            self.station.occupy()

        #update physical awareness info on train
        train.set("trackLength", self.length)
        train.set("trackGrade", self.grade)
        train.set("trackElevation", self.elevation)
        #send beacon to train. If there is no beacon on this block, send an empty string to indicate no beacon
        train.sendBeaconData(self.getBeacon())

        #update GUI Widgets
        self.setConnectionWidgets()
        self.occupiedWidget.setText("Yes")

    #update updates the block and the attached station (if it exists) based on the passage of time
    #update also relays authority and suggestedSpeed via the Track Circuit
    #Inputs: No inputs
    #Return: No return values
    def update(self) -> None:
        #Don't update the Yard
        if self.blockNum == 0:
            return
        
        self.inputs.update()
        self.updateTrackCircuit()
        if self.occupied is not None:
            self.occupied.setTrackCircuit(self.trackCircuit)
        if self.station is not None:
            self.station.update()

    #getBlockNum takes no inputs and returns the value of blockNum
    def getBlockNum(self) -> int:
        return self.blockNum
    
    #getLength takes no inputs and returns the value of length
    def getLength(self) -> float:
        return self.length
    
    #getElevation takes no inputs and returns the value of elevation
    def getElevation(self) -> float:
        return self.elevation

    #getGrade takes no inputs and returns the value of grade
    def getGrade(self) -> float:
        return self.grade
    
    #getSpeedLimit takes no inputs and returns the value of speedLimit
    def getSpeedLimit(self) -> int:
        return self.speedLimit
    
    #getSwitchState determines if a switch on the block is in the standard position
    #Inputs: No inputs
    #Return: boolean indicating whether a switch is in the default connection
    def getSwitchState(self) -> bool:
        for connection in self.connections:
            if connection[0] == self.defaultConnection:
                return (connection[3] and connection[2])
        return True
    
    #getLighting takes no inputs and returns the value of lighting
    def getLighting(self) -> bool:
        return self.lighting
    
    #getHeated takes no inputs and returns the value of heated
    def getHeated(self) -> bool:
        return self.heated
    
    #getCrossLights takes no inputs and returns the value of crossLights
    def getCrossLights(self) -> bool:
        return self.crossLights
    
    #getOccupied takes no inputs and returns a boolean indicating if a train is on this block of track
    def getOccupied(self) -> bool:
        return self.occupied is not None

    #getSwitchLight takes no inputs and returns the value of switchLight
    def getSwitchLight(self) -> str:
        return self.switchLight
    
    #getBeacon takes no inputs and returns the value of beacon
    def getBeacon(self) -> str:
        return self.beacon

    #getTemperature takes no inputs and returns the value of temperature
    def getTemperature(self) -> int:
        return self.temperature

    #getPowerFailure takes no inputs and returns the value of powerFailure
    def getPowerFailure(self) -> bool:
        return self.powerFailure
    
    #getTrackFailure takes no inputs and returns the value of trackFailure
    def getTrackFailure(self) -> bool:
        return self.trackFailure
    
    #getCircuitFailure takes no inputs and returns the value of circuitFailure
    def getCircuitFailure(self) -> bool:
        return self.circuitFailure
    
    #getSwitchFailure takes no inputs and returns the value of switchFailure
    def getSwitchFailure(self) -> bool:
        return self.switchFailure

    #getStation has no inputs and returns a pointer to the station
    #if this block has no station, it returns None
    def getStation(self) -> 'Station':
        return self.station

class Station:
    #Constants
    block: Block
    name: str
    stationSide: str

    #Changing values
    ticketsSold: int
    occupied: bool
    boarding: int
    disembarking: int

    #Gui Widgets that need updating
    ticketSalesWidget: QtWidgets.QLabel
    occupiedWidget: QtWidgets.QLabel
    boardingWidget: QtWidgets.QLabel
    disembarkingWidget: QtWidgets.QLabel

    #__init__ initializes the station based on a preset configuration
    #Inputs: station: a dictionary from a line config file describing the station
    #        block: a pointer to the block that the station is connected to
    #Return: No return values
    def __init__(self, station: dict, block : Block) -> None:
        #intialize pointer
        self.block = block

        #initialize default values from config and constants
        self.name = station['name']
        self.ticketsSold = 0
        self.stationSide = station['side']
        self.occupied = False
        self.boarding = 0
        self.disembarking = 0

        #initialize changing widgets
        self.ticketSalesWidget = QtWidgets.QLabel("0")
        self.occupiedWidget = QtWidgets.QLabel("No")
        self.boardingWidget = QtWidgets.QLabel("0")
        self.disembarkingWidget = QtWidgets.QLabel("0")

        #initialize ticket sales
        self.sellTickets()
    
    #occupy updates the station that a train is entering, but has not yet stopped at
    #Inputs: No inputs
    #Return: No return values
    def occupy(self) -> None:
        #update instance variables
        self.occupied = True
        self.boarding = randrange(0, self.ticketsSold + 1)
        self.ticketsSold = self.ticketsSold - self.boarding

        #update gui
        self.occupiedWidget.setText("Yes")
        self.boardingWidget.setText(str(self.boarding))
        self.ticketSalesWidget.setText(str(self.ticketsSold))

    #departing updates the station that a train is leaving from
    #Inputs: No inputs
    #Return: No return values
    def departing(self) -> None:
        #update instance variables
        self.occupied = False
        self.boarding = 0
        self.disembarking = 0

        #update tickets
        self.sellTickets()        

        #update gui
        self.occupiedWidget.setText("No")
        self.boardingWidget.setText("0")
        self.disembarkingWidget.setText("0")

    #sellTickets updates the number of tickets sold by a random amount
    #Inputs: No inputs
    #Return: No return values
    def sellTickets(self) -> None:
        #Sell a random number of tickets
        self.ticketsSold = self.ticketsSold + randrange(5, 26)
        #update gui
        self.ticketSalesWidget.setText(str(self.ticketsSold))
    
    #exchangePassengers communicates with a train to exchange passengers boarding and disembarking
    #Inputs: train: a pointer to the train to be exchanged with
    #return: No return values
    def exchangePassengers(self, train: 'Train') -> None:
        #get passengers from train and give passengers boarding
        self.disembarking = train.exchangePassengers(self.boarding)

        #update gui
        self.disembarkingWidget.setText(str(self.disembarking))
    
    #update updates the values of the station based on the passage of time
    #Inputs: No inputs
    #Return: No return values
    def update(self) -> None:
        pass

    #getName takes no inputs and returns the name of the station
    def getName(self) -> str:
        return self.name

    #getSide takes no inputs and returns the side of the tracks that the station is on
    def getSide(self) -> str:
        return self.stationSide
    
    #getBoarding takes no inputs and returns the number of passengers boarding
    def getBoarding(self) -> int:
        return self.boarding
    
    #getDisembarking takes no inputs and returns the number of passengers disembarking
    def getDisembarking(self) -> int:
        return self.disembarking

    #getTicketsSold takes no inputs and returns the number of tickets sold
    def getTicketsSold(self) -> int:
        return self.ticketsSold

class Input:
    block: Block
    train: 'TrainModelInterface'
    wayside: 'WaysideController'
    started: bool

    def __init__(self, block: Block):
        self.block = block
        self.train = TrainModelInterface(block)
        self.wayside = WaysideController(block)
        self.started = False
    
    def start(self):
        try:
            self.block.wayside.sendErrorToCTC(self.block.blockNum, "Power Failure", True)
        except:
            pass
        self.block.setTrainModel(self.train)
        self.block.setWayside(self.wayside)
        self.wayside.powerFailure = self.block.powerFailure
        self.wayside.trackFailure = self.block.trackFailure
        self.wayside.circuitFailure = self.block.circuitFailure
        self.wayside.switchFailure = self.block.switchFailure
        self.wayside.setErrorWidgets()
        self.started = True
    
    def update(self):
        if self.started:
            self.train.update()
            self.wayside.update()

class WaysideController:
    occupied: bool

    commandedSpeed: int
    authority: bool

    powerFailure: bool
    trackFailure: bool
    circuitFailure: bool
    switchFailure: bool

    occupiedWidget: QtWidgets.QLabel
    speedWidget: QtWidgets.QLabel
    authorityWidget: QtWidgets.QLabel
    powerFailWidget: QtWidgets.QLabel
    trackFailWidget: QtWidgets.QLabel
    circuitFailWidget: QtWidgets.QLabel
    switchFailWidget: QtWidgets.QLabel

    def __init__(self, block : Block) -> None:
        self.block = block
        self.occupied = False
        self.commandedSpeed = 30
        self.authority = 1.0

        self.powerFailure = False
        self.trackFailure = False
        self.circuitFailure = False
        self.switchFailure = False

        self.occupiedWidget = QtWidgets.QLabel("No")
        self.speedWidget = QtWidgets.QLabel("30")
        self.authorityWidget = QtWidgets.QLabel("True")
        self.powerFailWidget = QtWidgets.QLabel()
        self.trackFailWidget = QtWidgets.QLabel()
        self.circuitFailWidget = QtWidgets.QLabel()
        self.switchFailWidget = QtWidgets.QLabel()
    
    def update(self) -> None:
        self.block.setSuggestedSpeed(self.commandedSpeed)
        self.block.setAuthority(self.authority)

    def relayTrackOccupancy(self, previous: int, next: int):
        pass
    
    def sendErrorToCTC(self, error: List[str]):
        if error[1] == "Power Failure":
            self.powerFailure = error[2]
        elif error[1] == "Broken Track Failure":
            self.trackFailure = error[2]
        elif error[1] == "Circuit Failure":
            self.circuitFailure = error[2]
        elif error[1] == "Switch Failure":
            self.switchFailure = error[3]
        self.setErrorWidgets()
    
    def setErrorWidgets(self):
        if self.powerFailure:
            self.powerFailWidget.setText("Warning: Power Failure")
        else:
            self.powerFailWidget.setText("")
        if self.powerFailure:
            self.powerFailWidget.setText("Warning: Power Failure")
        else:
            self.powerFailWidget.setText("")
        if self.powerFailure:
            self.powerFailWidget.setText("Warning: Power Failure")
        else:
            self.powerFailWidget.setText("")
        if self.powerFailure:
            self.powerFailWidget.setText("Warning: Power Failure")
        else:
            self.powerFailWidget.setText("")
    
    def toggleOccupied(self) -> None:
        if self.block.station is not None:
            if self.occupied:
                self.block.station.occupy()
                self.occupiedWidget.setText("Yes")
            else:
                self.block.station.departing()
                self.occupiedWidget.setText("No")
        self.occupied = not self.occupied
    
    def lowerCommandedSpeed(self) -> None:
        if self.commandedSpeed != 0:
            self.commandedSpeed = self.commandedSpeed - 1
            self.setSuggestedSpeedWidget()
    
    def raiseCommandedSpeed(self) -> None:
        self.commandedSpeed = self.commandedSpeed + 1
        self.setSuggestedSpeedWidget()
    
    def setSuggestedSpeedWidget(self):
        self.speedWidget.setText(int(self.commandedSpeed))
    
    def toggleAuthority(self) -> None:
        self.authority = not self.authority
    
    def switch(self) -> None:
        self.block.switch()
    
    def setTrackHeating(self, state: bool) -> None:
        if (state != self.block.getHeated()):
            self.block.toggleHeated()
    
    def toggleSwitchLight(self) -> None:
        if self.block.switchLight == "RED":
            self.block.setSwitchLight("GREEN")
        elif self.block.switchLight == "GREEN":
            self.block.setSwitchLight("RED")
    
    def toggleLighting(self) -> None:
        self.block.toggleLighting()
    
    def toggleCrossLights(self) -> None:
        self.block.toggleCrossLights()
    

class TrainModelInterface:
    occupied: bool
    disembarking: int
    boarding: int
    trackCircuit: str

    occupiedWidget: QtWidgets.QLabel
    disembarkingWidget: QtWidgets.QLabel
    boardingWidget: QtWidgets.QLabel
    trackCircuitWidget: QtWidgets.QLabel

    def __init__(self, block : Block) -> None:
        self.occupied = False
        self.block = block
        self.disembarking = 0
        self.trackCircuit = "0b00000000000000"

        self.occupiedWidget = QtWidgets.QLabel("No")
        self.disembarkingWidget = QtWidgets.QLabel("0")
        self.boardingWidget = QtWidgets.QLabel("0")
        self.trackCircuitWidget = QtWidgets.QLabel(self.trackCircuit)
    
    def update(self) -> None:
        pass
    
    def toggleOccupancy(self) -> None:
        if self.block.getOccupied():
            self.block.getNextBlock(self)
            self.occupiedWidget.setText("No")
        else:
            self.block.addOccupancy(self)
            self.occupiedWidget.setText("Yes")

    def lowerDisembarking(self) -> None:
        if self.disembarking != 0:
            self.disembarking = self.disembarking - 1
        self.disembarkingWidget.setText(str(self.disembarking))
    
    def raiseDisembarking(self) -> None:
        self.disembarking = self.disembarking + 1
        self.disembarkingWidget.setText(str(self.disembarking))

    def exchangePassengers(self, boarding: int) -> None:
        self.boarding = boarding
        self.boardingWidget.setText(str(self.boarding))
        return self.disembarking
    
    def startExchange(self) -> None:
        self.block.getStation().exchangePassengers(self)

    def set(self, name: str, val: str) -> None:
        pass

    def get(self, name: str):
        if name == "lastBlock":
            return 0

    def sendBeaconData(self, data: str) -> None:
        pass

    def setTrackCircuit(self, data: bytes) -> None:
        self.trackCircuit = data.decode()
        self.trackCircuitWidget.setText(self.trackCircuit)

class Train(TrainModelInterface):
    def __init__(self):
        TrainModelInterface.__init__()