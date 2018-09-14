# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(861, 621)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.masterProgressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.masterProgressBar.setGeometry(QtCore.QRect(10, 530, 561, 23))
        self.masterProgressBar.setProperty("value", 0)
        self.masterProgressBar.setObjectName("masterProgressBar")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 290, 361, 231))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButtonDownloadForDay = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonDownloadForDay.setObjectName("pushButtonDownloadForDay")
        self.gridLayout_2.addWidget(self.pushButtonDownloadForDay, 1, 1, 1, 1)
        self.yearSelector = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.yearSelector.setObjectName("yearSelector")
        self.gridLayout_2.addWidget(self.yearSelector, 3, 0, 1, 1)
        self.daySelector = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.daySelector.setObjectName("daySelector")
        self.gridLayout_2.addWidget(self.daySelector, 1, 0, 1, 1)
        self.pushButtonDownloadForYear = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonDownloadForYear.setObjectName("pushButtonDownloadForYear")
        self.gridLayout_2.addWidget(self.pushButtonDownloadForYear, 3, 1, 1, 1)
        self.pushButtonDownloadForMonth = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonDownloadForMonth.setObjectName("pushButtonDownloadForMonth")
        self.gridLayout_2.addWidget(self.pushButtonDownloadForMonth, 2, 1, 1, 1)
        self.monthSelector = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.monthSelector.setObjectName("monthSelector")
        self.gridLayout_2.addWidget(self.monthSelector, 2, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.gridLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 357, 140))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 361, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 861, 21))
        self.menubar.setObjectName("menubar")
        self.menuNTB_Datacollection_Automation = QtWidgets.QMenu(self.menubar)
        self.menuNTB_Datacollection_Automation.setObjectName("menuNTB_Datacollection_Automation")
        self.menuConfigoration = QtWidgets.QMenu(self.menubar)
        self.menuConfigoration.setObjectName("menuConfigoration")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.openConfFileButton = QtWidgets.QAction(MainWindow)
        self.openConfFileButton.setObjectName("openConfFileButton")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuNTB_Datacollection_Automation.addAction(self.actionQuit)
        self.menuConfigoration.addAction(self.openConfFileButton)
        self.menubar.addAction(self.menuNTB_Datacollection_Automation.menuAction())
        self.menubar.addAction(self.menuConfigoration.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonDownloadForDay.setText(_translate("MainWindow", "Download For Day"))
        self.yearSelector.setDisplayFormat(_translate("MainWindow", "yyyy"))
        self.pushButtonDownloadForYear.setText(_translate("MainWindow", "Download For Year"))
        self.pushButtonDownloadForMonth.setText(_translate("MainWindow", "Download For Month"))
        self.monthSelector.setDisplayFormat(_translate("MainWindow", "M/yyyy"))
        self.menuNTB_Datacollection_Automation.setTitle(_translate("MainWindow", "File"))
        self.menuConfigoration.setTitle(_translate("MainWindow", "Configuration"))
        self.openConfFileButton.setText(_translate("MainWindow", "Open Configuration File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
