# Written 11 - 29 -2020
# Author: Morgana Iacocca - morgana.iacocca@gmail.com
# Purpose: To simulate models of trains

# imports
import math
from random import randrange
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPropertyAnimation, QPoint

#from ControllerGroup import ControllerGroup
#from Train_Controller import TrainController

# The Interfacing class, that all other classes talk to when they want to interact with a train
class TrainModelInterface:
   def __init__(self, dtime, controllerGroup, trackModel):
      self.controllerGroup = controllerGroup
      self.trackModel = trackModel
      self.trains = {}
      
      self.trashTrains = {}
      
      self.dtime = dtime
      self.IDcount = 1
      self.trainSelWindow = 0
      
      
      self.needsToUpdate = False

   # addTrain() adds a train to the internal dictionary of trains
   # Inputs: None
   # Outputs: None
   def addTrain(self):
      newTrain = Train(100, 5, 5, 2000, 0, 222, 80, 2, 0.5, 20, 2.73, 1.2, 120000, self.controllerGroup, self.trackModel)
      self.trains[self.IDcount] = newTrain
      self.IDcount += 1
      self.needsToUpdate = True 
   
   
   # removeTrain() removes a train from the internal dictionary of trains
   # Inputs: ID (int) is theID of the train being removed
   # Outputs: None   
   def removeTrain(self, ID):
     x = self.trains.pop(ID)
     
     self.trashTrains[ID] = x
     
     self.needsToUpdate = True
   
   # setWindow() sets internal TrainSelectWindow
   # Inputs: window (TrainSelectWindow) is the window being set
   # Ouputs: None  
   def setWindow(self, window):
      self.trainSelWindow = window
     
   # update() updates all trains and GUIs
   # Inputs: None
   # Ouputs: None
   def update(self):
      if(self.needsToUpdate):
         if(self.trainSelWindow != 0):
            self.trainSelWindow.update()
            self.needsToUpdate = False
      for trainID in self.trains:
         self.trains[trainID].update(self.dtime)    

# This is a train  
class Train:
   def __init__(self, length, width, height, mass, passengers, maxPassengers, averagePersonWeight, crew, maxAccel, maxSpeed, eBrakeDecel, serviceBrakeDecel, maxPower, controllerGroup, trackModel):
      
      # Data dictionary stores all data in a train
      self.data = {}
      
      # Window is the GUI window associated with each train
      self.window= 0
      self.controllerGroup = controllerGroup
      
      ct = self.controllerGroup.addController(self)
      self.trackModel = trackModel
      self.trainController = ct
      
      self.data["length"] = length # m
      self.data["width"] = width # m
      self.data["height"] = height # m
      self.data["mass"] = mass # kg
      self.data["passengers"] = passengers # count
      self.data["maxPassengers"] = maxPassengers
      self.data["averagePersonWeight"] = averagePersonWeight # kg
      self.data["crew"] = crew # count
      self.data["totalMass"] = mass + averagePersonWeight*(crew + passengers)# count
      self.data["maxAccel"] = maxAccel # m/s^2
      self.data["maxSpeed"] = maxSpeed # m/s
      self.data["timeStep"] = 1 # seconds
      self.data["maxForce"] = 1000000 # newtons, not a real value, just a big number
      self.data["eBrakeDecel"] = eBrakeDecel
      self.data["serviceBrakeDecel"] = serviceBrakeDecel
      self.data["maxPower"] = maxPower
      
      self.data["lastVelocity"] = 0
      self.data["currentVelocity"] = 0
      
      self.data["lastAcceleration"] = 0
      self.data["currentAcceleration"] = 0
      
      # For Track Model
      
      self.data["lastBlock"] = 0 # ID number
      self.data["currentBlock"] = self.trackModel.getBlock(0).defaultConnection
      
      # From CTC
      
      self.data["authority"] = True
      self.data["suggestedSpeed"] = 0 # Renamed suggestedSpeed, in km/hr

      
      # From Track Model
      
      self.data["trackGrade"] = 0.0 
      self.data["trackElevation"] = 0.0
      self.data["trackLength"] = 0.0 # m
      
      self.data["upcomingStop"] = "Unknown"
      self.data["stopSide"] = "Both"
      
      # From train controller
      
      self.data["lightsOn"] = False
      self.data["doorsClosed"] = True
      self.data["announcingStop"] = False
      self.data["temperature"] = 67.0 # Fahrenheight
      self.data["power"] = 0
      
      # For train controller 
      
      self.data["engineFailure"] = False
      self.data["brakeFailure"] = False
      self.data["signalFailure"] = False
      
      self.data["eBrakeEngaged"] = False
      self.data["serviceBrakeEngaged"] = False
      
      self.trackModel.getBlock(self.data["currentBlock"]).addOccupancy(self)
   
   # setController() sets the train's train controller
   # Inputs: controller (TrainController)
   # Outputs: None
   def setController(self, controller):
      self.trainController = controller
   
   # sendBeaconData() sends the beacon data to the train controller
   # Inputs: beaconData (str)
   # Outputs: None
   def sendBeaconData(self, beaconData):
      self.trainController.sendBeacon(beaconData)
      
      
   # setTrackCircuit() decodes track circuit signal stores decoded data to internal variables
   # Inputs: signal (bytes)
   # Outputs: None
   def setTrackCircuit(self, signal: bytes):
      if(self.data["signalFailure"]):
         pass
      else:
         signalString = signal.decode()[2:]
         if signalString[0] == "1":
            authorityString = signalString[1:4]
            speedString = signalString[4:]
            authority = (authorityString == "111")
            speed = int(speedString, 2)
         else:
            authority = False
            speed = 0
         self.set("suggestedSpeed", speed)
         self.set("authority", authority)
   
   # set() sets a value of a key-value pair in the data dictionary to a new value
   # Inputs: name (str) is the name of the key in the dictionary being updated
   #         val <Type T> is the new value replacing the old value of the key-value pair
   # Outputs: Returns True if the data was successfully updated
   #          Returns False if the key is not in the dictionary         
   def set(self, name, val):
      if(name not in self.data):
         return False
      else:
         # Absolutely zero type checking, so lets use this CAREFULLY
         self.data[name] = val
         return True
   
   # get() returns the value of the key-value pair in the data dictionary at the specified key
   # Inputs: name (str) is the name of the key in the dictionary whose value is being retrieved
   # Outputs: Returns value of the key-value pair in the data dictionary
   def get(self, name):
      if(name not in self.data):
         return None
      else:
         return self.data[name]
   
   # stopAtStation() exchanges passengers with the station on the current block
   # Inputs: None
   # Outputs: None
   def stopAtStation(self):
        self.trackModel.getBlock(self.data["currentBlock"]).getStation().exchangePassengers(self)

   # exchangePassengers() calculates a random number of passengers to deboard, deboards them,
   #                      and then boards the number of passengers waiting to board at the station
   #                      up to the carrying capacity of the train and no more
   # Inputs: numPassengers (int) is the number of passengers trying to board the train
   # Outputs: numDeboarded (int) is the number of passengers who got off the train
   def exchangePassengers(self, numPassengers):
        numDeboarded = randrange(0,self.data["passengers"]+1)
        self.data["passengers"] = self.data["passengers"] - numDeboarded

        self.data["passengers"] += numPassengers
        if(self.data["passengers"] > self.data["maxPassengers"]):
            self.data["passengers"] = self.data["maxPassengers"]
        self.data["totalMass"] = self.data["mass"] + self.data["averagePersonWeight"]*self.data["passengers"]
        return numDeboarded

   # updateSpeed() calculates the new speed of the train based on current speed, 
   #               the input power, the grade of the track, and the status of the brakes
   #               and any failure modes
   # Inputs: None
   # Outputs: None
   def updateSpeed(self):
      forceApplied = 0.0
      if(abs(self.data["currentVelocity"]) < 0.0001):
         if(self.data["power"] > 0):
            forceApplied = self.data["maxForce"]
         else:
            forceApplied = 0.0
      else:
         forceApplied = self.data["power"]/self.data["currentVelocity"]
      self.data["lastAcceleration"] = self.data["currentAcceleration"]
      
      if (self.data["engineFailure"]):
         forceApplied = 0.0
      
      # Grade contributions
      slope = self.data["trackGrade"]/(100.0)
      angleOfSlope = math.atan(abs(slope))
      gravForceSloped = 9.8*self.data["totalMass"]*math.sin(angleOfSlope)
      if(self.data["trackGrade"] >= 0):
         forceApplied = forceApplied - gravForceSloped
      else:
         forceApplied = forceApplied + gravForceSloped
      
      self.data["currentAcceleration"] = min(forceApplied/self.data["totalMass"], self.data["maxAccel"])
      
      # Brake Considerations
      
      decel = 0
      if (self.data["eBrakeEngaged"]):
         decel = self.data["eBrakeDecel"]
      elif(self.data["serviceBrakeEngaged"]):
         if(self.data["brakeFailure"]):
            decel = 0
         else:
            decel = self.data["serviceBrakeDecel"]
      
      self.data["currentAcceleration"] = self.data["currentAcceleration"] - decel
      
      # Calculate velocities and distances
            
      self.data["lastVelocity"] = self.data["currentVelocity"]
      self.data["currentVelocity"] = self.data["lastVelocity"] + (self.data["timeStep"]/2)*(self.data["lastAcceleration"] + self.data["currentAcceleration"])
      
      if(self.data["currentVelocity"] < 0 ):
         self.data["currentVelocity"] = 0
         self.data["currentAcceleration"] = 0
      
      distTraveled = (self.data["timeStep"]/2)*(self.data["lastVelocity"] + self.data["currentVelocity"])
      self.data["trackLength"] = self.data["trackLength"] - distTraveled
   
   # update() steps the train through time and updates the GUI window associated with it
   # Inputs: dTime (float) is the amount of time that has passed
   # Outputs: None
   def update(self, dtime): # add dTime
      self.data["timeStep"] = dtime
      self.updateSpeed()
      if(self.data["trackLength"] < 0):
         self.trackModel.getBlock(self.data["currentBlock"]).getNextBlock(self)
      if(self.window != 0):      
        if(self.window.doneInit):
            self.window.updateTrain()

# Widget that shows ads and moved them side to side
class adWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        OGpixmap = QPixmap("ads.jpg")
        pixmap = OGpixmap.scaledToHeight(100)
        self.ad1 = QLabel(self)
        self.ad1.setPixmap(pixmap)
        
        self.anim1 = QPropertyAnimation(self.ad1, b"pos")
        self.anim1.setEndValue(QPoint(-300, 0))
        self.anim1.setDuration(6000)
        
        self.anim2 = QPropertyAnimation(self.ad1, b"pos")
        self.anim2.setEndValue(QPoint(0, 0))
        self.anim2.setDuration(6000)
        
        self.animGroup = QSequentialAnimationGroup()
        self.animGroup.addAnimation(self.anim1)
        self.animGroup.addAnimation(self.anim2)
        
        self.animGroup.setLoopCount(500000)
        self.animGroup.start()

# This is the home window that includes a drop down menu for each of the trains
class TrainSelectWindow(QWidget):
   def __init__(self, trainInterface, homeFunction):
      super().__init__()
      
      self.homeFunction = homeFunction
      self.trainWindows = []
      self.trainInterface = trainInterface
      self.trainInterface.setWindow(self)
      self.IDdict = {}

      self.initUI()
   
   # initUI() initializes the UI of the GUI
   # Inputs: None
   # Outputs: None
   def initUI(self):
      self.setWindowTitle("Train Select")
            
      self.dropDownMenu = QComboBox()
      self.dropDownMenu.addItem("Select Train:")
      
      self.IDdict = {}
      count = 1
      for ID in self.trainInterface.trains:
         self.dropDownMenu.addItem("Train " + str(ID))
         self.IDdict[count] = ID
         count+=1
         
      self.dropDownMenu.currentIndexChanged.connect(self.indexChanged)   
      
      self.dropDownInnerLayout = QHBoxLayout()
      self.dropDownInnerLayout.addWidget(QWidget(), 20)
      self.dropDownInnerLayout.addWidget(self.dropDownMenu, 60)
      self.dropDownInnerLayout.addWidget(QWidget(), 20)
      
      self.dropDownOuterLayout = QVBoxLayout()
      self.dropDownOuterLayout.addWidget(QWidget(), 20)
      self.dropDownOuterLayout.addWidget(QLabel("Please Select a Train:"), 15)
      self.dropDownOuterLayout.addWidget(self.dropDownMenu, 20)
      self.dropDownOuterLayout.addWidget(QWidget(), 45)
      
      self.dropDownInnerLayout = QHBoxLayout()
      self.dropDownInnerLayout.addWidget(QWidget(), 20)
      self.dropDownInnerLayout.addLayout(self.dropDownOuterLayout, 60)
      self.dropDownInnerLayout.addWidget(QWidget(), 20)


      self.dropDownMenu.setFixedSize(QSize(500, 20))
      self.dropDownGroup = QGroupBox("")
      self.dropDownGroup.setLayout(self.dropDownInnerLayout)
            
      self.backButtonLayout = QHBoxLayout()
      backButton = QPushButton("Home")
      backButton.pressed.connect(self.homeFunction)
      self.backButtonLayout.addWidget(backButton, 5)
      self.backButtonLayout.addWidget(QWidget(), 95)
      
      self.layout = QVBoxLayout()
      self.layout.addLayout(self.backButtonLayout, 5)
      self.layout.addWidget(self.dropDownGroup, 95)
            
      self.setLayout(self.layout)
      
      self.setMinimumSize(QSize(1000, 800))
      self.show()
   
   # indexChanged() opens a window for a train selected from a drop down menu
   # Inputs: index (int) is the index of the drop down menu
   # Outputs: None
   def indexChanged(self, index):
      if(index == 0):
         pass
      else:
         ID = self.IDdict[index]
         trainChosen = self.trainInterface.trains[ID]
         tw = TrainWindow(trainChosen, ID)
         self.trainWindows.append(tw)
         tw.show()
         self.dropDownMenu.setCurrentIndex(0)
         
   # update() updates the train select window to make sure it has all current trains
   # Inputs: None
   # Outputs: None   
   def update(self):
      self.dropDownMenu.clear()
      self.dropDownMenu.addItem("Select Train:")
      self.IDdict = {}
      count = 1
      for ID in self.trainInterface.trains:
         self.dropDownMenu.addItem("Train " + str(ID))
         self.IDdict[count] = ID
         count+=1
         
      self.dropDownMenu.setCurrentIndex(0)

# This class paints circles of a given color
class circlePainter(QWidget):
   def __init__(self, color):
      super().__init__()

      self.initUI(color)

   # initUI() initializes the UI of the circle
   # Inputs: None
   # Outputs: None
   def initUI(self, color):

      self.color = color

   # paintEvent() paints a circle when an the paint event is called
   # Inputs: event
   # Outputs: None
   def paintEvent(self, event):
      size = self.frameSize()
      x = 50 #size.width()
      y = 50 #size.height()
      d = min(x, y)
      painter = QPainter()
      painter.begin(self)
      painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
      painter.setBrush(QBrush(self.color, Qt.SolidPattern))
      painter.drawEllipse(math.floor(d/4.0), math.floor(y/2.0-d/4.0), math.floor(d/2.0), math.floor(d/2.0))
      painter.end()

# the trainPainter class paints train graphics in a widget
class trainPainter(QWidget):
   def __init__(self, left, right, lights):
      super().__init__()
      self.left = left
      self.right = right
      self.lights = lights
      self.initUI()

   # initUI() does nothing
   # Inputs: None
   # Outputs: None
   def initUI(self):

      self.text = "testttt"
   
   # paintEvent() paints the train 
   # Inputs: event ()
   # Outputs: None
   def paintEvent(self, event):
      size = self.frameSize()
      x = size.width()
      y = size.height()
      painter = QPainter()
      painter.begin(self)
      painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
      painter.drawLine(math.floor(x/3), math.floor(y/8), math.floor(x/3), math.floor(y/4))
      painter.drawLine(math.floor(2*x/3), math.floor(y/8), math.floor(2*x/3), math.floor(y/4))
      painter.drawLine(math.floor(x/3), math.floor(y/8), math.floor(2*x/3), math.floor(y/8))
      
      painter.drawLine(math.floor(x/3), math.floor(3*y/8), math.floor(x/3), math.floor(5*y/8))
      painter.drawLine(math.floor(2*x/3), math.floor(3*y/8), math.floor(2*x/3), math.floor(5*y/8))
      
      painter.drawLine(math.floor(x/3), math.floor(6*y/8), math.floor(x/3), math.floor(7*y/8))
      painter.drawLine(math.floor(2*x/3), math.floor(6*y/8), math.floor(2*x/3), math.floor(7*y/8))
      painter.drawLine(math.floor(x/3), math.floor(7*y/8), math.floor(2*x/3), math.floor(7*y/8))
      
      # headlights
      if(self.lights):
         points = [QPoint(math.floor(4*x/9), math.floor(y/8)),
                   QPoint(math.floor(x/2), math.floor(y/16)),
                   QPoint(math.floor(5*x/9), math.floor(y/8)),
                   QPoint(math.floor(6*x/9), 1),
                   QPoint(math.floor(3*x/9), 1)]
         painter.setPen(QPen(Qt.yellow, 2, Qt.SolidLine))
         painter.setBrush(QBrush(Qt.yellow, Qt.Dense4Pattern))
         headlightPolygon = QPolygon(points)
         
         painter.drawPolygon(headlightPolygon)
         
      # left doors
      if(self.left):
         painter.setPen(QPen(Qt.green, 4, Qt.SolidLine))
         painter.drawLine(math.floor(x/3)-6, math.floor(3*y/16), math.floor(x/3)-6, math.floor(y/4))
         painter.drawLine(math.floor(x/3)-6, math.floor(3*y/8), math.floor(x/3)-6, math.floor(7*y/16))
         painter.drawLine(math.floor(x/3)-6, math.floor(9*y/16), math.floor(x/3)-6, math.floor(5*y/8))
         painter.drawLine(math.floor(x/3)-6, math.floor(6*y/8), math.floor(x/3)-6, math.floor(13*y/16))
      else:
         painter.setPen(QPen(Qt.blue, 6, Qt.SolidLine))
         painter.drawLine(math.floor(x/3), math.floor(y/4), math.floor(x/3), math.floor(3*y/8))
         painter.drawLine(math.floor(x/3), math.floor(5*y/8), math.floor(x/3), math.floor(6*y/8))
      # right doors
      if(self.right):
         painter.setPen(QPen(Qt.green, 4, Qt.SolidLine))
         painter.drawLine(math.floor(2*x/3)+6, math.floor(3*y/16), math.floor(2*x/3)+6, math.floor(y/4))
         painter.drawLine(math.floor(2*x/3)+6, math.floor(3*y/8), math.floor(2*x/3)+6, math.floor(7*y/16))
         painter.drawLine(math.floor(2*x/3)+6, math.floor(9*y/16), math.floor(2*x/3)+6, math.floor(5*y/8))
         painter.drawLine(math.floor(2*x/3)+6, math.floor(6*y/8), math.floor(2*x/3)+6, math.floor(13*y/16))
      else:
         painter.setPen(QPen(Qt.blue, 6, Qt.SolidLine))
         painter.drawLine(math.floor(2*x/3), math.floor(y/4), math.floor(2*x/3), math.floor(3*y/8))
         painter.drawLine(math.floor(2*x/3), math.floor(5*y/8), math.floor(2*x/3), math.floor(6*y/8))
      painter.end()

# The Train Window is the GUI for each individual train
class TrainWindow(QWidget):
   doneInit = False
   def __init__(self, train, ID):
      super().__init__()
      self.doneInit = False
      self.ID = ID      
      self.train = train
      self.train.window = self
      self.simulation = True
      
      self.data = {}
      self.outputs = {}
      
      self.currentLayout = QStackedLayout()
      self.initUI()
      self.doneInit = True
  
   # initUI() initializes the GUI of the train window
   # Inputs: None
   # Outputs: None
   def initUI(self):
      
      '''self.currentPowerInput = ""
      
      beautyLabel = QLabel("Input Power Here: ")
      
      
      self.speedDisplay = QLabel("Current Speed = 0 m/s")
      font = self.speedDisplay.font()
      font.setPointSize(30)
      self.speedDisplay.setFont(font)
      self.speedDisplay.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
      
      self.powerInput = QLineEdit()
      self.powerInput.textChanged.connect(self.changePowerInput)
      
      self.calculateButton = QPushButton("Calculate Speed")
      self.calculateButton.setCheckable(True)
      self.calculateButton.clicked.connect(self.makeTrainCalculateSpeed)

      test = QHBoxLayout()
      test.addWidget(beautyLabel)
      test.addWidget(self.powerInput)

      layout = QVBoxLayout()
      layout.addLayout(test)
      layout.addWidget(self.speedDisplay)
      layout.addWidget(self.calculateButton)
   
      container = QWidget()
      container.setLayout(layout)'''
      
      trainPhysicalOuter = QVBoxLayout()
      trainPhysical = QVBoxLayout()
      trainStatus = QVBoxLayout()
      trainDetails = QVBoxLayout()
      
      ### Train Physical
      
      physicalGroupBox = QGroupBox("Train " + str(self.ID) + " Hardware")
      physicalGroupBox.setLayout(trainPhysical)
      
      # Back Button
      '''backButtonLayout = QHBoxLayout()
      backButton = QPushButton("Back")
      backButton.pressed.connect(self.backFunction)
      backButtonLayout.addWidget(backButton)
      backButtonLayout.addWidget(QWidget())
      backButtonLayout.addWidget(QWidget())
      trainPhysicalOuter.addLayout(backButtonLayout, 5)'''
      
      self.adAnim = adWindow()
      
      trainPhysicalOuter.addWidget(QWidget(), 5)
      trainPhysicalOuter.addWidget(physicalGroupBox, 75)
      trainPhysicalOuter.addWidget(self.adAnim, 20)

      # Internal Display:
      internalDisplayLayout = QVBoxLayout()
      displayDeco = QLabel("Current Display Reading:")
      self.displayOutput = QLabel("")
      self.displayOutput.setStyleSheet("color: red; background-color: grey; border: 1px solid black;")
      self.displayOutput.setFont(QFont('courier', 18, QFont.Bold))
      internalDisplayLayout.addWidget(displayDeco, 30)
      internalDisplayLayout.addWidget(self.displayOutput, 70)
      
      trainPhysical.addLayout(internalDisplayLayout, 10)
      
      # Thermometer Display:
      thermomenterDisplayLayout = QHBoxLayout()
      thermometerDeco = QLabel("Current \nTemperature:")
      
      self.outputs["temperature"] = QLabel(str(self.train.data["temperature"]) + " F")
      self.outputs["temperature"].setStyleSheet("color: lightblue; background-color: grey; border: 1px solid black;")
      self.outputs["temperature"].setFont(QFont('courier', 18, QFont.Bold))
      thermomenterDisplayLayout.addWidget(thermometerDeco, 30)
      thermomenterDisplayLayout.addWidget(self.outputs["temperature"] , 70)
      trainPhysical.addLayout(thermomenterDisplayLayout, 10)
      
      # Add train image
      self.currentTrainPaint = QStackedLayout()
      self.currentTrainPaint.addWidget(trainPainter(False, False, True)) # Both closed, light on
      self.currentTrainPaint.addWidget(trainPainter(False, False, False)) # Both closed, light off
      self.currentTrainPaint.addWidget(trainPainter(True, False, True)) # left open, light on
      self.currentTrainPaint.addWidget(trainPainter(True, False, False)) # left open, light off
      self.currentTrainPaint.addWidget(trainPainter(False, True, True)) # right open, light on
      self.currentTrainPaint.addWidget(trainPainter(False, True, False)) # right open, light off
      self.currentTrainPaint.addWidget(trainPainter(True, True, True)) # both open, light on
      self.currentTrainPaint.addWidget(trainPainter(True, True, False)) # both open, light off
      self.currentTrainPaint.setCurrentIndex(1)
      trainPhysical.addLayout(self.currentTrainPaint, 70)
      
      # E Brake:
      eBrakeButton = QPushButton("Emergency\nBrake")
      eBrakeButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
      eBrakeButton.setCheckable(True)
      eBrakeButton.clicked.connect(self.toggleEBrake)
      eBrakeButton.setStyleSheet("background-color : red")
      eBrakeButton.setFont(QFont('Courier', 24, QFont.Bold))
      trainPhysical.addWidget(eBrakeButton, 10)
      
      ### Train Status
      
      # Switch Modes
      modeButtonLayout = QHBoxLayout()
      simulationButton = QPushButton("Simulation")
      simulationButton.pressed.connect(self.switchToSimulation)
      
      testingButton = QPushButton("Testing Commands")
      testingButton.pressed.connect(self.switchToTesting)
      
      modeButtonLayout.addWidget(QWidget(), 30)
      modeButtonLayout.addWidget(simulationButton, 20)
      modeButtonLayout.addWidget(testingButton, 20)
      modeButtonLayout.addWidget(QWidget(), 30)
      modeButtonLayout.setSpacing(0)
      trainStatus.addLayout(modeButtonLayout, 5)
      
      # Status - Sim
      
      statusGroupBox = QGroupBox("Train Status")
      simulationLayout = QVBoxLayout()
      simulationLayout.setSpacing(2)
      statusGroupBox.setLayout(simulationLayout)
      
      # Lights
      simRow1Layout = QHBoxLayout()
      self.currentDoorLight = QStackedLayout()
      self.currentDoorLight.addWidget(circlePainter(Qt.gray))
      self.currentDoorLight.addWidget(circlePainter(Qt.green))
      
      if(self.train.data["doorsClosed"]):
         self.currentDoorLight.setCurrentIndex(1)
      
      simRow1Layout.addLayout(self.currentDoorLight, 15)
      simRow1Layout.addWidget(QWidget(), 5)
      simRow1Layout.addWidget(QLabel("\nDoors Closed\n"), 25)
      simRow1Layout.addWidget(QWidget(), 5)
      
      self.currentSignalFailureLight = QStackedLayout()
      self.currentSignalFailureLight.addWidget(circlePainter(Qt.gray))
      self.currentSignalFailureLight.addWidget(circlePainter(Qt.red))
      
      if(self.train.data["signalFailure"]):
         self.currentSignalFailureLight.setCurrentIndex(1)
         
      simRow1Layout.addLayout(self.currentSignalFailureLight, 15)
      simRow1Layout.addWidget(QWidget(), 5)
      simRow1Layout.addWidget(QLabel("\nSignal Pickup\nFailure\n"), 25)
      simRow1Layout.addWidget(QWidget(), 5)
      
      simulationLayout.addLayout(simRow1Layout, 10)
      
      simRow2Layout = QHBoxLayout()
      
      self.currentHeadlightLight = QStackedLayout()
      self.currentHeadlightLight.addWidget(circlePainter(Qt.gray))
      self.currentHeadlightLight.addWidget(circlePainter(Qt.green))
      
      if(self.train.data["lightsOn"]):
         self.currentDoorLight.setCurrentIndex(1)
         
      simRow2Layout.addLayout(self.currentHeadlightLight, 15)
      simRow2Layout.addWidget(QWidget(), 5)
      simRow2Layout.addWidget(QLabel("\nHeadlights On\n"), 25)
      simRow2Layout.addWidget(QWidget(), 5)
      
      self.currentEngineFailureLight = QStackedLayout()
      self.currentEngineFailureLight.addWidget(circlePainter(Qt.gray))
      self.currentEngineFailureLight.addWidget(circlePainter(Qt.red))
      
      if(self.train.data["engineFailure"]):
         self.currentEngineFailureLight.setCurrentIndex(1)
         
      simRow2Layout.addLayout(self.currentEngineFailureLight, 15)
      simRow2Layout.addWidget(QWidget(), 5)
      simRow2Layout.addWidget(QLabel("\nEngine\nFailure\n"), 25)
      simRow2Layout.addWidget(QWidget(), 5)
      
      simulationLayout.addLayout(simRow2Layout, 10)
      
      simRow3Layout = QHBoxLayout()
      
      
      self.currentAnnouncementLight = QStackedLayout()
      self.currentAnnouncementLight.addWidget(circlePainter(Qt.gray))
      self.currentAnnouncementLight.addWidget(circlePainter(Qt.green))
      
      if(self.train.data["announcingStop"]):
         self.currentAnnouncementLight.setCurrentIndex(1)
         
      simRow3Layout.addLayout(self.currentAnnouncementLight, 15)
      simRow3Layout.addWidget(QWidget(), 5)
      simRow3Layout.addWidget(QLabel("\nAnnouncing\nStop\n"), 25)
      simRow3Layout.addWidget(QWidget(), 5)
      
      self.currentBrakeFailureLight = QStackedLayout()
      self.currentBrakeFailureLight.addWidget(circlePainter(Qt.gray))
      self.currentBrakeFailureLight.addWidget(circlePainter(Qt.red))
      
      if(self.train.data["brakeFailure"]):
         self.currentBrakeFailureLight.setCurrentIndex(1)
         
      simRow3Layout.addLayout(self.currentBrakeFailureLight, 15)
      simRow3Layout.addWidget(QWidget(), 5)
      simRow3Layout.addWidget(QLabel("\nBrake\nFailure\n"), 25)
      simRow3Layout.addWidget(QWidget(), 5)
      
      simulationLayout.addLayout(simRow3Layout, 10)
      
      simRow4Layout = QHBoxLayout()
      
      self.currentServiceBrakeLight = QStackedLayout()
      self.currentServiceBrakeLight.addWidget(circlePainter(Qt.gray))
      self.currentServiceBrakeLight.addWidget(circlePainter(Qt.green))
      
      if(self.train.data["serviceBrakeEngaged"]):
         self.currentServiceBrakeLight.setCurrentIndex(1)
         
      simRow4Layout.addLayout(self.currentServiceBrakeLight, 15)
      simRow4Layout.addWidget(QWidget(), 5)
      simRow4Layout.addWidget(QLabel("Service\nBrake\nEngaged"), 25)
      simRow4Layout.addWidget(QWidget(), 5)
      
      self.currentEBrakeLight = QStackedLayout()
      self.currentEBrakeLight.addWidget(circlePainter(Qt.gray))
      self.currentEBrakeLight.addWidget(circlePainter(Qt.green))
      
      if(self.train.data["eBrakeEngaged"]):
         self.currentEBrakeLight.setCurrentIndex(1)
         
      simRow4Layout.addLayout(self.currentEBrakeLight, 15)
      simRow4Layout.addWidget(QWidget(), 5)
      simRow4Layout.addWidget(QLabel("Emergency\nBrake\nEngaged"), 25)
      simRow4Layout.addWidget(QWidget(), 5)
      
      simulationLayout.addLayout(simRow4Layout, 10)
      
      # Displays
      simRow5Layout = QHBoxLayout()
      
      authorityLabel = QLabel("Authority")
      authorityLabel.setFont(QFont('Arial', 8))
      simRow5Layout.addWidget(authorityLabel, 15)
      self.outputs["authority"] = QLabel(str(self.train.data["authority"]))
      self.outputs["authority"].setFont(QFont("Arial", 10))
      self.outputs["authority"].setStyleSheet("font-family: Courier; font-weight: bold; color: purple; background-color: grey; border: 4px solid black;")
      #self.outputs["authority"].setFont(QFont("Courier", 20))
      self.outputs["authority"].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      simRow5Layout.addWidget(self.outputs["authority"], 30)
      simRow5Layout.addWidget(QWidget(), 5)
      
      suggSpeedLabel = QLabel("Suggested\nSpeed\n(mph)")
      suggSpeedLabel.setFont(QFont('Arial', 8))
      simRow5Layout.addWidget(suggSpeedLabel, 15)
      self.outputs["suggestedSpeed"] = QLabel(str(2.23694*self.train.data["suggestedSpeed"]))
      self.outputs["suggestedSpeed"].setFont(QFont("Arial", 10))
      self.outputs["suggestedSpeed"].setStyleSheet("font-family: Courier; font-weight: bold; color: purple; background-color: grey; border: 4px solid black;")
      self.outputs["suggestedSpeed"].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      simRow5Layout.addWidget(self.outputs["suggestedSpeed"], 30)
      simRow5Layout.addWidget(QWidget(), 5)
      
      simulationLayout.addLayout(simRow5Layout, 10)
      
      simRow6Layout = QHBoxLayout()
      
      powerLabel = QLabel("Power\n(W)")
      powerLabel.setFont(QFont('Arial', 8))
      simRow6Layout.addWidget(powerLabel, 15)
      self.outputs["power"] = QLabel(str(self.train.data["power"]))
      self.outputs["power"].setFont(QFont("Arial", 10))
      self.outputs["power"].setStyleSheet("font-family: Courier; font-weight: bold; color: purple; background-color: grey; border: 4px solid black;")
      self.outputs["power"].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      simRow6Layout.addWidget(self.outputs["power"], 30)
      simRow6Layout.addWidget(QWidget(), 5)
      
      currentSpeedLabel = QLabel("Current\nSpeed\n(mph)")
      currentSpeedLabel.setFont(QFont('Arial', 8))
      simRow6Layout.addWidget(currentSpeedLabel, 15)
      self.outputs["currentVelocity"] = QLabel(str(2.23694*self.train.data["currentVelocity"]))
      self.outputs["currentVelocity"].setFont(QFont("Arial", 10))
      self.outputs["currentVelocity"].setStyleSheet("font-family: Courier; font-weight: bold; color: purple; background-color: grey; border: 4px solid black;")
      self.outputs["currentVelocity"].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      simRow6Layout.addWidget(self.outputs["currentVelocity"], 30)
      simRow6Layout.addWidget(QWidget(), 5)
      
      simulationLayout.addLayout(simRow6Layout, 10)
      
      simRow7Layout = QHBoxLayout()
      
      trackGradeLabel = QLabel("Track\nGrade\n(%)")
      trackGradeLabel.setFont(QFont('Arial', 8))
      simRow7Layout.addWidget(trackGradeLabel, 15)
      self.outputs["trackGrade"] = QLabel(str(self.train.data["trackGrade"]))
      self.outputs["trackGrade"].setFont(QFont("Arial", 10))
      self.outputs["trackGrade"].setStyleSheet("font-family: Courier; font-weight: bold; color: purple; background-color: grey; border: 4px solid black;")
      self.outputs["trackGrade"].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      simRow7Layout.addWidget(self.outputs["trackGrade"], 30)
      simRow7Layout.addWidget(QWidget(), 5)
      
      trackElevationLabel = QLabel("Track\nElevation\n(ft)")
      trackElevationLabel.setFont(QFont('Arial', 8))
      simRow7Layout.addWidget(trackElevationLabel, 15)
      self.outputs["trackElevation"] = QLabel(str(self.train.data["trackElevation"]))
      self.outputs["trackElevation"].setFont(QFont("Arial", 10))
      self.outputs["trackElevation"].setStyleSheet("font-family: Courier; font-weight: bold; color: purple; background-color: grey; border: 4px solid black;")
      self.outputs["trackElevation"].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      simRow7Layout.addWidget(self.outputs["trackElevation"], 30)
      simRow7Layout.addWidget(QWidget(), 5)   
         
      simulationLayout.addLayout(simRow7Layout, 10)
      
      simRow8Layout = QHBoxLayout()
      
      currentAccelLabel = QLabel("Current\nAccel\n(ft/s^2)")
      currentAccelLabel.setFont(QFont('Arial', 8))
      simRow8Layout.addWidget(currentAccelLabel, 15)
      self.outputs["currentAcceleration"] = QLabel(str(self.train.data["currentAcceleration"]))
      self.outputs["currentAcceleration"].setFont(QFont("Arial", 10))
      self.outputs["currentAcceleration"].setStyleSheet("font-family: Courier; font-weight: bold; color: purple; background-color: grey; border: 4px solid black;")
      self.outputs["currentAcceleration"].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      simRow8Layout.addWidget(self.outputs["currentAcceleration"], 30)
      simRow8Layout.addWidget(QWidget(), 5)
      
      trackLengthLabel = QLabel("Block\nLength\nLeft (ft)")
      trackLengthLabel.setFont(QFont('Arial', 8))
      simRow8Layout.addWidget(trackLengthLabel, 15)
      self.outputs["trackLength"] = QLabel(str(self.train.data["trackLength"]))
      self.outputs["trackLength"].setFont(QFont("Arial", 10))
      self.outputs["trackLength"].setStyleSheet("font-family: Courier; font-weight: bold; color: purple; background-color: grey; border: 4px solid black;")
      self.outputs["trackLength"].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      simRow8Layout.addWidget(self.outputs["trackLength"], 30)
      simRow8Layout.addWidget(QWidget(), 5)
      
      simulationLayout.addLayout(simRow8Layout, 10)
      
      simRow9Layout = QHBoxLayout()
      
      stationNameLabel = QLabel("Station\nName\n")
      stationNameLabel.setFont(QFont('Arial', 8))
      simRow9Layout.addWidget(stationNameLabel, 15)
      self.outputs["upcomingStop"] = QLabel(str(self.train.data["upcomingStop"]))
      self.outputs["upcomingStop"].setFont(QFont("Arial", 10))
      self.outputs["upcomingStop"].setStyleSheet("font-family: Courier; font-weight: bold; color: purple; background-color: grey; border: 4px solid black;")
      self.outputs["upcomingStop"].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      simRow9Layout.addWidget(self.outputs["upcomingStop"], 30)
      simRow9Layout.addWidget(QWidget(), 5)
      
      stopSideLabel = QLabel("Station\nSide\n")
      stopSideLabel.setFont(QFont('Arial', 8))
      simRow9Layout.addWidget(stopSideLabel, 15)
      self.outputs["stopSide"] = QLabel(str(self.train.data["stopSide"]))
      self.outputs["stopSide"].setFont(QFont("Arial", 10))
      self.outputs["stopSide"].setStyleSheet("font-family: Courier; font-weight: bold; color: purple; background-color: grey; border: 4px solid black;")
      self.outputs["stopSide"].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      simRow9Layout.addWidget(self.outputs["stopSide"], 30)
      simRow9Layout.addWidget(QWidget(), 5)
      
      simulationLayout.addLayout(simRow9Layout, 10)
      
      simRow10Layout = QHBoxLayout()
      
      passengerLabel = QLabel("Num\nRiders")
      passengerLabel.setFont(QFont('Arial', 8))
      simRow10Layout.addWidget(passengerLabel, 15)
      self.outputs["passengers"] = QLabel(str(self.train.data["passengers"]))
      self.outputs["passengers"].setFont(QFont("Arial", 10))
      self.outputs["passengers"].setStyleSheet("font-family: Courier; font-weight: bold; color: purple; background-color: grey; border: 4px solid black;")
      self.outputs["passengers"].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      simRow10Layout.addWidget(self.outputs["passengers"], 30)
      simRow10Layout.addWidget(QWidget(), 5)
      
      totalMassLabel = QLabel("Total\nWeight\n(lbs)")
      totalMassLabel.setFont(QFont('Arial', 8))
      simRow10Layout.addWidget(totalMassLabel, 15)
      self.outputs["totalMass"] = QLabel(str(self.train.data["totalMass"]))
      self.outputs["totalMass"].setFont(QFont("Arial", 10))
      self.outputs["totalMass"].setStyleSheet("font-family: Courier; font-weight: bold; color: purple; background-color: grey; border: 4px solid black;")
      self.outputs["totalMass"].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      simRow10Layout.addWidget(self.outputs["totalMass"], 30)
      simRow10Layout.addWidget(QWidget(), 5)
      
      simulationLayout.addLayout(simRow10Layout, 10)
      simulationLayout.setSpacing(10)
      
      
      # Testing Commands
      
      controlsGroupBox = QGroupBox("Train " + str(self.ID) + " Status")
      controlsLayout = QVBoxLayout()
      controlsLayout.setSpacing(2)
      controlsGroupBox.setLayout(controlsLayout)
      
      # Buttons
      buttonsAndTogglesLayout = QHBoxLayout()
      controlButtonsLayout = QVBoxLayout()
      
      controlButtonsRow1 = QHBoxLayout()
      failEngineButton = QPushButton("Fail\nEngine")
      failEngineButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
      failEngineButton.pressed.connect(self.failEngine)
      controlButtonsRow1.addWidget(failEngineButton)
      failBrakesButton = QPushButton("Fail\nBrakes")
      failBrakesButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
      failBrakesButton.pressed.connect(self.failBrakes)
      controlButtonsRow1.addWidget(failBrakesButton)
      cutSignalButton = QPushButton("Cut\nSignal")
      cutSignalButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
      cutSignalButton.pressed.connect(self.cutSignal)
      controlButtonsRow1.addWidget(cutSignalButton)
      
      controlButtonsLayout.addLayout(controlButtonsRow1)
      
      controlButtonsRow2 = QHBoxLayout()
      fixEngineButton = QPushButton("Fix\nEngine")
      fixEngineButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
      fixEngineButton.pressed.connect(self.fixEngine)
      controlButtonsRow2.addWidget(fixEngineButton)
      fixBrakesButton = QPushButton("Fix\nBrakes")
      fixBrakesButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
      fixBrakesButton.pressed.connect(self.fixBrakes)
      controlButtonsRow2.addWidget(fixBrakesButton)
      repairSignalButton = QPushButton("Repair\nSignal")
      repairSignalButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
      repairSignalButton.pressed.connect(self.repairSignal)
      controlButtonsRow2.addWidget(repairSignalButton)
      
      controlButtonsLayout.addLayout(controlButtonsRow2)
      
      controlButtonsRow3 = QHBoxLayout()
      controlButtonsRow3.addWidget(QWidget(),33)
      updateTrainButton = QPushButton("Update Train\n and \nCalculate Velocity")
      updateTrainButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
      updateTrainButton.pressed.connect(self.updateTrain)
      controlButtonsRow3.addWidget(updateTrainButton,33)
      controlButtonsRow3.addWidget(QWidget(),33)
      
      controlButtonsLayout.addLayout(controlButtonsRow3)
      buttonsAndTogglesLayout.addLayout(controlButtonsLayout, 50)
      
      # Toggles
      togglesLayout = QVBoxLayout()
      
      eBrakeToggle = QPushButton("Engage E-Brake")
      eBrakeToggle.setCheckable(True)
      eBrakeToggle.clicked.connect(self.toggleEBrake)
      togglesLayout.addWidget(eBrakeToggle)
      
      
      serviceBrakeToggle = QPushButton("Engage Service Brake")
      serviceBrakeToggle.setCheckable(True)
      serviceBrakeToggle.clicked.connect(self.toggleServiceBrake)
      togglesLayout.addWidget(serviceBrakeToggle)
      
      
      lightsToggle = QPushButton("Headlights On")
      lightsToggle.setCheckable(True)
      lightsToggle.clicked.connect(self.toggleLights)
      togglesLayout.addWidget(lightsToggle)
      
      
      doorToggle = QPushButton("Open Door")
      doorToggle.setCheckable(True)
      doorToggle.clicked.connect(self.toggleDoor)
      togglesLayout.addWidget(doorToggle)
      
      announceStopToggle = QPushButton("Announce Stop")
      announceStopToggle.setCheckable(True)
      announceStopToggle.clicked.connect(self.toggleAnnounce)
      togglesLayout.addWidget(announceStopToggle)
      
      doorSideToggle = QHBoxLayout()
      leftDoorButton = QRadioButton("Left", self)
      leftDoorButton.toggled.connect(self.updateDoorSide)
      bothDoorButton = QRadioButton("Both", self)
      bothDoorButton.toggled.connect(self.updateDoorSide)
      rightDoorButton = QRadioButton("Right", self)
      rightDoorButton.toggled.connect(self.updateDoorSide)
      
      # implement updating function for this toggle
      doorSideToggle.addWidget(leftDoorButton)
      doorSideToggle.addWidget(bothDoorButton)
      doorSideToggle.addWidget(rightDoorButton)
      
      togglesLayout.addLayout(doorSideToggle)
      buttonsAndTogglesLayout.addWidget(QWidget(), 15)
      buttonsAndTogglesLayout.addLayout(togglesLayout, 35)
      
      controlsLayout.addLayout(buttonsAndTogglesLayout, 50)
      
      # Inputs
      
      inputLayout = QVBoxLayout()
      
      # Row 6 --- ill renumber them later, i just think this looks better first
      inputRow6Layout = QHBoxLayout()
      
      inputRow6Layout.addWidget(QWidget(),60)
      
      self.data["temperature"] = ""
      temperatureInput = QLineEdit("Enter temperature (F)")
      temperatureInput.textChanged.connect(lambda: self.changeMyData("temperature", temperatureInput.text()))
      inputRow6Layout.addWidget(temperatureInput, 20)
      

      setTemperatureButton = QPushButton("Set Temperature")
      setTemperatureButton.pressed.connect(lambda: self.updateTrainData("temperature"))
      inputRow6Layout.addWidget(setTemperatureButton, 20)
      
      inputLayout.addLayout(inputRow6Layout,10)
      inputLayout.addWidget(QWidget(), 10)
      # Row 1
      inputRow1Layout = QHBoxLayout()
      
      self.data["power"] = ""
      powerInput = QLineEdit("Enter Wattage Here")
      powerInput.textChanged.connect(lambda: self.changeMyData("power", powerInput.text()))
      inputRow1Layout.addWidget(powerInput,20)
      
      setPowerButton = QPushButton("Set Power\nConsumption (W)")
      setPowerButton.pressed.connect(lambda: self.updateTrainData("power"))
      inputRow1Layout.addWidget(setPowerButton,20)
      
      inputRow1Layout.addWidget(QWidget(),20)
      
      self.data["authority"] = ""
      authorityInput = QLineEdit("Enter Authority Here (km)")
      authorityInput.textChanged.connect(lambda: self.changeMyData("authority", authorityInput.text()))
      inputRow1Layout.addWidget(QWidget(), 20)
      
      setAuthorityButton = QPushButton("Toggle Authority")
      setAuthorityButton.setCheckable(True)
      setAuthorityButton.clicked.connect(self.toggleAuthority)
      inputRow1Layout.addWidget(setAuthorityButton, 20)
      
      inputLayout.addLayout(inputRow1Layout,10)
      inputLayout.addWidget(QWidget(), 10)
      
      # Row 2
      
      inputRow2Layout = QHBoxLayout()
      
      self.data["numPeopleBoard"] = ""
      boardInput = QLineEdit("Enter number boarded")
      boardInput.textChanged.connect(lambda: self.changeMyData("numPeopleBoard", boardInput.text()))
      inputRow2Layout.addWidget(boardInput,20)
      
      boardButton = QPushButton("Board people")
      boardButton.pressed.connect(self.boardPassengers)
      inputRow2Layout.addWidget(boardButton, 20)
      
      inputRow2Layout.addWidget(QWidget(),20)
      
      self.data["numPeopleDeboard"] = ""
      deboardInput = QLineEdit("Enter number deboarded")
      deboardInput.textChanged.connect(lambda: self.changeMyData("numPeopleDeboard", deboardInput.text()))
      inputRow2Layout.addWidget(deboardInput, 20)
      
      deboardButton = QPushButton("Deboard people")
      deboardButton.pressed.connect(self.deboardPassengers)
      inputRow2Layout.addWidget(deboardButton, 20)
      
      inputLayout.addLayout(inputRow2Layout, 10)
      inputLayout.addWidget(QWidget(), 10)
      
      
      
      # Row 3
      
      inputRow3Layout = QHBoxLayout()
      
      self.data["upcomingStop"] = ""
      stationNameInput = QLineEdit("Enter station name")
      stationNameInput.textChanged.connect(lambda: self.changeMyData("upcomingStop", stationNameInput.text()))
      inputRow3Layout.addWidget(stationNameInput,20)
      
      setStationNameButton = QPushButton("Set Station\nName")
      setStationNameButton.pressed.connect(lambda: self.updateTrainData("upcomingStop"))
      inputRow3Layout.addWidget(setStationNameButton, 20)
      
      inputRow3Layout.addWidget(QWidget(),20)
      
      self.data["trackLength"] = ""
      trackLengthInput = QLineEdit("Enter block length (m)")
      trackLengthInput.textChanged.connect(lambda: self.changeMyData("trackLength", trackLengthInput.text()))
      inputRow3Layout.addWidget(trackLengthInput, 20)
      
      setStationDistanceButton = QPushButton("Set Station\nDistance")
      setStationDistanceButton.pressed.connect(lambda: self.updateTrainData("trackLength"))
      inputRow3Layout.addWidget(setStationDistanceButton, 20)
      
      inputLayout.addLayout(inputRow3Layout,10)
      inputLayout.addWidget(QWidget(), 10)
      
      # Row 4
      inputRow4Layout = QHBoxLayout()
      
      self.data["trackGrade"] = ""
      trackGradeInput = QLineEdit("Enter track grade (%)")
      trackGradeInput.textChanged.connect(lambda: self.changeMyData("trackGrade", trackGradeInput.text()))
      inputRow4Layout.addWidget(trackGradeInput,20)
      
      setTrackGradeButton = QPushButton("Set Track\nGrade")
      setTrackGradeButton.pressed.connect(lambda: self.updateTrainData("trackGrade"))
      inputRow4Layout.addWidget(setTrackGradeButton, 20)
      
      inputRow4Layout.addWidget(QWidget(),20)
      
      self.data["trackElevation"] = ""
      trackElevationInput = QLineEdit("Enter track elevation (m)")
      trackElevationInput.textChanged.connect(lambda: self.changeMyData("trackElevation", trackElevationInput.text()))
      inputRow4Layout.addWidget(trackElevationInput, 20)
      

      setTrackElevationButton = QPushButton("Set Track\nElevation")
      setTrackElevationButton.pressed.connect(lambda: self.updateTrainData("trackElevation"))
      inputRow4Layout.addWidget(setTrackElevationButton, 20)
      
      inputLayout.addLayout(inputRow4Layout,10)
      inputLayout.addWidget(QWidget(), 10)
      
      # Row 5
      inputRow5Layout = QHBoxLayout()
      
      self.data["suggestedSpeed"] = ""
      commandedSpeedInput = QLineEdit("Enter suggested speed (m/s)")
      commandedSpeedInput.textChanged.connect(lambda: self.changeMyData("suggestedSpeed", commandedSpeedInput.text()))
      inputRow5Layout.addWidget(commandedSpeedInput,20)
      
      setCommandedSpeedButton = QPushButton("Set Commanded\nSpeed")
      setCommandedSpeedButton.pressed.connect(lambda: self.updateTrainData("suggestedSpeed"))
      inputRow5Layout.addWidget(setCommandedSpeedButton, 20)
      
      inputRow5Layout.addWidget(QWidget(),20)
      
      self.data["currentVelocity"] = ""
      currentSpeedInput = QLineEdit("Enter current speed (m/s)")
      currentSpeedInput.textChanged.connect(lambda: self.changeMyData("currentVelocity", currentSpeedInput.text()))
      inputRow5Layout.addWidget(currentSpeedInput, 20)
      

      setCurrentSpeedButton = QPushButton("Set Current\nSpeed")
      setCurrentSpeedButton.pressed.connect(lambda: self.updateTrainData("currentVelocity"))
      inputRow5Layout.addWidget(setCurrentSpeedButton, 20)
      
      inputLayout.addLayout(inputRow5Layout,10)
      
      
      
      # 
      #self.simulationGroupBox = statusGroupBox
      #self.testingGroupBox = controlsGroupBox
      
      controlsLayout.addWidget(QWidget(), 5)
      controlsLayout.addLayout(inputLayout, 45)
      
      self.currentLayout = QStackedLayout()
      self.currentLayout.addWidget(statusGroupBox)
      self.currentLayout.addWidget(controlsGroupBox)
      
      trainStatus.addLayout(self.currentLayout, 95) 
      
      # Train Details
      detailsGroupBox = QGroupBox("Train " + str(self.ID) + " Details")
      detailsLayout = QVBoxLayout()
      detailsLayout.setSpacing(2)
      detailsGroupBox.setLayout(detailsLayout)

      
      detailRow1Layout = QHBoxLayout()
      detailRow1Layout.addWidget(QLabel("Train Length"), 60)
      detailRow1Layout.addWidget(QLabel(str(self.train.data["length"])+" m"), 40)
      detailsLayout.addLayout(detailRow1Layout)
      
      detailRow2Layout = QHBoxLayout()
      detailRow2Layout.addWidget(QLabel("Train Width"), 60)
      detailRow2Layout.addWidget(QLabel(str(self.train.data["width"])+" m"), 40)
      detailsLayout.addLayout(detailRow2Layout)
      
      detailRow3Layout = QHBoxLayout()
      detailRow3Layout.addWidget(QLabel("Train Height"), 60)
      detailRow3Layout.addWidget(QLabel(str(self.train.data["height"])+" m"), 40)
      detailsLayout.addLayout(detailRow3Layout)
      
      detailRow4Layout = QHBoxLayout()
      detailRow4Layout.addWidget(QLabel("Maximum Speed"), 60)
      detailRow4Layout.addWidget(QLabel(str(self.train.data["maxSpeed"])+" m/s"), 40)
      detailsLayout.addLayout(detailRow4Layout)
      
      detailRow5Layout = QHBoxLayout()
      detailRow5Layout.addWidget(QLabel("Maximum\nAcceleration"), 60)
      detailRow5Layout.addWidget(QLabel(str(self.train.data["maxAccel"])+" m/s^2"), 40)
      detailsLayout.addLayout(detailRow5Layout)
      
      detailRow6Layout = QHBoxLayout()
      detailRow6Layout.addWidget(QLabel("Emergency Brake\nDeceleration"), 60)
      detailRow6Layout.addWidget(QLabel(str(self.train.data["eBrakeDecel"])+" m/s^2"), 40)
      detailsLayout.addLayout(detailRow6Layout)
      
      detailRow7Layout = QHBoxLayout()
      detailRow7Layout.addWidget(QLabel("Service Brake\nDeceleration"), 60)
      detailRow7Layout.addWidget(QLabel(str(self.train.data["serviceBrakeDecel"])+" m/s^2"), 40)
      detailsLayout.addLayout(detailRow7Layout)
      
      detailRow8Layout = QHBoxLayout()
      detailRow8Layout.addWidget(QLabel("Maximum\nPassengers"), 60)
      detailRow8Layout.addWidget(QLabel(str(self.train.data["maxPassengers"])), 40)
      detailsLayout.addLayout(detailRow8Layout)
      
      detailRow9Layout = QHBoxLayout()
      detailRow9Layout.addWidget(QLabel("Crew Onboard"), 60)
      detailRow9Layout.addWidget(QLabel(str(self.train.data["crew"])), 40)
      detailsLayout.addLayout(detailRow9Layout)
      
      trainDetails.addWidget(QWidget(), 5)
      trainDetails.addWidget(detailsGroupBox, 95)
      
      
      
      layout = QGridLayout()
      layout.addLayout(trainPhysicalOuter, 0,0)
      layout.addLayout(trainStatus,0,1)
      layout.addLayout(trainDetails,0,2)
      layout.setColumnStretch(0,1)
      layout.setColumnStretch(1,3)
      layout.setColumnStretch(2,1)
      layout.setSpacing(10)
      #layout.setContentsMargin(0, 0, 0, 0)
      #layout.addLayout(trainStatus)
      #layout.addLayout(trainDetails)
      
      container = QWidget()
      container.setLayout(layout)

        # Set the central widget of the Window.
      self.setLayout(layout)
      #print(self.frameSize())
      #self.setFixedSize(QSize(750, 600))
      
      self.updateTrain()
   
   # updateTrain() updates the train window with all of the current data values of the train
   # Inputs: None
   # Outputs: None
   def updateTrain(self):
      self.outputs["authority"].setText(str(self.train.data["authority"]))
      self.outputs["suggestedSpeed"].setText("%.2f" % (0.6213*self.train.data["suggestedSpeed"]))
      self.outputs["power"].setText("%.1f" % self.train.data["power"])
      self.outputs["currentVelocity"].setText("%.2f" % (2.23694*self.train.data["currentVelocity"]))
      self.outputs["trackGrade"].setText("%.2f" % self.train.data["trackGrade"])
      self.outputs["trackElevation"].setText("%.2f" % (3.28084*self.train.data["trackElevation"]))
      self.outputs["currentAcceleration"].setText("%.2f" % (3.2808399*self.train.data["currentAcceleration"]))
      self.outputs["trackLength"].setText("%.2f" % (3.28084*self.train.data["trackLength"]))
      self.outputs["upcomingStop"].setText(self.train.data["upcomingStop"])
      self.outputs["stopSide"].setText(self.train.data["stopSide"])
      self.outputs["passengers"].setText(str(self.train.data["passengers"]))
      self.outputs["totalMass"].setText("%.2f" % (2.20462*self.train.data["totalMass"]))
      self.outputs["temperature"].setText(str(self.train.data["temperature"]) + " F")
      
      if(self.train.data["doorsClosed"]):
         self.currentDoorLight.setCurrentIndex(1)
      else:
         self.currentDoorLight.setCurrentIndex(0)
      
      if(self.train.data["lightsOn"]):
         self.currentHeadlightLight.setCurrentIndex(1)
      else:
         self.currentHeadlightLight.setCurrentIndex(0)
      
      if(self.train.data["announcingStop"]):
         self.displayOutput.setText(self.train.data["upcomingStop"])
         self.currentAnnouncementLight.setCurrentIndex(1)
      else:
         self.displayOutput.setText("")
         self.currentAnnouncementLight.setCurrentIndex(0)
         
      if(self.train.data["eBrakeEngaged"]):
         self.currentEBrakeLight.setCurrentIndex(1)
      else:
         self.currentEBrakeLight.setCurrentIndex(0)    
         
      if(self.train.data["serviceBrakeEngaged"]):
         self.currentServiceBrakeLight.setCurrentIndex(1)
      else:
         self.currentServiceBrakeLight.setCurrentIndex(0)              
      
      if(self.train.data["engineFailure"]):
         self.currentEngineFailureLight.setCurrentIndex(1)
      else:
         self.currentEngineFailureLight.setCurrentIndex(0)
         
      if(self.train.data["brakeFailure"]):
         self.currentBrakeFailureLight.setCurrentIndex(1)
      else:
         self.currentBrakeFailureLight.setCurrentIndex(0)
         
      if(self.train.data["signalFailure"]):
         self.currentSignalFailureLight.setCurrentIndex(1)
      else:
         self.currentSignalFailureLight.setCurrentIndex(0)
         
      self.updateTrainDisplay()
      
   # changeMyData updates the data of the window based on inputs from the GUI
   #              NOTE: THIS DOES NOT UPDATE THE TRAIN DATA
   # Inputs: dataName (str) is the name of the data being updated (the key of the key-value pair)
   #         newData () is the newData being written to the window's internal data (value of key-value pair)
   # Outputs: None
   def changeMyData(self, dataName, newData):
      self.data[dataName] = newData
   
   # updateTrainData() pushes the window data to the train object
   #                   NOTE: THIS ONE CHANGES THE TRAIN'S DATA
   # Inputs: dataName (str) is the name of the data being pushed to the Train object
   # Outputs: None
   def updateTrainData(self, dataName):
      if(dataName == "upcomingStop"):
         self.train.data["upcomingStop"] = self.data["upcomingStop"]
         self.outputs["upcomingStop"].setText(self.data["upcomingStop"])
      else:
         try:
            newData = float(self.data[dataName])
            self.train.data[dataName] = newData
            self.outputs[dataName].setText(str(newData))
         except ValueError:
            print("Not a float, please try again")
            return   

   # boardPassengers() moves the number of passengers onto the train if there's enough room
   # Inputs: None
   # Outputs: None
   def boardPassengers(self):
      passengerCount = 0
      try:
         passengerCount = int(self.data["numPeopleBoard"])
      except ValueError:
         print("Not an int, please try again")
         return
      totalPassengers = self.train.data["passengers"] + passengerCount
      if(totalPassengers > self.train.data["maxPassengers"]):
         totalPassengers = self.train.data["maxPassengers"]
      totalMass = float(self.train.data["mass"]) + float(self.train.data["averagePersonWeight"])*(totalPassengers + int(self.train.data["crew"]))   
      self.outputs["passengers"].setText(str(totalPassengers))
      self.outputs["totalMass"].setText(str(totalMass))
      self.train.data["passengers"] = totalPassengers
      self.train.data["totalMass"] = totalMass
   
   # deboardPassengers() moves the number of passengers off the train if there's enough room
   # Inputs: None
   # Outputs: None
   def deboardPassengers(self):
      passengerCount = 0
      try:
         passengerCount = int(self.data["numPeopleDeboard"])
      except ValueError:
         print("Not an int, please try again")
         return
      totalPassengers = int(self.train.data["passengers"]) - passengerCount
      if(totalPassengers < 0):
         totalPassengers = 0
      totalMass = float(self.train.data["mass"]) + float(self.train.data["averagePersonWeight"])*(totalPassengers + int(self.train.data["crew"]))
      self.outputs["passengers"].setText(str(totalPassengers))
      self.outputs["totalMass"].setText(str(totalMass))
      self.train.data["passengers"] = totalPassengers
      self.train.data["totalMass"] = totalMass
      
   # switchToSimulation() changes the current view to include the simulation layout
   # Inputs: None
   # Outputs: None
   def switchToSimulation(self):
      self.currentLayout.setCurrentIndex(0)
   
   # switchToTesting() changes the current view to include the simulation layout
   # Inputs: None
   # Outputs: None
   def switchToTesting(self):
      self.currentLayout.setCurrentIndex(1)
   
   # updateTrainDisplay() changes the drawing of the train in the window to match current train data
   # Inputs: None
   # Outputs: None
   def updateTrainDisplay(self):
      if(self.train.data["doorsClosed"]):
         if(self.train.data["lightsOn"]):
            self.currentTrainPaint.setCurrentIndex(0)
         else:
            self.currentTrainPaint.setCurrentIndex(1)
      else:
         if(self.train.data["lightsOn"]):
            if(self.train.data["stopSide"] == "Left"):
               self.currentTrainPaint.setCurrentIndex(2)
            elif(self.train.data["stopSide"] == "Right"):
               self.currentTrainPaint.setCurrentIndex(4)
            else:
               self.currentTrainPaint.setCurrentIndex(6)
         else:
            if(self.train.data["stopSide"] == "Left"):
               self.currentTrainPaint.setCurrentIndex(3)
            elif(self.train.data["stopSide"] == "Right"):
               self.currentTrainPaint.setCurrentIndex(5)
            else:
               self.currentTrainPaint.setCurrentIndex(7)

   # toggleAuthority() toggles the Authority of the current track
   # Inputs: None
   # Outputs: None         
   def toggleAuthority(self):
      if(self.train.data["authority"]):
         self.train.data["authority"] = False
         self.outputs["authority"].setText(str(self.train.data["authority"]))
      else:
         self.train.data["authority"] = True
         self.outputs["authority"].setText(str(self.train.data["authority"]))      
   
   # toggleDoor() toggles the status of the door
   # Inputs: None
   # Outputs: None  
   def toggleDoor(self):
      if(self.train.data["doorsClosed"]):
         self.train.data["doorsClosed"] = False
         self.currentDoorLight.setCurrentIndex(0)
      else:
         self.train.data["doorsClosed"] = True
         self.currentDoorLight.setCurrentIndex(1)
      self.updateTrainDisplay()

   # toggleLights() toggles the status of the lights
   # Inputs: None
   # Outputs: None 
   def toggleLights(self):
      if(self.train.data["lightsOn"]):
         self.train.data["lightsOn"] = False
         self.currentHeadlightLight.setCurrentIndex(0)
      else:
         self.train.data["lightsOn"] = True
         self.currentHeadlightLight.setCurrentIndex(1)
      self.updateTrainDisplay()

   # toggleEBrake() toggles the status of the emergency brake
   # Inputs: None
   # Outputs: None 
   def toggleEBrake(self):
      if(self.train.data["eBrakeEngaged"]):
         self.train.data["eBrakeEngaged"] = False
         self.currentEBrakeLight.setCurrentIndex(0)
      else:
         self.train.data["eBrakeEngaged"] = True
         self.currentEBrakeLight.setCurrentIndex(1) 
   
   # toggleServiceBreke() toggles the status of the service brake
   # Inputs: None
   # Outputs: None 
   def toggleServiceBrake(self):
      if(self.train.data["serviceBrakeEngaged"]):
         self.train.data["serviceBrakeEngaged"] = False
         self.currentServiceBrakeLight.setCurrentIndex(0)
      else:
         self.train.data["serviceBrakeEngaged"] = True
         self.currentServiceBrakeLight.setCurrentIndex(1)  
   
   # toggleAnnounce() toggles the status of announcing the current station
   # Inputs: None
   # Outputs: None 
   def toggleAnnounce(self):
      if(self.train.data["announcingStop"]):
         self.train.data["announcingStop"] = False
         self.displayOutput.setText("")
         self.currentAnnouncementLight.setCurrentIndex(0)
      else:
         self.train.data["announcingStop"] = True
         self.displayOutput.setText(self.train.data["upcomingStop"])  
         self.currentAnnouncementLight.setCurrentIndex(1)    

   # updateDoorSide() updates the value of the side the station is on
   # Inputs: value (None)
   # Outputs: None
   def updateDoorSide(self, value):
      sideToggled = self.sender()
      
      if (sideToggled.isChecked() == True):
         self.train.data["stopSide"] = sideToggled.text()
         self.outputs["stopSide"].setText(sideToggled.text())

   # failEngine() sets the engine failure status to true
   # Inputs: None
   # Outputs: None
   def failEngine(self):
      self.train.data["engineFailure"] = True
      self.currentEngineFailureLight.setCurrentIndex(1)         

   # failBrakes() sets the brake failure status to true
   # Inputs: None
   # Outputs: None
   def failBrakes(self):
      self.train.data["brakeFailure"] = True
      self.currentBrakeFailureLight.setCurrentIndex(1) 

   # cutSignal() sets the signal failure status to true
   # Inputs: None
   # Outputs: None
   def cutSignal(self):
      self.train.data["signalFailure"] = True
      self.currentSignalFailureLight.setCurrentIndex(1) 
      
   # fixEngine() sets the engine failure status to False
   # Inputs: None
   # Outputs: None
   def fixEngine(self):
      self.train.data["engineFailure"] = False
      self.currentEngineFailureLight.setCurrentIndex(0)         

   # fixBrakes() sets the brake failure status to False
   # Inputs: None
   # Outputs: None
   def fixBrakes(self):
      self.train.data["brakeFailure"] = False
      self.currentBrakeFailureLight.setCurrentIndex(0) 

   # repairSignal() sets the signal failure status to False
   # Inputs: None
   # Outputs: None
   def repairSignal(self):
      self.train.data["signalFailure"] = False
      self.currentSignalFailureLight.setCurrentIndex(0)

      
#myControllerGroup = ControllerGroup(0.1, "something")     # FILL THIS IN  
#myInterface = TrainModelInterface(0.1, myControllerGroup)
#Train(length, width, height, mass, passengers, maxPassengers, averagePersonWeight, crew, maxAccel, maxSpeed, eBrakeDecel, sBrakeDecel, maxPower)


#testTrain = Train(100, 5, 5, 2000, 0, 222, 80, 2, 0.5, 20, 2.73, 1.2, 120000)
#myInterface.addTrain(testTrain)


#app = QApplication(sys.argv)
#window = TrainSelectWindow(myInterface)
#window.show()
#app.exec()
       
