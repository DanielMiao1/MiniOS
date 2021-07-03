# -*- coding: utf-8 -*-
"""
Applications/MiniTerminal/terminal.py
Mini Terminal
Terminal Emulator made by Daniel M using Python 3 for the MiniOS project: https://github.com/DanielMiao1/MiniOS
"""

# Imports
import os
import re
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Widget Overrides
class MainWindow(QMainWindow):
	"""Add Event Filter for Main Window: Not finished"""
	def eventFilter(self, a0: QObject, a1: QEvent) -> bool or None:
		"""Add event filter"""
		if a0 == QLineEdit:
			if a1.type() == QEvent.Type.KeyPress:
				key_event = QKeyEvent(a1)
				if key_event.key() == Qt.Key.Key_Up: return True

class Terminal(QWidget):
	"""Main Window"""
	def __init__(self) -> None:
		super(Terminal, self).__init__()
		self.setStyleSheet("QLineEdit {qproperty-frame: false;}")
		self.path = os.path.abspath(os.getcwd()) # Get current path
		self.commands = ["ls", "echo", "pwd", "history"] # Define valid operation commands
		self.setFixedSize(QSize(450, 250)) # Set window size
		self.input_box = QLineEdit(self) # Create the command input box
		self.input_box.setFont(QFont("Consolas", 15)) # Set font and font size of command input box
		self.input_box.move(20, 20) # Align the command input box
		self.input_box.resize(400, 25) # Resize the command input box
		self.input_box.setPlaceholderText("Enter command...") # Set placeholder text
		self.input_box.returnPressed.connect(self.evalCommand)
		self.input_box.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
		self.output_box = QTextEdit(self) # Create the output box
		self.output_box.setReadOnly(True) # Make the output box read only
		self.output_box.setFont(QFont("Consolas", 15)) # Set font and font size of output box
		self.output_box.setPlaceholderText("Output") # Set placeholder text
		self.output_box.move(20, 65) # Align the output box
		self.output_box.resize(400, 165) # Resize the output box
		self.output_box.setFrameStyle(QFrame.NoFrame)
		self.show() # Show widgets

	def evalCommand(self) -> None:
		"""Evaluate the command in the command input box and write to the output box"""
		if self.input_box.text() == "": return # Exit function if the input box is empty
		open("Applications/MiniTerminal/history.txt", "a+").write(f"{self.input_box.text()}\n") # Write current command to the history file
		arguments = self.getListFromCommand(self.removeSpaces(self.input_box.text()))[1:] if len(self.getListFromCommand(self.removeSpaces(self.input_box.text()))) > 1 else [] # Get command
		operation_command = self.getListFromCommand(self.removeSpaces(self.input_box.text()))[0] if self.getListFromCommand(self.removeSpaces(self.input_box.text()))[0] in self.commands else None # Get the operation command
		if operation_command is None: # If operation command is None
			self.output_box.setText(f"Command not found: '{self.getListFromCommand(self.removeSpaces(self.input_box.text()))[0]}'") # Output command not found message
			self.input_box.setText("")
			return # Exit from function
		elif operation_command == "ls": # List command
			if len(arguments) == 0: self.output_box.setText("    ".join(str(i) for i in os.listdir("./") if not i.startswith("."))) # If the arguments list is empty; output files and directories in the current directory
			elif len(arguments) == 1:
				if arguments[0] == "-a": self.output_box.setText("    ".join(str(i) for i in [".", ".."] + os.listdir("./")))
				elif arguments[0] == "-A": self.output_box.setText("    ".join(str(i) for i in os.listdir("./")))
				elif arguments[0] == "-1": self.output_box.setText("\n".join(str(i) for i in os.listdir("./")))
			elif len(arguments) == 2: pass
			elif len(arguments) == 3: pass
			else: pass
		elif operation_command == "echo": # Echo command
			if (arguments[0].startswith("\"") and arguments[-1].endswith("\"")) or (arguments[0].startswith("'") and arguments[-1].endswith("'")):
				self.output_box.setText(" ".join(str(i) for i in arguments)[1:-1])
			elif len(arguments) == 0: self.output_box.setText("") # If the arguments list is empty; output ''
			elif len(arguments) == 1: # If there is one argument after 'echo'
				if arguments[0] == "-n": self.output_box.setText("") # If the argument is '-n', output ''
				elif arguments[0] == "-e": self.output_box.setText("\n") # If the argument is '-e', output a new line
				else: self.output_box.setText("".join(str(i) for i in list(arguments[0])[1:-1] if i != "\\")) if (arguments[0].startswith("\"") and arguments[0].endswith("\"")) or (arguments[0].startswith("'") and arguments[0].endswith("'")) else self.output_box.setText("".join(str(i) for i in list(arguments[0]) if i != "\\")) # Otherwise, output the argument if it is not quoted; however if it is quoted, output the argument without quotes.
			elif len(arguments) == 2: # If there are two arguments after 'echo'
				escape_characters = False # If escape characters such as '\n' is allowed
				newline_at_end = True # If a newline is inserted at the end of output
				if arguments[0].startswith("-") and len(arguments[0]) > 1:
					option = list(arguments[0][1:]) # Store options
					if "e" in option: escape_characters = True # Allow escape characters
					elif "n" in option: newline_at_end = False # Do not print newline
					string = " ".join(str(i) for i in arguments[1:])[1:-1] if (arguments[1].startswith("\"") and arguments[-1].endswith("\"")) or (arguments[1].startswith("'") and arguments[-1].endswith("'")) else " ".join(str(i) for i in arguments[1:])
					if escape_characters: string = self.processEscapeCharacters(string)
					if newline_at_end: string += "\n"
					self.output_box.setText(string)
				else:
					self.output_box.setText(f"Invalid command: at argument {arguments[0]}")
					self.input_box.setText("")
					return # Otherwise, output an error message and return
			else: pass
		elif operation_command == "pwd": self.output_box.setText(self.path) # Output current directory if operation command is 'pwd', regardless of the arguments
		elif operation_command == "history": # If the operation command is 'history'
			if len(arguments) >= 1: # If there are one or more arguments
				if arguments[0].startswith("-") and len(arguments[0]) > 1: # If the first argument starts with a hyphen and there are more than one arguments
					option = list(arguments[0][1:]) # Assign variable option to the first argument excluding the first hyphen as a list
					if "c" in option: # If 'option' contains a 'c'
						open("Applications/MiniTerminal/history.txt", "w+").write("") # Clear the Applications/MiniTerminal/history.txt file
						self.output_box.setText("\n") # Clear the output
						self.input_box.setText("") # Clear the input box
						return # Exit function
					else: self.output_box.setText(open("Applications/MiniTerminal/history.txt", "r").read()) # Otherwise, output the contents of Applications/MiniTerminal/history.txt
				elif arguments[0].isnumeric(): # If the first argument is a non-negative whole number
					if open("Applications/MiniTerminal/history.txt", "r").read().count("\n") < (int(arguments[0]) - 1): self.output_box.setText(open("Applications/MiniTerminal/history.txt", "r").read()) # If the history entries in Applications/MiniTerminal/history.txt is less than the amount entered, output the entire history
					else: self.output_box.setText("\n".join(str(i) for i in str(open("Applications/MiniTerminal/history.txt", "r").read()).splitlines()[::-1][:int(arguments[0])])) # Otherwise, output the first given amount of history entries
				else: self.output_box.setText(open("Applications/MiniTerminal/history.txt", "r").read()) # Otherwise, output the contents of Applications/MiniTerminal/history.txt
			else: self.output_box.setText(open("Applications/MiniTerminal/history.txt", "r").read()) # Otherwise, output the contents of Applications/MiniMiniTerminal/history.txt
		self.input_box.setText("") # Clear the input box

	@staticmethod # Make the removeSpaces function static
	def removeSpaces(text: str) -> str:
		"""Return the text without spaces in the front using re.search, if spaces exists"""
		return text[re.search(r"[^ ]", text).start():]

	@staticmethod # Make the getListFromCommand function static
	def getListFromCommand(command: str) -> str:
		"""Return command as a list separated at spaces"""
		return command.split(" ")

	@staticmethod # Make the updateEscapeCharacters function static
	def processEscapeCharacters(string: str) -> str:
		"""Process escape characters"""
		string = list(string)
		new_string = ""
		for i in string:
			if string[string.index(i)] == "\\" and string[string.index(i) + 1] in ["n", "t", "\\"]: del string[string.index(i) + 1], string[string.index(i)]
			if string[string.index(i)] == "\\" and string[string.index(i) + 1] == "n": new_string += "\n"
			elif string[string.index(i)] == "\\" and string[string.index(i) + 1] == "t": new_string += "\t"
			elif string[string.index(i)] == "\\" and string[string.index(i) + 1] == "\\": new_string += "\\"
			else: new_string += i
		return new_string


if __name__ == "__main__":
	app, window = QApplication(sys.argv), Terminal()
	window.show()
	app.exec_()
