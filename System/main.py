"""
System/main.py
The Simplifyc Operating System main script
Made by Daniel M using Python 3
"""

# Imports
import os
import sys

# Try to import PyQt5, if PyQt5 is not installed using pip, ask the user to install it
try: import PyQt5
except ImportError:
	if input("The PyQt5 Library is not installed. Enter 'install' to install the module, or anything else to stop the process: ").lower() == "install":
		os.system("pip3 install PyQt5")

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Check if PyQt5.QtWebEngineWidgets is installed for the browser application, if the module is not installed using pip, ask the user to install it
try: import PyQt5.QtWebEngineWidgets
except ImportError:
	if input("The PyQtWebEngineWidgets Library is not installed. Enter 'install' to install the module, or anything else to stop the process: ").lower() == "install":
		os.system("pip3 install PyQtWebEngine")

print("Starting the Simplifyc Operating System...") # Print startup message

# noinspection PyUnresolvedReferences,PyArgumentList
class AboutDialog(QDialog):
	"""About Dialog"""
	def __init__(self, parent = None):
		super(AboutDialog, self).__init__(parent = parent)
		template = QGridLayout() # Set layout to grid
		# Set fixed width and height
		self.setFixedHeight(self.height() - 175)
		self.setFixedWidth(self.width() + 100)
		title = QLabel("SimplifycOS") # Add title
		title_font = title.font() # Add new font
		title_font.setPointSize(50) # Set point size for font
		title_font.setBold(True) # Make font bold
		title.setFont(title_font) # Set font for title widget
		image_label = QLabel(self) # Create QLabel for image
		image = QPixmap("System/images/logo.png") # Load image at System/images/logo.png
		image_resized = image.scaled(345, 300)
		image_label.setPixmap(image_resized) # Render image
		# Add widgets to layout
		template.addWidget(title, 1, 2)
		template.addWidget(QLabel("The SimplifycOS was made by Daniel M using Python 3"), 2, 2)
		template.addWidget(image_label, 2, 1)
		for i in range(template.count()): template.itemAt(i).setAlignment(Qt.AlignHCenter) # Align all widgets to center
		self.setStyleSheet("color: white; background-color: #18082C;") # Set background color of dialog to #18082C and color of text to white
		self.setLayout(template) # Display the widgets

class Window(QMainWindow):
	"""Main Window"""
	def __init__(self):
		super(Window, self).__init__()
		self.windows = None
		self.about = self.menuBar().addMenu("About")
		self.about.triggered.connect(self.openAbout)
		self.about.addAction(QAction("About", self))
		self.setMinimumSize(1280, 720)
		self.dock = QToolBar("Dock") # Create a dock
		self.dock.setMovable(False) # Make the dock fixed
		self.dock.setToolButtonStyle(Qt.ToolButtonIconOnly) # Always display icons instead of text in the dock
		self.dock.setIconSize(QSize(32, 32)) # Configure the dock icon size
		self.addToolBar(Qt.BottomToolBarArea, self.dock) # Display the toolbar at the bottom of the screen
		self.applications = [QAction(QIcon("System/images/browser.png"), "Browser", self), QAction(QIcon("System/images/terminal.png"), "Terminal", self), QAction(QIcon("System/images/calculator.png"), "Calculator", self), QAction(QIcon("System/images/textedit.png"), "TextEdit", self)] # Create list of applications
		# Triggered signals
		self.applications[0].triggered.connect(lambda: self.openApplication("Browser"))
		self.applications[1].triggered.connect(lambda: self.openApplication("Terminal"))
		self.applications[2].triggered.connect(lambda: self.openApplication("Calculator"))
		self.applications[3].triggered.connect(lambda: self.openApplication("TextEdit"))
		for i in self.applications: self.dock.addAction(i) # Add application to the dock
		self.show() # Show the main window

	def openApplication(self, app):
		"""Opens the specified application"""
		exec(f"self.window = {app}()")
		self.window.show()
	
	@staticmethod
	def openAbout():
		"""Opens the about dialog"""
		dialog = AboutDialog()
		dialog.exec_()


(application, window) = (QApplication(sys.argv), Window()) # Construct QApplication and QMainWindow
# Local Imports

sys.path.insert(1, "Applications/SimplifycBrowser")
try:
	from browser import Browser
except ImportError:
	os.system("An error occurred. Please re-run the program.")
sys.path.insert(1, "Applications/SimplifycTerminal")
from terminal import Terminal
sys.path.insert(1, "Applications/SimplifycCalculator")
from calculator import Calculator
sys.path.insert(1, "Applications/SimplifycTextEdit")
from textedit import TextEdit

window.show() # Show Main Window
application.exec_() # Execute QApplication
