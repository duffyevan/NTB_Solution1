# NTB WPZ Automation
Automating the data collection process from SPS (PLC) modules in the field.



# Installation
This section will walk you through the steps required to get the program up and running.
### Installing Python 3
If python is not already installed, please follow these instructions:

The program is written for python 3, specifically 3.5 and above. 
1. Go To [The Python Install Page](https://www.python.org/downloads/) and chose the most recent version of python3 (currently 3.7)
2. Run the installer that is downloaded, and follow the steps for a default installation (if asked, make sure you add python to PATH and associate .py files with the python launcher, these should be done by default)
    1. If prompted, make sure you chose to install `pip` as well.
3. Open up CMD and make sure python is in the path by running python (or python3 if that doesn't work). If a prompt comes up, then python is installed correctly. Type `exit()` to close python.


### Installing Required Python Packages
1. In the command window, naviage to the `NTB-WPZ-Automation` folder that came out of the zip file and then navigate to the `Setup` folder.
2. Run the command `python -m pip -r requirements.txt` to install the required packages.
    1. You may need to have admin privileges to run this command. If so, reopen CMD in administrator mode

### Installing LinkManager
1. Grab the latest version of LinkManager at the [B&R Automation Download Page](https://www.br-automation.com/en/downloads/#categories=Software/Remote+Maintenance/LinkManager)
2. Run the installer as an administrator and let it go through the default installation.
3. Once installed, there should be a LinkManager shortcut in the Start Menu or on the Desktop. Give it a try to make sure it starts up.
    1. LinkManager runs in the app tray in the bottom right of the screen in Windows. Once it has fully loaded it will open an internet browser page with a console.
    
### Getting a Certificate For LinkManager
1. The Certificate must be obtained from someone at NTB who owns the license. Currently (27/9/2018) that person is Rupert Fritz.
2. Once the certificate is obtained, open the console of LinkManager and upload the cert file using the interface, then enter the password linked to the certificate.

### Creating A Shortcut to The Main Program
You're almost there! All that needs to be done now is creating an easy way to launch the program. 
1. Navigate to the `NTB-WPZ-Automation` folder that came out of the zip file and then navigate to the `ProgramFiles` folder.
2. Right click the `main_frontend.py` file, and chose `Send To... -> Desktop (Create Shortcut)`.
3. Rename the shortcut on the desktop to something memorable



# Running The Program
To run the program, double click the shortcut created in the previous section or just run `main_frontend.py`. On the first 
run, you will likely need to set the SPS Addresses to the addresses of your SPSs. To do so, open the `Configuration` tab 
in the menubar and select `Open Configuration File`. Once in notepad, edit the `addresses` variable to be a list of ip 
addresses or hostname separated by commas (but no spaces). Edit any other parameters you would like to change from the default.

Once satisfied with the config file, save and close notepad. You will be prompted by the program to restart the program 
for the changed to take effect. Please do so.

On the next run, the list of SPS addresses should be updated to your configuration. You can now select a day, month or 
year, select a subset of addresses and then press the download button. This will download files from the SPSs for that given
time period to the download location which is `NTB-WPZ-Automation\DownloadedFiles` by default.



# LinkManager Caveat
The limitation to the current LinkManager setup is that only one SPS can be connected to at a time, meaning even 
though this program is capable of sequentially downloading from and unlimited number of SPSs, LinkManager makes it 
impossible to download from more than one SPS per go. We tried to set up LogTunnel which would have allowed us to 
connect to all SPSs at the same time via LinkManager, but we ran into licencing issues and chose to take a different 
approach to the problem. If in the future, LogTunnel or something similar is set up where all SPSs are on the local 
network at once, this program will be able to download from all of them at once. 

Currently the best option is to connect to one SPS, select that once SPS in the python program, and download. Once 
done, disconnect using LinkManager and connect to the next SPS via LinkManager and repeat.
