from re import S
from typing import Callable
from PyQt5 import QtCore, QtWidgets, QtGui
from typing import Callable
from SystemCloser import systemCloser, WarningWindow
from SystemController import SystemController

crazyTrainImage = "crazyTrain.jpg"
redLineImage = "TrackModelModule/redLine.jpg"
greenLineImage = "TrackModelModule/greenLine.jpg"

class LoadingWindow(QtWidgets.QWidget):

    def __init__(self, qtRectangle: QtCore.QRect):
        #Initialize Window Dimensions and Title
        QtWidgets.QWidget.__init__(self)
        self.move(qtRectangle.topLeft())
        self.setWindowTitle('Loading Window')

        #Set initial layout
        self.layoutMain = QtWidgets.QGridLayout()
        self.setLayout(self.layoutMain)

        #add title
        self.label00 = QtWidgets.QLabel("Select the train line to simulate")
        self.label00.setStyleSheet("background-color:#989898")
        self.label00.setFont(QtGui.QFont("Arial",20))
        self.layoutMain.addWidget(self.label00, 0, 0, 1, 2)

        #add line widgets
        self.label10 = QtWidgets.QLabel("Green Line")
        self.label10.setAlignment(QtCore.Qt.AlignCenter)
        self.label10.setStyleSheet("background-color:#989898")
        self.label10.setFont(QtGui.QFont("Arial",20))
        self.layoutMain.addWidget(self.label10, 1, 0)

        self.label11 = QtWidgets.QLabel("Red Line")
        self.label11.setAlignment(QtCore.Qt.AlignCenter)
        self.label11.setStyleSheet("background-color:#989898")
        self.label11.setFont(QtGui.QFont("Arial",20))
        self.layoutMain.addWidget(self.label11, 1, 1)

        self.greenButton = QtWidgets.QPushButton()
        self.greenButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.greenButton.setIcon(QtGui.QIcon(QtGui.QPixmap(greenLineImage)))
        self.greenButton.setIconSize(QtCore.QSize(400,450))
        self.greenButton.clicked.connect(SystemController.setGreenLine)
        self.greenButton.clicked.connect(self.close)
        self.layoutMain.addWidget(self.greenButton, 2, 0)

        self.redButton = QtWidgets.QPushButton()
        self.redButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.redButton.setIcon(QtGui.QIcon(redLineImage))
        self.redButton.setIconSize(QtCore.QSize(400,450))
        self.redButton.clicked.connect(SystemController.setRedLine)
        self.redButton.clicked.connect(self.close)
        self.layoutMain.addWidget(self.redButton, 2, 1)

class MainWindow(QtWidgets.QWidget):

    system: SystemController

    def __init__(self, system: SystemController, showCTC: Callable, showWaysides: Callable, showTrackModel: Callable, showTrainModel: Callable, showTrainControllers: Callable, qtRectangle : QtCore.QRect):
        #Initialize Window Dimensions and Title
        QtWidgets.QWidget.__init__(self)
        self.move(qtRectangle.topLeft())
        self.system = system
        self.setWindowTitle('Main Window')

        self.layoutMain = QtWidgets.QVBoxLayout()

        #Create Title Layout
        self.layoutTitle = QtWidgets.QGridLayout()
        self.layoutTitle.setColumnStretch(0,7)
        self.layoutTitle.setColumnStretch(1,1)
        self.layoutMain.addLayout(self.layoutTitle)

        #Create Title widget
        self.labelTitle = QtWidgets.QLabel("Team Crazy Train NSE Project")
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle.setFont(QtGui.QFont("Arial",45))
        self.layoutTitle.addWidget(self.labelTitle, 0, 0)

        #Add Close Program Button
        def openWarning():
            self.warningWindow = WarningWindow("This will close the entire program.\nAre you sure that you would like to continue?", systemCloser.closeProgram)
            self.warningWindow.show()
        self.closeProgram = QtWidgets.QPushButton("Close Program")
        self.closeProgram.clicked.connect(openWarning)
        self.layoutTitle.addWidget(self.closeProgram, 0, 1)

        #Create Lower Layout
        self.layoutLower = QtWidgets.QHBoxLayout()

        #Create Buttons
        self.layoutButtons = QtWidgets.QGridLayout()
        self.buttonCTC = QtWidgets.QPushButton("CTC Office")
        self.buttonWayside = QtWidgets.QPushButton("Wayside Controllers")
        self.buttonTrack = QtWidgets.QPushButton("Track Model")
        self.buttonTrain = QtWidgets.QPushButton("Train Model")
        self.buttonTrainControllers = QtWidgets.QPushButton("Train Controllers")
        #Set Button Fonts
        self.buttonCTC.setFont(QtGui.QFont("Arial",30))
        self.buttonWayside.setFont(QtGui.QFont("Arial",30))
        self.buttonTrack.setFont(QtGui.QFont("Arial",30))
        self.buttonTrain.setFont(QtGui.QFont("Arial",30))
        self.buttonTrainControllers.setFont(QtGui.QFont("Arial",30))
        #Connect Buttons
        self.buttonCTC.clicked.connect(showCTC)
        self.buttonWayside.clicked.connect(showWaysides)
        self.buttonTrack.clicked.connect(showTrackModel)
        self.buttonTrain.clicked.connect(showTrainModel)
        self.buttonTrainControllers.clicked.connect(showTrainControllers)
        #Add Buttons to Button Layout
        self.layoutButtons.addWidget(self.buttonCTC,0,0,1,3)
        self.layoutButtons.addWidget(self.buttonWayside,1,0,1,3)
        self.layoutButtons.addWidget(self.buttonTrack,2,0,1,3)
        self.layoutButtons.addWidget(self.buttonTrain,3,0,1,3)
        self.layoutButtons.addWidget(self.buttonTrainControllers,4,0,1,3)

        #Spacer
        self.dummyLabel0 = QtWidgets.QLabel("\t")
        self.dummyLabel1 = QtWidgets.QLabel("\t")
        self.layoutButtons.addWidget(self.dummyLabel0,5,0)
        self.layoutButtons.addWidget(self.dummyLabel1,6,0)

        #Create Time Controller
        self.currentTimeLabel = QtWidgets.QLabel("Current Time")
        self.currentTimeLabel.setStyleSheet("background-color:#989898")
        self.currentTimeLabel.setFont(QtGui.QFont("Arial",20))
        self.currentTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentTimeValue = self.system.timeWidget
        self.currentTimeValue.setFont(QtGui.QFont("Arial",20))
        self.currentTimeValue.setAlignment(QtCore.Qt.AlignCenter)
        self.layoutButtons.addWidget(self.currentTimeLabel,7,1)
        self.layoutButtons.addWidget(self.currentTimeValue,8,0,1,3)

        #Create Rate Controller
        self.labelRate = QtWidgets.QLabel("Rate")
        self.labelRate.setStyleSheet("background-color:#989898")
        self.labelRate.setFont(QtGui.QFont("Arial",20))
        self.labelRate.setAlignment(QtCore.Qt.AlignCenter)
        self.layoutButtons.addWidget(self.labelRate,9,1)
        #Add Rate Buttons
        self.buttonRateLower = QtWidgets.QPushButton("<")
        self.buttonRateRaise = QtWidgets.QPushButton(">")
        self.buttonRateLower.clicked.connect(system.lowerRate)
        self.buttonRateRaise.clicked.connect(system.raiseRate)
        self.buttonRateLower.clicked.connect(self.setRateVal)
        self.buttonRateRaise.clicked.connect(self.setRateVal)
        self.layoutButtons.addWidget(self.buttonRateLower,10,0)
        self.layoutButtons.addWidget(self.buttonRateRaise,10,2)
        #Add Rate Value
        self.labelRateVal = QtWidgets.QLabel(str(self.system.rate))
        self.labelRateVal.setFont(QtGui.QFont("Arial",20))
        self.labelRateVal.setAlignment(QtCore.Qt.AlignCenter)
        self.layoutButtons.addWidget(self.labelRateVal,10,1)
        
        #Finalize Buttons
        self.layoutLower.addLayout(self.layoutButtons)

        #Create Crazy Train Icon
        self.labelImage = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap(crazyTrainImage)
        self.labelImage.setPixmap(self.pixmap)
        self.layoutLower.addWidget(self.labelImage)

        #Finalize Lower Layout
        self.layoutMain.addLayout(self.layoutLower)

        #Finalize Window
        self.setLayout(self.layoutMain)
    
    def setRateVal(self):
        rate = self.system.getRate()
        if rate == 0:
            self.labelRateVal.setText("Paused")
        else:
            self.labelRateVal.setText(str(rate))

class EmptyWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        qtRectangle = self.frameGeometry()
        topLeftPoint = QtWidgets.QDesktopWidget().availableGeometry().topLeft()
        qtRectangle.moveTopLeft(topLeftPoint)
        self.move(qtRectangle.topLeft())