# -*- coding: utf-8 -*-
"""
Applications/MiniCalculator/calculator.py
Mini Calculator
Calculator made by Daniel M using Python 3, HTML, CSS, and JavaScript for the MiniOS project: https://github.com/DanielMiao1/MiniOS
Main calculator code at calculator/index.html
"""

# Imports
import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class Calculator(QMainWindow):
	"""Main Window"""
	def __init__(self) -> None:
		super(Calculator, self).__init__()
		self.view = QWebEngineView() # Create new web engine view
		self.setCentralWidget(self.view) # Set central widget
		self.view.load(QUrl.fromLocalFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "calculator/index.html")))) # Load page
		self.show() # Show Window