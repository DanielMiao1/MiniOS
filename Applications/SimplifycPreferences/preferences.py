"""
Applications/SimplifycPreferences/preferences.py
Simplifyc Preferences
Application made by Daniel M using Python 3 for the SimplifycOS project: https://github.com/DanielMiao1/SimplifycOS
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from json import load

import sys

sys.path.insert(1, "Applications/.ApplicationSupport")
import get_properties

class Preferences(QDialog):
	def __init__(self) -> None:
		super(Preferences, self).__init__()
		self.setWindowTitle("Preferences")
		self.restart_required = False
		self.layout = QGridLayout()
		self.widgets = {"restart-message": [QLabel(""), [1, 1]], "background-color-label": [QLabel("Background Color"), [2, 1]], "background-color": [QPushButton(self), [2, 2]]}
		self.widgets["restart-message"][0].setStyleSheet("color: red;")
		self.background_color = get_properties.returnProperties()["background-color"]
		self.widgets["background-color"][0].setText(self.background_color)
		self.widgets["background-color"][0].setStyleSheet(f"border: none; background-color: transparent; color: {self.background_color};")
		self.widgets["background-color"][0].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		self.widgets["background-color"][0].clicked.connect(self.changeBackgroundColor)
		for i in self.widgets.keys(): self.layout.addWidget(self.widgets[i][0], self.widgets[i][1][0], self.widgets[i][1][1])
		self.setLayout(self.layout)
	
	def changeBackgroundColor(self) -> None:
		self.background_color = QColorDialog.getColor().name()
		if not self.restart_required:
			self.restart_required = True
			self.widgets["restart-message"][0].setText("A restart is required for the changes to apply.")
		self.widgets["background-color"][0].setStyleSheet(f"border: none; background-color: transparent; color: {self.background_color};")
		self.widgets["background-color"][0].setText(self.background_color)
		with open("System/config/colors.json", "r+") as file:
			data = load(file)
			data["background-color"] = self.background_color
			open("System/config/colors.json", "w").write(str(data).replace("'", "\""))
		
	def closeEvent(self, a0: QCloseEvent) -> None:
		if self.restart_required:
			print("Restarting...")
			__import__("os").execl(sys.executable, sys.executable, *sys.argv)
