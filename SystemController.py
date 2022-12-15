from datetime import datetime, date, timedelta, time
from PyQt5 import QtCore, QtWidgets
from time import sleep

from CTC import CTCOffice
import CTC
from SystemCloser import systemCloser
from WaysideControllerGroup import WaysideControllerGroup
from TrackModel import TrackModel
from TrainModelModule import TrainModelInterface
from ControllerGroup import ControllerGroup

class SystemController:
    #Static variables
    line: str

    #other modules
    ctcOffice: CTCOffice
    waysides: WaysideControllerGroup
    trackModel: TrackModel
    trainModel: TrainModelInterface
    trainControllers: ControllerGroup

    #instance variables
    rate: int
    period: float

    #gui widgets
    timeWidget: QtWidgets.QWidget

    def __init__(self) -> None:
        self.rate = 1
        self.period = 0.1

        self.trackModel = TrackModel(SystemController.line)
        self.trainControllers = ControllerGroup(self.period)
        self.trainModel = TrainModelInterface(self.period, self.trainControllers, self.trackModel)
        self.waysides = WaysideControllerGroup(self.trackModel, SystemController.line)
        self.ctcOffice = CTCOffice(self.waysides, self.trainModel, SystemController.line)

        self.waysides.ctc = self.ctcOffice
        self.trackModel.setTrainModelInterface(self.trainModel)

        self.timeWidget = QtWidgets.QLabel()
    
    def update(self) -> None:
        self.ctcOffice.update()
        self.waysides.update()
        self.trackModel.update()
        self.trainControllers.update()
        self.trainModel.update()

        self.updateTime()

    def getRate(self) -> int:
        return self.rate
    
    def getPeriod(self) -> float:
        return self.period

    def lowerRate(self) -> None:
        if self.rate == 0:
            self.rate = 0
        elif self.rate == 1:
            self.rate = 0
        elif self.rate == 10:
            self.rate = 1
        elif self.rate == 50:
            self.rate = 10
        else:
            self.rate = 0

    def raiseRate(self) -> None:
        if self.rate == 0:
            self.rate = 1
        elif self.rate == 1:
            self.rate = 10
        elif self.rate == 10:
            self.rate = 15
        elif self.rate == 15:
            self.rate = 15
        else:
            self.rate = 15
    
    def updateTime(self) -> None:
        self.timeWidget.setText(CTC.currentTime.strftime("%I:%M:%S"))
    
    @staticmethod
    def setRedLine() -> None:
        SystemController.line = "RED"
    
    @staticmethod
    def setGreenLine() -> None:
        SystemController.line = "GREEN"

class SystemRunner(QtCore.QRunnable):

    system: SystemController
    running: bool

    def __init__(self, system: SystemController):
        QtCore.QRunnable.__init__(self)
        self.system = system
        self.running = True
        CTC.currentTime = datetime.combine(date.today(), time(6,0,0,0))
        self.system.trackModel.setErrorSignal(systemCloser.errorSignal)

    def run(self) -> None:
        rate = self.system.getRate()
        period = self.system.getPeriod()
        while(self.running):
            if(rate > 0):
                self.update()
                if rate == 1:
                    sleepTime = period
                elif rate == 10:
                    sleepTime = 0.001
                elif rate == 15:
                    sleepTime = 0
                sleep(sleepTime)
            rate = self.system.getRate()

    def update(self) -> None:
        CTC.currentTime = CTC.currentTime + timedelta(0,self.system.period)
        self.system.update()
    
    def end(self) -> None:
        self.running = False