from Control_Window import controlWindow
from Train_Controller import TrainController
from SpeedLimit import SpeedLimit
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ControllerGroup:
    speedLimits: SpeedLimit
    controllerArray = []
    windowArray = []
    period = 1
    backFunc = 0
    def __init__(self, period):
        self.period = period        
        
    def addController(self, train):
        tc = TrainController(self.period, train)
        cw = controlWindow(tc, self.backFunc)
        self.controllerArray.append(tc)
        self.windowArray.append(cw)
        return tc
        
    def getController(self, x):
        return self.controllerArray[x]
    
    def getWindow(self, x):
        return self.windowArray[x]
        
    def update(self):
        for x in self.controllerArray:
            x.recalculateAttributes()


class CWindowSelector(QWidget):
    group: ControllerGroup
    backButton: QPushButton
    refreshButton: QPushButton
    trainButtons = []
    layout = QVBoxLayout()
    initialized = 0
    backFunc = 0
    def __init__(self, cg, backFunction):
        super().__init__()
        self.group = cg
        self.setLayout(self.layout)
        self.backFunc = backFunction
        self.setWindowTitle("Controller Selector")
        self.setGeometry(0,0,400,300)
        self.updateLayout()
        initialized = 1
        
        
    def updateLayout(self):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().deleteLater()
        self.trainButtons.clear()
        
        
        refreshButton = QPushButton("Refresh")
        refreshButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        refreshButton.setCheckable(True)
        refreshButton.setFont(QFont("Arial",12))
        refreshButton.clicked.connect(self.updateLayout)
        self.layout.addWidget(refreshButton, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        i = 0
        for x in self.group.windowArray:
            x.setBackFunc(self.show)
            self.trainButtons.append(QPushButton("Train " + str(i+1)))
            self.trainButtons[i].setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
            self.trainButtons[i].setCheckable(True)
            self.trainButtons[i].setFont(QFont("Arial",12))
            self.trainButtons[i].clicked.connect(x.show)
            self.trainButtons[i].clicked.connect(self.close)
            self.layout.addWidget(self.trainButtons[i], alignment=QtCore.Qt.AlignHCenter)
            i = i + 1
            
        backButton = QPushButton("Back to Home")
        backButton.setStyleSheet("QPushButton{border : 2px solid black; background-color : azure; color : black}QPushButton::pressed{border : 2px solid black; background-color : grey; color : black}QPushButton:disabled {border:2px solid gray;background-color:lightgray;color:gray}")
        backButton.setCheckable(True)
        backButton.setFont(QFont("Arial",12))
        backButton.clicked.connect(self.backFunc)
        backButton.clicked.connect(self.close)
        self.layout.addWidget(backButton, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        

		
def back():
	print("Sent back to home")
	return

"""
def main():
	myLimits = 0 #SpeedLimit()
	app = QApplication(sys.argv)
	cg = ControllerGroup(.1, back, myLimits)
	t = []
	
	for i in range(0,4,1):
		t.append(Train(100, 5, 5, 2000, 0, 222, 80, 2, 0.5, 20, 2.73, 1.2, 120000, cg))
		t[i].set("timeStep",.1)
		#cg.addController(t[i])
	
	cws = CWindowSelector(cg, back)
	tw = TrainWindow(t[0],back,1)
  
	
	threadpool = []
	loop = []
	
	i = 0
	for x in cg.controllerArray:
		loop.append(Cycle(x.train,x))
		threadpool.append(QtCore.QThreadPool())
		threadpool[i].start(loop[i])
		i = i + 1
	
	cws.show()
	tw.show()
	sys.exit(app.exec_())
	


if __name__ == '__main__':
	main()
"""
