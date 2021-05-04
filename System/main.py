# The Simplifyc Operating System main script
# Made by Daniel M using Python 3

# Imports
import os
import sys

try: import PyQt5
except ImportError:
	if input("The PyQt5 Library is not installed. Enter 'install' to install the module, or anything else to stop the process: ").lower() == "install":
		os.system("pip3 install PyQt5")
finally:
	from PyQt5.QtGui import *
	from PyQt5.QtCore import *
	from PyQt5.QtWidgets import *

try: import PyQt5.QtWebEngineWidgets
except ImportError:
	if input("The PyQtWebEngineWidgets Library is not installed. Enter 'install' to install the module, or anything else to stop the process: ").lower() == "install":
		os.system("pip3 install PyQtWebEngine")
finally: from PyQt5.QtWebEngineWidgets import *

print("Starting the Simplifyc Operating System...") # Print startup message

class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.dock = QToolBar("Dock") # Create a dock
		self.dock.setMovable(False) # Make the dock fixed
		self.dock.setToolButtonStyle(Qt.ToolButtonIconOnly) # Always display icons instead of text in the dock
		self.dock.setIconSize(QSize(16, 16)) # Configure the dock icon size
		self.addToolBar(Qt.BottomToolBarArea, self.dock) # Display the toolbar at the bottom of the screen
		self.applications = [QAction(QIcon("System/images/browser.png"), "Browser", self)] # Create list of applications
		self.applications[0].triggered.connect(lambda: os.system("python3 Applications/OSApplications/SimplifycBrowser/main.py")) # Run Applications/OSApplications/SimplifycBrowser/main.py script when the first item in self.applications list is triggered
		for i in self.applications: self.dock.addAction(i)
		self.show() # Show the main window

(application, window) = (QApplication(sys.argv), Window())
application.exec_() # Create new Qt application and run Window class
