from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QTableWidget,QTableWidgetItem
from PyQt5.QtWidgets import QComboBox,QSpinBox, QCheckBox,QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush

#GUI Class for WaysideController Objects
class WaysideControllerGUI(QWidget):
    #Initialize WaysideControllerGUI
    #Inputs: WaysideController ptr, function to go back to the WaysideControllerGroupGUI
    #Outputs: None
    def __init__(self, wcPtr, backFunc):
        super().__init__()
        self.testUI = WaysideControllerTestGUI(wcPtr, self)
        self.testUIButton = QPushButton("Go To Test UI")
        self.testUIButton.clicked.connect(self.showTestUI)
        self.controllerPtr = wcPtr
        self.controllerPtr.groupPtr.controllerDispGUI = self

        # init app window
        self.setWindowTitle('Wayside Controller')

        layout = QVBoxLayout()
        miscLayout = QHBoxLayout()

        # init back button and add to misc layout
        backButton = QPushButton('Back to Wayside Menu')
        backButton.clicked.connect(backFunc)
        miscLayout.addWidget(backButton)

        # init Tracks table
        self.trackTable = QTableWidget(len(self.controllerPtr.blockList), 9)
        self.trackTable.setEnabled(False)
        trackHeaders = ['Block Number', 'Occupancy', 'Switch Position', 'Light Status', 'Maintenance', 'Broken Rail', 'Switch Failure', 'Power Failure',
                        'Circuit Failure']
        nullRowHeaders = ['', '', '', '', '', '', '', '', '', '', '', '', '', '','']
        self.trackTable.setHorizontalHeaderLabels(trackHeaders)
        self.trackTable.setVerticalHeaderLabels(nullRowHeaders)

        self.lightLayout = QHBoxLayout()
        self.lightLabel = QLabel("Lighting: ")
        self.lightStatus = QLabel()
        self.lightLayout.addWidget(self.lightLabel)
        self.lightLayout.addWidget(self.lightStatus)

        self.crossingLayout = QHBoxLayout()
        self.crossingLabel = QLabel("Crossbar: ")
        self.crossingStatus = QLabel()
        self.crossingLayout.addWidget(self.crossingLabel)
        self.crossingLayout.addWidget(self.crossingStatus)

        # set data in table
        self.updateGUI()

        # init PLC Buttons
        buttonLayout = QHBoxLayout()
        self.loadButton = QPushButton('Load PLC File')
        buttonLayout.addWidget(self.loadButton)
        self.loadButton.clicked.connect(self.getFileFromUpload)

        #add testUIButton to miscLayout
        miscLayout.addWidget(self.testUIButton)

        # init window layout and add sub-layouts
        windowLayout = QVBoxLayout(self)
        windowLayout.addLayout(miscLayout)
        windowLayout.addWidget(self.trackTable)
        windowLayout.addLayout(self.lightLayout)
        windowLayout.addLayout(self.crossingLayout)
        windowLayout.addLayout(buttonLayout)
        self.setLayout(layout)

    #switchControllers(): Change the controllers for the PLCCompiler and ControllerPtr that belong to the GUI and update GUI accordingly
    #Inputs: int - index of WaysideController to be displayed on the GUI
    def switchControllers(self, value):
        self.controllerPtr.compiler.controllerPtr = self.controllerPtr.groupPtr.waysideDict[value]
        self.controllerPtr = self.controllerPtr.groupPtr.waysideDict[value]
        self.controllerPtr.update()

    #showTestUI(): Displays Test UI for Wayside Controller - connects to testUI button
    #No Inputs or Outputs
    def showTestUI(self):
        self.testUI.show()

    #updateGUI() - Update GUI attributes and Track Table
    #No Inputs or Outputs
    def updateGUI(self):
        count = 0
        for x in self.controllerPtr.blockList:
            rowNum = QTableWidgetItem(str(x))
            occButton = QTableWidgetItem()
            occ = self.controllerPtr.trackModel.getBlock(x).getOccupied()
            if occ:
                occButton.setCheckState(Qt.Checked)
            else:
                occButton.setCheckState(Qt.Unchecked)

            if x == self.controllerPtr.switchBlock:
                if self.controllerPtr.switchPos:
                    if self.controllerPtr.defaultPos:
                        switchPos = QTableWidgetItem('Curved')
                    else:
                        switchPos = QTableWidgetItem('Straight')
                else:
                    if self.controllerPtr.defaultPos:
                        switchPos = QTableWidgetItem('Straight')
                    else:
                        switchPos = QTableWidgetItem('Curved')
            else:
                switchPos = QTableWidgetItem('None')

            #Set text color to allow another method of indicating light status
            textColorGreen = QBrush(Qt.green)
            textColorRed = QBrush(Qt.red)
            # set data in table
            if (self.controllerPtr.lightList != None) and (x in self.controllerPtr.lightList):
                if self.controllerPtr.lightStatus[x]=='GREEN':
                    lightStatus = QTableWidgetItem('GREEN')
                    lightStatus.setForeground(textColorGreen)
                elif self.controllerPtr.lightStatus[x]=='RED':
                    lightStatus = QTableWidgetItem('RED')
                    lightStatus.setForeground(textColorRed)
            else:
                lightStatus = QTableWidgetItem('NONE')

            if self.controllerPtr.maintenanceBlocks[x]:
                maintenanceMode = QTableWidgetItem('ON')
            else:
                maintenanceMode = QTableWidgetItem('OFF')

            if self.controllerPtr.railFail[x]:
                railFail = QTableWidgetItem('FAILED')
                railFail.setForeground(textColorRed)
            else:
                railFail = QTableWidgetItem()

            if self.controllerPtr.switchFail[x]:
                switchFail = QTableWidgetItem('FAILED')
                switchFail.setForeground(textColorRed)
            else:
                switchFail = QTableWidgetItem()

            if self.controllerPtr.powerFail[x]:
                powerFail = QTableWidgetItem('FAILED')
                powerFail.setForeground(textColorRed)
            else:
                powerFail = QTableWidgetItem()

            if self.controllerPtr.circuitFail[x]:
                circuitFail = QTableWidgetItem('FAILED')
                circuitFail.setForeground(textColorRed)
            else:
                circuitFail = QTableWidgetItem()

            self.trackTable.setItem(count, 0, rowNum)
            self.trackTable.setItem(count, 1, occButton)
            self.trackTable.setItem(count, 2, switchPos)
            self.trackTable.setItem(count, 3, lightStatus)
            self.trackTable.setItem(count, 4, maintenanceMode)
            self.trackTable.setItem(count, 5, railFail)
            self.trackTable.setItem(count, 6, switchFail)
            self.trackTable.setItem(count, 7, powerFail)
            self.trackTable.setItem(count, 8, circuitFail)
            count = count + 1
        if self.controllerPtr.tunnelLightStatus:
            self.lightStatus.setText("ON")
        else:
            self.lightStatus.setText("OFF")

        if self.controllerPtr.cross >= 0:
            if self.controllerPtr.trackModel.getBlock(self.controllerPtr.cross).getCrossLights():
                self.crossingStatus.setText("DOWN")
            else:
                self.crossingStatus.setText("UP")
        else:
            self.crossingStatus.setText("NONE")

        self.testUI.updateGUI()

    #getFileFromUpload() - gets PLC file that the user uploads - connects to Upload PLC File button
    #No Inputs or Outputs
    def getFileFromUpload(self):
        self.controllerPtr.compiler.getFileFromUpload()
        self.updateGUI()

#Test UI class for the Wayside Controller
class WaysideControllerTestGUI(QWidget):
    #Initialize Test UI
    #Inputs: WaysideController ptr, WaysideControllerGUI ptr
    #Outputs: None
    def __init__(self,wcPtr, guiPtr):
        super().__init__()
        layout = QVBoxLayout()
        self.controllerPtr = wcPtr
        self.GUIPtr = guiPtr

        # init app window
        self.setWindowTitle('Wayside Controller Test UI')

        miscLayout = QHBoxLayout()

        # init suggested speed and add to misc layout
        suggSpeedLabel = QLabel('Suggested Speed')
        self.suggSpeedSBox = QSpinBox()
        miscLayout.addWidget(suggSpeedLabel)
        miscLayout.addWidget(self.suggSpeedSBox)

        # init suggested speed block num and add to misc layout
        suggSpeedBlockLabel = QLabel('Block Number')
        self.suggSpeedBlock = -1
        self.speedBlockCBox = QComboBox()
        for x in self.controllerPtr.blockList:
            self.speedBlockCBox.addItem(str(x))
        miscLayout.addWidget(suggSpeedBlockLabel)
        miscLayout.addWidget(self.speedBlockCBox)

        # init enter speed button and add to misc layout
        sendSpeedButton = QPushButton('Send Speed')
        sendSpeedButton.clicked.connect(self.transmitSpeed)
        miscLayout.addWidget(sendSpeedButton)

        # init authority and add to misc layout
        self.authCBox = QCheckBox('Authority')
        miscLayout.addWidget(self.authCBox)

        # init authority block number and add to misc layout
        authBlockLabel = QLabel('Block Number')
        self.authBlock = -1
        self.authBlockCBox = QComboBox()
        for x in self.controllerPtr.blockList:
            self.authBlockCBox.addItem(str(x))
        miscLayout.addWidget(authBlockLabel)
        miscLayout.addWidget(self.authBlockCBox)

        # init close test UI button and add to misc layout
        sendAuthButton = QPushButton('Send Authority')
        sendAuthButton.clicked.connect(self.transmitAuthority)
        miscLayout.addWidget(sendAuthButton)

        # init Track Heating and add to misc layout
        self.trackHeatCBox = QCheckBox('Heat Tracks')
        miscLayout.addWidget(self.trackHeatCBox)

        # init close test UI button and add to misc layout
        exitTestUIButton = QPushButton('Close Test UI')
        exitTestUIButton.clicked.connect(self.hide)
        miscLayout.addWidget(exitTestUIButton)

        # init Tracks table
        self.testTrackTable = QTableWidget(len(self.controllerPtr.blockList), 7)
        self.testTrackTable.cellClicked.connect(self.trackStatusChanged)
        trackHeaders = ['Block Number', 'Occupancy', 'Maintenance', 'Broken Rail', 'Switch Failure', 'Power Failure', 'Circuit Failure']
        nullRowHeaders = ['', '', '', '', '', '', '', '', '', '', '', '', '', '','', '']  # init null row headers for tables
        self.testTrackTable.setHorizontalHeaderLabels(trackHeaders)
        self.testTrackTable.setVerticalHeaderLabels(nullRowHeaders)

        # set data in table
        self.updateGUI()

        # init window layout and add sub-layouts
        windowLayout = QVBoxLayout(self)
        windowLayout.addLayout(miscLayout)
        windowLayout.addWidget(self.testTrackTable)

        self.label = QLabel(" Wayside Test UI")
        layout.addWidget(self.label)
        self.setLayout(layout)

    #transmitSpeed() - called when speed enter button is clicked - used to relay suggested speed
    #No Inputs or Outputs
    def transmitSpeed(self):
        self.updateAttr()
        self.controllerPtr.groupPtr.relaySuggSpeed(self.suggSpeedBlock, self.controllerPtr.suggSpeed)

    # transmitAuthority() - called when authority enter button is clicked - used to relay authority
    # No Inputs or Outputs
    def transmitAuthority(self):
        self.updateAttr()
        self.controllerPtr.groupPtr.relayAuthority(self.authBlock, self.controllerPtr.authority)

    #trackStatusChanged() - called when an item in the track table is changes - used to update WaysideControllerGUI
    #Inputs: None
    #Outputs: None
    def trackStatusChanged(self):
        count = 0
        for i in self.controllerPtr.blockList:
            occ = self.testTrackTable.item(count, 1).checkState()
            if occ == 2:
                self.controllerPtr.blockOcc[i] = True
            else:
                self.controllerPtr.blockOcc[i] = False

            maint = self.testTrackTable.item(count,2).checkState()
            self.controllerPtr.maintenanceBlocks[i] = maint

            rail = self.testTrackTable.item(count,3).checkState()
            self.controllerPtr.railFail[i] = rail

            switch = self.testTrackTable.item(count, 4).checkState()
            self.controllerPtr.switchFail[i] = switch

            power = self.testTrackTable.item(count, 5).checkState()
            self.controllerPtr.powerFail[i] = power

            circuit = self.testTrackTable.item(count, 6).checkState()
            self.controllerPtr.circuitFail[i] = circuit

            count = count+1
        self.GUIPtr.controllerPtr.compiler.execFile()
        self.GUIPtr.updateGUI()

    #updateGUI() - Updates test UI trackTable
    #Inputs: None
    #Outputs: None
    def updateGUI(self):
        count = 0
        for x in self.controllerPtr.blockList:
            rowNum = QTableWidgetItem(str(x))
            occButton = QTableWidgetItem()
            if self.controllerPtr.blockOcc[x]:
                occButton.setCheckState(Qt.Checked)
            else:
                occButton.setCheckState(Qt.Unchecked)
            maintButton = QTableWidgetItem()
            if self.controllerPtr.maintenanceBlocks[x]:
                maintButton.setCheckState(Qt.Checked)
            else:
                maintButton.setCheckState(Qt.Unchecked)

            railButton = QTableWidgetItem()
            if self.controllerPtr.railFail[x]:
                railButton.setCheckState(Qt.Checked)
            else:
                railButton.setCheckState(Qt.Unchecked)

            switchButton = QTableWidgetItem()
            if self.controllerPtr.switchFail[x]:
                switchButton.setCheckState(Qt.Checked)
            else:
                switchButton.setCheckState(Qt.Unchecked)

            powerButton = QTableWidgetItem()
            if self.controllerPtr.powerFail[x]:
                powerButton.setCheckState(Qt.Checked)
            else:
                powerButton.setCheckState(Qt.Unchecked)

            circuitButton = QTableWidgetItem()
            if self.controllerPtr.circuitFail[x]:
                circuitButton.setCheckState(Qt.Checked)
            else:
                circuitButton.setCheckState(Qt.Unchecked)

            self.testTrackTable.setItem(count, 0, rowNum)
            self.testTrackTable.setItem(count, 1, occButton)
            self.testTrackTable.setItem(count, 2, maintButton)
            self.testTrackTable.setItem(count, 3, railButton)
            self.testTrackTable.setItem(count, 4, switchButton)
            self.testTrackTable.setItem(count, 5, powerButton)
            self.testTrackTable.setItem(count, 6, circuitButton)
            count = count + 1

    #updateAttr() - updates attributes based on what has been entered into the test ui
    #No Inputs or Outputs
    def updateAttr(self):
        self.controllerPtr.authority = self.authCBox.isChecked()
        self.controllerPtr.suggSpeed = int(self.suggSpeedSBox.text())
        self.controllerPtr.heatTracks = self.trackHeatCBox.isChecked()
        self.authBlock = self.controllerPtr.blockList[self.authBlockCBox.currentIndex()]
        self.suggSpeedBlock = self.controllerPtr.blockList[self.speedBlockCBox.currentIndex()]