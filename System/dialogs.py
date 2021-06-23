"""
System/dialogs.py
Dialogs used in main script
Made by Daniel M using Python 3
"""

# Library imports
from json import load

# Local file imports
from config import returnProperties
from overrides import PushButton, Slider

# PyQt imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Preferences(QWidget):
	"""System Preferences Application"""
	def __init__(self, update_function) -> None:
		super(Preferences, self).__init__()
		self.setFixedSize(QSize(800, 350))
		self.setStyleSheet(f"background-color: {returnProperties()['background-color']}")
		self.setWindowTitle("Preferences")
		self.update_function = update_function
		self.layout = QGridLayout()
		self.text_color, self.background_color, self.secondary_background_color, self.font_size = returnProperties()["text-color"], returnProperties()["background-color"], returnProperties()["secondary-background-color"], returnProperties()["font-size"]
		self.widgets = {
			"background-color-label": [QLabel("Background Color"), [2, 1]],
			"background-color": [QPushButton(self), [2, 2]],
			"reset-background-color": [PushButton("Reset", self.text_color), [2, 3]],
			"secondary-background-color-label": [QLabel("Secondary Background Color"), [3, 1]],
			"secondary-background-color": [QPushButton(self), [3, 2]],
			"reset-secondary-background-color": [PushButton("Reset", self.text_color), [3, 3]],
			"text-color-label": [QLabel("Text Color"), [4, 1]],
			"text-color": [QPushButton(self), [4, 2]],
			"reset-text-color": [PushButton("Reset", self.text_color), [4, 3]],
			"font-size-label": [QLabel("Font Size"), [5, 1]],
			"font-size": [Slider(5, 25, int(returnProperties()["font-size"])), [5, 2]]
		}
		for i in ["background-color-label", "secondary-background-color-label", "text-color-label", "font-size-label"]: self.widgets[i][0].setStyleSheet("color: " + returnProperties()["text-color"])
		for x, y in zip(["background-color", "secondary-background-color", "text-color"], [self.changeBackgroundColor, self.changeSecondaryBackgroundColor, self.changeTextColor]):
			self.widgets[x][0].setText(self.background_color if x == "background-color" else self.secondary_background_color if x == "secondary-background-color" else self.text_color)
			self.widgets[x][0].setStyleSheet(f"border: none; color: {self.text_color}")
			self.widgets[x][0].setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
			self.widgets[x][0].clicked.connect(y)
		for x, y in zip(["reset-background-color", "reset-secondary-background-color", "reset-text-color"], [self.resetBackgroundColor, self.resetSecondaryBackgroundColor, self.resetTextColor]): self.widgets[x][0].clicked.connect(y)
		for i in self.widgets.keys(): self.layout.addWidget(self.widgets[i][0], self.widgets[i][1][0], self.widgets[i][1][1])
		self.setLayout(self.layout)
	
	def _update(self):
		self.setStyleSheet(f"background-color: {returnProperties()['background-color']}; color: {self.text_color}")
		for i in ["background-color-label", "secondary-background-color-label", "text-color-label"]: self.widgets[i][0].setStyleSheet("color: " + returnProperties()["text-color"])
		for i in ["background-color", "secondary-background-color", "text-color"]: self.widgets[i][0].setStyleSheet(f"border: none; color: {self.text_color}")
		for i in ["reset-background-color", "reset-secondary-background-color", "reset-text-color"]: self.widgets[i][0].updateColor(self.text_color)
		self.update_function()
	
	def resetTextColor(self) -> None:
		self.text_color = "#000000"
		self.widgets["text-color"][0].setText(self.text_color)
		with open("System/config/colors.json") as file:
			data = load(file)
			data["text-color"] = self.text_color
			open("System/config/colors.json", "w").write(str(data).replace("'", "\""))
		self._update()
	
	def resetBackgroundColor(self) -> None:
		self.background_color = "#ffffff"
		self.widgets["background-color"][0].setText(self.background_color)
		with open("System/config/colors.json") as file:
			data = load(file)
			data["background-color"] = self.background_color
			open("System/config/colors.json", "w").write(str(data).replace("'", "\""))
		self._update()
	
	def resetSecondaryBackgroundColor(self) -> None:
		self.secondary_background_color = "#ffffff"
		self.widgets["secondary-background-color"][0].setText(self.secondary_background_color)
		with open("System/config/colors.json") as file:
			data = load(file)
			data["secondary-background-color"] = self.secondary_background_color
			open("System/config/colors.json", "w").write(str(data).replace("'", "\""))
		self._update()
	
	def changeFontSize(self) -> None:
		self.font_size = self.widgets["font-size"][0].value()
	
	def changeTextColor(self) -> None:
		self.text_color = QColorDialog.getColor().name()
		self.widgets["text-color"][0].setText(self.text_color)
		with open("System/config/colors.json", "r+") as file:
			data = load(file)
			data["text-color"] = self.text_color
			open("System/config/colors.json", "w").write(str(data).replace("'", "\""))
		self._update()
	
	def changeBackgroundColor(self) -> None:
		self.background_color = QColorDialog.getColor().name()
		self.widgets["background-color"][0].setText(self.background_color)
		with open("System/config/colors.json", "r+") as file:
			data = load(file)
			data["background-color"] = self.background_color
			open("System/config/colors.json", "w").write(str(data).replace("'", "\""))
		self._update()
	
	def changeSecondaryBackgroundColor(self) -> None:
		self.secondary_background_color = QColorDialog.getColor().name()
		self.widgets["secondary-background-color"][0].setText(self.secondary_background_color)
		with open("System/config/colors.json", "r+") as file:
			data = load(file)
			data["secondary-background-color"] = self.secondary_background_color
			open("System/config/colors.json", "w").write(str(data).replace("'", "\""))
		self._update()
	
class AboutDialog(QDialog):
	"""About Dialog"""
	def __init__(self, parent = None) -> None:
		super(AboutDialog, self).__init__(parent = parent)
		template = QGridLayout() # Set layout to grid
		# Set fixed width and height
		self.setFixedHeight(self.height() - 175)
		self.setFixedWidth(self.width() + 100)
		title = QLabel("SimplifycOS") # Add title
		title_font = title.font() # Add new font
		title_font.setPointSize(50) # Set point size for font
		title_font.setBold(True) # Make font bold
		title.setFont(title_font) # Set font for title widget
		# Add widgets to layout
		template.addWidget(title, 1, 2)
		template.addWidget(QLabel("Made by Daniel M using Python 3 and the PyQt5 Graphics Library"), 2, 2)
		for x in range(template.count()): template.itemAt(x).setAlignment(Qt.AlignmentFlag.AlignHCenter) # Align all widgets to center
		self.setStyleSheet("color: white; background-color: #18082C;") # Set background color of dialog to #18082C and color of text to white
		self.setLayout(template) # Display the widgets
