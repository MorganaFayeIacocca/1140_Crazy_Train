from WaysideController import WaysideController
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout

#This class serves as a container class, holding and managing all instances of the WaysideController object
class WaysideControllerGroup:

    #initialize WaysideControllerGroup Object - Used in SystemController
    #Inputs: TrackModel, string (denotes red or green line)
    #Outputs: None
    def __init__(self,trackModel, line):
        self.line = line
        self.controllerDisp = None
        self.controllerDispGUI = None
        self.trackModel = trackModel
        self.ctc = None
        self.waysideDict = {}
        self.line = line

        #initialize controllers
        #WaysideController Constructor inputs: List of Blocks controlled by Wayside, TrackModel ptr, Default switch pos (True if default is straight, False otherwise)
        # Block# containing switch (-1 if no switch), list of blocks that have traffic lights, WaysideControllerGroup ptr,
        # Default PLC file to be loaded, list of blocks that are underground, crossbar Block# (-1 if no crossbar)
        if(line=="GREEN"):
            blockList1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
            lightList1 = [1,12,13]
            wayside1 = WaysideController(blockList1, trackModel, True, 13, lightList1, self, "Green_1_PLC", None,-1)
            self.waysideDict[1] = wayside1

            blockList2 = [16,17,18,19,20]
            wayside2 = WaysideController(blockList2, trackModel, True, -1, None, self, "Green_2_PLC", None,19)
            self.waysideDict[2] = wayside2

            blockList3 = [21,22,23,24,25,26,27,28,29,30,31,32,149,150]
            lightList3 = [29,30,150]
            wayside3 = WaysideController(blockList3, trackModel, False, 29, lightList3, self, "Green_3_PLC", None,-1)
            self.waysideDict[3] = wayside3

            blockList4 = [33,34,35,36,37,38,39,40,41,42,43,44,45,46,47]
            tunnelListI = [36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57]
            wayside4 = WaysideController(blockList4, trackModel, False, -1, None, self, "Green_4_PLC", tunnelListI,-1)
            self.waysideDict[4] = wayside4

            blockList5 = [48,49,50,51,25,53,54,55,56,57,58,59,60,61]
            wayside5 = WaysideController(blockList5, trackModel, False, -1, None, self, "Green_5_PLC", tunnelListI,-1)
            self.waysideDict[5] = wayside5

            blockList6 = [62,63,64,65,66,67,68,69,70,71,72,73,74,75]
            wayside6 = WaysideController(blockList6, trackModel, True, -1, None, self, "Green_6_PLC", None,-1)
            self.waysideDict[6] = wayside6

            blockList7 = [76,77,78,79,80,81,82,83,101]
            lightList7 = [76,77,101]
            wayside7 = WaysideController(blockList7, trackModel, True, 77, lightList7, self, "Green_7_PLC", None,-1)
            self.waysideDict[7] = wayside7

            blockList8 = [84,85,86,87,98,99,100]
            lightList8 = [85,86,100]
            wayside8 = WaysideController(blockList8, trackModel, False, 85, lightList8, self, "Green_8_PLC", None,-1)
            self.waysideDict[8] = wayside8

            blockList9 = [88, 89,90,91,92,93,94,95,96,97]
            wayside9 = WaysideController(blockList9, trackModel, False, -1, None ,self, "Green_9_PLC", None,-1)
            self.waysideDict[9] = wayside9

            blockList10 = [102,103,104,105,106,107,108,109,110,111,112,113,114,115,116]
            wayside10 = WaysideController(blockList10, trackModel, True, -1, None, self, "Green_10_PLC", None,-1)
            self.waysideDict[10] = wayside10

            blockList11 = [117,118,119,120,121,122,123,124,125,126,127,128,129,130,131]
            tunnelListW = [122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143]
            wayside11 = WaysideController(blockList11, trackModel, True, -1, None, self, "Green_11_PLC", tunnelListW,-1)
            self.waysideDict[11] = wayside11

            blockList12 = [132,133,134,135,136,137,138,139,140,141,142,143]
            wayside12 = WaysideController(blockList12, trackModel, False, -1, None, self, "Green_12_PLC", tunnelListW,-1)
            self.waysideDict[12] = wayside12

            blockList13 = [144,145,146,147,148]
            wayside13 = WaysideController(blockList13, trackModel, False, -1, None, self, "Green_13_PLC", None,-1)
            self.waysideDict[13] = wayside13

        elif (line == "RED"):
            blockList1 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
            wayside1 = WaysideController(blockList1, trackModel, True, -1, None, self, "Red_1_PLC", None, -1)
            self.waysideDict[1] = wayside1

            blockList2 = [1, 2, 15, 16, 17, 18, 19, 20, 21, 22, 23]
            lightList2 = [1,15,16]
            wayside2 = WaysideController(blockList2, trackModel, True, 16, lightList2, self, "Red_2_PLC", None, -1)
            self.waysideDict[2] = wayside2

            blockList3 = [24, 25, 26, 27, 28, 29, 75, 76]
            lightList3 = [27,28,76]
            tunnelListHOPQRST = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76]
            wayside3 = WaysideController(blockList3, trackModel, False, 27, lightList3, self, "Red_3_PLC", tunnelListHOPQRST, -1)
            self.waysideDict[3] = wayside3

            blockList4 = [30, 31, 32, 33, 34, 35, 36, 72, 73, 74]
            lightList4 = [32,33,72]
            wayside4 = WaysideController(blockList4, trackModel, True, 33, lightList4, self, "Red_4_PLC",tunnelListHOPQRST, -1)
            self.waysideDict[4] = wayside4

            blockList5 = [37, 38, 39, 40, 69, 70, 71]
            lightList5 = [38,39,71]
            wayside5 = WaysideController(blockList5, trackModel, False, 38, lightList5, self, "Red_5_PLC",tunnelListHOPQRST, -1)
            self.waysideDict[5] = wayside5

            blockList6 = [41,42,43,44,45,46,47,48,67,68]
            lightList6 = [43,44,67]
            wayside6 = WaysideController(blockList6, trackModel, True, 44, lightList6, self, "Red_6_PLC", tunnelListHOPQRST, 47)
            self.waysideDict[6] = wayside6

            blockList7 = [49,50,51,52,53,54,55,56,57,64,65,66]
            lightList7 = [52,53,66]
            wayside7 = WaysideController(blockList7, trackModel, False, 52, lightList7, self, "Red_7_PLC", None, -1)
            self.waysideDict[7] = wayside7

            blockList8 = [58,59,60,61,62,63]
            wayside8 = WaysideController(blockList8, trackModel, False, -1, None, self, "Red_8_PLC", None, -1)
            self.waysideDict[8] = wayside8

    #update() - Called by SystemController, updates individual waysideController objects
    #Inputs: None
    #Outputs: None
    def update(self):
        for x in self.waysideDict:
            self.waysideDict[x].update()
        if self.controllerDispGUI:
            self.controllerDispGUI.updateGUI()

    #relaySuggSpeed() - Called by CTC to relay suggested speed to track model
    #Inputs: int (block number), int (suggested speed)
    #Outputs: None
    def relaySuggSpeed(self, blockNum, speed):
        self.trackModel.getBlock(int(blockNum)).setSuggestedSpeed(speed)

    # relayAuthority() - Called by CTC to relay authority to track model
    # Inputs: int (block number), bool (authority)
    # Outputs: None
    def relayAuthority(self, blockNum, authority):
        self.trackModel.getBlock(int(blockNum)).setAuthority(authority)

    # setMaintenanceMode() - Called by CTC to set a block into maintenance mode
    # Inputs: int (index of block), bool (True if entering maintenance mode, False if coming out of maintenance mode)
    # Outputs: None
    def setMaintenanceMode(self, blockNum: int, mode: bool):
        waysidePtr = self.trackModel.getBlock(blockNum).wayside
        waysidePtr.maintenanceBlocks[blockNum] = mode
        if True in waysidePtr.maintenanceBlocks:
            waysidePtr.maintenance = True
        else:
            waysidePtr.maintenance = False

#GUI class for WaysideControllerGroup - allows user to select wayside to view
class WaysideGroupGUI(QWidget):

    #initialize WaysideGroupGUI
    #Inputs: WaysideControllerGroup, function (for showing individual wayside window), function (for showing main screen)
    #Outputs: None
    def __init__(self, controllerGroup, showWayside, showMain):
        super().__init__()

        layout = QVBoxLayout()

        self.groupPtr = controllerGroup
        self.showWaysideController = showWayside

        # allows each controller to get its own version of the function to show controller
        # useful since we do not yet know which controller we want to show
        def makeFunc(k : int):
            def func():
                controllerGroup.controllerDisp = controllerGroup.waysideDict[k]
                showWayside()
            return func

        #add a button to navigate to each wayside controller gui
        for x in controllerGroup.waysideDict:
            button = QPushButton()
            button.setText("Controller " + str(x))
            funcConnect = makeFunc(x)
            button.clicked.connect(funcConnect)
            layout.addWidget(button)

        homeButton = QPushButton('Home')
        homeButton.clicked.connect(showMain)
        layout.addWidget(homeButton)

        self.setLayout(layout)

        self.setGeometry(250, 250, 300, 400)
        self.setWindowTitle("Wayside Menu")