# -*- coding: utf-8 -*-
"""
Applications/MiniTerminal/terminal.py
Mini Terminal
Shell Emulator made by Daniel M using Python 3 for the MiniOS project: https://github.com/DanielMiao1/MiniOS
"""

# Imports
import os
import sys
import subprocess

# Local file imports
sys.path.insert(1, "Applications/.ApplicationSupport")
import get_properties

# PyQt imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TextEdit(QTextEdit):
	def __init__(self, parent, return_pressed_event=None, PS1: str = "$ ", PS2: str = "> "):
		super(TextEdit, self).__init__(parent=parent)
		self.return_pressed_event, self.pressed, self.PS1, self.PS2, self.history_entry_index = return_pressed_event, False, PS1, PS2, 0
	
	def keyPressEvent(self, event: QKeyEvent) -> None:
		if event.key() in [Qt.Key_Enter, Qt.Key_Return] and self.return_pressed_event is not None:
			self.return_pressed_event()
			self.history_entry_index = 0
			return
		if (self.toPlainText().splitlines()[-1] == self.PS1 and event.key() in [Qt.Key_Backspace, Qt.Key_Left, Qt.Key_Right]) or (event.key() == Qt.Key_H and QApplication.keyboardModifiers() == Qt.MetaModifier) or (event.key() == Qt.Key_Left and self.toPlainText()[:self.textCursor().position()].splitlines()[-1] == self.PS1):
			return
		if event.key() in [Qt.Key_Up, Qt.Key_Down]:
			if (len(open("Applications/MiniTerminal/history.txt", "r").read().splitlines()) < self.history_entry_index + 2 and event.key() == Qt.Key_Up) or (self.history_entry_index - 1 < 0 and event.key() == Qt.Key_Down):
				return
			self.history_entry_index += 1 if event.key() == Qt.Key_Up else -1
			self.setText(self.toPlainText()[:len(self.toPlainText()) - (len(self.toPlainText().splitlines()[-1]) - len(self.PS1))] + (open("Applications/MiniTerminal/history.txt", "r").read().splitlines()[::-1] + [""])[self.history_entry_index - 1])
			cursor = self.textCursor()
			cursor.movePosition(QTextCursor.End)
			self.setTextCursor(cursor)
			return
		super(TextEdit, self).keyPressEvent(event)
	
	def mousePressEvent(self, _) -> None:
		if self.pressed:
			return
		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.End)
		self.setTextCursor(cursor)
		self.pressed = True
	
	def mouseDoubleClickEvent(self, _) -> None:
		return


class Terminal(QWidget):
	"""Main Window"""
	def __init__(self) -> None:
		super(Terminal, self).__init__()
		self.setFixedSize(497, 455)
		self.setStyleSheet(f"background-color: {get_properties.returnBackgroundProperties()['background-color']}; color: {get_properties.returnBackgroundProperties()['text-color']}")
		self.path, self.commands, self.PS1, self.PS2 = os.path.abspath(os.getcwd()), ["ls", "echo", "pwd", "history"], "$ ", ">" # Get current path
		self.text_edit = TextEdit(self, return_pressed_event=lambda: self.evalCommand(self.text_edit.toPlainText().splitlines()[-1][len(self.PS1):])) # Create the text box
		self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.text_edit.setFixedSize(QSize(492, 455))
		self.text_edit.setFont(QFont("Consolas", 15)) # Set font and font size of command input box
		self.text_edit.move(0, 0)
		self.text_edit.resize(self.geometry().size())
		self.text_edit.setText(f"Terminal for MiniOS version dev-0.1\n{self.PS1}") # Set text
		self.text_edit.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
		self.text_edit.setFrameStyle(QFrame.NoFrame)
		self.show() # Show widgets

	def parentResizeEvent(self, event: QResizeEvent) -> None:
		self.setFixedSize(event.size().width(), event.size().height() - 45)
		self.text_edit.setFixedSize(event.size().width() - 5, event.size().height() - 45)

	def evalCommand(self, command) -> None:
		"""Evaluate the command in the command input box and write output"""
		if command == "":
			self.addNewLine()
			return
		open("Applications/MiniTerminal/history.txt", "a+").write(command + "\n") # Write current command to the history file
		command = command.rstrip().lstrip()
		if command == "":
			self.addNewLine()
			return
		arguments, operation_command = command.split(" ")[1:], (command[:command.index(" ")] if " " in command else command)
		if operation_command == "history": # If the operation command is 'history'
			if len(arguments) >= 1: # If there are one or more arguments
				if arguments[0].startswith("-") and len(arguments[0]) > 1: # If the first argument starts with a hyphen and there is more than one argument
					option = list(arguments[0][1:]) # Assign variable option to the first argument excluding the first hyphen as a list
					if "c" in option: # If 'option' contains a 'c'
						open("Applications/MiniTerminal/history.txt", "w+").write("") # Clear the Applications/MiniTerminal/history.txt file
						self.addNewLine()
						return
					else:
						self.appendOutput("\n".join([f"{str(y).rjust(len(str(len(open('Applications/MiniTerminal/history.txt', 'r').read().splitlines()))) + 2)}  {x}" for x, y in zip(open("Applications/MiniTerminal/history.txt", "r").read().splitlines(), range(1, len(open("Applications/MiniTerminal/history.txt", "r").read().splitlines()) + 1))]) + "\n") # Otherwise, output the contents of Applications/MiniTerminal/history.txt
				elif arguments[0].isnumeric(): # If the first argument is a non-negative whole number
					if open("Applications/MiniTerminal/history.txt", "r").read().count("\n") < (int(arguments[0]) - 1):
						self.appendOutput("\n".join([f"{str(y).rjust(len(str(len(open('Applications/MiniTerminal/history.txt', 'r').read().splitlines()))) + 2)}  {x}" for x, y in zip(open("Applications/MiniTerminal/history.txt", "r").read().splitlines(), range(1, len(open("Applications/MiniTerminal/history.txt", "r").read().splitlines()) + 1))]) + "\n") # If the history entries in Applications/MiniTerminal/history.txt is less than the amount entered, output the entire history
					else:
						self.appendOutput("\n".join(str(i) for i in str(open("Applications/MiniTerminal/history.txt", "r").read()).splitlines()[::-1][:int(arguments[0])]) + "\n") # Otherwise, output the first given amount of history entries
				else:
					self.appendOutput("\n".join([f"{str(y).rjust(len(str(len(open('Applications/MiniTerminal/history.txt', 'r').read().splitlines()))) + 2)}  {x}" for x, y in zip(open("Applications/MiniTerminal/history.txt", "r").read().splitlines(), range(1, len(open("Applications/MiniTerminal/history.txt", "r").read().splitlines()) + 1))]) + "\n") # Otherwise, output the contents of Applications/MiniTerminal/history.txt
			else:
				self.appendOutput("\n".join([f"{str(y).rjust(len(str(len(open('Applications/MiniTerminal/history.txt', 'r').read().splitlines()))) + 2)}  {x}" for x, y in zip(open("Applications/MiniTerminal/history.txt", "r").read().splitlines(), range(1, len(open("Applications/MiniTerminal/history.txt", "r").read().splitlines()) + 1))]) + "\n") # Otherwise, output the contents of Applications/MiniTerminal/history.txt
		else:
			try: pipe = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			except FileNotFoundError:
				self.appendOutput(f"Command not found: {operation_command}\n")
				return
			except PermissionError: pipe = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			self.appendOutput(str(pipe.communicate()[1 if str(pipe.communicate()[1], "utf-8") != "" else 0], "utf-8"))

	def appendOutput(self, output: str) -> None:
		"""Append a string to the text box"""
		self.text_edit.setText(f"{self.text_edit.toPlainText()}\n{output}{self.PS1}")
		cursor = self.text_edit.textCursor()
		cursor.movePosition(QTextCursor.End)
		self.text_edit.setTextCursor(cursor)
	
	def addNewLine(self) -> None:
		"""Add new line to the text box"""
		self.text_edit.setText(f"{self.text_edit.toPlainText()}\n{self.PS1}")
		cursor = self.text_edit.textCursor()
		cursor.movePosition(QTextCursor.End)
		self.text_edit.setTextCursor(cursor)
