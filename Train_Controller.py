from SpeedLimit import SpeedLimit

class TrainController:
    window = 0
    speedLimits: SpeedLimit
    #Constants
    maxPower = 120000
    minimumTemp = 55
    maximumTemp = 85
    timerBaseDuration = 10
    train: object
    #speedLimits: SpeedLimit
    
    #Attributes that require setting
    currentSpeed = 0
    speedSetpoint = 0
    suggestedSpeed = 0
    maximumSpeed = 19.4444
    engineFailure = 0
    brakeFailure = 0
    signalPickupFailure = 0
    wheelSlippageFailure = 0
    authority = 0
    side = "Both"
    timer = 0
    
    nextStop = 'Uknown'
    temperature = 67
    
    kP = 400
    kI = 20
    inTunnel = 0
    atStation = 0
    
    #Attributes that are toggled
    serviceBrake = 0
    emergencyBrake = 0
    leftDoors = 0
    rightDoors = 0
    lights = 0
    mode = 0

    #Attributes to store to calculate power
    e = 0
    ePrevious = 0
    ePrevUsed = 0
    uK = 0
    uKPrevious = 0
    uKPrevUsed = 0
    T = 1

    #Attributes that require calculation
    power = 0
    
    #Constructor
    def __init__(self, period, inputTrain):
        self.speedLimits = SpeedLimit()
        self.T = period
        self.train = inputTrain
        self.train.set("temperature", self.temperature)
        
    #Set Methods
    def setSpeedSetpoint(self, x):
        self.speedSetpoint = x
    def setMaximumSpeed(self, x):
        self.maximumSpeed = x
    def setAuthority(self, x):
        self.authority = x
    def setNextStop(self, x):
        self.nextStop = x
    def setCurrentSpeed(self, x):
        self.currentSpeed = x
    def setFailures(self, w, x, y, z):
        self.engineFailure = w
        self.brakeFailure = x
        self.signalPickupFailure = y
        self.wheelSlippageFailure = z
    def setErrorMessage(self, x):
        self.errorMessage = x
    def setKValues(self, x, y):
        self.kP = x
        self.kI = y
    def setPeriod(self, x):
        self.T = 1

    def setBeaconInfo(self, x, y):
        self.inTunnel = x
        self.atStation = y
    
    #Toggle Methods
    def toggleServiceBrake(self):
        self.serviceBrake = not self.serviceBrake
        self.train.set("serviceBrakeEngaged", self.serviceBrake)
        
    def toggleEmergencyBrake(self):
        self.emergencyBrake = not self.emergencyBrake
        self.train.set("eBrakeEngaged", self.emergencyBrake)
        
    def toggleLeftDoors(self):
        self.leftDoors = not self.leftDoors
        self.setTrainDoorStates()
    
    def toggleRightDoors(self):
        self.rightDoors = not self.rightDoors
        self.setTrainDoorStates()
        
    def setTrainDoorStates(self):
        if(self.rightDoors and self.leftDoors):
            self.train.set("stopSide", "Both")
            self.train.set("doorsClosed", False)
        elif(self.rightDoors):
            self.train.set("stopSide", "Right")
            self.train.set("doorsClosed", False)
            
        elif(self.leftDoors):
            self.train.set("stopSide", "Left")
            self.train.set("doorsClosed", False)
        else:
            self.train.set("stopSide", "Both")
            self.train.set("doorsClosed", True)

    def toggleLights(self):
        self.lights = not self.lights
        self.train.set("lightsOn", self.lights)
        
    def toggleMode(self):
        self.mode = not self.mode
        
    def toggleEngineFailure(self):
        self.engineFailure = not self.engineFailure
        
    def toggleBrakeFailure(self):
        self.brakeFailure = not self.brakeFailure
        
    def toggleSignalFailure(self):
        self.signalPickupFailure = not self.signalPickupFailure
        
    def toggleWheelFailure(self):
        self.wheelSlippageFailure = not self.wheelSlippageFailure
        
    #Get Methods
    def getPower(self):
        return self.power
    def getServiceBrakeState(self):
        if (self.serviceBrake == 0):
            return 'Off'
        else:
            return 'On'
    def getEmergencyBrakeState(self):
        if (self.emergencyBrake == 0):
            return 'Off'
        else:
            return 'On'
    def getLeftDoorState(self):
        if (self.leftDoors == 0):
            return 'Closed'
        else:
            return 'Open'
    def getRightDoorState(self):
        if (self.rightDoors == 0):
            return 'Closed'
        else:
            return 'Open'
    def getLightState(self):
        if (self.lights == 0):
            return 'Off'
        else:
            return 'On'
    def getEngineFailureStatus(self):
        if (self.engineFailure == 0):
            return 'Functional'
        else:
            return 'Failure'
    def getBrakeFailureStatus(self):
        if (self.brakeFailure == 0):
            return 'Functional'
        else:
            return 'Failure'
    def getSignalFailureStatus(self):
        if (self.signalPickupFailure == 0):
            return 'Functional'
        else:
            return 'Failure'
    def getWheelSlippageStatus(self):
        if (self.wheelSlippageFailure == 0):
            return 'Functional'
        else:
            return 'Slipping'
    def getAuthorityState(self):
        if(self.authority == 0):
            return 'No'
        else:
            return 'Yes'
    def getStoppingStatus(self):
        if(self.timer == self.timerBaseDuration/self.T):
            return 'Stopping at Station...'
        elif(self.timer > 0):
            return 'Stopped!'
        else:
            return 'Proceeding to Next Station'
    
    def sendBeacon(self, beaconString):
        self.maximumSpeed = self.speedLimits.getNextSpeedLimit(beaconString)*.277778
        #Trunacte speed setpoint to speed limit if setpoint is over the speed limit upon transitioning blocks
        if(self.speedSetpoint > self.maximumSpeed):
            self.speedSetpoint = self.maximumSpeed
			
        if(beaconString.find("Underground:") > -1):
            self.inTunnel = not self.inTunnel
            if(self.inTunnel == 1 and self.lights == 0):
                self.toggleLights()
            elif(self.inTunnel == 0 and self.lights == 1):
                self.toggleLights()
        
        if(beaconString.find("Station:") > -1):
            if(self.atStation == 1):
                self.atStation = 0
                startLocation = beaconString.find("NextStation:") + len("NextStation:")
                endLocation = beaconString.find(":",startLocation)
                self.nextStop = beaconString[startLocation:endLocation]
                self.train.set("upcomingStop", self.nextStop)
                
            elif(beaconString.find("Side:") > -1):
                self.atStation = 1    
                self.timer = self.timerBaseDuration/self.T
                startLocation = beaconString.find("Side:") + len("Side:")
                endLocation = beaconString.find(":",startLocation)
                self.side = beaconString[startLocation:endLocation]
                
                self.train.set("announcingStop", True)
            else:
                startLocation = beaconString.find("Station:") + len("Station:")
                endLocation = beaconString.find(":",startLocation)
                self.nextStop = beaconString[startLocation:endLocation]
                self.train.set("upcomingStop", self.nextStop)    
            
    #Function for redundancy for calculating power - made by Steph
    def checkPower(self, currentSpeed, setpoint, oldE, oldU):
		
		#Finds power like in lecture slides
        E = setpoint - currentSpeed
        if(self.power < self.maxPower):
            U = oldU + (self.T/2)*(E - oldE)
        else:
            U = oldU
        power = self.kP*E + self.kI*U
        if power > self.maxPower:
            power = self.maxPower
        if power < 0:
            power = 0
        #Checks that the calculated power is the same
        if(power != self.power):
            print("Error: Train Controller powers do not agree.")
		
		
        
    #Calculate Methods
    def recalculateAttributes(self):
        self.suggestedSpeed = self.train.get("suggestedSpeed")*0.277778
        self.currentSpeed = self.train.get("currentVelocity")
        self.emergencyBrake = self.train.get("eBrakeEngaged")
        self.engineFailure = self.train.get("engineFailure")
        self.signalPickupFailure = self.train.get("brakeFailure")
        self.signalPickupFailure = self.train.get("signalFailure")
        self.authority = self.train.get("authority")
      
        #Used in test UI
        self.ePrevUsed = self.ePrevious
        self.uKPrevUsed = self.uKPrevious
        
        
        #Emergency from failure
        if ((self.engineFailure or self.brakeFailure or self.signalPickupFailure or self.wheelSlippageFailure) and self.emergencyBrake == 0):
            self.toggleEmergencyBrake()
        
        
                
        #Overwrite speed setpoint in automatic mode to suggested speed
        if (self.mode == 0):
            self.speedSetpoint = self.suggestedSpeed
			
            
         
        
        if(self.authority == 0):
            self.speedSetpoint = 0
        
        #Timer to force stops at stations for predefined duration
        if(self.timer > 0):
            self.speedSetpoint = 0
            
            #When speed reaches zero, we want to do a variety of things while timer is running
            if(self.currentSpeed == 0):
				#Open doors when we come to a stop
                if(self.timer == self.timerBaseDuration/self.T):
                    self.train.stopAtStation()
                    if(self.side == "Left"):
                        if(self.leftDoors == 0):
                            self.toggleLeftDoors()
                        if(self.rightDoors == 1):
                            self.toggleRightDoors()
                    elif(self.side == "Right"):
                        if(self.leftDoors == 1):
                            self.toggleLeftDoors()
                        if(self.rightDoors == 0):
                            self.toggleRightDoors()
                    else:
                        if(self.leftDoors == 0):
                            self.toggleLeftDoors()
                        if(self.rightDoors == 0):
                            self.toggleRightDoors()
                #Close doors and stop announcing station when we start are going to start moving again
                elif(self.timer == 1):
                    if(self.leftDoors == 1):
                        self.toggleLeftDoors()
                    if(self.rightDoors == 1):
                        self.toggleRightDoors()
                    self.train.set("announcingStop", False)
                #Decrements timer
                self.timer = self.timer - 1
                
        #Make sure doors are closed at all times while moving - Safety Critical
        if(self.currentSpeed != 0 and self.leftDoors == 1):
            self.toggleLeftDoors()
        if(self.currentSpeed != 0 and self.rightDoors == 1):
            self.toggleRightDoors()
		
		#Determines when to pull or release service brake
        if(self.serviceBrake == 0 and (self.speedSetpoint < self.currentSpeed) and self.emergencyBrake == 0):
            self.toggleServiceBrake()
        elif(self.serviceBrake == 1 and (self.speedSetpoint > self.currentSpeed or self.emergencyBrake == 1)):
            self.toggleServiceBrake()
  
            
            
      
        
        
        #Find error term
        self.e = self.speedSetpoint - self.currentSpeed
        
        #Finds integral of error term
        if(self.power < self.maxPower):
            self.uK = self.uKPrevious + (self.T/2)*(self.e - self.ePrevious)
        else:
            self.uK = self.uKPrevious
        
        #Calculates power command value
        self.power = self.kP*self.e + self.kI*self.uK
            
        #Keeps power in bounds
        if self.power > self.maxPower:
            self.power = self.maxPower
        if self.power < 0:
            self.power = 0
            
        #Checks power with redundancy
        self.checkPower(self.currentSpeed, self.speedSetpoint, self.ePrevious, self.uKPrevious)
        
        #Set power to zero if brake is on
        if(self.emergencyBrake == 1 or self.serviceBrake == 1):
            self.power = 0
        
        self.train.set("power", self.power)
        self.train.set("authority",self.authority)
        
        #Stores values of e and uK for next calculation
        self.ePrevious = self.e
        self.uKPrevious = self.uK
        
        self.window.refreshValues()
		
