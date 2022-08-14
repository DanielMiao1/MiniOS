# -*- coding: utf-8 -*-
"""
System/main.py
The Mini Operating System main script
Made by Daniel M using Python 3
"""


import sys
from os import path

from config import *
from dialogs import *
from widgets import *
from widgets.buttons import *
from applications import *
from core import *
import applications as _applications
import desktop

__import__("import_modules").checkModules()

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

applications, config = _applications.returnApplications(), Config()

print("Starting the Mini Operating System...")  # Print starting message (maybe remove?)


class Window(QMainWindow):
	"""Main Window"""
	def __init__(self, parent=None) -> None:
		"""Main window __init__"""
		super(Window, self).__init__(parent=parent)  # Call super class __init__ function
		self.context_menu = None
		self.showing_keyboard_viewer = False
		self.file_created_session = False  # Set file_created_session variable to False
		self.setStyleSheet("background-color: " + returnBackgroundProperties()["background-color"])  # Set window style
		self.window_size = application.primaryScreen().availableGeometry().width(), application.primaryScreen().availableGeometry().height()  # Get window size property
		self.windows = []  # Create windows list
		self.about = self.menuBar().addMenu("About")  # Add about menu
		self.about.triggered.connect(self.openAbout)  # Connect about menu trigger signal
		self.about.addAction(QAction("About", self))  # Add action "about" to about menu
		self.setMinimumSize(1280, 720)  # Set window minimum size
		# Top toolbar
		self.top_tool_bar = QToolBar("Top menu bar")  # Create the top menu bar
		self.top_tool_bar.setMovable(False)  # Make the top menu bar fixed
		self.top_tool_bar.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}; border: 4px solid {returnBackgroundProperties()['background-color-2']}; color: {returnBackgroundProperties()['text-color']}")  # Set stylesheet properties for the top menu bar
		# Define actions
		# # Clock
		self.clock = Clock(self)
		self.clock.setStyles(background_color=returnBackgroundProperties()["background-color-2"], text_color=returnBackgroundProperties()["text-color"], font_size=returnProperties()["font-size"], font_family=returnProperties()["font-family"])
		# # Separator
		self.top_tool_bar_separator = QWidget()
		self.top_tool_bar_separator.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		# # Options
		self.options = OptionsMenu(self, close_event=self.shutDownWindow, keyboard_viewer_event=self.showKeyboardViewer)
		# Add actions to the Tool Bar
		self.top_tool_bar.addWidget(self.clock)  # Add clock widget
		self.top_tool_bar.addWidget(self.top_tool_bar_separator)  # Add separator
		self.top_tool_bar.addWidget(self.options)  # Add options menu button
		self.top_tool_bar.setFixedHeight(40)  # Set fixed height
		self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.top_tool_bar)  # Add Tool Bar to the Window
		# Applications dock
		self.dock = dock.Dock(self)
		self.dock.setStyles(background_color=returnBackgroundProperties()["background-color-2"], text_color=returnBackgroundProperties()["text-color"], font_size=returnProperties()["font-size"], font_family=returnProperties()["font-family"])
		for x in applications.keys():  # Iterate through the applications
			# Check if the application has an icon
			if path.exists(f"Applications/{x}/images/logo.png"):
				icon_path = f"Applications/{x}/images/logo.png"
			elif path.exists(f"Applications/{x}/images/logo.jpg"):
				icon_path = f"Applications/{x}/images/logo.jpg"
			elif path.exists(f"Applications/{x}/images/logo.jpeg"):
				icon_path = f"Applications/{x}/images/logo.jpeg"
			elif path.exists(f"Applications/{x}/images/icon.png"):
				icon_path = f"Applications/{x}/images/icon.png"
			elif path.exists(f"Applications/{x}/images/icon.jpg"):
				icon_path = f"Applications/{x}/images/icon.jpg"
			elif path.exists(f"Applications/{x}/images/icon.jpeg"):
				icon_path = f"Applications/{x}/images/icon.jpeg"
			else:
				continue
			self.dock.addItem(applications[x]["name"], icon_path, applications[x]["run_class"])
		self.dock.addItem("Settings", "System/images/preferences.png")
		# for x in range(1, len(self.dock_items)):
		# 	exec(f"self.dock_items[{x}][0].triggered.connect(lambda _, self = self: self.openApplication('{applications[self.dock_items[x][1]]['run_class']}'))") # Connect dock item trigger signal
		# 	self.dock_items[x][0].setFont(QFont(returnProperties()["font-family"], int(returnProperties()["font-size"]))) # Set font size
		# for x in self.dock_items:
		# 	self.dock.addAction(x[0]) # Add applications to the dock
		# self.dock.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}; border: none; font-size: {returnProperties()['font-size']}") # Set the dock's style properties
		# Desktop
		self.files, self.edit_file, self.focused_file = [], [None, None], None  # Assign variables
		row, column = 0, 40  # Set default row and column variable
		for x in desktop.returnItems().keys():
			if column + 137.5 > self.window_size[1]:
				row += 1
				column = 40
			self.files.append(ToolButton(self))  # Append new ToolButton
			self.files[-1].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none;")  # Set style
			self.files[-1].setText(desktop.returnItems()[x]["displayname"])  # Set text
			self.files[-1].setIcon(desktop.getFileIcon(desktop.returnItems()[x]["extension"], desktop.returnItems()[x]["type"]))  # Set icon
			self.files[-1].setIconSize(QSize(75, 75))  # Set icon size
			self.files[-1].resize(68, 100)  # Resize
			self.files[-1].setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)  # Set text/icon position
			self.files[-1].move(row * 70, column)  # Move
			self.files[-1].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))  # Set font
			self.files[-1].pressed.connect((lambda self, length: (lambda: self.setFocusedFile(self.files[length])))(self, len(self.files) - 1))
			column += 100  # Increase column count
		self.showFullScreen()  # Show window in full screen
		self.options.updateMenuPosition(self.width() - 100, "default")  # Update the Options Menu position

	def setFocusedFile(self, file: typing.Union[ToolButton, None] = None):
		"""Sets the focused file"""
		if file is None:
			return  # Exit function if file is None
		if self.focused_file is not None:
			self.focused_file.setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none;")  # If there is already a focused file, reset its stylesheet properties
		file.setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none; background-color: {returnBackgroundProperties()['background-color-2']};")  # Set the new focused file's stylesheet properties
		self.focused_file = file  # Set focused file variable to file
		
	def openApplication(self, app: str) -> None:
		"""Opens the specified application"""
		application_window = application_imports[app]()
		self.windows.append(ApplicationWindow(self, QPoint(0, 0), application_window, background_color=(returnApplicationProperties()[app]["background-color"] if returnApplicationProperties()[app]["background-color"] != "default" else returnBackgroundProperties()["background-color"]), window_name=app, toolbar_background_color=returnBackgroundProperties()["background-color-3"], window_size=returnApplicationProperties()[app]["window-size"]))

	def openPreferences(self, position: QPoint = QPoint(0, 0)) -> None:
		"""Opens the preferences window"""
		self.windows.append(ApplicationWindow(self, position, Preferences(self.updateElements), background_color=returnBackgroundProperties()["background-color-2"], window_name="Preferences", custom_stylesheet="background-color: " + returnBackgroundProperties()["background-color-2"], restart_window_function=self.openPreferences))  # Create new window

	@staticmethod
	def openAbout() -> None:
		"""Opens the 'About' dialog"""
		dialog = AboutDialog()  # Call the AboutDialog class
		dialog.exec()  # Show class
		
	def contextMenuEvent(self, event: QContextMenuEvent) -> None:
		"""Set context menu for desktop"""
		menu = QMenu(self)  # Create menu
		new_file, new_directory, action = menu.addAction("New file"), menu.addAction("New directory"), menu.exec(self.mapToGlobal(event.pos()))  # Add actions
		if action == new_file:  # New file action
			# Get row and column count
			row, column = 0, 40
			for _ in range(len(self.files)):
				if column + 137.5 > self.window_size[1]:
					row += 1
					column = 40
				column += 100
			self.edit_file = [ToolButton(self), FileEditLineEdit(self, cancel_function=self.newFileDelete)]  # Make new ToolButton and line edit
			# ToolButton properties
			self.edit_file[0].resize(68, 100)  # Resize
			self.edit_file[0].move(row * 70, column - (100 if self.file_created_session else 0) - (8 if column - 8 != 32 else 0 if not self.file_created_session else -100))  # Move
			self.edit_file[0].setIcon(desktop.getFileIcon("", ""))  # Set default icon
			self.edit_file[0].setIconSize(QSize(75, 75))  # Set icon size
			self.edit_file[0].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none")  # Set styles
			# Line edit properties
			self.edit_file[1].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))  # Set font
			self.edit_file[1].resize(68, 20)  # Resize
			self.edit_file[1].move(row * 70, (column - (100 if self.file_created_session else 0) - (8 if column - 8 != 32 else 0 if not self.file_created_session else -100)) + 98)  # Move
			self.edit_file[1].setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)  # Set attribute
			self.edit_file[1].setStyleSheet(f"border: 1px solid {returnBackgroundProperties()['text-color']}; background-color: {returnBackgroundProperties()['background-color-2']}")  # Set styles
			self.edit_file[1].returnPressed.connect(lambda: self.newFileReturnPressed())  # Return key pressed signal
			self.edit_file[1].setFocus()  # Set focus
			# Show ToolButton and line edit
			self.edit_file[0].show()
			self.edit_file[1].show()
			if not self.file_created_session:
				self.file_created_session = True  # Toggle self.file_created_session variable
		elif action == new_directory:  # New directory
			# Get row and column count
			row, column = 0, 40  # Set default values
			for _ in range(len(self.files)):
				if column + 137.5 > self.window_size[1]:
					row += 1
					column = 40
				column += 100
			self.edit_file = [ToolButton(self), FileEditLineEdit(self, cancel_function=self.newFileDelete)]  # Make new ToolButton and line edit
			# ToolButton properties
			self.edit_file[0].resize(68, 100)  # Resize
			self.edit_file[0].move(row * 70, column - (100 if self.file_created_session else 0) - (8 if column - 8 != 32 else 0 if not self.file_created_session else -100))  # Move
			self.edit_file[0].setIcon(desktop.getFileIcon("", "directory"))  # Set default icon
			self.edit_file[0].setIconSize(QSize(75, 75))  # Set icon size
			self.edit_file[0].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none")  # Set styles
			# Line edit properties
			self.edit_file[1].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))  # Set font
			self.edit_file[1].resize(68, 20)  # Resize
			self.edit_file[1].move(row * 70, (column - (100 if self.file_created_session else 0) - (8 if column - 8 != 32 else 0 if not self.file_created_session else -100)) + 98)  # Move
			self.edit_file[1].setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)  # Set attribute
			self.edit_file[1].setStyleSheet(f"border: 1px solid {returnBackgroundProperties()['text-color']}; background-color: {returnBackgroundProperties()['background-color-2']}")  # Set styles
			self.edit_file[1].returnPressed.connect(lambda: self.newFileReturnPressed(_type="directory"))  # Return key pressed signal
			self.edit_file[1].setFocus()  # Focus
			# Show ToolButton and QLineEdit
			self.edit_file[0].show()
			self.edit_file[1].show()
			
	def newFileDelete(self) -> None:
		"""Deletes new file tool button and line edit"""
		self.edit_file[0].deleteLater()  # Delete tool button
		self.edit_file[1].deleteLater()  # Delete line edit
		
	def newFileReturnPressed(self, _type: str = "file") -> None:
		"""Creates new file"""
		file_name = f"{self.edit_file[1].text()}.minios{'dir' if _type == 'directory' else ''}"  # Assign file_name variable (local) to the path of the new file
		os.system(f"{'touch' if _type == 'file' else 'mkdir'} Home/Desktop/{file_name}")  # Create file using system() (os module function)
		self.newFileDelete()  # Remove tool button and line edit
		self.edit_file = [None, None]  # Clear self.edit_file list
		# Display new file (by reloading all desktop files)
		for x in self.files:
			x.deleteLater()  # Remove all desktop widgets
		row, column = 0, 40  # Set default row/column values
		self.files = [ToolButton(self)]  # Reset self.files
		for x in desktop.returnItems().keys():  # Add to desktop
			if column + 137.5 > self.window_size[1]:
				row += 1  # Increase row count
				column = 40  # Reset column count
			self.files.append(ToolButton(self))  # Append ToolButton
			self.files[-1].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none;")  # Set style
			self.files[-1].setText(desktop.returnItems()[x]["displayname"])  # Set text
			self.files[-1].setIcon(desktop.getFileIcon(desktop.returnItems()[x]["extension"], desktop.returnItems()[x]["type"]))  # Set icon
			self.files[-1].setIconSize(QSize(75, 75))  # Set icon size
			self.files[-1].resize(68, 100)  # Resize
			self.files[-1].setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)  # Set tool button text/icon position
			self.files[-1].move(row * 70, column)  # Move
			self.files[-1].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))  # Set font
			self.files[-1].pressed.connect((lambda self, length: (lambda: self.setFocusedFile(self.files[length])))(self, len(self.files) - 1))
			self.files[-1].show()  # Show tool button
			column += 100  # Increase column count
		self.focused_file = None  # Clear focused file
		
	def updateElements(self) -> None:
		"""Updates elements' properties"""
		self.top_tool_bar.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}; border: 4px solid {returnBackgroundProperties()['background-color-2']}; color: {returnBackgroundProperties()['text-color']}; font-family: {returnProperties()['font-family']}")  # Update stylesheet properties for the top menu bar
		self.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color']}; color: {returnBackgroundProperties()['text-color']}")  # Update the window stylesheet
		# Update style of desktop files
		for x in range(len(self.files)):
			self.files[x].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none")  # Set stylesheet
			self.files[x].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))  # Set font
		self.clock.setStyles(background_color=returnBackgroundProperties()["background-color-2"], text_color=returnBackgroundProperties()["text-color"], font_size=returnProperties()["font-size"], font_family=returnProperties()["font-family"])
		self.dock.setStyles(background_color=returnBackgroundProperties()["background-color-2"], text_color=returnBackgroundProperties()["text-color"], font_size=returnProperties()["font-size"], font_family=returnProperties()["font-family"])
		self.options.updateStyleSheets()
		
	def resizeEvent(self, event: QResizeEvent) -> None:
		"""
		Resize Events:
		Rearrange desktop files
		Update Options Menu position
		"""
		self.options.updateMenuPosition(self.width() - 100, "default")  # Update the Options Menu position
		# Rearrange desktop files
		row, column = 0, 40  # Set default row and column variables
		for x in range(len(self.files)):
			if column + 137.5 > event.size().height():
				row += 1
				column = 40
			self.files[x].move(row * 70, column)  # Move file to row/column
			column += 100
		self.dock.adjustGeometry()
		super(Window, self).resizeEvent(event)  # Call resizeEvent function from super class
		
	def keyPressEvent(self, event: QKeyEvent) -> None:
		"""Processes key press events"""
		if event.key() in [Qt.Key.Key_Delete, Qt.Key.Key_Backspace] and QApplication.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier and self.focused_file is not None: # If the Delete/Backspace key and the Control(Windows)/Command(Mac) modifier key is pressed at the same time, and there is a focused file
			self.focused_file.deleteLater()  # Delete the focused file
			for x in desktop.returnItems().keys():  # Iterate through applications
				if desktop.returnItems()[x]["displayname"] == self.focused_file.text():  # If the application is the focused file
					os.system(f"mv Home/Desktop/{x} Home/Trash/")  # Move the file to the Trash directory
					# Re-arrange desktop files
					for y in self.files:
						y.deleteLater()
					self.focused_file = None
					self.files, row, column = [], 0, 40
					for y in desktop.returnItems().keys():
						if column + 137.5 > self.window_size[1]:
							row += 1
							column = 40
						self.files.append(ToolButton(self))
						self.files[-1].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none;")
						self.files[-1].setText(desktop.returnItems()[y]["displayname"])
						self.files[-1].setIcon(desktop.getFileIcon(desktop.returnItems()[y]["extension"], desktop.returnItems()[y]["type"]))
						self.files[-1].setIconSize(QSize(75, 75))
						self.files[-1].resize(68, 100)
						self.files[-1].setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
						self.files[-1].move(row * 70, column)
						self.files[-1].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))
						self.files[-1].pressed.connect((lambda self, length: (lambda: self.setFocusedFile(self.files[length])))(self, len(self.files) - 1))
						self.files[-1].show()
						column += 100
					break  # Exit loop
		
		if self.showing_keyboard_viewer:
			self.showing_keyboard_viewer.child_widget.highlightKey(event)
	
	def mousePressEvent(self, event) -> None:
		if self.context_menu is not None:
			self.context_menu.deleteLater()
			self.context_menu = None
			
	def keyReleaseEvent(self, event) -> None:
		if self.showing_keyboard_viewer:
			self.showing_keyboard_viewer.child_widget.stopHighlightKey(event)
	
	def showKeyboardViewer(self):
		def closeKeyboardViewer():
			self.showing_keyboard_viewer = False

		self.windows.append(ApplicationWindow(self, QPoint(0, 0), KeyboardViewer(), background_color=returnBackgroundProperties()["background-color"], window_name="Keyboard Viewer", custom_stylesheet="background-color: " + returnBackgroundProperties()["background-color"], window_size=QSize(600, 250), allow_resize=False))
		self.showing_keyboard_viewer = self.windows[-1]
		self.windows[-1].window_closed.connect(closeKeyboardViewer)
	
	def shutDownWindow(self):
		self.windows.append(ApplicationWindow(self, QPoint(0, 0), ShutDownWindow(QApplication.quit), background_color=returnBackgroundProperties()["background-color-3"], window_name="Shut Down", custom_stylesheet="background-color: " + returnBackgroundProperties()["background-color-3"], window_size=QSize(250, 100)))


application = QApplication(sys.argv)  # Construct application

application_imports = {}

# Application Imports
for i in applications.keys():
	if "." in i:
		print("An application path contains a '.' character, skipping.")
		continue
	sys.path.insert(1, f"Applications/{i}")
	application_imports[applications[i]["run_class"]] = vars(__import__(applications[i]["file"][:-3]))[applications[i]["run_class"]]

window = Window()  # Call main Window class
window.show()  # Show Main Window

sys.exit(application.exec())  # Execute QApplication
