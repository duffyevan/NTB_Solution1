import sys
import datetime
from typing import List

from PyQt5 import QtGui
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QVBoxLayout, QWidget, QScrollArea

from data_collection_automation.frontend.ConfigManager import ConfigManager
from data_collection_automation.frontend.mainwindow import Ui_MainWindow
from data_collection_automation import SPSLib, HostpointLib

window = None
ui = None
config = ConfigManager('c:\\Users\\c-duffy\\Documents\\MQP\\code\\data_collection_automation\\collection.conf')
checkBoxes: List[QCheckBox] = []


def test():
    print("HelloWorld")


def downloadFilesForDay():
    for host in getSelectedHosts():
        with SPSLib.SPSLib(host, config.SPSuser, config.SPSpassword) as sps:
            qdate = ui.daySelector.date()
            dt = datetime.date(qdate.year(), qdate.month(), qdate.day())
            sps.download_files_for_day(dt)


def downloadFilesForMonth():
    for host in getSelectedHosts():
        with SPSLib.SPSLib(host, config.SPSuser, config.SPSpassword) as sps:
            qdate = ui.daySelector.date()
            dt = datetime.date(qdate.year(), qdate.month(), 1)
            sps.download_files_for_month(dt)


def downloadFilesForYear():
    for host in getSelectedHosts():
        with SPSLib.SPSLib(host, config.SPSuser, config.SPSpassword) as sps:
            qdate = ui.yearSelector.date()
            year = qdate.year()
            for i in range(1, 12):
                dt = datetime.date(year, i, 1)
                sps.download_files_for_month(dt)


def getSelectedHosts():
    selected_addresses: List[str] = []
    for checkBox in checkBoxes:
        if checkBox.isChecked():
            selected_addresses.append(checkBox.text())  # TODO FIXME this is bad
    return selected_addresses

def setCheckedAllHosts(selected):
    for checkBox in checkBoxes:
        checkBox.setChecked(selected)

def setup_ui(interface):
    interface.pushButtonDownloadForDay.clicked.connect(downloadFilesForDay)
    interface.pushButtonDownloadForMonth.clicked.connect(downloadFilesForMonth)
    interface.pushButtonDownloadForYear.clicked.connect(downloadFilesForYear)
    interface.daySelector.setDate(QDate(datetime.datetime.today()))
    interface.monthSelector.setDate(QDate(datetime.datetime.today()))
    interface.yearSelector.setDate(QDate(datetime.datetime.today()))

    checkBoxes = []

    for address in config.SPSaddresses:
        ccb = QCheckBox(interface.verticalLayoutWidget)
        ccb.setObjectName(address.replace('.', '') + "Checkbox")
        ccb.setText(address)
        interface.verticalLayout.addWidget(ccb)
        checkBoxes.append(ccb)

    interface.masterProgressBar.setDisabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    setup_ui(ui)
    window.show()
    sys.exit(app.exec_())
