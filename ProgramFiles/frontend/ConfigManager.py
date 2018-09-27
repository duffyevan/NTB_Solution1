import configparser
import os


class ConfigManager:
    ## Constructor
    # Loads a configuration from the given file name
    def __init__(self, filename):
        if not os.path.isfile(filename):
            print('\033[91mCould Not Find Configuration File On Disk, Using Default Settings (Which Are Probably Wrong)\033[0m')
            self._defaults()
        else:
            self.__config = configparser.ConfigParser()
            self.__config.read(filename)

            self.SPSaddresses = (self.__config['DEFAULT']['addresses']).split(',')
            self.SPSuser = self.__config['DEFAULT']['username']
            self.SPSpassword = self.__config['DEFAULT']['password']
            self.downloaddestination = self.__config['DEFAULT']['default_destination'].replace("~",
                                                                                               "c:\\Users\\" + os.getlogin())
            self.connectionnumretries = int(self.__config['DEFAULT']['number_connection_retries'])
            self.connectionretrydelay = int(self.__config['DEFAULT']['connection_retry_delay'])
            self.SPSfullwarningdays = int(self.__config['EMAIL']['warning_days'])
            self.log_path = self.__config['DEFAULT']['log_path']

    ## Default Constructor
    # Just uses default values
    def _defaults(self):
        self.SPSaddresses = ["10.0.0.1"]
        self.SPSuser = "ts"
        self.SPSpassword = "ts4all"
        self.downloaddestination = "./"
        self.logfilelocation = "./log.txt"
        self.connectionnumretries = 1
        self.connectionretrydelay = 1
        self.SPSfullwarningdays = 0
        self.log_path = './log.txt'
