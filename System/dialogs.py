"""
System/dialogs.py
Dialogs used in main script
Made by Daniel M using Python 3
"""

# Library imports
from json import load

# Local file imports
from config import returnProperties, returnBackgroundProperties
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
		self.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color']}")
		self.setWindowTitle("Preferences")
		self.update_function = update_function
		self.layout = QGridLayout()
		self.theme, self.font_size, self.font_family = returnProperties()["theme"], returnProperties()["font-size"], returnProperties()["font-family"]
		self.widgets, self.group_box_widgets = {
			"theme-label": [QLabel("Theme"), [3, 1]],
			"theme-group-box": [QGroupBox(self), [3, 2]],
			"font-size-label": [QLabel("Font Size"), [5, 1]],
			"font-size": [Slider(5, 20, int(returnProperties()["font-size"]), self.changeFontSize), [5, 2]],
			"reset-font-size": [PushButton("Reset"), [5, 3]],
			"font-family-label": [QLabel("Font Family"), [6, 1]],
			"font-family": [QComboBox(self), [6, 2]]
		}, {
			"theme-light": [QToolButton(self), [3, 2]],
			"theme-dark": [QToolButton(self), [3, 3]]
		}
		# Specific widget properties
		# # Font family properties
		self.widgets["font-family"][0].addItems(returnProperties()["fonts"])
		self.widgets["font-family"][0].setStyleSheet("QComboBox QAbstractItemView { selection-color: #AAAAAA; };")
		self.widgets["font-family"][0].setCurrentIndex(returnProperties()["fonts"].index(self.font_family))
		self.widgets["font-family"][0].currentIndexChanged.connect(self.changeFontFamily)
		# # Reset font size properties
		self.widgets["reset-font-size"][0].clicked.connect(self.resetFontSize)
		# # Label properties
		for i in ["theme-label", "font-size-label", "font-family-label"]:
			self.widgets[i][0].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']};")
			self.widgets[i][0].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))
		# # Theme group box properties
		self.widgets["theme-group-box"][0].setStyleSheet("QGroupBox { border: none; }")
		self.group_box_layout = QHBoxLayout()
		for i in self.group_box_widgets: self.group_box_layout.addWidget(self.group_box_widgets[i][0])
		self.widgets["theme-group-box"][0].setLayout(self.group_box_layout)
		# # Theme button properties
		for i in ["theme-light", "theme-dark"]:
			self.group_box_widgets[i][0].setIcon(QIcon("System/images/theme_icons/white.png" if i == "theme-light" else "System/images/theme_icons/black.png"))
		# Add to layout
		for i in self.widgets.keys(): self.layout.addWidget(self.widgets[i][0], self.widgets[i][1][0], self.widgets[i][1][1])
		self.setLayout(self.layout) # Set layout
	
	def _update(self):
		for i in ["theme-label", "font-size-label", "font-family-label"]:
			self.widgets[i][0].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; font-size: {returnProperties()['font-size']}")
			self.widgets[i][0].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))
		self.widgets["font-family"][0].setStyleSheet("QComboBox QAbstractItemView {selection-color: #AAAAAA}")
		self.update_function()
		
	def resetFontSize(self) -> None:
		self.font_size = 12
		self.widgets["font-size"][0].setValue(12)
		with open("System/config/font.json") as file:
			data = load(file)
			data["font-size"] = self.font_size
			open("System/config/font.json", "w").write(str(data).replace("'", "\""))
		self._update()
		
	def changeFontFamily(self) -> None:
		self.font_family = self.widgets["font-family"][0].currentText()
		with open("System/config/font.json", "r+") as file:
			data = load(file)
			data["font-family"] = self.font_family
			open("System/config/font.json", "w").write(str(data).replace("'", "\""))
		self._update()
		
	def changeFontSize(self) -> None:
		self.font_size = self.widgets["font-size"][0].value()
		with open("System/config/font.json", "r+") as file:
			data = load(file)
			data["font-size"] = self.font_size
			open("System/config/font.json", "w").write(str(data).replace("'", "\""))
		self._update()
		
	def changeTheme(self, theme) -> None:
		self.theme = QColorDialog.getColor().name()
		print(theme)
		with open("System/config/colors.json", "r+") as file:
			data = load(file)
			data["theme"] = self.theme
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
