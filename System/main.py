# -*- coding: utf-8 -*-
"""
System/main.py
The Simplifyc Operating System main script
Made by Daniel M using Python 3
"""

__import__("import_modules").checkModules()

# Library Imports
import os
import sys
import datetime

# Local File Imports
from config import *
from dialogs import *
# from overrides import *
from desktop_files import returnItems
from get_file_icon import getFileIcon
from applications import returnApplications

# PyQt imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Define global variables
applications, config = returnApplications(), Config()

print("Starting the Simplifyc Operating System...") # Print starting message

class Window(QMainWindow):
	"""Main Window"""
	def __init__(self, parent = None) -> None:
		super(Window, self).__init__(parent = parent)
		self.setStyleSheet("background-color: " + returnBackgroundProperties()["background-color"])
		self.window_size = returnProperties()["size"] if returnProperties()["size"] != "full" else [screen.availableGeometry().width(), screen.availableGeometry().height()] # Get window size property
		self.resize(self.window_size[0], self.window_size[1]) # Resize window
		self.setMinimumSize(256, 144) # Set minimum size
		self.windows = None
		self.about = self.menuBar().addMenu("About")
		self.about.triggered.connect(self.openAbout)
		self.about.addAction(QAction("About", self))
		self.setMinimumSize(1280, 720)
		self.top_menu_bar = QToolBar("Top menu bar") # Create the top menu bar
		self.top_menu_bar.setMovable(False) # Make the top menu bar fixed
		self.top_menu_bar.setStyleSheet(f"background-color: {returnBackgroundProperties()['secondary-background-color']}; border: 4px solid {returnBackgroundProperties()['secondary-background-color']}; color: {returnBackgroundProperties()['text-color']}") # Set stylesheet properties for the top menu bar
		# Add actions
		self.clock = QAction(self)
		self.clock.setFont(QFont(returnProperties()["font-family"], int(returnProperties()["font-size"])))
		self.clock_content = QTimer(self)
		self.clock_content.timeout.connect(self.updateTime)
		self.clock_content.start(1000)
		# Add actions to the Tool Bar
		self.top_menu_bar.addAction(self.clock)
		self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.top_menu_bar) # Add Tool Bar to the Window
		# Applications dock
		self.dock = QToolBar("Dock") # Create a dock
		self.dock.setMovable(False) # Make the dock fixed
		self.dock.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly) # Always display icons instead of text in the dock
		self.dock.setIconSize(QSize(32, 32)) # Configure the dock icon size
		self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.dock) # Display the toolbar at the bottom of the screen
		self.dock_items = [[QAction(QIcon("System/images/preferences.png"), "Preferences", self)]] # Create dock_items list
		self.dock_items[0][0].triggered.connect(self.openPreferences)
		for x in applications.keys():
			if os.path.exists(f"Applications/{x}/images/logo_small.png"): self.dock_items.append([QAction(QIcon(f"Applications/{x}/images/logo_small.png"), applications[x]["name"], self), x]) # Add values to dock_items list
			else: self.dock_items.append([QAction(applications[x]["name"], self), x]) # Add values to dock_items list
		# Trigger signals
		for x in range(1, len(self.dock_items)):
			exec(f"self.dock_items[{x}][0].triggered.connect(lambda _, self = self: self.openApplication('{applications[self.dock_items[x][1]]['run_class']}'))")
			self.dock_items[x][0].setFont(QFont(returnProperties()["font-family"], int(returnProperties()["font-size"])))
		for x in self.dock_items: self.dock.addAction(x[0]) # Add applications to the dock
		self.dock.setStyleSheet(f"background-color: {returnBackgroundProperties()['secondary-background-color']}; border: none; font-size: {returnProperties()['font-size']}") # Make the dock's background color white
		self.files = []
		row = 0
		column = 25
		for x in returnItems().keys():
			if column + 100 > self.window_size[1]:
				row += 1
				column = 25
			self.files.append([QToolButton(self), returnItems()[x]])
			self.files[-1][0].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none")
			self.files[-1][0].setText(returnItems()[x]["displayname"])
			self.files[-1][0].setIcon(getFileIcon(returnItems()[x]["extension"], returnItems()[x]["type"]))
			self.files[-1][0].setIconSize(QSize(75, 75))
			self.files[-1][0].resize(68, 100)
			self.files[-1][0].setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
			self.files[-1][0].move(row * 70, column)
			column += 100
		self.show() # Show the main window

	def openApplication(self, app: str) -> None:
		"""Opens the specified application"""
		exec(f"self.window = {app}()")
		self.window.show()

	def openPreferences(self):
		"""Opens the Preferences window"""
		self.preferences = Preferences(self.updateElements)
		self.preferences.show()

	@staticmethod
	def openAbout() -> None:
		"""Opens the about dialog"""
		dialog = AboutDialog()
		dialog.exec_()

	def updateTime(self) -> None:
		"""Updates the clock"""
		current_time = f"{('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')[datetime.datetime.today().weekday()]} {dict([['01', 'Jan'], ['02', 'Feb'], ['03', 'Mar'], ['04', 'Apr'], ['05', 'May'], ['06', 'Jun'], ['07', 'Jul'], ['08', 'Aug'], ['09', 'Sep'], ['10', 'Oct'], ['11', 'Nov'], ['12', 'Dec']])[QDateTime.currentDateTime().toString('MM')]} {QDateTime.currentDateTime().toString('dd hh:mm:ss')}"
		self.clock.setText(current_time)
	
	def contextMenuEvent(self, _) -> None: """Set empty context menu"""
	
	def updateElements(self) -> None:
		self.top_menu_bar.setStyleSheet(f"background-color: {returnBackgroundProperties()['secondary-background-color']}; border: 4px solid {returnBackgroundProperties()['secondary-background-color']}; color: {returnBackgroundProperties()['text-color']}; font-family: {returnProperties()['font-family']}") # Update stylesheet properties for the top menu bar
		self.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color']}; color: {returnBackgroundProperties()['text-color']}") # Update the window stylesheet
		for x in range(len(self.files)):
			self.files[x][0].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none")
			self.files[x][0].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))
		for x in range(1, len(self.dock_items)): self.dock_items[x][0].setFont(QFont(returnProperties()["font-family"], int(returnProperties()["font-size"]))) # Update the dock items' font
		self.dock.setStyleSheet(f"background-color: {returnBackgroundProperties()['secondary-background-color']}; border: none; font-size: {returnProperties()['font-size']}") # Update the dock's stylesheet
		self.clock.setFont(QFont(returnProperties()["font-family"], int(returnProperties()["font-size"]))) # Update the clock's font
		

application = QApplication(sys.argv) # Construct application

screen = application.primaryScreen()

window = Window() # Call main Window class

# Application Imports
for i in applications.keys(): exec(f"sys.path.insert(1, 'Applications/{i}'); " + "from " + applications[i]['file'][:-3] + " import " + applications[i]['run_class'])

window.show() # Show Main Window
application.exec_() # Execute QApplication
