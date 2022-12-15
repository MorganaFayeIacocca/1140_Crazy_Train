from typing import Callable
from math import sqrt
from PyQt5 import QtCore, QtWidgets, QtGui
from TrackModel import TrackModel, Block, Station, Input
from SystemCloser import WarningWindow

trackImage = "TrackModelModule/track.jpg"
stationImage = "TrackModelModule/station.jpg"

class TrackModelWindow(QtWidgets.QWidget):

    def __init__(self, model : TrackModel, showBlock : Callable, showMain : Callable, qtRectangle : QtCore.QRect):
        QtWidgets.QWidget.__init__(self)
        self.move(qtRectangle.topLeft())
        self.setWindowTitle('Track Model')

        layout = QtWidgets.QHBoxLayout()

        buttonsAll = QtWidgets.QGridLayout()

        def makeF(k : int):
            def f():
                BlockWindow.setNextWindowBlock(k)
                showBlock()
            return f
        
        total_buttons = len(model.blocks)
        buttons_wide = int(total_buttons/15)
        for i in range(1, total_buttons, buttons_wide):
            for j in range(buttons_wide):
                k = i+j
                if k >= total_buttons:
                    break
                f = makeF(k)
                button = QtWidgets.QPushButton("Block {}".format(k))
                button.clicked.connect(f)
                buttonsAll.addWidget(button, int(i/buttons_wide), j)
        
        layout.addLayout(buttonsAll)

        layoutRight = QtWidgets.QVBoxLayout()
        layout.addLayout(layoutRight)

        buttonBack = QtWidgets.QPushButton("Show Main")
        buttonBack.clicked.connect(showMain)
        layoutRight.addWidget(buttonBack, alignment=QtCore.Qt.AlignRight)

        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(model.map).scaled(400, 450, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        label.setPixmap(pixmap)
        layoutRight.addWidget(label)

        self.setLayout(layout)

class BlockWindow(QtWidgets.QWidget):
    #Static Variables
    nextBlock: int

    #Instance Variables
    blockNum: int
    block: Block

    def __init__(self, track : TrackModel, showTrackModel : Callable, showMain : Callable, showStation : Callable, qtRectangle : QtCore.QRect):
        QtWidgets.QWidget.__init__(self)

        self.blockNum = BlockWindow.nextBlock

        self.move(qtRectangle.topLeft())
        self.block = track.getBlock(self.blockNum) 
        self.setWindowTitle("Block {}".format(self.block.blockNum))
        mainLayout = QtWidgets.QHBoxLayout()

        layout1 = QtWidgets.QGridLayout()

        label100 = QtWidgets.QLabel("Length")
        label100.setStyleSheet("background-color:#989898")
        label100.setFont(QtGui.QFont("Arial",20))
        layout1.addWidget(label100, 0, 0)
        label110 = QtWidgets.QLabel("Elevation")
        label110.setStyleSheet("background-color:#989898")
        label110.setFont(QtGui.QFont("Arial",20))
        layout1.addWidget(label110, 1, 0)
        label120 = QtWidgets.QLabel("Grade")
        label120.setStyleSheet("background-color:#989898")
        label120.setFont(QtGui.QFont("Arial",20))
        layout1.addWidget(label120, 2, 0)
        label130 = QtWidgets.QLabel("Speed Limit")
        label130.setStyleSheet("background-color:#989898")
        label130.setFont(QtGui.QFont("Arial",20))
        layout1.addWidget(label130, 3, 0)
        label140 = QtWidgets.QLabel("Connected Blocks")
        label140.setStyleSheet("background-color:#989898")
        label140.setFont(QtGui.QFont("Arial",20))
        layout1.addWidget(label140, 4, 0)
        label150 = QtWidgets.QLabel("Adjacent Blocks")
        label150.setStyleSheet("background-color:#989898")
        label150.setFont(QtGui.QFont("Arial",20))
        layout1.addWidget(label150, 5, 0)
        label160 = QtWidgets.QLabel("Occupied")
        label160.setStyleSheet("background-color:#989898")
        label160.setFont(QtGui.QFont("Arial",20))
        layout1.addWidget(label160, 6, 0)
        label170 = QtWidgets.QLabel("Lighting")
        label170.setStyleSheet("background-color:#989898")
        label170.setFont(QtGui.QFont("Arial",20))
        layout1.addWidget(label170, 7, 0)
        label180 = QtWidgets.QLabel("Crossing Lights")
        label180.setStyleSheet("background-color:#989898")
        label180.setFont(QtGui.QFont("Arial",20))
        layout1.addWidget(label180, 8, 0)
        label190 = QtWidgets.QLabel("Heating")
        label190.setStyleSheet("background-color:#989898")
        label190.setFont(QtGui.QFont("Arial",20))
        layout1.addWidget(label190, 9, 0)
        label1100 = QtWidgets.QLabel("Switch Light")
        label1100.setStyleSheet("background-color:#989898")
        label1100.setFont(QtGui.QFont("Arial",20))
        if self.block.switchLight != "NONE":
            layout1.addWidget(label1100, 10, 0)

        label101 = QtWidgets.QLabel("{:.2f} ft.".format(self.block.length*3.28084))
        label101.setFont(QtGui.QFont("Arial", 15))
        layout1.addWidget(label101, 0, 1)
        label111 = QtWidgets.QLabel("{:.2f} ft.".format(self.block.elevation*3.28084))
        label111.setFont(QtGui.QFont("Arial", 15))
        layout1.addWidget(label111, 1, 1)
        label121 = QtWidgets.QLabel("{:.2f}%".format(self.block.grade))
        label121.setFont(QtGui.QFont("Arial", 15))
        layout1.addWidget(label121, 2, 1)
        label131 = QtWidgets.QLabel("{:.2f} mph".format(self.block.speedLimit*0.621371))
        label131.setFont(QtGui.QFont("Arial", 15))
        layout1.addWidget(label131, 3, 1)

        self.label141 = self.block.connectedWidget
        self.label141.setFont(QtGui.QFont("Arial", 15))
        layout1.addWidget(self.label141, 4, 1)
        self.label151 = self.block.adjacentWidget
        self.label151.setFont(QtGui.QFont("Arial", 15))
        layout1.addWidget(self.label151, 5, 1)

        self.label161 = self.block.occupiedWidget
        self.label161.setFont(QtGui.QFont("Arial", 15))
        layout1.addWidget(self.label161, 6, 1)
        self.label171 = self.block.lightingWidget
        self.label171.setFont(QtGui.QFont("Arial", 15))
        layout1.addWidget(self.label171, 7, 1)
        self.label181 = self.block.crossingWidget
        self.label181.setFont(QtGui.QFont("Arial", 15))
        layout1.addWidget(self.label181, 8, 1)
        self.label191 = self.block.heatingWidget
        self.label191.setFont(QtGui.QFont("Arial", 15))
        layout1.addWidget(self.label191, 9, 1)
        self.label1101 = self.block.switchLightWidget
        layout1.addWidget(self.label1101, 10, 1)

        layout2 = QtWidgets.QVBoxLayout()
        label21 = QtWidgets.QLabel("Block {}".format(self.block.blockNum))
        label21.setFont(QtGui.QFont("Arial",30,weight=QtGui.QFont.Bold))
        layout2.addWidget(label21)
        label22 = QtWidgets.QLabel()
        pixmap22 = QtGui.QPixmap(trackImage)
        label22.setPixmap(pixmap22)
        layout2.addWidget(label22)

        layout3 = QtWidgets.QVBoxLayout()
        layout31 = QtWidgets.QGridLayout()
        button312 = QtWidgets.QPushButton("Show Main Menu")
        button312.clicked.connect(showMain)
        layout31.addWidget(button312, 1, 2)
        button311 = QtWidgets.QPushButton("Show Track Model")
        button311.clicked.connect(showTrackModel)
        layout31.addWidget(button311, 0, 2)
        button310 = QtWidgets.QLabel("\t")
        layout31.addWidget(button310, 0, 1)
        def showInputs():
            self.block.inputs.start()
            self.inputWindow = InputWindow(self.block.inputs)
            self.inputWindow.show()
        def showInputWarning():
            self.warningWindow = WarningWindow("Warning: Opening the manual inputs page will disconnect this block from the model.\nThis may cause unpredictable behavior in other modules.\nThis action cannot be undone.", showInputs)
            self.warningWindow.show()
        label312 = QtWidgets.QPushButton("Test Inputs")
        label312.clicked.connect(showInputWarning)
        layout31.addWidget(label312, 2, 0)
        if self.block.station is None:
            label313 = QtWidgets.QLabel("\t\t")
            layout31.addWidget(label313, 3, 0)
        else:
            button313 = QtWidgets.QPushButton("Show Station")
            def f():
                BlockWindow.setNextWindowBlock(self.blockNum)
                showStation()
            button313.clicked.connect(f)
            layout31.addWidget(button313, 3, 0)
        label314 = QtWidgets.QLabel("")
        layout31.addWidget(label314, 2, 1)
        layout3.addLayout(layout31)

        labelFailures = QtWidgets.QLabel("Failures")
        labelFailures.setStyleSheet("background-color:#989898")
        labelFailures.setFont(QtGui.QFont("Arial", 20))
        layout3.addWidget(labelFailures)

        layout32 = QtWidgets.QGridLayout()
        label320 = QtWidgets.QLabel("Power")
        label320.setFont(QtGui.QFont("Arial", 15))
        label320.setAlignment(QtCore.Qt.AlignCenter)
        layout32.addWidget(label320, 1, 0)
        label321 = QtWidgets.QLabel("Track")
        label321.setFont(QtGui.QFont("Arial", 15))
        label321.setAlignment(QtCore.Qt.AlignCenter)
        layout32.addWidget(label321, 1, 1)
        label322 = QtWidgets.QLabel("Circuit")
        label322.setFont(QtGui.QFont("Arial", 15))
        label322.setAlignment(QtCore.Qt.AlignCenter)
        layout32.addWidget(label322, 1, 2)
        label323 = QtWidgets.QLabel("Switch")
        label323.setFont(QtGui.QFont("Arial", 15))
        label323.setAlignment(QtCore.Qt.AlignCenter)
        layout32.addWidget(label323, 1, 3)
        self.button320 = self.block.powerFailureWidget
        self.button321 = self.block.trackFailureWidget
        self.button322 = self.block.circuitFailureWidget
        self.button323 = self.block.switchFailureWidget
        self.button320.setIconSize(QtCore.QSize(60,60))
        self.button321.setIconSize(QtCore.QSize(60,60))
        self.button322.setIconSize(QtCore.QSize(60,60))
        self.button323.setIconSize(QtCore.QSize(60,60))
        layout32.addWidget(self.button320, 0, 0)
        layout32.addWidget(self.button321, 0, 1)
        layout32.addWidget(self.button322, 0, 2)
        layout32.addWidget(self.button323, 0, 3)
        layout3.addLayout(layout32)

        labelTemperature = QtWidgets.QLabel("Temperature")
        labelTemperature.setStyleSheet("background-color:#989898")
        labelTemperature.setFont(QtGui.QFont("Arial", 20))
        layout3.addWidget(labelTemperature)

        layout34 = QtWidgets.QHBoxLayout()
        button340 = QtWidgets.QPushButton("<")
        button340.clicked.connect(self.block.lowerTemperature)
        button340.clicked.connect(self.setTemperature)
        layout34.addWidget(button340)
        self.label340 = QtWidgets.QLabel()
        self.setTemperature()
        self.label340.setAlignment(QtCore.Qt.AlignCenter)
        self.label340.setFont(QtGui.QFont("Arial",15))
        layout34.addWidget(self.label340)
        button341 = QtWidgets.QPushButton(">")
        button341.clicked.connect(self.block.raiseTemperature)
        button341.clicked.connect(self.setTemperature)
        layout34.addWidget(button341)
        label343 = QtWidgets.QLabel("")
        label344 = QtWidgets.QLabel("")
        layout34.addWidget(label343)
        layout34.addWidget(label344)
        layout3.addLayout(layout34)

        labelBeacon = QtWidgets.QLabel("Beacon")
        labelBeacon.setStyleSheet("background-color:#989898")
        labelBeacon.setFont(QtGui.QFont("Arial", 20))
        layout3.addWidget(labelBeacon)

        beaconString = self.block.getBeacon()
        if beaconString == "":
            beaconString = "NONE"
        label35 = QtWidgets.QLabel(beaconString)
        label35.setAlignment(QtCore.Qt.AlignLeft)
        label35.setFont(QtGui.QFont("Arial",15))
        layout3.addWidget(label35)

        labelTrackCircuit = QtWidgets.QLabel("Track Circuit")
        labelTrackCircuit.setStyleSheet("background-color:#989898")
        labelTrackCircuit.setFont(QtGui.QFont("Arial", 20))
        layout3.addWidget(labelTrackCircuit)

        layout35 = QtWidgets.QGridLayout()
        label3501 = QtWidgets.QLabel("Binary: ")
        label3501.setFont(QtGui.QFont("Arial", 15))
        layout35.addWidget(label3501,0,0)
        label3502 = self.block.binaryWidget
        label3502.setFont(QtGui.QFont("Arial", 15))
        layout35.addWidget(label3502,0,1)
        label3510 = QtWidgets.QLabel("Authority: ")
        label3510.setFont(QtGui.QFont("Arial", 15))
        layout35.addWidget(label3510,1,0)
        label3511 = self.block.authorityWidget
        label3511.setFont(QtGui.QFont("Arial", 15))
        layout35.addWidget(label3511,1,1)
        label3512 = QtWidgets.QLabel("Suggested Speed: ")
        label3512.setFont(QtGui.QFont("Arial", 15))
        layout35.addWidget(label3512,2,0)
        label3513 = self.block.speedWidget
        label3513.setFont(QtGui.QFont("Arial", 15))
        layout35.addWidget(label3513,2,1)
        layout3.addLayout(layout35)

        mainLayout.addLayout(layout1)
        mainLayout.addLayout(layout2)
        mainLayout.addLayout(layout3)
        self.setLayout(mainLayout)

    def setTemperature(self) -> None:
        self.label340.setText(str(self.block.getTemperature()) + "°F")
    
    def close(self) -> bool:
        self.block.connectedWidget.setParent(None)
        self.block.adjacentWidget.setParent(None)
        self.block.occupiedWidget.setParent(None)
        self.block.lightingWidget.setParent(None)
        self.block.crossingWidget.setParent(None)
        self.block.heatingWidget.setParent(None)
        self.block.switchLightWidget.setParent(None)
        self.block.powerFailureWidget.setParent(None)
        self.block.trackFailureWidget.setParent(None)
        self.block.circuitFailureWidget.setParent(None)
        self.block.switchFailureWidget.setParent(None)
        self.block.authorityWidget.setParent(None)
        self.block.speedWidget.setParent(None)
        self.block.binaryWidget.setParent(None)
        return QtWidgets.QWidget.close(self)

    @staticmethod
    def setNextWindowBlock(blockNum: int) -> None:
        BlockWindow.nextBlock = blockNum

class StationWindow(QtWidgets.QWidget):
    #Static variables

    #Instance variables
    blockNum: int
    station: Station

    def __init__(self, track : TrackModel, showBlock : Callable, showMain : Callable, qtRectangle : QtCore.QRect) -> None:
        QtWidgets.QWidget.__init__(self)

        self.blockNum = BlockWindow.nextBlock

        self.move(qtRectangle.topLeft())
        self.station = track.getBlock(self.blockNum).getStation()
        self.setWindowTitle(self.station.name)

        mainLayout = QtWidgets.QVBoxLayout()

        majorLayout1 = QtWidgets.QHBoxLayout()
        layout11 = QtWidgets.QGridLayout()

        label100 = QtWidgets.QLabel("Name")
        label100.setStyleSheet("background-color:#989898")
        label100.setFont(QtGui.QFont("Arial",20))
        layout11.addWidget(label100, 0, 0)
        label110 = QtWidgets.QLabel("Tickets Sold")
        label110.setStyleSheet("background-color:#989898")
        label110.setFont(QtGui.QFont("Arial",20))
        layout11.addWidget(label110, 1, 0)
        label120 = QtWidgets.QLabel("Station Side")
        label120.setStyleSheet("background-color:#989898")
        label120.setFont(QtGui.QFont("Arial",20))
        layout11.addWidget(label120, 2, 0)
        label130 = QtWidgets.QLabel("Train in Station")
        label130.setStyleSheet("background-color:#989898")
        label130.setFont(QtGui.QFont("Arial",20))
        layout11.addWidget(label130, 3, 0)
        label140 = QtWidgets.QLabel("Boarding")
        label140.setStyleSheet("background-color:#989898")
        label140.setFont(QtGui.QFont("Arial",20))
        layout11.addWidget(label140, 4, 0)
        label150 = QtWidgets.QLabel("Disembarking")
        label150.setStyleSheet("background-color:#989898")
        label150.setFont(QtGui.QFont("Arial",20))
        layout11.addWidget(label150, 5, 0)

        self.label111 = self.station.ticketSalesWidget
        self.label111.setFont(QtGui.QFont("Arial", 15))
        layout11.addWidget(self.label111, 1, 1)
        self.label121 = QtWidgets.QLabel(str(self.station.stationSide))
        self.label121.setFont(QtGui.QFont("Arial", 15))
        layout11.addWidget(self.label121, 2, 1)
        self.label131 = self.station.occupiedWidget
        self.label131.setFont(QtGui.QFont("Arial", 15))
        layout11.addWidget(self.label131, 3, 1)
        self.label141 = self.station.boardingWidget
        self.label141.setFont(QtGui.QFont("Arial", 15))
        layout11.addWidget(self.label141, 4, 1)
        self.label151 = self.station.disembarkingWidget
        self.label151.setFont(QtGui.QFont("Arial", 15))
        layout11.addWidget(self.label151, 5, 1)
        
        layout12 = QtWidgets.QVBoxLayout()

        layout121 = QtWidgets.QHBoxLayout()
        label1211 = QtWidgets.QLabel(self.station.name)
        label1211.setFont(QtGui.QFont("Arial",30,weight=QtGui.QFont.Bold))
        layout121.addWidget(label1211)

        layout1213 = QtWidgets.QGridLayout()
        label121300 = QtWidgets.QLabel("\t")
        layout1213.addWidget(label121300,0,0)
        button121301 = QtWidgets.QPushButton("Show Block")
        button121301.clicked.connect(showBlock)
        layout1213.addWidget(button121301, 0, 1)
        button121311 = QtWidgets.QPushButton("Show Home")
        button121311.clicked.connect(showMain)
        layout1213.addWidget(button121311, 1, 1)
        layout121.addLayout(layout1213)

        layout12.addLayout(layout121)

        label122 = QtWidgets.QLabel()
        pixmap122 = QtGui.QPixmap(stationImage)
        label122.setPixmap(pixmap122)
        layout12.addWidget(label122)

        majorLayout1.addLayout(layout11)
        majorLayout1.addLayout(layout12)

        mainLayout.addLayout(majorLayout1)
        self.setLayout(mainLayout)

    def close(self) -> bool:
        self.station.ticketSalesWidget.setParent(None)
        self.station.occupiedWidget.setParent(None)
        self.station.boardingWidget.setParent(None)
        self.station.disembarkingWidget.setParent(None)
        return QtWidgets.QWidget.close(self)

class InputWindow(QtWidgets.QWidget):
    inputs: Input

    def __init__(self, inputs: Input) -> None:
        QtWidgets.QWidget.__init__(self)
        self.inputs = inputs
        self.setWindowTitle("Block {} I/O".format(inputs.block.blockNum))

        layout = QtWidgets.QGridLayout()

        label00 = QtWidgets.QLabel("Block {} Inputs".format(inputs.block.blockNum))
        label00.setFont(QtGui.QFont("Arial",30, weight=QtGui.QFont.Bold))
        layout.addWidget(label00, 0, 0)

        label01 = QtWidgets.QLabel("Inputs")
        label02 = QtWidgets.QLabel("Outputs")
        label01.setFont(QtGui.QFont("Arial", 18))
        label02.setFont(QtGui.QFont("Arial", 18))
        label01.setAlignment(QtCore.Qt.AlignCenter)
        label02.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label01, 0, 1)
        layout.addWidget(label02, 0, 2)

        label10 = QtWidgets.QLabel("Train Model")
        label10.setStyleSheet("background-color:#989898")
        label10.setFont(QtGui.QFont("Arial", 20))
        layout.addWidget(label10, 1, 0)

        layout11 = QtWidgets.QGridLayout()
        
        label1110 = QtWidgets.QLabel("Disembarking")
        label1110.setStyleSheet("background-color:#989898")
        label1110.setFont(QtGui.QFont("Arial", 15))
        layout11.addWidget(label1110, 1, 0)
        button1111 = QtWidgets.QPushButton("<")
        button1111.clicked.connect(inputs.train.lowerDisembarking)
        layout11.addWidget(button1111, 1, 1)
        label1112 = self.inputs.train.disembarkingWidget
        label1112.setAlignment(QtCore.Qt.AlignCenter)
        layout11.addWidget(label1112, 1, 2)
        button1113 = QtWidgets.QPushButton(">")
        button1113.clicked.connect(inputs.train.raiseDisembarking)
        layout11.addWidget(button1113, 1, 3)
        layout.addLayout(layout11, 1, 1)

        layout12 = QtWidgets.QGridLayout()
        label1200 = QtWidgets.QLabel("Track Circuit")
        label1200.setStyleSheet("background-color:#989898")
        label1200.setFont(QtGui.QFont("Arial", 15))
        layout12.addWidget(label1200, 0, 0)
        label1201 = self.inputs.train.trackCircuitWidget
        label1201.setAlignment(QtCore.Qt.AlignCenter)
        layout12.addWidget(label1201, 0, 1)
        label1210 = QtWidgets.QLabel("Boarding")
        label1210.setStyleSheet("background-color:#989898")
        label1210.setFont(QtGui.QFont("Arial", 15))
        layout12.addWidget(label1210, 1, 0)
        label1212 = self.inputs.train.boardingWidget
        label1212.setAlignment(QtCore.Qt.AlignCenter)
        layout12.addWidget(label1212, 1, 2)
        label1213 = QtWidgets.QPushButton("Exchange Passengers")
        label1213.clicked.connect(self.inputs.train.startExchange)
        layout12.addWidget(label1213, 1, 3)
        label1230 = QtWidgets.QLabel("Occupying")
        label1230.setStyleSheet("background-color:#989898")
        label1230.setFont(QtGui.QFont("Arial", 15))
        layout12.addWidget(label1230, 3, 0)
        label1232 = self.inputs.train.occupiedWidget
        label1232.setAlignment(QtCore.Qt.AlignCenter)
        layout12.addWidget(label1232, 3, 2)
        label1233 = QtWidgets.QPushButton("Toggle")
        label1233.clicked.connect(self.inputs.train.toggleOccupancy)
        layout12.addWidget(label1233, 3, 3)

        layout.addLayout(layout12, 1, 2)

        labelSpace = QtWidgets.QLabel()
        layout.addWidget(labelSpace, 2, 0)

        label20 = QtWidgets.QLabel("Track Controller")
        label20.setStyleSheet("background-color:#989898")
        label20.setFont(QtGui.QFont("Arial", 20))
        layout.addWidget(label20, 3, 0)

        layout21 = QtWidgets.QGridLayout()

        label2100 = QtWidgets.QLabel("Suggested Speed")
        label2100.setStyleSheet("background-color:#989898")
        label2100.setFont(QtGui.QFont("Arial", 15))
        layout21.addWidget(label2100, 0, 0)
        button2101 = QtWidgets.QPushButton("<")
        button2101.clicked.connect(inputs.wayside.lowerCommandedSpeed)
        layout21.addWidget(button2101, 0, 1)
        label2102 = self.inputs.wayside.speedWidget
        label2102.setAlignment(QtCore.Qt.AlignCenter)
        layout21.addWidget(label2102, 0, 2)
        button2103 = QtWidgets.QPushButton(">")
        button2103.clicked.connect(inputs.wayside.raiseCommandedSpeed)
        layout21.addWidget(button2103, 0, 3)
        label2110 = QtWidgets.QLabel("Authority")
        label2110.setStyleSheet("background-color:#989898")
        label2110.setFont(QtGui.QFont("Arial", 15))
        layout21.addWidget(label2110, 1, 0)
        label2112 = self.inputs.wayside.authorityWidget
        label2112.setAlignment(QtCore.Qt.AlignCenter)
        layout21.addWidget(label2112, 1, 2)
        button2113 = QtWidgets.QPushButton("Toggle")
        button2113.clicked.connect(inputs.wayside.toggleAuthority)
        layout21.addWidget(button2113, 1, 3)

        label2120 = QtWidgets.QLabel("Lighting")
        label2120.setStyleSheet("background-color:#989898")
        label2120.setFont(QtGui.QFont("Arial", 15))
        layout21.addWidget(label2120, 2, 0)
        button2122 = QtWidgets.QPushButton("Toggle")
        button2122.clicked.connect(inputs.block.wayside.toggleLighting)
        layout21.addWidget(button2122, 2, 2)
        label2130 = QtWidgets.QLabel("Crossing Lights")
        label2130.setStyleSheet("background-color:#989898")
        label2130.setFont(QtGui.QFont("Arial", 15))
        layout21.addWidget(label2130, 3, 0)
        button2132 = QtWidgets.QPushButton("Toggle")
        button2132.clicked.connect(inputs.block.wayside.toggleCrossLights)
        layout21.addWidget(button2132, 3, 2)
        label2150 = QtWidgets.QLabel("Switch")
        label2150.setStyleSheet("background-color:#989898")
        label2150.setFont(QtGui.QFont("Arial", 15))
        layout21.addWidget(label2150, 5, 0)
        button2152 = QtWidgets.QPushButton("Toggle")
        button2152.clicked.connect(inputs.block.wayside.switch)
        layout21.addWidget(button2152, 5, 2)
        
        layout.addLayout(layout21, 3, 1)

        layout22 = QtWidgets.QGridLayout()
        label2210 = QtWidgets.QLabel("Occupied")
        label2210.setStyleSheet("background-color:#989898")
        label2210.setFont(QtGui.QFont("Arial", 15))
        layout22.addWidget(label2210, 1, 0)
        label2211 = self.inputs.wayside.occupiedWidget
        label2211.setAlignment(QtCore.Qt.AlignCenter)
        layout22.addWidget(label2211, 1, 1)

        label2240 = self.inputs.wayside.powerFailWidget
        label2240.setFont(QtGui.QFont("Arial", 12))
        layout22.addWidget(label2240, 4, 0)
        label2250 = self.inputs.wayside.trackFailWidget
        label2250.setFont(QtGui.QFont("Arial", 12))
        layout22.addWidget(label2250, 5, 0)
        label2260 = self.inputs.wayside.circuitFailWidget
        label2260.setFont(QtGui.QFont("Arial", 12))
        layout22.addWidget(label2260, 6, 0)
        label2270 = self.inputs.wayside.switchFailWidget
        label2270.setFont(QtGui.QFont("Arial", 12))
        layout22.addWidget(label2270, 7, 0)
        layout.addLayout(layout22, 3, 2)

        self.setLayout(layout)