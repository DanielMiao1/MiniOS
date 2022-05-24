# -*- coding: utf-8 -*-
"""
System/dialogs.py
Dialogs used in main script
Made by Daniel M using Python 3
"""

from json import load

from config import returnProperties, returnBackgroundProperties, Themes
from widgets import Slider
from widgets.buttons import *

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Preferences(QWidget):
	"""System Preferences Application"""
	class Appearance(QWidget):
		class ThemeLabel(QLabel):
			def __init__(self, parent):
				super(Preferences.Appearance.ThemeLabel, self).__init__(parent)
				self.setCursor(Qt.PointingHandCursor)
				self.index = None
				self.setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))
				self.setAlignment(Qt.AlignCenter)
			
			def mousePressEvent(self, event):
				self.parent().parent().changeTheme(self.index)
				super(Preferences.Appearance.ThemeLabel, self).mousePressEvent(event)
			
		class Theme(QWidget):
			def __init__(self, parent, update_function):
				super(Preferences.Appearance.Theme, self).__init__(parent=parent)
				self.update_function = update_function
				self.layout = QGridLayout()
				self.theme, self.font_size, self.font_family = returnProperties()["theme"], returnProperties()["font-size"], returnProperties()["font-family"]
				self.top_bar = QGroupBox(self)
				self.top_bar.setLayout(QHBoxLayout())
				self.back_button = QPushButton("Back", self.top_bar)
				self.back_button.pressed.connect(lambda self=self: self.parent().setCurrentIndex(0))
				self.top_bar.layout().addWidget(self.back_button)
				# self.layout.addWidget(self.top_bar, 0, 0)
				self.widgets, self.group_box_widgets = {
					"top-bar": [self.top_bar, [0, 0]],
					"theme-label": [QLabel("Theme"), [3, 0]],
					"theme-group-box": [QGroupBox(self), [3, 1]],
					"font-size-label": [QLabel("Font Size"), [5, 0]],
					"font-size": [Slider(5, 20, int(returnProperties()["font-size"]), self.changeFontSize), [5, 1]],
					"reset-font-size": [PushButton("Reset"), [5, 2]],
					"font-family-label": [QLabel("Font Family"), [6, 0]],
					"font-family": [QComboBox(self), [6, 1]]
				}, {}
				# Append to self.group_box_widgets
				for x, y in zip(Themes.getThemes(), range(1, len(Themes.getThemes().keys()) + 1)):
					self.group_box_widgets[x] = [Preferences.Appearance.ThemeLabel(self), [1, y]]
				# Specific widget properties
				# # Font family properties
				self.widgets["font-family"][0].addItems(returnProperties()["fonts"])
				self.widgets["font-family"][0].setStyleSheet(f"QComboBox QAbstractItemView {{ selection-color: {'#AAAAAA' if returnProperties()['theme'] == 'light' else '#555555'}; color: {returnBackgroundProperties()['text-color']}; }};")
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
				for i in self.group_box_widgets:
					self.group_box_layout.addWidget(self.group_box_widgets[i][0])
				self.widgets["theme-group-box"][0].setLayout(self.group_box_layout)
				self.widgets["theme-group-box"][0].setFixedSize(540, 100)
				self.widgets["theme-group-box"][0].layout().setContentsMargins(30, 30, 30, 30)
				# # Theme button properties
				for i in self.group_box_widgets.keys():
					self.group_box_widgets[i][0].setText(i.title())
					self.group_box_widgets[i][0].setStyleSheet(f"color: #{str(Themes.getThemes()[i]['text-color'])[1:].lower()}; border: none; background: #{str(Themes.getThemes()[i]['background-color'])[1:].lower()};")
					self.group_box_widgets[i][0].index = i
					# exec(f"self.group_box_widgets[i][0].pressed.connect(lambda self=self: self.changeTheme('{i}'))", globals(), locals())
				# Add to layout
				for i in self.widgets.keys():
					self.layout.addWidget(self.widgets[i][0], self.widgets[i][1][0], self.widgets[i][1][1])
				self.setLayout(self.layout) # Set layout
			
			def _update(self):
				self.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}")
				for i in ["theme-label", "font-size-label", "font-family-label"]:
					self.widgets[i][0].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; font-size: {returnProperties()['font-size']}")
					self.widgets[i][0].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))
				for i in self.group_box_widgets.keys():
					self.group_box_widgets[i][0].setStyleSheet(f"color: {returnBackgroundProperties()['text-color']}; border: none")
					self.group_box_widgets[i][0].setFont(QFont(returnProperties()["font-family"], returnProperties()["font-size"]))
				# self.widgets["font-family"][0].setStyleSheet("QComboBox QAbstractItemView {selection-color: #AAAAAA}")
				if returnProperties()["theme"] == "light":
					self.widgets["font-family"][0].setStyleSheet("QComboBox QAbstractItemView { selection-color: #AAAAAA; color: #000000; };")
				else:
					self.widgets["font-family"][0].setStyleSheet("QComboBox QAbstractItemView { selection-color: #555555; color: #FFFFFF; };")
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
				
			def changeTheme(self, theme):
				self.theme = theme
				with open("System/config/theme.json", "r+") as file:
					data = load(file)
					data["theme"] = self.theme
					open("System/config/theme.json", "w").write(str(data).replace("'", "\""))
				self._update()
				self.parent().parent().parent().parent().parent().restartWindow()
			
			def resizeEvent(self, event) -> None:
				self.top_bar.resize(QSize(event.size().width(), self.top_bar.size().height()))
				super(Preferences.Appearance.Theme, self).resizeEvent(event)
		
		class AppearanceWidget(QWidget):
			def __init__(self, parent, update_function):
				super(Preferences.Appearance.AppearanceWidget, self).__init__(parent)
				self.update_function = update_function
				self.buttons = []
				self.buttons.append(ActionPushButton(self, "General", lambda: self.parent().setCurrentIndex(1)))
				self.buttons.append(ActionPushButton(self, "Windows", lambda: self.parent().setCurrentIndex(1)))
				self.buttons.append(ActionPushButton(self, "Dock", lambda: self.parent().setCurrentIndex(1)))
				width = self.buttons[0].width()
				for i in range(len(self.buttons)):
					self.buttons[i].move(QPoint(i * (width + 5), 0))
			
			def resizeEvent(self, event) -> None:
				single_width, width, y = self.buttons[0].width(), 0, 0
				for i in range(len(self.buttons)):
					if (width + 5) >= self.width():
						y += self.buttons[i].height() + 5
						width = 0
					self.buttons[i].move(QPoint(width, y))
					width += single_width + 5
				super(Preferences.Appearance.AppearanceWidget, self).resizeEvent(event)
		
		def __init__(self, parent, update_function):
			super(Preferences.Appearance, self).__init__(parent)
			self.update_function = update_function
			self.stacked_widgets, self.pages = QStackedWidget(self), {"main": Preferences.Appearance.AppearanceWidget(self, update_function), "theme": Preferences.Appearance.Theme(self, update_function)}
			for i in self.pages.values():
				self.stacked_widgets.addWidget(i)
		
		def resizeEvent(self, event) -> None:
			for i in self.pages.values():
				i.resize(event.size())
			super(Preferences.Appearance, self).resizeEvent(event)
			
	def __init__(self, update_function) -> None:
		super(Preferences, self).__init__()
		self.setCursor(Qt.ArrowCursor)
		self.tabs = QScrollArea(self)
		self.tabs.setWidgetResizable(True)
		
		self.tab_widget = QWidget()
		self.tabs.setWidget(self.tab_widget)
		
		self.tab_layout = QVBoxLayout(self.tab_widget)
		self.tab_layout.addWidget(TabButton(self.tab_widget, lambda: self.stacked_widgets.setCurrentIndex(0), "Appearance"))
		self.tab_layout.addItem(QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))
		
		self.tabs.setStyleSheet("border: none; background: #F0F0F0")
		
		self.stacked_widgets, self.pages = QStackedWidget(self), {"appearance": Preferences.Appearance(self, update_function)}
		for i in self.pages.values():
			self.stacked_widgets.addWidget(i)
		
	def resizeEvent(self, event):
		self.tabs.resize(QSize(event.size().width() // 5, event.size().height()))
		self.stacked_widgets.resize(QSize(event.size().width() // 5 * 4, event.size().height()))
		self.stacked_widgets.move(self.tabs.width(), 0)
		super(Preferences, self).resizeEvent(event)
	
	
class ShutDownWindow(QWidget):
	"""Shut Down Confirmation Window"""
	def __init__(self, shut_down_function) -> None:
		super(ShutDownWindow, self).__init__()
		self.setCursor(Qt.ArrowCursor)
		self.layout, self.cancel, self.confirm = QHBoxLayout(), Buttons.CancelButton(self, text="Cancel"), Buttons.ContinueButton(self, text="Shut Down")
		self.cancel.pressed.connect(self.closeWindow)
		self.confirm.pressed.connect(shut_down_function)
		self.layout.addWidget(self.cancel)
		self.layout.addWidget(self.confirm)
		self.setLayout(self.layout)
	
	def closeWindow(self) -> None:
		self.parent().closeWindow()


class KeyboardViewer(QWidget):
	"""Keyboard Viewer Window"""
	class KeyGroup(QGroupBox):
		def __init__(self, parent):
			super(KeyboardViewer.KeyGroup, self).__init__(parent)
			self.setStyleSheet("border: none;")
			self.setLayout(QHBoxLayout())
			self.layout().setSpacing(0)
			self.layout().setContentsMargins(0, 0, 0, 0)
	
	def __init__(self):
		super(KeyboardViewer, self).__init__()
		self.setCursor(Qt.ArrowCursor)
		self.setStyleSheet("background-color: #FFFFFF")
		self.layout = QVBoxLayout()
		self.layout.setSpacing(0)
		self.groups = {
			"functions": KeyboardViewer.KeyGroup(self),
			"numbers": KeyboardViewer.KeyGroup(self),
			"r1": KeyboardViewer.KeyGroup(self),
			"r2": KeyboardViewer.KeyGroup(self),
			"r3": KeyboardViewer.KeyGroup(self),
			"modifiers": KeyboardViewer.KeyGroup(self)
		}
		self.groups["functions"].move(QPoint(0, 0))
		self.groups["numbers"].move(QPoint(0, 35))
		self.groups["r1"].move(QPoint(0, 70))
		self.groups["r2"].move(QPoint(0, 105))
		self.groups["r3"].move(QPoint(0, 140))
		self.groups["modifiers"].move(QPoint(0, 175))
		self.buttons = []
		for i in ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "⌫"]:
			self.buttons.append(Buttons.KeyboardButton(self.groups["numbers"], text=i, size=QSize(50, 35) if i == "⌫" else QSize(35, 35)))
			self.groups["numbers"].layout().addWidget(self.buttons[-1])
		self.buttons.append(Buttons.KeyboardButton(self.groups["r1"], icon=QIcon("System/images/characters/tab.png"), size=QSize(45, 35)))
		self.groups["r1"].layout().addWidget(self.buttons[-1])
		for i in ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"]:
			self.buttons.append(Buttons.KeyboardButton(self.groups["r1"], text=i, size=QSize(35, 35)))
			self.groups["r1"].layout().addWidget(self.buttons[-1])
		self.buttons.append(Buttons.KeyboardButton(self.groups["r2"], text="Caps Lock", size=QSize(60, 35)))
		self.groups["r2"].layout().addWidget(self.buttons[-1])
		for i in ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"]:
			self.buttons.append(Buttons.KeyboardButton(self.groups["r2"], text=i, size=QSize(35, 35)))
			self.groups["r2"].layout().addWidget(self.buttons[-1])
		self.buttons.append(Buttons.KeyboardButton(self.groups["r2"], text="Return", size=QSize(50, 35)))
		self.groups["r2"].layout().addWidget(self.buttons[-1])
		self.buttons.append(Buttons.KeyboardButton(self.groups["r3"], text="Shift", size=QSize(65, 35)))
		self.groups["r3"].layout().addWidget(self.buttons[-1])
		for i in ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]:
			self.buttons.append(Buttons.KeyboardButton(self.groups["r3"], text=i, size=QSize(35, 35)))
			self.groups["r3"].layout().addWidget(self.buttons[-1])
		self.buttons.append(Buttons.KeyboardButton(self.groups["r3"], text="Shift", size=QSize(65, 35)))
		self.groups["r3"].layout().addWidget(self.buttons[-1])
		self.layout.addWidget(self.groups["functions"])
		self.layout.addWidget(self.groups["numbers"])
		self.layout.addWidget(self.groups["r1"])
		self.layout.addWidget(self.groups["r2"])
		self.layout.addWidget(self.groups["r3"])
		self.layout.addWidget(self.groups["modifiers"])
		self.layout.addStretch()
		self.setLayout(self.layout)
	
	def getKey(self, event):
		if event.text() in ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="]:
			return self.buttons[["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="].index(event.text())]
		elif event.key() in [Qt.Key.Key_Backspace, Qt.Key.Key_Delete]:
			return self.buttons[13]
		elif event.key() == Qt.Key.Key_Tab:
			return self.buttons[14]
		elif event.text() in ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"]:
			return self.buttons[["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"].index(event.text()) + 15]
		elif event.key() == Qt.Key.Key_CapsLock:
			return self.buttons[28]
		elif event.text() in ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"]:
			return self.buttons[["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"].index(event.text()) + 29]
		elif event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter]:
			return self.buttons[40]
		elif event.key() == Qt.Key.Key_Shift:
			return [self.buttons[41], self.buttons[52]]
		elif event.text() in ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]:
			return self.buttons[["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"].index(event.text()) + 42]
	
	def highlightKey(self, event):
		key = self.getKey(event)
		if key is None:
			return
		if isinstance(key, list):
			for i in key:
				i.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}; color: {returnBackgroundProperties()['text-color']}; border: none;")
		else:
			key.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color-2']}; color: {returnBackgroundProperties()['text-color']}; border: none;")
	
	def stopHighlightKey(self, event):
		key = self.getKey(event)
		if key is None:
			return
		if isinstance(key, list):
			for i in key:
				i.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color']}; color: {returnBackgroundProperties()['text-color']}; border: none;")
		else:
			key.setStyleSheet(f"background-color: {returnBackgroundProperties()['background-color']}; color: {returnBackgroundProperties()['text-color']}; border: none;")


class AboutDialog(QDialog):
	"""About Dialog"""
	def __init__(self, parent=None) -> None:
		super(AboutDialog, self).__init__(parent=parent)
		template = QGridLayout() # Set layout to grid
		# Set fixed width and height
		self.setFixedHeight(self.height() - 175)
		self.setFixedWidth(self.width() + 100)
		title = QLabel("MiniOS") # Add title
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
