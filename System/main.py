# -*- coding: utf-8 -*-
"""
System/main.py
The Simplifyc Operating System main script
Made by Daniel M using Python 3
"""

# Library Imports
import os
import sys
import datetime

# Local File Imports
from getApplications import returnApplications

# Define global variables
rerun, applications = False, returnApplications()
# Try to import PyQt5, if PyQt5 is not installed using pip, ask the user to install it
try:
	from PyQt5.QtGui import *
	from PyQt5.QtCore import *
	from PyQt5.QtWidgets import *
except ImportError:
	rerun = True # Set rerun variable to True
	if input("The PyQt5 Library is not installed. Enter 'install' to install the module, or anything else to stop the process: ").lower() == "install": os.system("pip3 install PyQt5")
	else:
		print("You can manually install the PyQt5 Library by running the 'pip3 install PyQt5' command in the terminal")
		exit()

# Check if PyQt5.QtWebEngineWidgets is installed for the browser application, if the module is not installed using pip, ask the user to install it
try: import PyQt5.QtWebEngineWidgets
except ImportError:
	rerun = True # Set rerun variable to True
	if input("The PyQtWebEngineWidgets Library is not installed. Enter 'install' to install the module, or anything else to stop the process: ").lower() == "install":
		os.system("pip3 install PyQtWebEngine")
	else:
		print("You can manually install the PyQtWebEngineWidgets Library by running the 'pip3 install PyQtWebEngine' command in the terminal")
		exit()

if rerun: os.system("python3 System/rerun.py") # Run System/rerun.py script if rerun variable is True

print("Starting the Simplifyc Operating System...") # Print starting message

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
		self.setMinimumWidth(QDesktopWidget().screenGeometry(-1).width())
		self.setMinimumHeight(QDesktopWidget().screenGeometry(-1).height() - 100)
		self.windows = None
		self.about = self.menuBar().addMenu("About")
		self.about.triggered.connect(self.openAbout)
		self.about.addAction(QAction("About", self))
		self.setMinimumSize(1280, 720)
		self.top_menu_bar = QToolBar("Top menu bar") # Create the top menu bar
		self.top_menu_bar.setMovable(False) # Make the top menu bar fixed
		# Add actions
		self.clock = QAction(self)
		self.clock_content = QTimer(self)
		self.clock_content.timeout.connect(self.updateTime)
		self.clock_content.start(1000)
		# Add actions to the Tool Bar
		self.top_menu_bar.addAction(self.clock)
		self.addToolBar(Qt.TopToolBarArea, self.top_menu_bar) # Add Tool Bar to the Window
		self.dock = QToolBar("Dock") # Create a dock
		self.dock.setMovable(False) # Make the dock fixed
		self.dock.setToolButtonStyle(Qt.ToolButtonIconOnly) # Always display icons instead of text in the dock
		self.dock.setIconSize(QSize(32, 32)) # Configure the dock icon size
		self.addToolBar(Qt.BottomToolBarArea, self.dock) # Display the toolbar at the bottom of the screen
		self.dock_items = [] # Create dock_items list
		for x in applications.keys(): self.dock_items.append([QAction(QIcon(f"Applications/{x}/images/logo_small.png"), applications[x]["name"], self), x]) # Add values to dock_items list
		# Trigger signals
		for x in range(len(self.dock_items)): exec(f"self.dock_items[{x}][0].triggered.connect(lambda _, self = self: self.openApplication('{applications[self.dock_items[x][1]]['run_class']}'))")
		for x in self.dock_items: self.dock.addAction(x[0]) # Add applications to the dock
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

	def updateTime(self):
		"""Updates the clock"""
		current_time = f"{('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')[datetime.datetime.today().weekday()]} {dict([['01', 'Jan'], ['02', 'Feb'], ['03', 'Mar'], ['04', 'Apr'], ['05', 'May'], ['06', 'Jun'], ['07', 'Jul'], ['08', 'Aug'], ['09', 'Sep'], ['10', 'Oct'], ['11', 'Nov'], ['12', 'Dec']])[QDateTime.currentDateTime().toString('MM')]} {QDateTime.currentDateTime().toString('dd hh:mm:ss')}"
		self.clock.setText(current_time)
		self.clock.setToolTip("Time")
	
	def contextMenuEvent(self, _): """Set empty context menu"""


(application, window) = (QApplication(sys.argv), Window()) # Construct QApplication and QMainWindow

# Application Imports
for i in applications.keys(): exec(f"sys.path.insert(1, 'Applications/{i}'); " + "from " + applications[i]['file'][:-3] + " import " + applications[i]['run_class'])

window.show() # Show Main Window
application.exec_() # Execute QApplication
