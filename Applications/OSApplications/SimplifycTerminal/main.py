# -*- coding: utf-8 -*-
# Simplifyc Terminal
# Terminal Emulator made by Daniel M using Python 3 for the SimplifycOS project: https://github.com/DanielMiao1/SimplifycOS

# Imports
import os
import re
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Window(QMainWindow):
	"""Main Window"""
	def __init__(self):
		super(Window, self).__init__()
		self.setFixedSize(QSize(450, 250)) # Set window size
		self.input_box = QLineEdit(self) # Create the command input box
		self.input_box.setFont(QFont("Consolas", 15)) # Set font and font size of command input box
		self.input_box.move(20, 20) # Align the command input box
		self.input_box.resize(400, 25) # Resize the command input box
		self.input_box.setPlaceholderText("Enter command...") # Set placeholder text
		self.input_box.returnPressed.connect(self.evalCommand)
		self.output_box = QTextEdit(self) # Create the output box
		self.output_box.setReadOnly(True) # Make the output box read only
		self.output_box.setFont(QFont("Consolas", 15)) # Set font and font size of output box
		self.output_box.setPlaceholderText("Output") # Set placeholder text
		self.output_box.move(20, 65) # Align the output box
		self.output_box.resize(400, 165) # Resize the output box
		self.show() # Show widgets

	def evalCommand(self): # Evaluate the command in the command input box and write to the output box
		command = self.getListFromCommand(self.removeSpaces(self.input_box.text())) # Get command
		if command[0] == "ls": # List command
			if len(command) == 1: self.output_box.setText("	".join(str(i) for i in os.listdir("./") if not i.startswith("."))) # If the command is simply 'ls'; output files and directories in the current directory
			elif len(command) == 2: pass
			elif len(command) == 3: pass
			elif len(command) == 4: pass
			else: pass
		else: self.output_box.setText(f"Command not found: '{self.removeSpaces(self.input_box.text())}'")

	@staticmethod # Make the removeSpaces function static
	def removeSpaces(text): return text[re.search(r"[^ ]", text).start():] # Return the text without spaces in the front using re.search

	@staticmethod # Make the getListFromCommand function static
	def getListFromCommand(command): return command.split(" ") # Return command as a list separated at spaces


# Create new Qt application and run Window class
(application, window) = (QApplication(sys.argv), Window())
application.exec_()
