import datetime
import ftplib
import os
import sys
from threading import Thread
from typing import List

from PyQt5.QtCore import QDate, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QMessageBox, QWidget, QVBoxLayout

from data_collection_automation.SPSLib import SPSConnectionException, SPSLib
from data_collection_automation.frontend.ConfigManager import ConfigManager
from data_collection_automation.frontend.mainwindow import Ui_MainWindow

config_file_path = '~\\Documents\\MQP\\code\\data_collection_automation\\collection.conf'.replace('~',
                                                                                                  'c:\\Users\\' + os.getlogin())


class Main(QObject):
    window = None
    ui = None
    config = ConfigManager(config_file_path)
    checkBoxes: List[QCheckBox] = []
    showDialogSignal = pyqtSignal(str, str)

    def __init__(self):
        super(Main, self).__init__()
        self.ui = None

    def SPSFactory(self, host):
        return SPSLib(host, self.config.SPSuser, self.config.SPSpassword, numretries=3,
                      retrydelay=1,
                      default_destination=self.config.downloaddestination)  # Create an SPS client that will try to connect 3 times waiting 1 second on each failed attempt

    def open_conf_file(self):
        # Thread(target=os.system, args=("notepad " + config_file_path,)).start()
        os.system("notepad " + config_file_path)
        QMessageBox.about(self.window, "Notice", "Please Restart The Program For Changes To Take Effect")

    def reload_conf_file(self):
        pass

    def install_scheduled_task(self):
        pass  # TODO Implement this...

    def threadDownloadForDay(self):
        Thread(target=self.downloadFilesForDay).start()

    def threadDownloadForMonth(self):
        Thread(target=self.downloadFilesForMonth).start()

    def threadDownloadForYear(self):
        Thread(target=self.downloadFilesForYear).start()

    def showDialog(self, title, message):
        QMessageBox.about(self.window, title, message)

    def downloadFilesForDay(self):
        self.setProgressBarEnabled(True)
        self.setAllButtonsEnabled(False)

        selected_hosts = self.getSelectedHosts()

        for host in selected_hosts:
            try:
                sps = self.SPSFactory(host)
                qdate = self.ui.daySelector.date()
                dt = datetime.date(qdate.year(), qdate.month(), qdate.day())
                sps.download_files_for_day(dt)
            except SPSConnectionException:
                self.setProgressBarEnabled(False)

                self.showDialogSignal.emit("Error!", "Error Connecting To SPS With Address " + host)

                self.setProgressBarEnabled(True)
            except ftplib.all_errors:
                self.setProgressBarEnabled(False)

                self.showDialogSignal.emit("Error!",
                                           "An FTP Error Occurred Communicating With SPS With Address " + host + ". Make Sure The Files You Are Looking For Exist")

                self.setProgressBarEnabled(True)

        self.showDialogSignal.emit("Done!", "Download Process Is Complete")

        self.setProgressBarEnabled(False)
        self.setAllButtonsEnabled(True)

    def downloadFilesForMonth(self):
        self.setProgressBarEnabled(True)
        self.setAllButtonsEnabled(False)

        selected_hosts = self.getSelectedHosts()

        for host in selected_hosts:
            try:
                sps = self.SPSFactory(host)
                qdate = self.ui.monthSelector.date()
                dt = datetime.date(qdate.year(), qdate.month(), qdate.day())
                sps.download_files_for_month(dt)
            except SPSConnectionException:
                self.setProgressBarEnabled(False)

                self.showDialogSignal.emit("Error!", "Error Connecting To SPS With Address " + host)

                self.setProgressBarEnabled(True)
            except ftplib.all_errors:
                self.setProgressBarEnabled(False)

                self.showDialogSignal.emit("Error!",
                                           "An FTP Error Occurred Communicating With SPS With Address " + host + ". Make Sure The Files You Are Looking For Exist")

                self.setProgressBarEnabled(True)

        self.showDialogSignal.emit("Done!", "Download Process Is Complete")

        self.setProgressBarEnabled(False)
        self.setAllButtonsEnabled(True)

    def downloadFilesForYear(self):
        self.setProgressBarEnabled(True)
        self.setAllButtonsEnabled(False)

        selected_hosts = self.getSelectedHosts()

        for host in selected_hosts:
            try:
                sps = self.SPSFactory(host)
                qdate = self.ui.yearSelector.date()
                year = qdate.year()
                for i in range(1, 12):
                    dt = datetime.date(year, i, 1)
                    try:
                        sps.download_files_for_month(dt)
                    except ftplib.all_errors:
                        continue
            except SPSConnectionException:
                self.setProgressBarEnabled(False)

                self.showDialogSignal.emit("Error!", "Error Connecting To SPS With Address " + host)

                self.setProgressBarEnabled(True)
            except:
                self.setProgressBarEnabled(False)

                self.showDialogSignal.emit("Error!",
                                           "An Unknown Error Occurred Communicating With SPS With Address " + host)

                self.setProgressBarEnabled(True)

        self.showDialogSignal.emit("Done!", "Download Process Is Complete")

        self.setProgressBarEnabled(False)
        self.setAllButtonsEnabled(True)

    def getSelectedHosts(self):
        selected_addresses: List[str] = []
        for checkBox in self.checkBoxes:
            if checkBox.isChecked():
                selected_addresses.append(checkBox.text())  # TODO FIXME this is bad
        return selected_addresses

    def setCheckedAllHosts(self, selected):
        for checkBox in self.checkBoxes:
            checkBox.setChecked(selected)

    def selectAllHosts(self):
        self.setCheckedAllHosts(True)

    def disselectAllHosts(self):
        self.setCheckedAllHosts(False)

    def setProgressBarEnabled(self, enabled):
        if enabled:
            self.ui.masterProgressBar.setRange(0, 0)
            self.ui.masterProgressBar.setEnabled(True)
        else:
            self.ui.masterProgressBar.setRange(0, 10)
            self.ui.masterProgressBar.setDisabled(True)

    def setAllButtonsEnabled(self, enabled):
        if enabled:
            self.ui.pushButtonDownloadForDay.setEnabled(True)
            self.ui.pushButtonDownloadForMonth.setEnabled(True)
            self.ui.pushButtonDownloadForYear.setEnabled(True)
        else:
            self.ui.pushButtonDownloadForDay.setEnabled(False)
            self.ui.pushButtonDownloadForMonth.setEnabled(False)
            self.ui.pushButtonDownloadForYear.setEnabled(False)

    def setup_ui(self):
        self.ui.pushButtonDownloadForDay.clicked.connect(self.threadDownloadForDay)
        self.ui.pushButtonDownloadForMonth.clicked.connect(self.threadDownloadForMonth)
        self.ui.pushButtonDownloadForYear.clicked.connect(self.threadDownloadForYear)

        self.ui.pushButtonSelectAll.clicked.connect(self.selectAllHosts)
        self.ui.pushButtonDisselectAll.clicked.connect(self.disselectAllHosts)

        self.ui.daySelector.setDate(QDate(datetime.datetime.today()))
        self.ui.monthSelector.setDate(QDate(datetime.datetime.today()))
        self.ui.yearSelector.setDate(QDate(datetime.datetime.today()))

        self.ui.openConfFileButton.triggered.connect(self.open_conf_file)

        self.checkBoxes.clear()

        self.ui.scrollArea.setWidgetResizable(True)

        scroll_content = QWidget(self.ui.scrollArea)
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)

        for address in self.config.SPSaddresses:
            ccb = QCheckBox(scroll_content)
            ccb.setObjectName(address.replace('.', '_') + "Checkbox")
            ccb.setText(address)
            scroll_layout.addWidget(ccb)
            self.checkBoxes.append(ccb)

        self.ui.scrollArea.setWidget(scroll_content)

        self.setProgressBarEnabled(False)

        self.showDialogSignal.connect(self.showDialog)


if __name__ == '__main__':
    main = Main()
    app = QApplication(sys.argv)
    main.window = QMainWindow()
    main.ui = Ui_MainWindow()
    main.ui.setupUi(main.window)
    main.setup_ui()
    main.window.show()
    sys.exit(app.exec_())
