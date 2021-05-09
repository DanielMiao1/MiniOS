# The Simplifyc Operating System main script
# Made by Daniel M using Python 3

# Imports
import os
import sys

# Try to import PyQt5, if PyQt5 is not installed using pip, ask the user to install it
try: import PyQt5
except ImportError:
	if input("The PyQt5 Library is not installed. Enter 'install' to install the module, or anything else to stop the process: ").lower() == "install":
		os.system("pip3 install PyQt5")
finally:
	from PyQt5.QtGui import *
	from PyQt5.QtCore import *
	from PyQt5.QtWidgets import *

# Check if PyQt5.QtWebEngineWidgets is installed for the browser application, if the module is not installed using pip, ask the user to install it
try: import PyQt5.QtWebEngineWidgets
except ImportError:
	if input("The PyQtWebEngineWidgets Library is not installed. Enter 'install' to install the module, or anything else to stop the process: ").lower() == "install":
		os.system("pip3 install PyQtWebEngine")

print("Starting the Simplifyc Operating System...") # Print startup message

class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.application = "MAIN"
		self.setMinimumSize(1280, 720)
		self.dock = QToolBar("Dock") # Create a dock
		self.dock.setMovable(False) # Make the dock fixed
		self.dock.setToolButtonStyle(Qt.ToolButtonIconOnly) # Always display icons instead of text in the dock
		self.dock.setIconSize(QSize(32, 32)) # Configure the dock icon size
		self.addToolBar(Qt.BottomToolBarArea, self.dock) # Display the toolbar at the bottom of the screen
		self.applications = {"Browser" : QAction(QIcon("System/images/browser.png"), "Browser", self), "Terminal" : QAction(QIcon("System/images/terminal.png"), "Terminal", self), "Calculator" : QAction(QIcon("System/images/calculator.png"), "Calculator", self), "TextEdit" : QAction(QIcon("System/images/textedit.png"), "TextEdit", self)} # Create list of applications
		# for i in self.applications: self.applications[i].triggered.connect(lambda: self.openApplication(i)) # Call the openApplication function with the application name when any application is triggered
		# self.applications["Browser"].triggered.connect(lambda: Browser()) # Run Applications/SimplifycBrowser/main.py script when the first action in self.applications list is triggered
		# self.applications["Terminal"].triggered.connect(lambda: a()) # Run Applications/SimplifycTerminal/main.py script when the second action in self.applications list is triggered
		# self.applications["Calculator"].triggered.connect(lambda: calculator()) # Run Applications/SimplifycCalculator/main.py script when the third action in self.applications list is triggered
		# self.applications["TextEdit"].triggered.connect(lambda: textEdit())  # Run Applications/SimplifycTextEdit/main.py script when the fourth action in self.applications list is triggered
		self.applications["Browser"].triggered.connect(lambda: os.system("python3 Applications/SimplifycBrowser/browser.py"))
		self.applications["Terminal"].triggered.connect(lambda: os.system("python3 Applications/SimplifycTerminal/terminal.py"))
		self.applications["Calculator"].triggered.connect(lambda: os.system("python3 Applications/SimplifycCalculator/calculator.py"))
		self.applications["TextEdit"].triggered.connect(lambda: os.system("python3 Applications/SimplifycTextEdit/textedit.py"))
		for i in self.applications: self.dock.addAction(self.applications[i]) # Add each application to the dock
		self.show() # Show the main window

		def a():
			Terminal()
	# def openApplication(self, app):
	# 	print(app)
	# 	if self.application == "MAIN": return
	# 	if app == "Browser": self.application = Browser() # If Application is browser; set self.application variable equal to Browser()
	# 	self.application.show()


(application, window) = (QApplication(sys.argv), Window()) # Construct QApplication and QMainWindow
# Local Imports

# sys.path.insert(1, "Applications/SimplifycBrowser")
# from browser import *
# sys.path.insert(1, "Applications/SimplifycTerminal")
# from terminal import Terminal
# sys.path.insert(1, "Applications/SimplifycCalculator")
# from calculator import *
# sys.path.insert(1, "Applications/SimplifycTextEdit")
# from textedit import *

window.show() # Show Main Window
application.exec_() # Execute QApplication
