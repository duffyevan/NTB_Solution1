# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogWindow(object):
    def setupUi(self, DialogWindow):
        DialogWindow.setObjectName("DialogWindow")
        DialogWindow.resize(300, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogWindow.sizePolicy().hasHeightForWidth())
        DialogWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(DialogWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(16, 52, 261, 91))
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        DialogWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DialogWindow)
        self.statusbar.setObjectName("statusbar")
        DialogWindow.setStatusBar(self.statusbar)
        self.openConfFileButton = QtWidgets.QAction(DialogWindow)
        self.openConfFileButton.setObjectName("openConfFileButton")
        self.actionQuit = QtWidgets.QAction(DialogWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.retranslateUi(DialogWindow)
        QtCore.QMetaObject.connectSlotsByName(DialogWindow)

    def retranslateUi(self, DialogWindow):
        _translate = QtCore.QCoreApplication.translate
        DialogWindow.setWindowTitle(_translate("DialogWindow", "MainWindow"))
        self.label.setText(_translate("DialogWindow", "TextLabel"))
        self.openConfFileButton.setText(_translate("DialogWindow", "Open Configuration File"))
        self.actionQuit.setText(_translate("DialogWindow", "Quit"))

