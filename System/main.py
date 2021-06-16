# -*- coding: utf-8 -*-
"""
System/main.py
The Simplifyc Operating System main script
Made by Daniel M using Python 3
"""

# Check if the PyQt5 library is installed with pip
from import_modules import checkModules
checkModules()

# Library Imports
import os
import sys
import datetime

# Local File Imports
from config import *
from dialogs import *
# from overrides import *
from applications import returnApplications

# PyQt imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Define global variables
rerun, applications, config = False, returnApplications(), Config()
color_properties, font_properties = ColorConfig.returnConfig(), FontConfig.returnConfig()

print("Starting the Simplifyc Operating System...") # Print starting message

class Window(QMainWindow):
	"""Main Window"""
	def __init__(self, parent = None) -> None:
		super(Window, self).__init__(parent = parent)
		self.setStyleSheet("background-color: " + color_properties["background-color"])
		self.setMinimumWidth(QDesktopWidget().screenGeometry(-1).width())
		self.setMinimumHeight(QDesktopWidget().screenGeometry(-1).height() - 100)
		self.windows = None
		self.about = self.menuBar().addMenu("About")
		self.about.triggered.connect(self.openAbout)
		self.about.addAction(QAction("About", self))
		self.setMinimumSize(1280, 720)
		self.top_menu_bar = QToolBar("Top menu bar") # Create the top menu bar
		self.top_menu_bar.setMovable(False) # Make the top menu bar fixed
		self.top_menu_bar.setStyleSheet(f"background-color: {color_properties['secondary-background-color']}; border: 4px solid {color_properties['secondary-background-color']}; color: {color_properties['text-color']}") # Set stylesheet properties for the top menu bar
		# Add actions
		self.clock = QAction(self)
		self.clock.setFont(QFont(font_properties["font-family"], int(font_properties["font-size"])))
		self.clock_content = QTimer(self)
		self.clock_content.timeout.connect(self.updateTime)
		self.clock_content.start(1000)
		# Add actions to the Tool Bar
		self.top_menu_bar.addAction(self.clock)
		self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.top_menu_bar) # Add Tool Bar to the Window
		self.dock = QToolBar("Dock") # Create a dock
		self.dock.setMovable(False) # Make the dock fixed
		self.dock.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly) # Always display icons instead of text in the dock
		self.dock.setIconSize(QSize(32, 32)) # Configure the dock icon size
		self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.dock) # Display the toolbar at the bottom of the screen
		self.dock_items = [] # Create dock_items list
		for x in applications.keys():
			if os.path.exists(f"Applications/{x}/images/logo_small.png"): self.dock_items.append([QAction(QIcon(f"Applications/{x}/images/logo_small.png"), applications[x]["name"], self), x]) # Add values to dock_items list
			else: self.dock_items.append([QAction(applications[x]["name"], self), x]) # Add values to dock_items list
		# Trigger signals
		for x in range(len(self.dock_items)): exec(f"self.dock_items[{x}][0].triggered.connect(lambda _, self = self: self.openApplication('{applications[self.dock_items[x][1]]['run_class']}'))")
		for x in range(len(self.dock_items)): self.dock_items[x][0].setFont(QFont(font_properties["font-family"], int(font_properties["font-size"])))
		for x in self.dock_items: self.dock.addAction(x[0]) # Add applications to the dock
		self.dock.setStyleSheet(f"background-color: {color_properties['secondary-background-color']}; border: none; font-size: {font_properties['font-size']}") # Make the dock's background color white
		self.show() # Show the main window

	def openApplication(self, app: str) -> None:
		"""Opens the specified application"""
		exec(f"self.window = {app}()")
		self.window.show()
	
	@staticmethod
	def openAbout() -> None:
		"""Opens the about dialog"""
		dialog = AboutDialog()
		dialog.exec_()

	def updateTime(self) -> None:
		"""Updates the clock"""
		current_time = f"{('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')[datetime.datetime.today().weekday()]} {dict([['01', 'Jan'], ['02', 'Feb'], ['03', 'Mar'], ['04', 'Apr'], ['05', 'May'], ['06', 'Jun'], ['07', 'Jul'], ['08', 'Aug'], ['09', 'Sep'], ['10', 'Oct'], ['11', 'Nov'], ['12', 'Dec']])[QDateTime.currentDateTime().toString('MM')]} {QDateTime.currentDateTime().toString('dd hh:mm:ss')}"
		self.clock.setText(current_time)
		self.clock.setToolTip(str())
	
	def contextMenuEvent(self, _) -> None: """Set empty context menu"""
	

(application, window) = (QApplication(sys.argv), Window()) # Construct QApplication and QMainWindow

# Application Imports
for i in applications.keys(): exec(f"sys.path.insert(1, 'Applications/{i}'); " + "from " + applications[i]['file'][:-3] + " import " + applications[i]['run_class'])

window.show() # Show Main Window
application.exec_() # Execute QApplication
