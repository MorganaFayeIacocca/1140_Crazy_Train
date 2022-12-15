import os
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDir

#PLCCompiler stores a filename and executes file when WaysideController is updated
#File determines switch, traffic light, tunnel light, and crossbar positions
#File can shall only contain boolean vars
class PLCCompiler(QWidget):
    #initialize PLCCompiler
    #Inputs: WaysideController (pointer to wayside that PLC commands), string (name of default file to be loaded into PLC)
    def __init__(self,contrPtr,filename):
        super().__init__()
        self.controllerPtr = contrPtr
        cwd = os.getcwd()
        filestr = '/PLC Files/' + filename + '.txt'
        dir = QDir(str(cwd))
        cwd = dir.currentPath()
        self.plcFile = str(cwd+filestr)

    #getFileFromUpload() - Allows user to select existing text file and upload to PLC
    #Inputs: None
    #Outputs: None
    def getFileFromUpload(self):
        # prompt user to select a file from file system
        filepath = QFileDialog.getOpenFileName(self, 'Upload PLC file',
                                            'c:\\', "Text files (*.txt)")
        self.plcFile = filepath[0]
        self.execFile()

    #execFile() - Execute instructions in a PLC File - computes each instruction 3 times to implement TMR with a voting system
    #Inputs: None
    #Output: None
    def execFile(self):
        if self.plcFile == None or self.plcFile == "" or self.controllerPtr.maintenance:
            return
        fileContents = open(self.plcFile, "r")
        for x in fileContents:
            # split string into instruction blocks
            instructions = x.split()
            if self.plcFile == None:
                return
            if instructions[0] == "STC":
                crossVal = self.storeCross(instructions)
                crossVal2 = self.storeCross(instructions)
                crossVal3 = self.storeCross(instructions)
                if(crossVal and crossVal2)or(crossVal and crossVal3)or(crossVal2 and crossVal3):
                    crossVal = True
                else:
                    crossVal = False
                currVal = self.controllerPtr.trackModel.getBlock(self.controllerPtr.cross).getCrossLights()
                if(crossVal!=currVal):
                    self.controllerPtr.trackModel.getBlock(self.controllerPtr.cross).toggleCrossLights()
            elif instructions[0] == "STS":
                switchVal = self.storeSwitch(instructions,2)
                switchVal2 = self.storeSwitch(instructions,2)
                switchVal3 = self.storeSwitch(instructions,2)
                if (switchVal and switchVal2) or (switchVal and switchVal3) or (switchVal2 and switchVal3):
                    switchVal = True
                else:
                    switchVal = False
                self.controllerPtr.switchPos = switchVal
                prevState = self.controllerPtr.trackModel.getBlock(int(instructions[1])).getSwitchState()
                if switchVal != prevState:
                    self.controllerPtr.trackModel.getBlock(int(instructions[1])).switch()
            elif instructions[0] == "STL":
                lightVal = self.storeTrafficLight(instructions,2)
                lightVal2 = self.storeTrafficLight(instructions,2)
                lightVal3 = self.storeTrafficLight(instructions,2)
                if (lightVal and lightVal2) or (lightVal and lightVal3) or (lightVal2 and lightVal3):
                    lightVal = True
                else:
                    lightVal = False
                if lightVal:
                    self.controllerPtr.trackModel.getBlock(int(instructions[1])).setSwitchLight('GREEN')
                    self.controllerPtr.lightStatus[int(instructions[1])] = 'GREEN'
                else:
                    self.controllerPtr.trackModel.getBlock(int(instructions[1])).setSwitchLight('RED')
                    self.controllerPtr.lightStatus[int(instructions[1])] = 'RED'
            elif instructions[0] == "STU":
                tunnelVal = self.storeTunnelLight(instructions)
                tunnelVal2 = self.storeTunnelLight(instructions)
                tunnelVal3 = self.storeTunnelLight(instructions)
                if (tunnelVal and tunnelVal2) or (tunnelVal and tunnelVal3) or (tunnelVal2 and tunnelVal3):
                    tunnelVal = True
                else:
                    tunnelVal = False
                self.controllerPtr.tunnelLightStatus = tunnelVal
                for block in self.controllerPtr.tunnelList:
                    currVal = self.controllerPtr.trackModel.getBlock(block).getLighting()
                    if currVal != tunnelVal:
                        self.controllerPtr.trackModel.getBlock(block).toggleLighting()
            else:
                self.displayError(x)
                self.plcFile = None
        fileContents.close()

    #storeSwitch() - determines switch position based on occupancy
    #Inputs: string[] containing instruction line broken up into components, int giving the start index
    #Outputs: returns true if switch should be in default position, false otherwise
    #This function is recursive so the index will change each time the function is called recursively
    def storeSwitch(self,instructions,index):
        if instructions[index][0] != '!':
            tempBool = self.controllerPtr.blockOcc.get(int(instructions[index]))
        else:
            blockIndex = int(instructions[index][1:])
            tempBool = not self.controllerPtr.blockOcc.get(blockIndex)

        #if we have reached the end of the array, do this
        if (len(instructions) - 1) == index:
            return tempBool

        #the way this program is written, it is as if there are parentheses around the last components
        #Ex: The PLC command 1 AND 2 AND 3 OR 4 is treated as (1 AND (2 AND (3 AND 4)))
        if instructions[index+1] == "AND":
            return (tempBool and self.storeSwitch(instructions,index + 2))
        elif instructions[index+1] == "OR":
            return (tempBool or self.storeSwitch(instructions, index + 2))
        else:
            s = ' '
            s = s.join(instructions)
            self.displayError('s')
            self.plcFile = None

    #storeTrafficLight() - determine status of individual traffic light (RED or GREEN) based on occupancy
    #Inputs: string[] (containing a line of instructions broken up into components), int (giving the starting index)
    #Outputs: bool: true if light is 'GREEN', false if light is 'RED'
    #This function is recursive so the index will change each time the function is called recursively
    def storeTrafficLight(self,instructions,index):
        if instructions[index][0] != '!':
            tempBool = self.controllerPtr.blockOcc.get(int(instructions[index]))
        else:
            blockIndex = int(instructions[index][1:])
            tempBool = not self.controllerPtr.blockOcc.get(blockIndex)

        #if we have reached the end of the array, do this
        if (len(instructions) - 1) == index:
            return tempBool

        # the way this program is written, it is as if there are parentheses around the last components
        # Ex: The PLC command 1 AND 2 AND 3 OR 4 is treated as (1 AND (2 AND (3 AND 4)))
        if instructions[index+1] == "AND":
            return (tempBool and self.storeTrafficLight(instructions,index + 2))
        elif instructions[index+1] == "OR":
            return (tempBool or self.storeTrafficLight(instructions, index + 2))
        else:
            s = ' '
            s = s.join(instructions)
            self.displayError('s')
            self.plcFile = None

    # storeTunnelLight() - determine status of all lights in a tunnel based on occupancy
    # Inputs: string[] (containing a line of instructions broken up into components)
    # Outputs: True if there is a train in the tunnel (lights should be on), False otherwise
    def storeTunnelLight(self,instructions):
        tempBool = False
        startBlock = int(instructions[1])
        endBlock = int(instructions[2])
        #check all blocks in the tunnel - if at least one is occupied, turn on all the lights
        for x in range(startBlock,(endBlock+1)):
            tempBool = tempBool or self.controllerPtr.trackModel.getBlock(x).getOccupied()
        return tempBool

    # storeCross() - determine status of crossbar (up or down) and crossing lights (on or off) based on occupancy
    # Inputs: string[] (containing a line of instructions broken up into components)
    # Outputs: True if there is a train on the crossing block or on the block immediately before or after, False otherwise
    def storeCross(self,instructions):
        tempBool = False
        startBlock = int(instructions[1])
        endBlock = int(instructions[2])
        # check block before, block with crossbar, and block after
        for x in range(startBlock, (endBlock + 1)):
            tempBool = tempBool or (self.controllerPtr.blockOcc.get(int(x))>0)
        return tempBool

    def displayError(self, instructions):
        #Initialize Window Dimensions and Title
        redLight = "TrackModelModule/redLight.jpg"
        self.err = QWidget()
        self.err.setWindowTitle('Error Message')
        #Add widgets
        layout = QGridLayout()
        #Error symbol
        errorSymbol = QLabel()
        pixmap = QtGui.QPixmap(redLight)
        errorSymbol.setPixmap(pixmap)
        layout.addWidget(errorSymbol,0,0)

        #Error message
        errorWidget = QLabel("This file is invalid.\nPlease create a file using the style specified by the User Manual.\nOnly Boolean variables are allowed\nThe invalid line is:")
        errorWidget.setFont(QtGui.QFont("Arial", 20))
        layout.addWidget(errorWidget,0,1)

        #display line which caused the error
        errorLineWidget = QLabel(instructions)
        errorLineWidget.setFont(QtGui.QFont("Arial", 20))
        layout.addWidget(errorLineWidget, 2, 1)

        #close button
        closeButton = QPushButton("OK")
        closeButton.clicked.connect(self.err.close)
        layout.addWidget(closeButton,3,2,QtCore.Qt.AlignRight)

        #Finalize layout
        self.err.setLayout(layout)
        self.err.show()