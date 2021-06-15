# -*- coding: utf-8 -*-
"""
Applications/SimplifycCalculator/calculator.py
Simplifyc Calculator
Calculator made by Daniel M using Python 3, HTML, CSS, and JavaScript for the SimplifycOS project: https://github.com/DanielMiao1/SimplifycOS
Main calculator code at calculator/index.html
"""

# Imports
import sys
import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class TabWidget(QTabWidget):
	"""Tab Widget"""
	def createTab(self):
		"""Create new tab"""
		view = QWebEngineView() # Make view
		self.addTab(view, "") # Create tab

class Calculator(QMainWindow):
	"""Main Window"""
	def __init__(self):
		super(Calculator, self).__init__()
		self.tabs = TabWidget() # Create tab widget
		self.tabs.setDocumentMode(True) # Set document mode true
		self.tabs.setTabsClosable(False) # Set tabs not closeable
		self.setCentralWidget(self.tabs) # Set central widget
		self.newTab(QUrl.fromLocalFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "calculator/index.html"))), "Basic Calculator")
		self.newTab(QUrl.fromLocalFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "calculator/index.html"))), "Basic Calculator")
		# self.web_view = QWebEngineView() # Create new Web Engine View
		# self.web_view.load(QUrl.fromLocalFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "calculator/index.html")))) # Load HTML page at calculator/index.html
		# self.setCentralWidget(self.web_view) # Set Central Widget
		self.show() # Show Window
		
	def newTab(self, path, label):
		"""Create new tab for tab widget"""
		engine = QWebEngineView()
		engine.load(path)
		url = self.tabs.addTab(engine, label)
		self.tabs.setCurrentIndex(url)
