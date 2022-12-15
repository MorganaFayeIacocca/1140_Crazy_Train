import sys
import time
from PyQt5 import QtCore
from Train_Controller import TrainController
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

	

class controlWindow(QWidget):
    controller: TrainController
    backFunc = 0
    def __init__(self, tc, backFunc):
        super().__init__()
        self.controller = tc
        self.controller.window = self
        self.controller.mode = 0
        self.backFunc = backFunc
        
        self.setWindowTitle("Train Controller")
        self.setGeometry(0,0,1200,725)
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        
        #Initializing Status Monitor GroupBox
        statusMonitorGroupBox = QGroupBox("Train Status Monitor")
        statusMonitorGroupBox.setFixedSize(1200,300)
        #Status Monitor Layout Definition
        statusLayout = QGridLayout()
        statusMonitorGroupBox.setLayout(statusLayout)
        
        #Initializing Speed Sub-GroupBox
        speedGroupBox = QGroupBox("Speed")
        
        #Speed Sub-GroupBox Layout
        speedVBox = QVBoxLayout()
        speedGroupBox.setLayout(speedVBox)
        
        #Adding text to speed GroupBox layout
        self.currentPowerLabel = QLabel("Current Power\t%.2f W" % self.controller.power)
        speedVBox.addWidget(self.currentPowerLabel)
        self.currentSpeedLabel = QLabel("Current Speed\t%.2f mph" % (self.controller.currentSpeed*2.23694))
        speedVBox.addWidget(self.currentSpeedLabel)
        self.setpointLabel = QLabel("Setpoint\t\t%.2f mph" % (self.controller.speedSetpoint*2.23694))
        speedVBox.addWidget(self.setpointLabel)
        self.suggestedLabel = QLabel("Suggested\t%.2f mph" % (self.controller.suggestedSpeed*2.23694))
        speedVBox.addWidget(self.suggestedLabel)
        self.maximumLabel = QLabel("Limit\t\t%.2f mph" % (self.controller.maximumSpeed*2.23694))
        speedVBox.addWidget(self.maximumLabel)
        
        
        
        #Initializing Brakes Sub-GroupBox
        brakesGroupBox = QGroupBox("Brakes")
        
        #Brakes Sub-GroupBox Layout
        brakesVBox = QVBoxLayout()
        brakesGroupBox.setLayout(brakesVBox)
        
        #Adding text to brakes GroupBox layout
        self.serviceBrakeLabel = QLabel("Service Brake\t\t" + self.controller.getServiceBrakeState())
        brakesVBox.addWidget(self.serviceBrakeLabel)
        self.emergencyBrakeLabel = QLabel("Emergency\t\t" + self.controller.getEmergencyBrakeState())
        brakesVBox.addWidget(self.emergencyBrakeLabel)
        
        
        
        
        #Initializing Location Sub-GroupBox
        locationGroupBox = QGroupBox("Location")
        
        #Brakes Sub-GroupBox Layout
        locationVBox = QVBoxLayout()
        locationGroupBox.setLayout(locationVBox)
        
        #Adding text to Location GroupBox layout
        self.authorityLabel = QLabel("Authority\t\t" + self.controller.getAuthorityState())
        locationVBox.addWidget(self.authorityLabel)
        self.stopLabel = QLabel("Next Stop:\t" + self.controller.nextStop)
        locationVBox.addWidget(self.stopLabel)
        self.stoppingLabel = QLabel("Status:\t\t" + self.controller.getStoppingStatus())
        locationVBox.addWidget(self.stoppingLabel)
        
        
        #Initializing Misc Sub-GroupBox
        miscGroupBox = QGroupBox("Miscellaneous")
        
        #Misc Sub-GroupBox Layout
        miscVBox = QVBoxLayout()
        miscGroupBox.setLayout(miscVBox)
        
        #Adding text to Location GroupBox layout
        self.leftDoorsLabel = QLabel("Left Doors\t\t" + self.controller.getLeftDoorState())
        miscVBox.addWidget(self.leftDoorsLabel)
        self.rightDoorsLabel = QLabel("Right Doors\t\t" + self.controller.getRightDoorState())
        miscVBox.addWidget(self.rightDoorsLabel)
        self.lightsLabel = QLabel("Lights\t\t\t" + self.controller.getLightState())
        miscVBox.addWidget(self.lightsLabel)
        self.tempLabel = QLabel("Temperature\t\t" + str(self.controller.temperature) + " *F")
        miscVBox.addWidget(self.tempLabel)
        
        
        #Initializing Failure Sub-GroupBox
        failureGroupBox = QGroupBox("Failure Monitoring")
        
        #Failure Sub-GroupBox Layout
        failureVBox = QVBoxLayout()
        failureGroupBox.setLayout(failureVBox)
        
        #Adding text to Failure GroupBox layout
        self.engineFailureLabel = QLabel("Engine\t\t\t" + self.controller.getEngineFailureStatus())
        failureVBox.addWidget(self.engineFailureLabel)
        self.brakeFailureLabel = QLabel("Brakes\t\t\t" + self.controller.getBrakeFailureStatus())
        failureVBox.addWidget(self.brakeFailureLabel)
        self.signalFailureLabel = QLabel("Signal Pickup\t\t" + self.controller.getSignalFailureStatus())
        failureVBox.addWidget(self.signalFailureLabel)
        
        #Add Sub-Groupboxes to Status monitor groupbox layout
        statusLayout.addWidget(speedGroupBox,0,0,2,1)
        statusLayout.addWidget(brakesGroupBox,0,1,1,1)
        statusLayout.addWidget(locationGroupBox,1,1,1,1)
        statusLayout.addWidget(miscGroupBox,0,2,2,1)
        statusLayout.addWidget(failureGroupBox,0,3,2,1)
        
        #Initializing Command Input Interface Groupbox
        self.commandInterfaceGroupBox = QGroupBox("Command Input Interface")
        self.commandInterfaceGroupBox.setFixedSize(1200,300)
        self.commandInterfaceGroupBox.setAlignment(Qt.AlignTop)
        #Command Interface Layout Definition
        commandLayout = QGridLayout()
        self.commandInterfaceGroupBox.setLayout(commandLayout)
        
        self.toggleModeButton = QPushButton("To Manual Mode")
        self.toggleModeButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.toggleModeButton.setCheckable(True)
        self.toggleModeButton.clicked.connect(self.modeButtonClicked)
        
        
        
        #Initializing Speed Control Sub-GroupBox
        speedControlGroupBox = QGroupBox("Speed Setpoint")
        
        #Speed Control Sub-GroupBox Layout
        speedControlGrid = QGridLayout()

        speedControlGroupBox.setLayout(speedControlGrid)
        
        


        
        #Add content to Interactive Speed Control
        speedDownButton = QPushButton("-")
        speedDownButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : red; color : white}QPushButton::pressed{border : 2px solid black; background-color : darkred; color : white}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        speedDownButton.setFont(QFont("Arial",15))
        speedDownButton.clicked.connect(self.speedDownButtonClicked)
        
        self.interactiveSetpointLabel = QLabel("%.2f mph" % (self.controller.speedSetpoint*2.23694))
        self.interactiveSetpointLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.interactiveSetpointLabel.setFont(QFont("Arial",13))
        
        speedUpButton = QPushButton("+")
        speedUpButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : green; color : white}QPushButton::pressed{border : 2px solid black; background-color : darkgreen; color : white}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        speedUpButton.setFont(QFont("Arial",15))
        speedUpButton.clicked.connect(self.speedUpButtonClicked)
        
        self.setpointLineEdit = QLineEdit()
        
        
        setSetpointButton = QPushButton("Set")
        setSetpointButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        setSetpointButton.setFont(QFont("Arial",10))
        setSetpointButton.clicked.connect(self.setSetpointButtonClicked)
        
        #Define speed control layout
        speedControlGrid.addWidget(speedDownButton,0,0,1,1)
        speedControlGrid.addWidget(self.interactiveSetpointLabel,0,1,1,1)
        speedControlGrid.addWidget(speedUpButton,0,2,1,1)
        speedControlGrid.addWidget(self.setpointLineEdit,1,0,1,2)
        speedControlGrid.addWidget(setSetpointButton,1,2,1,1)
        
        
        
        #Initializing Speed Control Sub-GroupBox
        tempControlGroupBox = QGroupBox("Adjust Temperature")
        
        #Speed Control Sub-GroupBox Layout
        tempControlGrid = QGridLayout()

        tempControlGroupBox.setLayout(tempControlGrid)
        
        


        
        #Add content to Interactive Speed Control
        tempDownButton = QPushButton("-")
        tempDownButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : red; color : white}QPushButton::pressed{border : 2px solid black; background-color : darkred; color : white}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        tempDownButton.setFont(QFont("Arial",15))
        tempDownButton.clicked.connect(self.tempDownButtonClicked)
        
        self.tempSetpointLabel = QLabel(str(self.controller.temperature) + " *F")
        self.tempSetpointLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tempSetpointLabel.setFont(QFont("Arial",13))
        
        tempUpButton = QPushButton("+")
        tempUpButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : green; color : white}QPushButton::pressed{border : 2px solid black; background-color : darkgreen; color : white}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        tempUpButton.setFont(QFont("Arial",15))
        tempUpButton.clicked.connect(self.tempUpButtonClicked)
        
        
        
        #Define speed control layout
        tempControlGrid.addWidget(tempDownButton,0,0,1,1)
        tempControlGrid.addWidget(self.tempSetpointLabel,0,1,1,1)
        tempControlGrid.addWidget(tempUpButton,0,2,1,1)
        
        
        
        #Initializing Brake Control GroupBox
        brakeControlGroupBox = QGroupBox("Brake Control")
        
        #Brake Control GroupBox Layout
        brakeControlVBox = QVBoxLayout()
        brakeControlVBox.setAlignment(Qt.AlignHCenter)
        brakeControlGroupBox.setLayout(brakeControlVBox)
        
        
        #Service Brake Button
        serviceBrakeLabel = QLabel("Service Brake")
        serviceBrakeLabel.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.toggleServiceBrakeButton = QPushButton("Toggle")
        self.toggleServiceBrakeButton.setFont(QFont("Arial",12))
        self.toggleServiceBrakeButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.toggleServiceBrakeButton.setCheckable(True)
        self.toggleServiceBrakeButton.setFixedSize(QtCore.QSize(100, 30))
        self.toggleServiceBrakeButton.clicked.connect(self.serviceBrakeButtonClicked)
        
        #Emergency Brake Button
        emergencyBrakeLabel = QLabel("Emergency Brake")
        emergencyBrakeLabel.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.toggleEmergencyBrakeButton = QPushButton("Toggle")
        self.toggleEmergencyBrakeButton.setFont(QFont("Arial",12))
        self.toggleEmergencyBrakeButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.toggleEmergencyBrakeButton.setCheckable(True)
        self.toggleEmergencyBrakeButton.setFixedSize(QtCore.QSize(100, 30))
        self.toggleEmergencyBrakeButton.clicked.connect(self.emergencyBrakeButtonClicked)
        
        
        
        #Add buttons and text to brake control box
        brakeControlVBox.addWidget(serviceBrakeLabel)
        brakeControlVBox.addWidget(self.toggleServiceBrakeButton, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        brakeControlVBox.addWidget(emergencyBrakeLabel)
        brakeControlVBox.addWidget(self.toggleEmergencyBrakeButton, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        
        
        
        
        
        
        
        
        
        #Initializing Brake Control GroupBox
        miscControlGroupBox = QGroupBox("Doors and Lights")
        miscControlVBox = QVBoxLayout()
        miscControlGroupBox.setLayout(miscControlVBox)
        
        lightsLabel = QLabel("Lights")
        lightsLabel.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.controlLightsButton = QPushButton("Toggle")
        self.controlLightsButton.setFont(QFont("Arial",12))
        self.controlLightsButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.controlLightsButton.setCheckable(True)
        self.controlLightsButton.setFixedSize(QtCore.QSize(100, 30))
        self.controlLightsButton.clicked.connect(self.lightsButtonClicked)
        
        leftDoorsLabel = QLabel("Left Doors")
        leftDoorsLabel.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.controlLeftDoorsButton = QPushButton("Toggle")
        self.controlLeftDoorsButton.setFont(QFont("Arial",12))
        self.controlLeftDoorsButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.controlLeftDoorsButton.setCheckable(True)
        self.controlLeftDoorsButton.setFixedSize(QtCore.QSize(100, 30))
        self.controlLeftDoorsButton.clicked.connect(self.leftDoorsButtonClicked)
        
        rightDoorsLabel = QLabel("Right Doors")
        rightDoorsLabel.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.controlRightDoorsButton = QPushButton("Toggle")
        self.controlRightDoorsButton.setFont(QFont("Arial",12))
        self.controlRightDoorsButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.controlRightDoorsButton.setCheckable(True)
        self.controlRightDoorsButton.setFixedSize(QtCore.QSize(100, 30))
        self.controlRightDoorsButton.clicked.connect(self.rightDoorsButtonClicked)
        
        miscControlVBox.addWidget(lightsLabel)
        miscControlVBox.addWidget(self.controlLightsButton, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        miscControlVBox.addWidget(leftDoorsLabel)
        miscControlVBox.addWidget(self.controlLeftDoorsButton, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        miscControlVBox.addWidget(rightDoorsLabel)
        miscControlVBox.addWidget(self.controlRightDoorsButton, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        
        #Adding widgets to Command Interface Layout
        commandLayout.addWidget(speedControlGroupBox,0,0,1,1)
        commandLayout.addWidget(brakeControlGroupBox,0,1,2,1)
        commandLayout.addWidget(tempControlGroupBox, 1,0,1,1)
        commandLayout.addWidget(miscControlGroupBox, 0,2,2,1)
        
        self.commandInterfaceGroupBox.setDisabled(True)
        
        #Button for test UI
        self.toggleTestUIButton = QPushButton("To Test UI")
        self.toggleTestUIButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.toggleTestUIButton.setCheckable(True)
        self.toggleTestUIButton.clicked.connect(self.toggleTestUIButtonClicked)
        
        #Button for engineer UI
        self.toggleEngineerUIButton = QPushButton("Open Engineer Interface")
        self.toggleEngineerUIButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.toggleEngineerUIButton.setCheckable(True)
        self.toggleEngineerUIButton.clicked.connect(self.toggleEngineerUIButtonClicked)
        
        #Test UI
        self.testInterface = QGroupBox("Test Interface")
        
        #Speed Control Sub-GroupBox Layout
        self.testInterfaceGrid = QGridLayout()
        self.testInterface.setLayout(self.testInterfaceGrid)
        
        
        #Add input LineEdits and Buttons
        self.currentSpeedLineEdit = QLineEdit("")
        self.setCurrentSpeedButton = QPushButton("Set Current Speed")
        self.setCurrentSpeedButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.setCurrentSpeedButton.clicked.connect(self.setCurrentSpeedButtonClicked)
        
        self.suggestedSpeedLineEdit = QLineEdit("")
        self.setSuggestedSpeedButton = QPushButton("Set Suggested Speed")
        self.setSuggestedSpeedButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.setSuggestedSpeedButton.clicked.connect(self.setSuggestedSpeedButtonClicked)
        
    
        self.nextStopLineEdit = QLineEdit("")
        self.setNextStopButton = QPushButton("Set Next Stop")
        self.setNextStopButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.setNextStopButton.clicked.connect(self.setNextStopButtonClicked)
        
        self.kpLineEdit = QLineEdit("")
        self.setKpButton = QPushButton("Set Kp")
        self.setKpButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.setKpButton.clicked.connect(self.setKpButtonClicked)
    
        self.kiLineEdit = QLineEdit("")
        self.setKiButton = QPushButton("Set Ki")
        self.setKiButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.setKiButton.clicked.connect(self.setKiButtonClicked)
        
        self.periodLineEdit = QLineEdit("")
        self.setPeriodButton = QPushButton("Set T")
        self.setPeriodButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.setPeriodButton.clicked.connect(self.setPeriodButtonClicked)
        
        self.beaconLineEdit = QLineEdit("")
        self.sendBeaconButton = QPushButton("Send Beacon")
        self.sendBeaconButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.sendBeaconButton.clicked.connect(self.sendBeaconButtonClicked)
        
        
  
        
        
        
        self.eLabel = QLabel("e = %.2f" % self.controller.e)
        self.ePrevLabel = QLabel("ePrev = %.2f" % self.controller.ePrevUsed)
        self.uLabel = QLabel("u = %.2f" % self.controller.uK)
        self.uPrevLabel = QLabel("uPrev = %.2f" % self.controller.uKPrevUsed)
        self.kpLabel = QLabel("kp = " + str(self.controller.kP))
        self.kiLabel = QLabel("ki = " + str(self.controller.kI))
        self.TLabel = QLabel("T = " + str(self.controller.kI))
        
        
        
        #Add items to test interface box
        self.testInterfaceGrid.addWidget(self.currentSpeedLineEdit,0,0,1,2)
        self.testInterfaceGrid.addWidget(self.setCurrentSpeedButton,0,2,1,1)
        self.testInterfaceGrid.addWidget(self.suggestedSpeedLineEdit,1,0,1,2)
        self.testInterfaceGrid.addWidget(self.setSuggestedSpeedButton,1,2,1,1)
        self.testInterfaceGrid.addWidget(self.beaconLineEdit,2,0,1,2)
        self.testInterfaceGrid.addWidget(self.sendBeaconButton,2,2,1,1)
        self.testInterfaceGrid.addWidget(self.nextStopLineEdit,4,0,1,2)
        self.testInterfaceGrid.addWidget(self.setNextStopButton,4,2,1,1)
        self.testInterfaceGrid.addWidget(self.kpLineEdit,5,0,1,2)
        self.testInterfaceGrid.addWidget(self.setKpButton,5,2,1,1)
        self.testInterfaceGrid.addWidget(self.kiLineEdit,6,0,1,2)
        self.testInterfaceGrid.addWidget(self.setKiButton,6,2,1,1)
        self.testInterfaceGrid.addWidget(self.periodLineEdit,7,0,1,2)
        self.testInterfaceGrid.addWidget(self.setPeriodButton,7,2,1,1)

        self.testInterfaceGrid.addWidget(self.eLabel,11,0,1,1)
        self.testInterfaceGrid.addWidget(self.uLabel,11,1,1,1)
        self.testInterfaceGrid.addWidget(self.ePrevLabel,12,0,1,1)
        self.testInterfaceGrid.addWidget(self.uPrevLabel,12,1,1,1)
        self.testInterfaceGrid.addWidget(self.kpLabel,13,0,1,1)
        self.testInterfaceGrid.addWidget(self.kiLabel,13,1,1,1)
        self.testInterfaceGrid.addWidget(self.TLabel,13,2,1,1)
        self.testInterface.setFixedSize(1200,300)
        self.testInterface.setVisible(False)
        self.testInterface.setDisabled(True)
        
        #Engineer UI
        self.engineerInterface = QGroupBox("Test Interface")
        
        #Engineer UI GroupBox Layout
        self.engineerInterfaceGrid = QGridLayout()
        self.engineerInterface.setLayout(self.engineerInterfaceGrid)
        
        self.engineerInterfaceGrid.addWidget(self.kpLineEdit,0,0,1,2)
        self.engineerInterfaceGrid.addWidget(self.setKpButton,0,2,1,1)
        self.engineerInterfaceGrid.addWidget(self.kiLineEdit,1,0,1,2)
        self.engineerInterfaceGrid.addWidget(self.setKiButton,1,2,1,1)
        self.engineerInterfaceGrid.addWidget(self.kpLabel,2,0,1,1)
        self.engineerInterfaceGrid.addWidget(self.kiLabel,2,1,1,1)
        
        self.engineerInterface.setFixedSize(1200,120)
        self.engineerInterface.setVisible(False)
        self.engineerInterface.setDisabled(True)
        
        
        self.toggleModeButton.setFixedSize(1200,20)
        self.toggleEngineerUIButton.setFixedSize(1200,20)
        self.toggleTestUIButton.setFixedSize(1200,20)
        
        
        self.backButton = QPushButton("Back")
        self.backButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        self.backButton.setCheckable(True)
        self.backButton.setFont(QFont("Arial",12))
        self.backButton.setFixedSize(60,25)
        self.backButton.clicked.connect(self.backFunc)
        self.backButton.clicked.connect(self.close)
        
        #Adding widgets to window layout
        layout.addWidget(statusMonitorGroupBox)
        layout.addWidget(self.commandInterfaceGroupBox)
        layout.addWidget(self.toggleModeButton)
        layout.addWidget(self.toggleEngineerUIButton)
        layout.addWidget(self.toggleTestUIButton)
        layout.addWidget(self.testInterface)
        layout.addWidget(self.engineerInterface)
        layout.addWidget(self.backButton)




    def setBackFunc(self, x):
        self.backButton.clicked.disconnect()
        self.backButton.clicked.connect(x)
        self.backButton.clicked.connect(self.close)

        
    def modeButtonClicked(self):
        if self.toggleModeButton.isChecked():
            self.toggleModeButton.setText("To Automatic Mode")
            self.commandInterfaceGroupBox.setDisabled(False)
            self.controller.mode = 1
        else:
            self.toggleModeButton.setText("To Manual Mode")
            self.commandInterfaceGroupBox.setDisabled(True)
            self.controller.mode = 0
    
    def toggleTestUIButtonClicked(self):
        if self.toggleTestUIButton.isChecked():
            self.toggleTestUIButton.setText("To Normal UI")
            self.toggleEngineerUIButton.setDisabled(True)
            self.setFixedHeight(1025)
            self.testInterface.setVisible(True)
            self.testInterface.setDisabled(False)
            
        else:
            self.toggleTestUIButton.setText("To Test UI")
            self.toggleEngineerUIButton.setDisabled(False)
            self.setFixedHeight(725)
            self.testInterface.setVisible(False)
            self.testInterface.setDisabled(True)
            
    
    def toggleEngineerUIButtonClicked(self):
        if self.toggleEngineerUIButton.isChecked():
            self.toggleEngineerUIButton.setText("Close Engineer Interface")
            self.toggleTestUIButton.setDisabled(True)
            self.engineerInterface.setVisible(True)
            self.engineerInterface.setDisabled(False)
            self.setFixedHeight(853)
        else:
            self.toggleEngineerUIButton.setText("Open Engineer Interface")
            self.toggleTestUIButton.setDisabled(False)
            self.setFixedHeight(725)
            self.engineerInterface.setVisible(False)
            self.engineerInterface.setDisabled(True)
            


    def serviceBrakeButtonClicked(self):
        self.controller.toggleServiceBrake()
        self.controller.speedSetpoint = 0
    
    def emergencyBrakeButtonClicked(self):
        self.controller.toggleEmergencyBrake()
        self.controller.speedSetpoint = 0
        
    def lightsButtonClicked(self):
        self.controller.toggleLights()
        
    def leftDoorsButtonClicked(self):
        self.controller.toggleLeftDoors()
        
    def rightDoorsButtonClicked(self):
        self.controller.toggleRightDoors()
        
    def speedDownButtonClicked(self):
        self.controller.speedSetpoint = ((self.controller.speedSetpoint*2.23694)-1)/2.23694
        if self.controller.speedSetpoint < 0:
            self.controller.speedSetpoint = 0
        
    def speedUpButtonClicked(self):
        self.controller.speedSetpoint = ((self.controller.speedSetpoint*2.23694)+1)/2.23694
        if self.controller.speedSetpoint > self.controller.maximumSpeed:
            self.controller.speedSetpoint = self.controller.maximumSpeed
        
    def setSetpointButtonClicked(self):
        if(self.controller.authority == 0):
            self.throwError("Cannot input speed. The train has no current authority.")
        try:
            if (float(self.setpointLineEdit.text()) < 0 or float(self.setpointLineEdit.text()) > self.controller.maximumSpeed*2.23694):
                raise ValueError('speed setpoint is out of bounds')
            self.controller.speedSetpoint = float(self.setpointLineEdit.text())/2.23694
        except:
            self.throwError("Input for setpoint value is incorrect. Please ensure the value entered is positive and does not exceed the max speed.")
        
        
    def tempDownButtonClicked(self):
        self.controller.temperature = self.controller.temperature - 1
        if self.controller.temperature < self.controller.minimumTemp:
            self.controller.temperature = self.controller.minimumTemp
        self.controller.train.set("temperature", self.controller.temperature)
        
    def tempUpButtonClicked(self):
        self.controller.temperature = self.controller.temperature + 1
        if self.controller.temperature > self.controller.maximumTemp:
            self.controller.temperature = self.controller.maximumTemp
        self.controller.train.set("temperature", self.controller.temperature)
    
    
    def setCurrentSpeedButtonClicked(self):
        try:
            self.controller.currentSpeed = float(self.currentSpeedLineEdit.text())/2.23694
        except:
            self.throwError("Input for current speed value is incorrect. Please ensure the value entered is a positive number.")
    
    def setSuggestedSpeedButtonClicked(self):
        try:
            if (float(self.suggestedSpeedLineEdit.text()) < 0 or float(self.suggestedSpeedLineEdit.text()) > self.controller.maximumSpeed*2.23694):
                raise ValueError('suggested speed is out of bounds')
            self.controller.suggestedSpeed = float(self.suggestedSpeedLineEdit.text())/2.23694
        except:
            self.throwError("Input for suggested speed value is incorrect. Please ensure the value entered is positive and does not exceed the max speed.")
    
    def sendBeaconButtonClicked(self):
        self.controller.sendBeacon(self.beaconLineEdit.text())
    
    def setNextStopButtonClicked(self):
        try:
            self.controller.nextStop = self.nextStopLineEdit.text()
        except:
            self.throwError("Invalid input. Issue Unknown.")
        
    def setKpButtonClicked(self):
        try:
            if (float(self.kpLineEdit.text()) < 0):
                raise ValueError('kp less than 0')
            self.controller.kP = float(self.kpLineEdit.text())
        except:
            self.throwError("Input for Kp value is incorrect. Please ensure the value entered is a positive decimal.")
        
    def setKiButtonClicked(self):
        try:
            if (float(self.kiLineEdit.text()) < 0):
                raise ValueError('ki less than 0')
            self.controller.kI = float(self.kiLineEdit.text())
        except:
            self.throwError("Input for Ki value is incorrect. Please ensure the value entered is a positive decimal.")
    
    def setPeriodButtonClicked(self):
        try:
            if (float(self.periodLineEdit.text()) < 0):
                raise ValueError('kp less than 0')
            self.controller.T = float(self.periodLineEdit.text())
        except:
            self.throwError("Input for T value is incorrect. Please ensure the value entered is a positive decimal.")

    def doorToggleButtonClicked(self):
        self.controller.setBeaconInfo(self.controller.inTunnel, not self.controller.atStation);
            
        
    def inTunnelButtonClicked(self):
        self.controller.setBeaconInfo(not self.controller.inTunnel, self.controller.atStation);
        
    def failEngineButtonClicked(self):
        self.controller.toggleEngineFailure()
        
    def failBrakesButtonClicked(self):    
        self.controller.toggleBrakeFailure()
        
    def failSignalButtonClicked(self):    
        self.controller.toggleSignalFailure()
        self.refreshValues()
        
    def failWheelsButtonClicked(self):
        self.controller.toggleWheelFailure()
        self.refreshValues()
        
    def authorityButtonClicked(self):
        self.controller.setAuthority(not self.controller.authority);
        self.refreshValues()
        
    def throwError(self, errorText):
        errorMsg = QMessageBox()
        errorMsg.setWindowTitle("Error")
        errorMsg.setText(errorText)
        errorMsg.exec_()


    def refreshValues(self):
        
        #Update speed info
        self.currentPowerLabel.setText("Current Power\t%.2f W" % self.controller.power)
        self.currentSpeedLabel.setText("Current Speed\t%.2f mph" % (self.controller.currentSpeed*2.23694))
        self.setpointLabel.setText("Setpoint\t\t%.2f mph" % (self.controller.speedSetpoint*2.23694))
        self.suggestedLabel.setText("Suggested\t%.2f mph" % (self.controller.suggestedSpeed*2.23694))
        self.maximumLabel.setText("Limit\t\t%.2f mph" % (self.controller.maximumSpeed*2.23694))
        
        #Update brake info
        self.serviceBrakeLabel.setText("Service Brake\t\t" + self.controller.getServiceBrakeState())
        self.emergencyBrakeLabel.setText("Emergency\t\t" + self.controller.getEmergencyBrakeState())
        
        #Update location info
        self.authorityLabel.setText("Authority\t\t" + self.controller.getAuthorityState())
        self.stopLabel.setText("Next Stop:\t" + str(self.controller.nextStop))
        self.stoppingLabel.setText("Status:\t\t" + self.controller.getStoppingStatus())
        
        #Update misc info
        self.leftDoorsLabel.setText("Left Doors\t\t" + self.controller.getLeftDoorState())
        self.rightDoorsLabel.setText("Right Doors\t\t" + self.controller.getRightDoorState())
        self.lightsLabel.setText("Lights\t\t\t" + self.controller.getLightState())
        self.tempLabel.setText("Temperature\t\t" + str(self.controller.temperature) + " *F")
        
        #Update failure info
        self.engineFailureLabel.setText("Engine\t\t\t" + self.controller.getEngineFailureStatus())
        self.brakeFailureLabel.setText("Brakes\t\t\t" + self.controller.getBrakeFailureStatus())
        self.signalFailureLabel.setText("Signal Pickup\t\t" + self.controller.getSignalFailureStatus())  
        self.interactiveSetpointLabel.setText("%.2f mph" % (self.controller.speedSetpoint*2.23694))
        self.tempSetpointLabel.setText(str(self.controller.temperature) + " *F")
        
        #Update Test UI Info
        self.eLabel.setText("e = %.2f" % self.controller.e)
        self.ePrevLabel.setText("ePrev = %.2f" % self.controller.ePrevUsed)
        self.uLabel.setText("u = %.2f" % self.controller.uK)
        self.uPrevLabel.setText("uPrev = %.2f" % self.controller.uKPrevUsed)
        self.kpLabel.setText("kp = " + str(self.controller.kP))
        self.kiLabel.setText("ki = " + str(self.controller.kI))
        self.TLabel.setText("T = " + str(self.controller.T))
        
        
        if(self.controller.currentSpeed == 0):
            self.controlLeftDoorsButton.setDisabled(False)
            self.controlRightDoorsButton.setDisabled(False)
        else:
            self.controlLeftDoorsButton.setDisabled(True)
            self.controlRightDoorsButton.setDisabled(True)
        
"""
class Cycle(QRunnable):
	t: Train
	tc: TrainController
	def __init__(self, train, controller):
		super().__init__()
		self.t = train
		self.tc = controller
		
	def run(self):
		while(1):
			time.sleep(.1)
			self.tc.recalculateAttributes()
			self.t.update()

def back():
		return
def main():
	app = QApplication(sys.argv)
	t = Train(100, 5, 5, 2000, 0, 222, 80, 2, 0.5, 20, 2.73, 1.2, 120000)
	t.set("timeStep",.1)
	tc = TrainController(.1,t)
	window = controlWindow(tc,back)
	
	loop = Cycle(t,tc)
	threadpool = QtCore.QThreadPool()
	threadpool.start(loop)
	window.show()
	sys.exit(app.exec_())
	


if __name__ == '__main__':
	main()
"""
