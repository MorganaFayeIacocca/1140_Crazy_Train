# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Train3.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setMouseTracking(True)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 30, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 150, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 90, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(30, 210, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(140, 801, 1571, 251))
        self.treeWidget.setMouseTracking(True)
        self.treeWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(1570, 110, 113, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(1570, 210, 113, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(1580, 280, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(1580, 340, 93, 28))
        self.pushButton_6.setObjectName("pushButton_6")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1590, 190, 81, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1570, 90, 111, 16))
        self.label_2.setObjectName("label_2")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setGeometry(QtCore.QRect(1510, 340, 62, 22))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.treeWidget_2 = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget_2.setGeometry(QtCore.QRect(1180, 100, 301, 651))
        self.treeWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeWidget_2.setObjectName("treeWidget_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(150, 100, 1001, 651))
        self.label_3.setStyleSheet("background-image: url(:/track/blueLine.jpg);")
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/track/blueLine.jpg"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton.setGeometry(QtCore.QRect(0, 140, 222, 48))
        self.commandLinkButton.setText("")
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(1180, 130, 101, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(1180, 150, 101, 22))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(1180, 210, 101, 22))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(1180, 190, 101, 22))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setGeometry(QtCore.QRect(1180, 170, 101, 22))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setGeometry(QtCore.QRect(1180, 270, 101, 22))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_9.setGeometry(QtCore.QRect(1180, 310, 101, 22))
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_10.setGeometry(QtCore.QRect(1180, 290, 101, 22))
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_11.setGeometry(QtCore.QRect(1180, 250, 101, 22))
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_12.setGeometry(QtCore.QRect(1180, 230, 101, 22))
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_13.setGeometry(QtCore.QRect(1180, 370, 101, 22))
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.lineEdit_14 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_14.setGeometry(QtCore.QRect(1180, 510, 101, 22))
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.lineEdit_15 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_15.setGeometry(QtCore.QRect(1180, 410, 101, 22))
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.lineEdit_16 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_16.setGeometry(QtCore.QRect(1180, 490, 101, 22))
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.lineEdit_17 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_17.setGeometry(QtCore.QRect(1180, 390, 101, 22))
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.lineEdit_18 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_18.setGeometry(QtCore.QRect(1180, 350, 101, 22))
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.lineEdit_19 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_19.setGeometry(QtCore.QRect(1180, 430, 101, 22))
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.lineEdit_20 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_20.setGeometry(QtCore.QRect(1180, 450, 101, 22))
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.lineEdit_21 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_21.setGeometry(QtCore.QRect(1180, 470, 101, 22))
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.lineEdit_22 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_22.setGeometry(QtCore.QRect(1180, 330, 101, 22))
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.lineEdit_23 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_23.setGeometry(QtCore.QRect(1180, 570, 101, 22))
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.lineEdit_24 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_24.setGeometry(QtCore.QRect(1180, 710, 101, 22))
        self.lineEdit_24.setObjectName("lineEdit_24")
        self.lineEdit_25 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_25.setGeometry(QtCore.QRect(1180, 610, 101, 22))
        self.lineEdit_25.setObjectName("lineEdit_25")
        self.lineEdit_26 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_26.setGeometry(QtCore.QRect(1180, 690, 101, 22))
        self.lineEdit_26.setObjectName("lineEdit_26")
        self.lineEdit_27 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_27.setGeometry(QtCore.QRect(1180, 590, 101, 22))
        self.lineEdit_27.setObjectName("lineEdit_27")
        self.lineEdit_28 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_28.setGeometry(QtCore.QRect(1180, 550, 101, 22))
        self.lineEdit_28.setObjectName("lineEdit_28")
        self.lineEdit_29 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_29.setGeometry(QtCore.QRect(1180, 630, 101, 22))
        self.lineEdit_29.setObjectName("lineEdit_29")
        self.lineEdit_30 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_30.setGeometry(QtCore.QRect(1180, 650, 101, 22))
        self.lineEdit_30.setObjectName("lineEdit_30")
        self.lineEdit_31 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_31.setGeometry(QtCore.QRect(1180, 670, 101, 22))
        self.lineEdit_31.setObjectName("lineEdit_31")
        self.lineEdit_32 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_32.setGeometry(QtCore.QRect(1180, 530, 101, 22))
        self.lineEdit_32.setObjectName("lineEdit_32")
        self.lineEdit_33 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_33.setGeometry(QtCore.QRect(1180, 730, 101, 22))
        self.lineEdit_33.setObjectName("lineEdit_33")
        self.lineEdit_34 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_34.setGeometry(QtCore.QRect(1280, 730, 101, 22))
        self.lineEdit_34.setObjectName("lineEdit_34")
        self.lineEdit_35 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_35.setGeometry(QtCore.QRect(1280, 410, 101, 22))
        self.lineEdit_35.setObjectName("lineEdit_35")
        self.lineEdit_36 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_36.setGeometry(QtCore.QRect(1280, 250, 101, 22))
        self.lineEdit_36.setObjectName("lineEdit_36")
        self.lineEdit_37 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_37.setGeometry(QtCore.QRect(1280, 370, 101, 22))
        self.lineEdit_37.setObjectName("lineEdit_37")
        self.lineEdit_38 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_38.setGeometry(QtCore.QRect(1280, 150, 101, 22))
        self.lineEdit_38.setObjectName("lineEdit_38")
        self.lineEdit_39 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_39.setGeometry(QtCore.QRect(1280, 330, 101, 22))
        self.lineEdit_39.setObjectName("lineEdit_39")
        self.lineEdit_40 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_40.setGeometry(QtCore.QRect(1280, 510, 101, 22))
        self.lineEdit_40.setObjectName("lineEdit_40")
        self.lineEdit_41 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_41.setGeometry(QtCore.QRect(1280, 430, 101, 22))
        self.lineEdit_41.setObjectName("lineEdit_41")
        self.lineEdit_42 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_42.setGeometry(QtCore.QRect(1280, 490, 101, 22))
        self.lineEdit_42.setObjectName("lineEdit_42")
        self.lineEdit_43 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_43.setGeometry(QtCore.QRect(1280, 290, 101, 22))
        self.lineEdit_43.setObjectName("lineEdit_43")
        self.lineEdit_44 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_44.setGeometry(QtCore.QRect(1280, 170, 101, 22))
        self.lineEdit_44.setObjectName("lineEdit_44")
        self.lineEdit_45 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_45.setGeometry(QtCore.QRect(1280, 530, 101, 22))
        self.lineEdit_45.setObjectName("lineEdit_45")
        self.lineEdit_46 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_46.setGeometry(QtCore.QRect(1280, 210, 101, 22))
        self.lineEdit_46.setObjectName("lineEdit_46")
        self.lineEdit_47 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_47.setGeometry(QtCore.QRect(1280, 570, 101, 22))
        self.lineEdit_47.setObjectName("lineEdit_47")
        self.lineEdit_48 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_48.setGeometry(QtCore.QRect(1280, 190, 101, 22))
        self.lineEdit_48.setObjectName("lineEdit_48")
        self.lineEdit_49 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_49.setGeometry(QtCore.QRect(1280, 130, 101, 22))
        self.lineEdit_49.setObjectName("lineEdit_49")
        self.lineEdit_50 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_50.setGeometry(QtCore.QRect(1280, 670, 101, 22))
        self.lineEdit_50.setObjectName("lineEdit_50")
        self.lineEdit_51 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_51.setGeometry(QtCore.QRect(1280, 270, 101, 22))
        self.lineEdit_51.setObjectName("lineEdit_51")
        self.lineEdit_52 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_52.setGeometry(QtCore.QRect(1280, 690, 101, 22))
        self.lineEdit_52.setObjectName("lineEdit_52")
        self.lineEdit_53 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_53.setGeometry(QtCore.QRect(1280, 470, 101, 22))
        self.lineEdit_53.setObjectName("lineEdit_53")
        self.lineEdit_54 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_54.setGeometry(QtCore.QRect(1280, 450, 101, 22))
        self.lineEdit_54.setObjectName("lineEdit_54")
        self.lineEdit_55 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_55.setGeometry(QtCore.QRect(1280, 650, 101, 22))
        self.lineEdit_55.setObjectName("lineEdit_55")
        self.lineEdit_56 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_56.setGeometry(QtCore.QRect(1280, 390, 101, 22))
        self.lineEdit_56.setObjectName("lineEdit_56")
        self.lineEdit_57 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_57.setGeometry(QtCore.QRect(1280, 310, 101, 22))
        self.lineEdit_57.setObjectName("lineEdit_57")
        self.lineEdit_58 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_58.setGeometry(QtCore.QRect(1280, 590, 101, 22))
        self.lineEdit_58.setObjectName("lineEdit_58")
        self.lineEdit_59 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_59.setGeometry(QtCore.QRect(1280, 610, 101, 22))
        self.lineEdit_59.setObjectName("lineEdit_59")
        self.lineEdit_60 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_60.setGeometry(QtCore.QRect(1280, 230, 101, 22))
        self.lineEdit_60.setObjectName("lineEdit_60")
        self.lineEdit_61 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_61.setGeometry(QtCore.QRect(1280, 550, 101, 22))
        self.lineEdit_61.setObjectName("lineEdit_61")
        self.lineEdit_62 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_62.setGeometry(QtCore.QRect(1280, 630, 101, 22))
        self.lineEdit_62.setObjectName("lineEdit_62")
        self.lineEdit_63 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_63.setGeometry(QtCore.QRect(1280, 350, 101, 22))
        self.lineEdit_63.setObjectName("lineEdit_63")
        self.lineEdit_64 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_64.setGeometry(QtCore.QRect(1280, 710, 101, 22))
        self.lineEdit_64.setObjectName("lineEdit_64")
        self.lineEdit_65 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_65.setGeometry(QtCore.QRect(1380, 730, 101, 22))
        self.lineEdit_65.setObjectName("lineEdit_65")
        self.lineEdit_66 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_66.setGeometry(QtCore.QRect(1380, 410, 101, 22))
        self.lineEdit_66.setObjectName("lineEdit_66")
        self.lineEdit_67 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_67.setGeometry(QtCore.QRect(1380, 250, 101, 22))
        self.lineEdit_67.setObjectName("lineEdit_67")
        self.lineEdit_68 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_68.setGeometry(QtCore.QRect(1380, 370, 101, 22))
        self.lineEdit_68.setObjectName("lineEdit_68")
        self.lineEdit_69 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_69.setGeometry(QtCore.QRect(1380, 150, 101, 22))
        self.lineEdit_69.setObjectName("lineEdit_69")
        self.lineEdit_70 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_70.setGeometry(QtCore.QRect(1380, 330, 101, 22))
        self.lineEdit_70.setObjectName("lineEdit_70")
        self.lineEdit_71 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_71.setGeometry(QtCore.QRect(1380, 510, 101, 22))
        self.lineEdit_71.setObjectName("lineEdit_71")
        self.lineEdit_72 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_72.setGeometry(QtCore.QRect(1380, 430, 101, 22))
        self.lineEdit_72.setObjectName("lineEdit_72")
        self.lineEdit_73 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_73.setGeometry(QtCore.QRect(1380, 490, 101, 22))
        self.lineEdit_73.setObjectName("lineEdit_73")
        self.lineEdit_74 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_74.setGeometry(QtCore.QRect(1380, 290, 101, 22))
        self.lineEdit_74.setObjectName("lineEdit_74")
        self.lineEdit_75 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_75.setGeometry(QtCore.QRect(1380, 170, 101, 22))
        self.lineEdit_75.setObjectName("lineEdit_75")
        self.lineEdit_76 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_76.setGeometry(QtCore.QRect(1380, 530, 101, 22))
        self.lineEdit_76.setObjectName("lineEdit_76")
        self.lineEdit_77 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_77.setGeometry(QtCore.QRect(1380, 210, 101, 22))
        self.lineEdit_77.setObjectName("lineEdit_77")
        self.lineEdit_78 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_78.setGeometry(QtCore.QRect(1380, 570, 101, 22))
        self.lineEdit_78.setObjectName("lineEdit_78")
        self.lineEdit_79 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_79.setGeometry(QtCore.QRect(1380, 190, 101, 22))
        self.lineEdit_79.setObjectName("lineEdit_79")
        self.lineEdit_80 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_80.setGeometry(QtCore.QRect(1380, 130, 101, 22))
        self.lineEdit_80.setObjectName("lineEdit_80")
        self.lineEdit_81 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_81.setGeometry(QtCore.QRect(1380, 670, 101, 22))
        self.lineEdit_81.setObjectName("lineEdit_81")
        self.lineEdit_82 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_82.setGeometry(QtCore.QRect(1380, 270, 101, 22))
        self.lineEdit_82.setObjectName("lineEdit_82")
        self.lineEdit_83 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_83.setGeometry(QtCore.QRect(1380, 690, 101, 22))
        self.lineEdit_83.setObjectName("lineEdit_83")
        self.lineEdit_84 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_84.setGeometry(QtCore.QRect(1380, 470, 101, 22))
        self.lineEdit_84.setObjectName("lineEdit_84")
        self.lineEdit_85 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_85.setGeometry(QtCore.QRect(1380, 450, 101, 22))
        self.lineEdit_85.setObjectName("lineEdit_85")
        self.lineEdit_86 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_86.setGeometry(QtCore.QRect(1380, 650, 101, 22))
        self.lineEdit_86.setObjectName("lineEdit_86")
        self.lineEdit_87 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_87.setGeometry(QtCore.QRect(1380, 390, 101, 22))
        self.lineEdit_87.setObjectName("lineEdit_87")
        self.lineEdit_88 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_88.setGeometry(QtCore.QRect(1380, 310, 101, 22))
        self.lineEdit_88.setObjectName("lineEdit_88")
        self.lineEdit_89 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_89.setGeometry(QtCore.QRect(1380, 590, 101, 22))
        self.lineEdit_89.setObjectName("lineEdit_89")
        self.lineEdit_90 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_90.setGeometry(QtCore.QRect(1380, 610, 101, 22))
        self.lineEdit_90.setObjectName("lineEdit_90")
        self.lineEdit_91 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_91.setGeometry(QtCore.QRect(1380, 230, 101, 22))
        self.lineEdit_91.setObjectName("lineEdit_91")
        self.lineEdit_92 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_92.setGeometry(QtCore.QRect(1380, 550, 101, 22))
        self.lineEdit_92.setObjectName("lineEdit_92")
        self.lineEdit_93 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_93.setGeometry(QtCore.QRect(1380, 630, 101, 22))
        self.lineEdit_93.setObjectName("lineEdit_93")
        self.lineEdit_94 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_94.setGeometry(QtCore.QRect(1380, 350, 101, 22))
        self.lineEdit_94.setObjectName("lineEdit_94")
        self.lineEdit_95 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_95.setGeometry(QtCore.QRect(1380, 710, 101, 22))
        self.lineEdit_95.setObjectName("lineEdit_95")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Train 1"))
        self.pushButton_3.setText(_translate("MainWindow", "Train 3"))
        self.pushButton_2.setText(_translate("MainWindow", "Train 2"))
        self.pushButton_4.setText(_translate("MainWindow", "Train 4"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Category"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Status"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "Location"))
        self.treeWidget.headerItem().setText(3, _translate("MainWindow", "Info"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Switch Failure"))
        self.treeWidget.topLevelItem(0).setText(1, _translate("MainWindow", "No issue"))
        self.treeWidget.topLevelItem(0).setText(2, _translate("MainWindow", "Track Number"))
        self.treeWidget.topLevelItem(0).setText(3, _translate("MainWindow", "Additional Info"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("MainWindow", "Track Occupancy"))
        self.treeWidget.topLevelItem(1).setText(1, _translate("MainWindow", "No issue"))
        self.treeWidget.topLevelItem(1).setText(2, _translate("MainWindow", "Track Number"))
        self.treeWidget.topLevelItem(1).setText(3, _translate("MainWindow", "Additional Info"))
        self.treeWidget.topLevelItem(2).setText(0, _translate("MainWindow", "Train Position"))
        self.treeWidget.topLevelItem(2).setText(1, _translate("MainWindow", "No issue"))
        self.treeWidget.topLevelItem(2).setText(2, _translate("MainWindow", "Track Number"))
        self.treeWidget.topLevelItem(2).setText(3, _translate("MainWindow", "Additional Info"))
        self.treeWidget.topLevelItem(3).setText(0, _translate("MainWindow", "Broken Rail"))
        self.treeWidget.topLevelItem(3).setText(1, _translate("MainWindow", "No issue"))
        self.treeWidget.topLevelItem(3).setText(2, _translate("MainWindow", "Track Number"))
        self.treeWidget.topLevelItem(3).setText(3, _translate("MainWindow", "Additional Info"))
        self.treeWidget.topLevelItem(4).setText(0, _translate("MainWindow", "Power Failure"))
        self.treeWidget.topLevelItem(4).setText(1, _translate("MainWindow", "No issue"))
        self.treeWidget.topLevelItem(4).setText(2, _translate("MainWindow", "Track Number"))
        self.treeWidget.topLevelItem(4).setText(3, _translate("MainWindow", "Additional Info"))
        self.treeWidget.topLevelItem(5).setText(0, _translate("MainWindow", "Track Circuit Failure"))
        self.treeWidget.topLevelItem(5).setText(1, _translate("MainWindow", "No issue"))
        self.treeWidget.topLevelItem(5).setText(2, _translate("MainWindow", "Track Number"))
        self.treeWidget.topLevelItem(5).setText(3, _translate("MainWindow", "Additional Info"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.lineEdit.setText(_translate("MainWindow", "10"))
        self.lineEdit_2.setText(_translate("MainWindow", "5"))
        self.pushButton_5.setText(_translate("MainWindow", "Disable Train"))
        self.pushButton_6.setText(_translate("MainWindow", "Disable Track"))
        self.label.setText(_translate("MainWindow", "Authority(km)"))
        self.label_2.setText(_translate("MainWindow", "Speed Limit(mph)"))
        self.treeWidget_2.headerItem().setText(0, _translate("MainWindow", "Train"))
        self.treeWidget_2.headerItem().setText(1, _translate("MainWindow", "Time"))
        self.treeWidget_2.headerItem().setText(2, _translate("MainWindow", "Destination"))
import image_rc
import test_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
