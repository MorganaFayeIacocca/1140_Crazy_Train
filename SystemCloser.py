import os
from typing import Callable
from PyQt5 import QtWidgets, QtGui, QtCore

redLight = "TrackModelModule/redLight.jpg"

class ErrorWindow(QtWidgets.QWidget):
    def __init__(self, errorMessage: str):
        #Initialize Window Dimensions and Title
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Error Message')

        #Add widgets
        layout = QtWidgets.QGridLayout()

        #Error symbol
        errorSymbol = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(redLight)
        errorSymbol.setPixmap(pixmap)
        layout.addWidget(errorSymbol,0,0)

        #Error message
        errorWidget = QtWidgets.QLabel(errorMessage)
        errorWidget.setFont(QtGui.QFont("Arial", 20))
        layout.addWidget(errorWidget,0,1)

        #close button
        closeButton = QtWidgets.QPushButton("OK")
        closeButton.clicked.connect(self.close)
        layout.addWidget(closeButton,1,1,QtCore.Qt.AlignRight)

        #Finalize layout
        self.setLayout(layout)

class WarningWindow(QtWidgets.QWidget):
    def __init__(self, message: str, action: Callable):
        #Initialize Window Dimensions and Title
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Warning')

        #Add widgets
        layout = QtWidgets.QGridLayout()

        #Error symbol
        errorSymbol = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(redLight)
        errorSymbol.setPixmap(pixmap)
        layout.addWidget(errorSymbol,0,0)

        #Warning message
        messageWidget = QtWidgets.QLabel(message)
        messageWidget.setFont(QtGui.QFont("Arial", 20))
        layout.addWidget(messageWidget,0,1)

        #Cancel button
        cancelButton = QtWidgets.QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)
        layout.addWidget(cancelButton,1,0,QtCore.Qt.AlignRight)

        #OK button
        closeButton = QtWidgets.QPushButton("OK")
        closeButton.clicked.connect(action)
        closeButton.clicked.connect(self.close)
        layout.addWidget(closeButton,1,1,QtCore.Qt.AlignLeft)

        #Finalize layout
        self.setLayout(layout)


class SystemCloser(QtCore.QObject):
    app: QtWidgets.QApplication
    error: bool
    errorMessage: str
    errorSignal = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.errorSignal.connect(self.showError)


    def setGuiController(self, controller) -> None:
        self.guiController = controller
    
    def setQApplication(self, app: QtWidgets.QApplication) -> None:
        self.app = app
    
    def closeProgram(self) -> None:
        os._exit(1)
    
    def closeWindows(self) -> None:
        if hasattr(self.guiController, "loadingWindow"):
            self.guiController.loadingWindow.close()
        if hasattr(self.guiController, "mainWindow"):
            self.guiController.mainWindow.close()
        if hasattr(self.guiController, "ctcWindow"):
            self.guiController.ctcWindow.close()
        if hasattr(self.guiController, "waysideGroupWindow"):
            self.guiController.waysideGroupWindow.close()
        if hasattr(self.guiController, "waysideWindow"):
            self.guiController.waysideWindow.close()
        if hasattr(self.guiController, "trackModelWindow"):
            self.guiController.trackModelWindow.close()
        if hasattr(self.guiController, "blockWindows"):
            for win in self.guiController.blockWindows:
                win.close()
        if hasattr(self.guiController, "stationWindows"):
            for win in self.guiController.stationWindows:
                win.close()
        if hasattr(self.guiController, "trainModelWindow"):
            for win in self.guiController.trainModelWindow.trainWindows:
                win.close()
            self.guiController.trainModelWindow.close()
        if hasattr(self.guiController, "trainControllerWindow"):
            for win in self.guiController.trainControllerWindow.group.windowArray:
                win.close()
            self.guiController.trainControllerWindow.close()

    def showError(self, errorMessage: str) -> None:
        self.errorWindow = ErrorWindow(errorMessage)
        self.errorWindow.show()
        self.closeWindows()

systemCloser = SystemCloser()