# -*- coding: utf-8 -*-
"""
System/main.py
The Mini Operating System main script
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
from widgets import *
# from overrides import *
from desktop_files import returnItems
from get_file_icon import getFileIcon
from applications import *

# PyQt imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

# Define global variables
applications, config = returnApplications(), Config()

print("Starting the Mini Operating System...") # Print starting message

class Window(QMainWindow):
	"""Main Window"""
	def __init__(self, parent = None) -> None:
		super(Window, self).__init__(parent = parent)
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.setStyleSheet("background-color: " + returnBackgroundProperties()["background-color"])
		self.window_size = screen.availableGeometry().width(), screen.availableGeometry().height() # Get window size property
		self.windows = []
		self.about = self.menuBar().addMenu("About")
		self.about.triggered.connect(self.openAbout)
		self.about.addAction(QAction("About", self))
		self.setMinimumSize(1280, 720)
		self.top_menu_bar = QToolBar("Top menu bar") # Create the top menu bar
		self.top_menu_bar.setMovable(False) # Make the top menu bar fixed
		self.top_menu_bar.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}; border: 4px solid {returnBackgroundProperties()['background-color-2']}; color: {returnBackgroundProperties()['text-color']}") # Set stylesheet properties for the top menu bar
		# Define actions
		# # Clock
		self.clock = QWebEngineView()
		self.clock.setUrl(QUrl(f"https://home.danielmiao1.repl.co/clock.html?background_color={returnBackgroundProperties()['background-color-2'][1:]}&text_color={returnBackgroundProperties()['text-color'][1:]}&font_size={returnProperties()['font-size']}px&font_family={returnProperties()['font-family']}"))
		# Add actions to the Tool Bar
		self.top_menu_bar.addWidget(self.clock)
		self.top_menu_bar.setFixedHeight(40)
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
		self.dock.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}; border: none; font-size: {returnProperties()['font-size']}") # Make the dock's background color white
		self.files = []
		row, column = 0, 40
		for x in returnItems().keys():
			if column + 137.5 > self.window_size[1]:
				row += 1
				column = 40
			self.files.append([QToolButton(self), returnItems()[x]])
			self.files[-1][0].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none")
			self.files[-1][0].setText(returnItems()[x]["displayname"])
			self.files[-1][0].setIcon(getFileIcon(returnItems()[x]["extension"], returnItems()[x]["type"]))
			self.files[-1][0].setIconSize(QSize(75, 75))
			self.files[-1][0].resize(68, 100)
			self.files[-1][0].setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
			self.files[-1][0].move(row * 70, column)
			column += 100
		self.showFullScreen()
		self.show() # Show the main window

	def openApplication(self, app: str) -> None:
		"""Opens the specified application"""
		exec(f"self.windows.append(ApplicationWindow(self, QPoint(0, 0), {app}(), background_color = '{returnApplicationProperties()[app]['background-color'] if returnApplicationProperties()[app]['background-color'] != 'default' else returnBackgroundProperties()['background-color']}', window_name = '{app}'))")
		self.setCentralWidget(self.windows[-1])

	def openPreferences(self) -> None:
		"""Opens the Preferences window"""
		self.windows.append(ApplicationWindow(self, QPoint(0, 0), Preferences(self.updateElements), background_color = returnBackgroundProperties()["background-color-2"], window_name = "Preferences"))
		self.setCentralWidget(self.windows[-1])
	
	@staticmethod
	def openAbout() -> None:
		"""Opens the about dialog"""
		dialog = AboutDialog()
		dialog.exec_()

	def contextMenuEvent(self, _) -> None: """Set empty context menu"""
	
	def updateElements(self) -> None:
		self.top_menu_bar.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}; border: 4px solid {returnBackgroundProperties()['background-color-2']}; color: {returnBackgroundProperties()['text-color']}; font-family: {returnProperties()['font-family']}") # Update stylesheet properties for the top menu bar
		self.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color']}; color: {returnBackgroundProperties()['text-color']}") # Update the window stylesheet
		for x in range(len(self.files)):
			self.files[x][0].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none")
			self.files[x][0].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))
		for x in range(1, len(self.dock_items)): self.dock_items[x][0].setFont(QFont(returnProperties()["font-family"], int(returnProperties()["font-size"]))) # Update the dock items' font
		self.dock.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}; border: none; font-size: {returnProperties()['font-size']}") # Update the dock's stylesheet
		
	def resizeEvent(self, event: QResizeEvent) -> None:
		row, column = 0, 40
		for x in range(len(self.files)):
			if column + 137.5 > event.size().height():
				row += 1
				column = 40
			self.files[x][0].move(row * 70, column)
			column += 100
			
			
application = QApplication(sys.argv) # Construct application

screen = application.primaryScreen()

window = Window() # Call main Window class

# Application Imports
for i in applications.keys(): exec(f"sys.path.insert(1, 'Applications/{i}'); " + "from " + applications[i]['file'][:-3] + " import " + applications[i]['run_class'])

window.show() # Show Main Window
application.exec_() # Execute QApplication
