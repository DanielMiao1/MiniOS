# -*- coding: utf-8 -*-
"""
System/main.py
The Mini Operating System main script
Made by Daniel M using Python 3
"""

__import__("import_modules").checkModules()

# Library Imports
from os import path, system
from sys import argv
from sys import path as sys_path

# Local File Imports
from config import *
from dialogs import *
from widgets import *
from overrides import *
from applications import *
from desktop_files import returnItems
from get_file_icon import getFileIcon

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
		self.clock = WebEngineView(hide_context_menu = True)
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
			if path.exists(f"Applications/{x}/images/logo_small.png"): self.dock_items.append([QAction(QIcon(f"Applications/{x}/images/logo_small.png"), applications[x]["name"], self), x]) # Add values to dock_items list
			else: self.dock_items.append([QAction(applications[x]["name"], self), x]) # Add values to dock_items list
		# Trigger signals
		for x in range(1, len(self.dock_items)):
			exec(f"self.dock_items[{x}][0].triggered.connect(lambda _, self = self: self.openApplication('{applications[self.dock_items[x][1]]['run_class']}'))")
			self.dock_items[x][0].setFont(QFont(returnProperties()["font-family"], int(returnProperties()["font-size"])))
		for x in self.dock_items: self.dock.addAction(x[0]) # Add applications to the dock
		self.dock.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}; border: none; font-size: {returnProperties()['font-size']}") # Make the dock's background color white
		self.files, self.edit_file = [], [None, None]
		row, column = 0, 40
		for x in returnItems().keys():
			if column + 137.5 > self.window_size[1]:
				row += 1
				column = 40
			self.files.append(QToolButton(self))
			self.files[-1].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none")
			self.files[-1].setText(returnItems()[x]["displayname"])
			self.files[-1].setIcon(getFileIcon(returnItems()[x]["extension"], returnItems()[x]["type"]))
			self.files[-1].setIconSize(QSize(75, 75))
			self.files[-1].resize(68, 100)
			self.files[-1].setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
			self.files[-1].move(row * 70, column)
			column += 100
		self.showFullScreen()
		self.show() # Show the main window

	def openApplication(self, app: str) -> None: exec(f"self.windows.append(ApplicationWindow(self, QPoint(0, 0), {app}(), background_color = '{returnApplicationProperties()[app]['background-color'] if returnApplicationProperties()[app]['background-color'] != 'default' else returnBackgroundProperties()['background-color']}', window_name = '{app}', toolbar_background_color = '{returnBackgroundProperties()['background-color-3']}', window_size = {returnApplicationProperties()[app]['window-size']}))")

	def openPreferences(self) -> None: self.windows.append(ApplicationWindow(self, QPoint(0, 0), Preferences(self.updateElements), background_color = returnBackgroundProperties()["background-color-2"], window_name = "Preferences", toolbar_background_color = returnBackgroundProperties()['background-color-3'], custom_stylesheet = "background-color: " + returnBackgroundProperties()["background-color-2"], restart_window_function = self.openPreferences))
	
	@staticmethod
	def openAbout() -> None:
		"""Opens the about dialog"""
		dialog = AboutDialog()
		dialog.exec_()

	def contextMenuEvent(self, event: QEvent) -> None:
		"""Set context menu for desktop"""
		menu = QMenu(self)
		new_file, new_directory, action = menu.addAction("New file"), menu.addAction("New directory"), menu.exec_(self.mapToGlobal(event.pos()))
		if action == new_file:
			# Get row and column count
			row, column = 0, 40 # Set default values
			for _ in range(len(self.files)):
				if column + 137.5 > self.window_size[1]:
					row += 1
					column = 40
				column += 100
			self.edit_file = [QToolButton(self), FileEditLineEdit(self)] # Make new QToolButton and QLineEdit
			# QToolButton properties
			self.edit_file[0].resize(68, 100) # Resize
			self.edit_file[0].move(row * 70, column - 8) # Move
			self.edit_file[0].setIcon(getFileIcon(None, None)) # Set default icon
			self.edit_file[0].setIconSize(QSize(75, 75)) # Set icon size
			self.edit_file[0].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none") # Set styles
			# QLineEdit properties
			self.edit_file[1].resize(68, 20) # Resize
			self.edit_file[1].move(row * 70, column + 98) # Move
			self.edit_file[1].setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False) # Set attribute
			self.edit_file[1].setStyleSheet(f"border: 1px solid {returnBackgroundProperties()['text-color']}; background-color: {returnBackgroundProperties()['background-color-2']}") # Set styles
			self.edit_file[1].returnPressed.connect(lambda: self.newFileReturnPressed(row, column)) # Return key pressed signal
			self.edit_file[1].setFocus() # Focus
			# Show QToolButton and QLineEdit
			self.edit_file[0].show()
			self.edit_file[1].show()
	
	def newFileReturnPressed(self, row, column, signal = 1) -> None:
		if signal != 1: return
		file_name = f"{self.edit_file[1].text()}.minios"
		system(f"touch Home/Desktop/{file_name}") # Make file
		# # Remove QToolButton and QLineEdit
		self.edit_file[0].deleteLater()
		self.edit_file[1].deleteLater()
		# Clear self.edit_file list
		self.edit_file = [None, None]
		# Make new file
		self.files.append(QToolButton(self))
		self.files[-1].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none")
		self.files[-1].setText(file_name[:-7])
		self.files[-1].setIcon(getFileIcon(None if len(file_name.split(".")) == 2 else file_name.split(".")[-2], "file"))
		self.files[-1].setIconSize(QSize(75, 75))
		self.files[-1].resize(68, 100)
		self.files[-1].setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
		self.files[-1].move(row * 70, column)
		self.files[-1].show()
		# self.update()
	
	def updateElements(self) -> None:
		self.top_menu_bar.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}; border: 4px solid {returnBackgroundProperties()['background-color-2']}; color: {returnBackgroundProperties()['text-color']}; font-family: {returnProperties()['font-family']}") # Update stylesheet properties for the top menu bar
		self.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color']}; color: {returnBackgroundProperties()['text-color']}") # Update the window stylesheet
		for x in range(len(self.files)):
			self.files[x].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none")
			self.files[x].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))
		for x in range(1, len(self.dock_items)): self.dock_items[x][0].setFont(QFont(returnProperties()["font-family"], int(returnProperties()["font-size"]))) # Update the dock items' font
		self.dock.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}; border: none; font-size: {returnProperties()['font-size']}") # Update the dock's stylesheet
		
	def resizeEvent(self, event: QResizeEvent) -> None:
		row, column = 0, 40
		for x in range(len(self.files)):
			if column + 137.5 > event.size().height():
				row += 1
				column = 40
			self.files[x].move(row * 70, column)
			column += 100
			
			
application = QApplication(argv) # Construct application

screen = application.primaryScreen()

window = Window() # Call main Window class

# Application Imports
for i in applications.keys(): exec(f"sys_path.insert(1, 'Applications/{i}'); " + "from " + applications[i]['file'][:-3] + " import " + applications[i]['run_class'])

window.show() # Show Main Window
application.exec_() # Execute QApplication
