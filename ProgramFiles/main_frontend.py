import datetime
import ftplib
import os
import sys
from threading import Thread
from typing import List
import logging

from PyQt5.QtCore import QDate, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QMessageBox, QWidget, QVBoxLayout

from SPSLib import SPSLib, SPSConnectionException
from frontend.ConfigManager import ConfigManager
from frontend.mainwindow import Ui_MainWindow

config_file_path = '../User/collection.conf'.replace('~', 'c:\\Users\\' + os.getlogin())


class Main(QObject):
    window = None
    ui = None
    config = None
    checkBoxes: List[QCheckBox] = []
    showDialogSignal = pyqtSignal(str, str)

    ## Constructor
    # Loads configuration and initializes superclass
    def __init__(self):
        super(Main, self).__init__()
        self.ui = None
        self.config = ConfigManager(config_file_path)
        logging.basicConfig(filename=self.config.log_path, level=logging.INFO,
                            format='%(asctime)s: %(levelname)s : %(message)s')
        logging.info("Starting...")

    ## Helper for creating a SPS object. Uses default username, password and settings
    # @param host the hostname (or IP address) of the SPS to be connected to
    # @return the SPS object
    def SPSFactory(self, host):
        return SPSLib(host, self.config.SPSuser, self.config.SPSpassword, numretries=3,
                      retrydelay=1,
                      default_destination=self.config.downloaddestination)  # Create an SPS client that will try to connect 3 times waiting 1 second on each failed attempt

    ## Opens the configuration in Notepad so the user can edit it.
    def open_conf_file(self):
        # Thread(target=os.system, args=("notepad " + config_file_path,)).start()
        os.system("notepad " + config_file_path)
        QMessageBox.about(self.window, "Notice", "Please Restart The Program For Changes To Take Effect")

    def open_log_file(self):
        Thread(target=os.system, args=("notepad " + self.config.log_path,)).start()
        # os.system("notepad " + config_file_path)
        # QMessageBox.about(self.window, "Notice", "Please Restart The Program For Changes To Take Effect")

    ## Reloads the configuration file
    # Not yet implemented
    def reload_conf_file(self):
        pass

    ## Installs the cron job on the users PC
    # Not yet implemented
    def install_scheduled_task(self):
        pass  # TODO Implement this...

    ## Threaded option for download for day
    def threadDownloadForDay(self):
        Thread(target=self.downloadFilesForDay).start()

    ## Threaded option for download for month
    def threadDownloadForMonth(self):
        Thread(target=self.downloadFilesForMonth).start()

    ## Threaded option for download for year
    def threadDownloadForYear(self):
        Thread(target=self.downloadFilesForYear).start()

    ## Threaded function tied to a signal for showing a dialog with the given informaiton
    # @param title The title of the dialog
    # @param message The message of the dialog
    def showDialog(self, title, message):
        QMessageBox.about(self.window, title, message)

    ## Download all files for a given day
    def downloadFilesForDay(self):
        logging.info("Initiated Download For Day")

        selected_hosts = self.getSelectedHosts()
        if len(selected_hosts) is 0:
            self.showDialogSignal.emit("Error!", "No PLC Selected")
            return

        self.setProgressBarEnabled(True)
        self.setAllButtonsEnabled(False)

        for host in selected_hosts:
            try:
                sps = self.SPSFactory(host)
                qdate = self.ui.daySelector.date()
                dt = datetime.date(qdate.year(), qdate.month(), qdate.day())
                sps.download_files_for_day(dt)
            except SPSConnectionException:
                self.setProgressBarEnabled(False)

                self.showDialogSignal.emit("Error!", "Error Connecting To SPS With Address " + host)
                logging.error("Error Connecting To SPS With Address " + host)

                self.setProgressBarEnabled(True)
            except ftplib.all_errors:
                self.setProgressBarEnabled(False)

                self.showDialogSignal.emit("Error!",
                                           "An FTP Error Occurred Communicating With SPS With Address " + host + ". Make Sure The Files You Are Looking For Exist")
                logging.error("An Unknown Error Occurred Communicating With SPS With Address " + host)

                self.setProgressBarEnabled(True)

        self.showDialogSignal.emit("Done!", "Download Process Is Complete")
        logging.info("Download Process Is Complete")

        self.setProgressBarEnabled(False)
        self.setAllButtonsEnabled(True)

    ## Download all files for a given month
    def downloadFilesForMonth(self):
        logging.info("Initiated Download For Month")

        selected_hosts = self.getSelectedHosts()
        if len(selected_hosts) is 0:
            self.showDialogSignal.emit("Error!", "No PLC Selected")
            return

        self.setProgressBarEnabled(True)
        self.setAllButtonsEnabled(False)

        for host in selected_hosts:
            try:
                sps = self.SPSFactory(host)
                qdate = self.ui.monthSelector.date()
                dt = datetime.date(qdate.year(), qdate.month(), qdate.day())
                sps.download_files_for_month(dt)
            except SPSConnectionException:
                self.setProgressBarEnabled(False)

                self.showDialogSignal.emit("Error!", "Error Connecting To SPS With Address " + host)
                logging.error("Error Connecting To SPS With Address " + host)

                self.setProgressBarEnabled(True)
            except ftplib.all_errors:
                self.setProgressBarEnabled(False)

                self.showDialogSignal.emit("Error!",
                                           "An FTP Error Occurred Communicating With SPS With Address " + host + ". Make Sure The Files You Are Looking For Exist")
                logging.error("An Unknown Error Occurred Communicating With SPS With Address " + host)

                self.setProgressBarEnabled(True)

        self.showDialogSignal.emit("Done!", "Download Process Is Complete")
        logging.info("Download Process Is Complete")

        self.setProgressBarEnabled(False)
        self.setAllButtonsEnabled(True)

    ## Download all files for a given year
    def downloadFilesForYear(self):
        logging.info("Initiated Download For Year")

        selected_hosts = self.getSelectedHosts()
        if len(selected_hosts) is 0:
            self.showDialogSignal.emit("Error!", "No PLC Selected")
            return

        self.setProgressBarEnabled(True)
        self.setAllButtonsEnabled(False)

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
                logging.error("Error Connecting To SPS With Address " + host)

                self.setProgressBarEnabled(True)
            except:
                self.setProgressBarEnabled(False)

                self.showDialogSignal.emit("Error!",
                                           "An Unknown Error Occurred Communicating With SPS With Address " + host)
                logging.error("An Unknown Error Occurred Communicating With SPS With Address " + host)

                self.setProgressBarEnabled(True)

        self.showDialogSignal.emit("Done!", "Download Process Is Complete")
        logging.info("Download Process Is Complete")

        self.setProgressBarEnabled(False)
        self.setAllButtonsEnabled(True)

    ## Iterate through the list of checkboxes and get a list of all those selected
    # @return An array of strings containing the addresses
    def getSelectedHosts(self):
        selected_addresses: List[str] = []
        for checkBox in self.checkBoxes:
            if checkBox.isChecked():
                selected_addresses.append(checkBox.text())  # TODO FIXME this is bad
        return selected_addresses

    ## Set all checkboxes' checked values to a given value
    # @param selected Boolean to set the checked values to
    def setCheckedAllHosts(self, selected: bool):
        for checkBox in self.checkBoxes:
            checkBox.setChecked(selected)

    ## Check all the host check boxes
    def selectAllHosts(self):
        self.setCheckedAllHosts(True)

    ## Uncheck all the host check boxes
    def disselectAllHosts(self):
        self.setCheckedAllHosts(False)

    ## Set the enabled status of the master progress bar. Enabled makes it pulsing and green. Disabled makes it greyed out
    # @param enabled the boolean value whether its enabled or not
    def setProgressBarEnabled(self, enabled: bool):
        if enabled:
            self.ui.masterProgressBar.setRange(0, 0)
            self.ui.masterProgressBar.setEnabled(True)
        else:
            self.ui.masterProgressBar.setRange(0, 10)
            self.ui.masterProgressBar.setDisabled(True)

    ## Sets the enabled status of all the buttons that can create a thread. Used to prevent multiple async downloads
    # @param enabled the boolean value whether its enabled or not
    def setAllButtonsEnabled(self, enabled):
        self.ui.pushButtonDownloadForDay.setEnabled(enabled)
        self.ui.pushButtonDownloadForMonth.setEnabled(enabled)
        self.ui.pushButtonDownloadForYear.setEnabled(enabled)
        self.ui.pushButtonDisselectAll.setEnabled(enabled)
        self.ui.pushButtonSelectAll.setEnabled(enabled)
        for checkbox in self.checkBoxes:
            checkbox.setEnabled(enabled)

    ## Set up the UI elements and do any needed config setup before starting the UI
    def setup_ui(self):
        logging.debug("Setting Up UI")
        self.ui.pushButtonDownloadForDay.clicked.connect(self.threadDownloadForDay)
        self.ui.pushButtonDownloadForMonth.clicked.connect(self.threadDownloadForMonth)
        self.ui.pushButtonDownloadForYear.clicked.connect(self.threadDownloadForYear)

        self.ui.pushButtonSelectAll.clicked.connect(self.selectAllHosts)
        self.ui.pushButtonDisselectAll.clicked.connect(self.disselectAllHosts)

        self.ui.daySelector.setDate(QDate(datetime.datetime.today()))
        self.ui.monthSelector.setDate(QDate(datetime.datetime.today()))
        self.ui.yearSelector.setDate(QDate(datetime.datetime.today()))

        self.ui.openConfFileButton.triggered.connect(self.open_conf_file)
        self.ui.openLogFileButton.triggered.connect(self.open_log_file)

        self.ui.actionQuit.triggered.connect(exit)

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
    # def run():
    main = Main()
    app = QApplication(sys.argv)
    main.window = QMainWindow()
    main.ui = Ui_MainWindow()
    main.ui.setupUi(main.window)
    main.setup_ui()
    main.window.show()
    logging.debug("Handing Process Over To UI Thread...")
    sys.exit(app.exec_())
