# Press Shift+F10.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QTableWidget,QTableWidgetItem,QSlider,QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QComboBox,QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QBrush

def initFrame():
    #init QApplication
    app = QApplication([])

    #init app window
    window = QWidget()
    window.setWindowTitle('Wayside Controller')
    window.setGeometry(0,0,2250,2000)
    window.show()

    miscLayout = QHBoxLayout()

    #init home button and add to misc layout
    homeButton = QPushButton(QIcon('homeButton.png'),'')
    miscLayout.addWidget(homeButton)

    #init controller selector and add to misc layout
    selControlLabel = QLabel('    Select Controller')
    selControlCBox = QComboBox()
    controllerID = ['1','2','3','4','5','6','7','8','9','10']
    selControlCBox.addItems(controllerID)
    miscLayout.addWidget(selControlLabel)
    miscLayout.addWidget(selControlCBox)

    # init speed limit and add to misc layout
    speedLimitLabel = QLabel('    Speed Limit')
    global speedLimitSBox
    speedLimitSBox = QSpinBox()
    speedLimitSBox.valueChanged.connect(determineCommandedSpeed)
    miscLayout.addWidget(speedLimitLabel)
    miscLayout.addWidget(speedLimitSBox)

    # init suggested speed and add to misc layout
    suggSpeedLabel = QLabel('    Suggested Speed')
    global suggSpeedSBox
    suggSpeedSBox = QSpinBox()
    suggSpeedSBox.valueChanged.connect(determineCommandedSpeed)
    miscLayout.addWidget(suggSpeedLabel)
    miscLayout.addWidget(suggSpeedSBox)

    # init commanded speed and add to misc layout
    commSpeedLabel = QLabel('    Commanded Speed')
    global commSpeedSBox
    commSpeedSBox = QSpinBox()
    suggSpeedSBox.valueChanged.connect(determineCommandedSpeed)
    commSpeedSBox.setReadOnly(True)
    miscLayout.addWidget(commSpeedLabel)
    miscLayout.addWidget(commSpeedSBox)

    # init authority and add to misc layout
    authLabel = QLabel('    Authority')
    global authSBox
    authSBox = QSpinBox()
    miscLayout.addWidget(authLabel)
    miscLayout.addWidget(authSBox)

    # init track heater slider and add to misc layout
    heatLabel = QLabel('    Track Heating')
    heatEnabledLabel = QLabel('OFF')
    heatSlider = QSlider()
    heatSlider.setMinimum(0)
    heatSlider.setMaximum(1)
    heatSlider.setOrientation(Qt.Horizontal)
    miscLayout.addWidget(heatLabel)
    miscLayout.addWidget(heatSlider)
    miscLayout.addWidget(heatEnabledLabel)

    # init logout button and add to misc layout
    logoutButton = QPushButton('Logout')
    miscLayout.addWidget(logoutButton)

    #init Tracks table
    global trackTable
    trackTable = QTableWidget(15, 7)
    trackTable.cellClicked.connect(trackOccupancyChanged)
    trackHeaders = ['Block Number','Occupancy','Broken Rail','Switch Failure','Power Failure','Circuit Failure','Switch Position']
    nullRowHeaders = ['','','','','','','','','','','','','','','']  #init null row headers for tables
    trackTable.setHorizontalHeaderLabels(trackHeaders)
    trackTable.setVerticalHeaderLabels(nullRowHeaders)
    trackRows = trackTable.rowCount()
    trackRows = trackRows
    #set data in table
    for x in range(0, trackRows):
        rowNum = QTableWidgetItem(str(x+1))
        occButton = QTableWidgetItem()
        occButton.setCheckState(Qt.Unchecked)
        #commSpeedLimit = QTableWidgetItem(str(0))
        railButton = QTableWidgetItem()
        railButton.setCheckState(Qt.Unchecked)
        switchButton = QTableWidgetItem()
        switchButton.setCheckState(Qt.Unchecked)
        powerButton = QTableWidgetItem()
        powerButton.setCheckState(Qt.Unchecked)
        circuitButton = QTableWidgetItem()
        circuitButton.setCheckState(Qt.Unchecked)
        if x==4:
            switchPos = QTableWidgetItem('5 to 6')
        else:
            switchPos = QTableWidgetItem('None')
        trackTable.setItem(x,0,rowNum)
        trackTable.setItem(x,1,occButton)
        #trackTable.setItem(x,2,commSpeedLimit)
        trackTable.setItem(x,2,railButton)
        trackTable.setItem(x,3,switchButton)
        trackTable.setItem(x,4,powerButton)
        trackTable.setItem(x,5,circuitButton)
        trackTable.setItem(x,6,switchPos)
    #endRowNum = QTableWidgetItem('149')
    #trackTable.setItem(4, 0, endRowNum)
    #endRowNum = QTableWidgetItem('150')
    #trackTable.setItem(5, 0, endRowNum)
    trackTable.show()

    # init Lights table
    lightTable = QTableWidget(1, 2)
    lightHeaders = ['Block Number', 'Light Status']
    lightTable.setHorizontalHeaderLabels(lightHeaders)
    lightTable.setVerticalHeaderLabels(nullRowHeaders)
    lightRows = lightTable.rowCount()
    textColor = QBrush(Qt.green)
    #set data in table
    for x in range(0, lightRows):
        rowNum = QTableWidgetItem('5')
        lightStatus = QTableWidgetItem('GREEN')
        lightStatus.setForeground(textColor)
        lightTable.setItem(x, 0, rowNum)
        lightTable.setItem(x, 1, lightStatus)
    lightTable.show()

    #init PLC Buttons
    buttonLayout = QHBoxLayout()
    loadButton = QPushButton('Load PLC File')
    buttonLayout.addWidget(loadButton)
    writeButton = QPushButton('Write PLC File')
    buttonLayout.addWidget(writeButton)
    loadButton.show()
    writeButton.show()

    #init window layout and add sub-layouts
    windowLayout = QVBoxLayout(window)
    windowLayout.addLayout(miscLayout)
    windowLayout.addWidget(trackTable)
    windowLayout.addWidget(lightTable)
    windowLayout.addLayout(buttonLayout)

    #execute application
    app.exec_()

#trackOccupancyChanged() updates switch states based on new track occupancies
#Inputs: None
#Outputs: None
def trackOccupancyChanged():
    #Get blocks needed to determine switch states
    global trackTable
    block6 = trackTable.item(5,1)
    block11 = trackTable.item(10,1)
    occ6 = block6.checkState()
    occ11 = block11.checkState()
    switchItem = trackTable.item(4, 6)
    if occ6==2:
        switchItem.setText('5 to 6')
    elif occ11==2:
        switchItem.setText('5 to 11')
    #blockF = trackTable.item(1,1)
    #blockG = trackTable.item(3,1)
    #blockY = trackTable.item(4,1)
    #blockZ = trackTable.item(5,1)
    #fOcc = blockF.checkState()
    #gOcc = blockG.checkState()
    #yOcc = blockY.checkState()
    #zOcc = blockZ.checkState()
    #if (fOcc==2 or gOcc==2) and yOcc==2 and zOcc==0:
    #    #print('Stop Y. Move to Straight. Wait for F and G to clear, then move to curved and start Y')
    #    switchItem = trackTable.item(2, 6)
    #    switchItem.setText('Straight')
    #elif gOcc==2:
    #    #print('Move to Straight')
    #    switchItem = trackTable.item(2, 6)
    #    switchItem.setText('Straight')
    #elif zOcc==2:
    #    #print('Move to Curved')
    #    switchItem = trackTable.item(2, 6)
    #    switchItem.setText('Curved')
    #elif fOcc==0 and gOcc==0 and yOcc==2:
    #    switchItem = trackTable.item(2, 6)
    #    switchItem.setText('Curved')

# getAuthority() returns Authority. Throws no exceptions
# Inputs: None
# Outputs: auth(int) authority in blocks
# Eventually, getAuthority shall invoke method in CTC module
def getAuthority():
    #auth = int(input('Please Enter A Value For Authority: '))
    global authSBox
    return authSBox.value()

# getSuggSpeed() returns Suggested Speed. Throws no exceptions
# Inputs: None
# Outputs: None (suggSpeed is global var)
# Eventually, getSuggSpeed shall invoke method in CTC module
def getSuggSpeed():
    global suggSpeedSBox
    return suggSpeedSBox.value()

# isTrackOccupied(trackNum) returns occupancy status for specified track. Throws no exceptions
# Inputs: trackNum(int) track ID # for which we would like occupancy status
# Outputs: occupied(boolean) occupancy status of track
# Eventually, isTrackOccupied shall utilize track circuit to determine occupancy
def isTrackOccupied(trackNum):
    occupied = input(F'Is Track {trackNum} Occupied? True or False ')

    if occupied=='True':
        return True
    elif occupied=='False':
        return False
    else:
        print('Please enter True Or False')
        return isTrackOccupied(trackNum)

# getSpeedLimit() returns Track Speed Limit. Throws no exceptions
# Inputs: None
# Outputs: None
# Eventually, getSpeedLimit shall invoke method in Track Model module
def getSpeedLimit():
    global speedLimitSBox
    return speedLimitSBox.value()

#initSpeedVars() initializes global speed variables and sets them = 0. Throws no exceptions
# Inputs: None
# Outputs: None
def initSpeedVars():
    global trackSpeed
    global suggSpeed
    global commSpeed
    trackSpeed = 0
    suggSpeed = 0
    commSpeed = 0

#determineCommandedSpeed() calculates commanded speed. Throws no exceptions
# All speed variables are global - nothing is input or returned
def determineCommandedSpeed():
    global commSpeedSBox
    speedLimit = getSpeedLimit()
    suggSpeed = getSuggSpeed()
    commSpeed = speedLimit if speedLimit<=suggSpeed else suggSpeed
    commSpeedSBox.setValue(commSpeed)

#Track Failure Methods - Will probably have to change how we do this

# getBrokenRails() returns Track ID # for Broken Rail. Throws no exceptions
# Inputs: None
# Outputs: trackNum(int) Track ID # for Broken Rail - if no rail is broken, return -1
def getBrokenRails():
    trackNum = int(input('Please Enter The Track ID # For The Broken Rail Or Enter -1 If No Rail Is Broken: '))
    if trackNum > 0:
        return trackNum
    elif trackNum == -1:
        return False
    else:
        print('Please enter A Valid Number')
        return getBrokenRails()

# getSwitchFailure() returns Track ID # for Switch Failure. Throws no exceptions
# Inputs: None
# Outputs: trackNum(int) Track ID # for Switch Failure - if no switch has failed, return -1
def getSwitchFailure():
    trackNum = int(input('Please Enter The Track ID # For The Switch Failure Or Enter -1 If No Switch Has Failed: '))
    if trackNum > 0:
        return trackNum
    elif trackNum == -1:
        return False
    else:
        print('Please enter A Valid Number')
        return getSwitchFailure()

# hasPowerFailed() returns power failure status. Throws no exceptions
# Inputs: None
# Outputs: powerFailed(boolean), True if power has failed, False otherwise
def hasPowerFailed():
    powerFailed = input(F'Is Power Failure Occuring? True or False ')
    if powerFailed == 'True':
        return True
    elif powerFailed == 'False':
        return False
    else:
        print('Please enter True Or False')
        return hasPowerFailed()

# hasCircuitFailed() returns track circuit failure status. Throws no exceptions
# Inputs: None
# Outputs: circuitFailed(boolean), True if track circuit has failed, False otherwise
def hasCircuitFailed():
    circuitFailed = input(F'Is Track Circuit Failure Occuring? True or False ')
    if circuitFailed == 'True':
        return True
    elif circuitFailed == 'False':
        return False
    else:
        print('Please enter True Or False')
        return hasCircuitFailed()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #global trackTable
    initFrame()
    #initSpeedVars()
    #auth = getAuthority()
    #getSuggSpeed()
    #getTrackSpeed()
    #determineCommandedSpeed()
    #print(commSpeed)
    #print(auth,suggSpeed)
    #trackNum = 7
    #occupied = isTrackOccupied(trackNum)
    #print(occupied)
    #if occupied:
    #    print(f'Track {trackNum} is occupied')
    #else:
    #    print(f'Track {trackNum} is not occupied')
    #brTrackNum = getBrokenRails()
    #swTrackNum = getSwitchFailure()
    #powerFailed = hasPowerFailed()
    #circuitFailed = hasCircuitFailed()
    #print(brTrackNum, swTrackNum, powerFailed, circuitFailed)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/