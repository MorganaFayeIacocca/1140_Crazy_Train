import sys
from typing import List
from PyQt5 import QtWidgets, QtCore
from SystemController import SystemController, SystemRunner
from SystemCloser import systemCloser

from MainWindow import LoadingWindow, MainWindow, EmptyWindow

from TrackModelGui import TrackModelWindow, BlockWindow, StationWindow
from WaysideControllerGroup import WaysideGroupGUI
from WaysideControllerGUI import WaysideControllerGUI
from TrainModelModule import TrainSelectWindow
from ControllerGroup import CWindowSelector

class GuiController:

    system: SystemController
    emptyWindow: EmptyWindow
    blockWindows: List[BlockWindow]
    stationWindows: List[StationWindow]

    def __init__(self):
        self.emptyWindow = EmptyWindow()
        self.blockWindows = []
        self.stationWindows = []
    
    def setSystem(self, system: SystemController) -> None:
        self.system = system
    
    def showLoading(self):
        self.loadingWindow = LoadingWindow(self.emptyWindow.frameGeometry())
        self.loadingWindow.show()
    
    def showMain(self):
        if not hasattr(self, "mainWindow"):
            self.mainWindow = MainWindow(self.system, self.showCTC, self.showWaysideGroup, self.showTrackModel, self.showTrainModel, self.showTrainControllerGroup, self.emptyWindow.frameGeometry())
        if self.mainWindow.isVisible():
            self.mainWindow.close()
        self.mainWindow.show()
    
    def showCTC(self):
        if hasattr(self, "ctcWindow"):
            self.ctcWindow.close()
        self.ctcWindow = QtWidgets.QMainWindow()
        self.system.ctcOffice.setupUi(self.ctcWindow)
        self.ctcWindow.show()

    def showWaysideGroup(self):
        if hasattr(self, "waysideGroupWindow"):
            self.waysideGroupWindow.close()
        self.waysideGroupWindow = WaysideGroupGUI(self.system.waysides,self.showWaysideController, self.showMain)
        self.waysideGroupWindow.show()

    def showWaysideController(self):
        if hasattr(self, "waysideWindow"):
            self.waysideWindow.close()
        self.waysideWindow = WaysideControllerGUI(self.system.waysides.controllerDisp,self.showWaysideGroup)
        self.waysideWindow.show()
    
    def showTrackModel(self):
        if hasattr(self, "trackModelWindow"):
            self.trackModelWindow.close()
        self.trackModelWindow = TrackModelWindow(self.system.trackModel, self.showBlock, self.showMain, self.emptyWindow.frameGeometry())
        self.trackModelWindow.show()

    def showBlock(self):
        for i in reversed(range(len(self.blockWindows))):
            if self.blockWindows[i].blockNum == BlockWindow.nextBlock:
                self.blockWindows.pop(i).close()
        blockWindowNew = BlockWindow(self.system.trackModel, self.showTrackModel, self.showMain, self.showStation, self.emptyWindow.frameGeometry())
        self.blockWindows.append(blockWindowNew)
        blockWindowNew.show()

    def showStation(self):
        for i in reversed(range(len(self.stationWindows))):
            if self.stationWindows[i].blockNum == BlockWindow.nextBlock:
                self.stationWindows.pop(i).close()
        stationWindowNew = StationWindow(self.system.trackModel, self.showBlock, self.showMain, self.emptyWindow.frameGeometry())
        self.stationWindows.append(stationWindowNew)
        stationWindowNew.show()

    def showTrainModel(self):
        if hasattr(self, "trainModelWindow"):
            self.trainModelWindow.close()
        self.trainModelWindow = TrainSelectWindow(self.system.trainModel, self.showMain)
        self.trainModelWindow.show()
    
    def showTrainControllerGroup(self):
        if hasattr(self, "trainControllerWindow"):
            self.trainControllerWindow.close()
        self.trainControllerWindow = CWindowSelector(self.system.trainControllers, self.showMain)
        self.trainControllerWindow.show()

def main():
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)

    #Intialize GUI controllers
    guiController = GuiController()
    systemCloser.setGuiController(guiController)
    systemCloser.setQApplication(app)

    #Determine if simulating Red Line or Green Line
    guiController.showLoading()
    app.exec_()

    if not hasattr(SystemController, "line"):
        systemCloser.showError("Error: No train line selected.\nRestart the program and select a train line to continue\nExiting")
        app.exec_()
        systemCloser.closeProgram()

    #Initialize system with correct line
    systemController = SystemController()
    #Continuously update the model
    systemRunner = SystemRunner(systemController)
    threadpool = QtCore.QThreadPool()
    threadpool.start(systemRunner)
    guiController.setSystem(systemController)
    
    systemController.trainControllers.backFunc = guiController.showMain
    systemController.ctcOffice.showMain = guiController.showMain

    #Start the GUI
    guiController.showMain()

    #Cleanup
    app.exec_()
    systemCloser.closeProgram()

if __name__ == '__main__':
    main()
