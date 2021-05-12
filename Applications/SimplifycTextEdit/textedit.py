# -*- coding: utf-8 -*-
"""
Applications/SimplifycTextEdit/textedit.py
Simplifyc Text Edit
Text Editor made by Daniel M using Python 3 for the SimplifycOS project: https://github.com/DanielMiao1/SimplifycOS
Main Text Edit code at textedit/index.html
"""

# Imports
import sys
import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class TextEdit(QMainWindow):
	"""Main Window"""
	def __init__(self):
		super(TextEdit, self).__init__()
		self.web_view = QWebEngineView() # Create new Web Engine View
		self.web_view.load(QUrl.fromLocalFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "textedit/index.html")))) # Load HTML page at textedit/index.html
		self.setCentralWidget(self.web_view) # Set Central Widget
		self.show() # Show Window
