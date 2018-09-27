import configparser
import os


class ConfigManager:
    def __init__(self, filename):
        self.__config = configparser.ConfigParser()
        self.__config.read(filename)

        self.SPSaddresses = (self.__config['DEFAULT']['addresses']).split(',')
        self.SPSuser = self.__config['DEFAULT']['username']
        self.SPSpassword = self.__config['DEFAULT']['password']
        self.downloaddestination = self.__config['DEFAULT']['default_destination'].replace("~", "c:\\Users\\" + os.getlogin())
        self.connectionnumretries = int(self.__config['DEFAULT']['number_connection_retries'])
        self.connectionretrydelay = int(self.__config['DEFAULT']['connection_retry_delay'])
        self.SPSfullwarningdays = int(self.__config['EMAIL']['warning_days'])
        self.log_path = self.__config['DEFAULT']['log_path']
