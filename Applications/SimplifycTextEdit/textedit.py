# -*- coding: utf-8 -*-
"""
Applications/SimplifycTextEdit/textedit.py
Simplifyc Text Edit
Text Editor made by Daniel M using Python 3 for the SimplifycOS project: https://github.com/DanielMiao1/SimplifycOS
"""

# Imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class TextEdit(QMainWindow):
	"""Main Window"""
	def __init__(self) -> None:
		super(TextEdit, self).__init__()
		self.editor = QTextEdit(self) # Create new text area
		self.editor.resize(self.width(), self.height()) # Resize text area
		self.editor.setFrameStyle(QFrame.NoFrame) # Hide border
		self.toolbar = QToolBar("tool bar") # Create new toolbar
		self.addToolBar(self.toolbar) # Add toolbar
		self.show() # Show Window
	
	def resizeEvent(self, a0: QResizeEvent) -> None:
		"""Resize Text Area on Window Resize"""
		self.editor.resize(self.width(), self.height()) # Resize text area
