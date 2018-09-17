import datetime
import os
import sys
from threading import Thread
from typing import List

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QDialog, QErrorMessage, QMessageBox, QWidget, \
    QVBoxLayout

from data_collection_automation.SPSLib import SPSConnectionException, SPSLib
from data_collection_automation.frontend.ConfigManager import ConfigManager
from data_collection_automation.frontend.mainwindow import Ui_MainWindow
from data_collection_automation.frontend.dialog import Ui_DialogWindow

config_file_path = '~\\Documents\\MQP\\code\\data_collection_automation\\collection.conf'.replace('~', 'c:\\Users\\' + os.getlogin())

window = None
ui = None
config = ConfigManager(config_file_path)
checkBoxes: List[QCheckBox] = []


def SPSFactory(host):
    return SPSLib(host, config.SPSuser, config.SPSpassword, numretries=1,
                  retrydelay=config.connectionretrydelay)


def open_conf_file():
    # Thread(target=os.system, args=("notepad " + config_file_path,)).start()
    os.system("notepad " + config_file_path)
    QMessageBox.about(window, "Notice", "Please Restart The Program For Changes To Take Effect")

def reload_conf_file():
    pass

def install_scheduled_task


def downloadFilesForDay():
    ui.masterProgressBar.setEnabled(True)  # TODO change this to a spinner rather than a bar
    ui.masterProgressBar.setValue(10)
    selected_hosts = getSelectedHosts()
    if len(selected_hosts) == 0:
        return
    for host in selected_hosts:
        try:
            with SPSFactory(host) as sps:
                qdate = ui.daySelector.date()
                dt = datetime.date(qdate.year(), qdate.month(), qdate.day())
                sps.download_files_for_day(dt)
        except SPSConnectionException:
            ui.masterProgressBar.setDisabled(True)

            QMessageBox.about(window, "Error!", "Problem Connecting To SPS At " + host)

            ui.masterProgressBar.setEnabled(True)

    QMessageBox.about(window, "Done!", "Download Process Complete!")
    ui.masterProgressBar.setEnabled(False)
    ui.masterProgressBar.setValue(0)


def downloadFilesForMonth():
    for host in getSelectedHosts():
        with SPSFactory(host) as sps:
            qdate = ui.daySelector.date()
            dt = datetime.date(qdate.year(), qdate.month(), 1)
            sps.download_files_for_month(dt)


def downloadFilesForYear():
    for host in getSelectedHosts():
        with SPSFactory(host) as sps:
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

    interface.openConfFileButton.triggered.connect(open_conf_file)
    # interface.actionQuit.triggered.connect()
    checkBoxes.clear()

    interface.scrollArea.setWidgetResizable(True)

    scroll_content = QWidget(interface.scrollArea)
    scroll_layout = QVBoxLayout(scroll_content)
    scroll_content.setLayout(scroll_layout)

    for address in config.SPSaddresses:
        ccb = QCheckBox(scroll_content)
        ccb.setObjectName(address.replace('.', '_') + "Checkbox")
        ccb.setText(address)
        scroll_layout.addWidget(ccb)
        checkBoxes.append(ccb)

    interface.scrollArea.setWidget(scroll_content)

    interface.masterProgressBar.setDisabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    setup_ui(ui)
    window.show()
    sys.exit(app.exec_())
