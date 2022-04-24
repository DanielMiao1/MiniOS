# -*- coding: utf-8 -*-
"""
Applications/MiniTextEdit/textedit.py
Mini Text Edit
Text Editor made by Daniel M using Python 3 for the MiniOS project: https://github.com/DanielMiao1/MiniOS
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TextEdit(QWidget):
	"""Main Window"""
	def __init__(self) -> None:
		super(TextEdit, self).__init__()
		self.layout = QBoxLayout(QBoxLayout.TopToBottom, self)
		self.editor = QTextEdit(self) # Create new text area
		self.editor.setFrameStyle(QFrame.NoFrame) # Hide border
		self.tool_bar = QToolBar(self)
		self.editor.move(0, 0)
		self.editor.resize(360, 512)
		self.layout.addWidget(self.tool_bar, alignment=Qt.AlignmentFlag.AlignTop)
		self.layout.addWidget(self.editor)
		self.resize(360, 512)
		
	def resizeEvent(self, event: QResizeEvent) -> None:
		"""Resize Text Area on Window Resize"""
		self.editor.move(0, 0)
		self.editor.resize(event.size().width(), event.size().height()) # Resize text area
