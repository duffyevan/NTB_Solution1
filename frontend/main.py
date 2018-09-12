import sys
from PyQt5.QtWidgets import QApplication, QWidget
from data_collection_automation.SPSLib import SPSLib
from data_collection_automation.HostpointLib import HostpointClient

app = QApplication(sys.argv)
w = QWidget(flags=None)
w.resize(500,500)
w.setWindowTitle("NTB Data Collection Automation")
w.show()

sys.exit(app.exec_())
