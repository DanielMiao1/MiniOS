# -*- coding: utf-8 -*-
"""
System/widgets.py
Widgets
Made by Daniel M using Python 3
"""

import sys
sys.path.insert(0, "../")


from config import returnBackgroundProperties
import config
from datetime import datetime

# PyQt imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class Menu(QWidget):
	def __init__(self, parent, **actions):
		super(Menu, self).__init__(parent=parent)
		self.items = []
		for x, y in actions.items():
			self.items.append(MenuItem(self, x, y))
			self.items[-1].move(QPoint(0, (len(self.items) - 1) * 20))
		self.setStyleSheet("border: none; background-color: #ccc;")
		maximum_width = max([i.width() for i in self.items])
		for i in self.items:
			i.setFixedSize(QSize(maximum_width, 20))
		self.setFixedSize(QSize(maximum_width + 5, 20 * len(self.items)))
		for i in QApplication.instance().topLevelWidgets():
			if isinstance(i, QMainWindow):
				i.context_menu = self


class MenuItem(QPushButton):
	def __init__(self, parent, text, action):
		super(MenuItem, self).__init__(parent=parent)
		self.setText(text)
		self.pressed.connect(action)
		self.setStyleSheet("MenuItem { border: none; background-color: #ccc; } MenuItem:hover { background-color: #888; }")


class Widget(QPushButton):
	pressed = pyqtSignal()
	released = pyqtSignal()
	context_pressed = pyqtSignal()
	context_released = pyqtSignal()
	
	def __init__(self, parent, text="", context_menu=None):
		super(Widget, self).__init__(parent=parent)
		self.setText(text) if text else None
		self.context_menu = context_menu
		self.context_widget = None
	
	def mousePressEvent(self, event) -> None:
		if event.buttons() == Qt.LeftButton:
			self.pressed.emit()
		if event.buttons() == Qt.RightButton:
			self.context_pressed.emit()
	
	def mouseReleaseEvent(self, event) -> None:
		if event.button() == Qt.LeftButton:
			self.released.emit()
		elif event.button() == Qt.RightButton:
			self.context_released.emit()
			self.context()
	
	def context(self) -> None:
		if self.context_menu:
			for i in QApplication.instance().topLevelWidgets():
				if isinstance(i, QMainWindow):
					self.context_widget = Menu(i, **self.context_menu)
					self.context_widget.move(QCursor.pos())
					self.context_widget.show()
					break
	
	def contextMenuEvent(self, event) -> None:
		return None


class GroupBox(QGroupBox):
	def __init__(self, parent):
		super(GroupBox, self).__init__(parent=parent)
		self.setFixedHeight(20)


class Slider(QWidget):
	def __init__(self, minimum, maximum, value, update_function, interval=1, labels=None) -> None:
		super(Slider, self).__init__()
		levels = range(minimum, maximum + interval, interval)
		self.update_function = update_function
		self.levels = list(zip(levels, labels)) if labels is not None else list(zip(levels, map(str, levels)))
		self.layout = QVBoxLayout(self)
		self.left_margin = 10
		self.top_margin = 10
		self.right_margin = 10
		self.bottom_margin = 10
		self.layout.setContentsMargins(self.left_margin, self.top_margin, self.right_margin, self.bottom_margin)
		self.slider = QSlider(Qt.Orientation.Horizontal, self)
		self.slider.setMinimum(minimum)
		self.slider.setMaximum(maximum)
		self.slider.setValue(value)
		self.slider.setTickPosition(QSlider.TicksBelow)
		self.slider.setMinimumWidth(300)
		self.slider.setTickInterval(interval)
		self.slider.setSingleStep(1)
		self.slider.valueChanged.connect(self.update_function)
		self.layout.addWidget(self.slider)
		
	def value(self) -> int or float:
		return self.slider.value()
	
	def setValue(self, value) -> None:
		self.slider.setValue(value)
	
	def paintEvent(self, event) -> None:
		super(Slider, self).paintEvent(event)
		painter = QPainter(self)
		style = self.slider.style()
		style_slider = QStyleOptionSlider()
		style_slider.initFrom(self.slider)
		style_slider.orientation = self.slider.orientation()
		length = style.pixelMetric(QStyle.PM_SliderLength, style_slider, self.slider)
		available = style.pixelMetric(QStyle.PM_SliderSpaceAvailable, style_slider, self.slider)
		for x, y in self.levels:
			rect = painter.drawText(QRect(), Qt.TextFlag.TextDontPrint, y)
			position = QStyle.sliderPositionFromValue(self.slider.minimum(), self.slider.maximum(), x, available) + length // 2
			bottom = self.rect().bottom()
			if x == self.slider.minimum():
				if position-rect.width() // 2 + self.left_margin <= 0:
					self.left_margin = rect.width() // 2 - position
				if self.bottom_margin <= rect.height():
					self.bottom_margin = rect.height()
				self.layout.setContentsMargins(self.left_margin, self.top_margin, self.right_margin, self.bottom_margin)
			if x == self.slider.maximum() and rect.width() // 2 >= self.right_margin:
				self.right_margin = rect.width() // 2
				self.layout.setContentsMargins(self.left_margin, self.top_margin, self.right_margin, self.bottom_margin)
			painter.drawText(QPoint(position - rect.width() // 2 + self.left_margin, bottom), y)


class WebEngineView(QWebEngineView):
	def __init__(self, hide_context_menu=False) -> None:
		super(WebEngineView, self).__init__()
		self.hide_context_menu = hide_context_menu
	
	def contextMenuEvent(self, _) -> None:
		if self.hide_context_menu:
			return
		super(WebEngineView, self).contextMenuEvent()


class FileEditLineEdit(QLineEdit):
	def __init__(self, parent, cancel_function=None) -> None:
		super(FileEditLineEdit, self).__init__(parent)
		self.cancel_function = cancel_function
	
	def keyPressEvent(self, event):
		if event.key() == Qt.Key.Key_Escape and self.cancel_function is not None:
			self.cancel_function()
		super(FileEditLineEdit, self).keyPressEvent(event)


class Clock(Widget):
	def __init__(self, parent):
		super(Clock, self).__init__(parent=parent, context_menu={})
		self.color = "black"
		self.background = "white"
		self.font_size = "12"
		self.font_family = "Arial"
		self.time = datetime.now()
		self.setText(self.time.strftime("%H:%M:%S"))
		self.timer = QTimer(self)
		self.timer.setInterval(1000)
		self.timer.timeout.connect(self.updateTime)
		self.timer.start()
	
	def updateTime(self):
		self.time = datetime.now()
		self.setText(self.time.strftime("%H:%M:%S"))
	
	def setStyles(self, **styles):
		self.color = styles["text_color"] if "text_color" in styles else self.color
		self.background = styles["background_color"] if "background_color" in styles else self.background
		self.font_size = styles["font_size"] if "font_size" in styles else self.font_size
		self.font_family = styles["font_family"] if "font_family" in styles else self.font_family
		self.setStyleSheet(f"background-color: {self.background}; color: {self.color}; font-size: {self.font_size}px; font-family: {self.font_family};")


class WebEngineView(QWebEngineView):
	def __init__(self, hide_context_menu=False) -> None:
		super(WebEngineView, self).__init__()
		self.hide_context_menu = hide_context_menu

	def contextMenuEvent(self, _) -> None:
		if self.hide_context_menu:
			return
		super(WebEngineView, self).contextMenuEvent()


class FileEditLineEdit(QLineEdit):
	def __init__(self, parent, cancel_function=None) -> None:
		super(FileEditLineEdit, self).__init__(parent)
		self.cancel_function = cancel_function
	
	def keyPressEvent(self, event):
		if event.key() == Qt.Key.Key_Escape and self.cancel_function is not None:
			self.cancel_function()
		super(FileEditLineEdit, self).keyPressEvent(event)


class MenuLabel(QLabel):
	def __init__(self, parent, text: str = "", mouse_pressed_event=None):
		"""Initialization"""
		super(MenuLabel, self).__init__(text, parent)
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.mouse_pressed_event = mouse_pressed_event
		self.setStyleSheet(f"color: {config.returnBackgroundProperties()['text-color']}; background-color: {config.returnBackgroundProperties()['background-color-2']};")
		self.setFont(QFont(config.returnProperties()["font-family"], config.returnProperties()["font-size"]))
		self.resize(100, 25)
		self.hide()
		
	def updateStyleSheets(self):
		self.setFont(QFont(config.returnProperties()["font-family"], config.returnProperties()["font-size"]))
		self.setStyleSheet(f"color: {config.returnBackgroundProperties()['text-color']}; background-color: {config.returnBackgroundProperties()['background-color-2']};")
	
	def mousePressEvent(self, _: QMouseEvent) -> None:
		"""Call mouse press event function"""
		self.setStyleSheet(f"color: {config.returnBackgroundProperties()['text-color']}; background-color: {config.returnBackgroundProperties()['background-color']};")
		if self.mouse_pressed_event is not None: self.mouse_pressed_event()
	
	def mouseReleaseEvent(self, _: QMouseEvent) -> None:
		self.setStyleSheet(f"color: {config.returnBackgroundProperties()['text-color']}; background-color: {config.returnBackgroundProperties()['background-color-3']};")
	
	def enterEvent(self, _: QEvent) -> None:
		self.setStyleSheet(f"color: {config.returnBackgroundProperties()['text-color']}; background-color: {config.returnBackgroundProperties()['background-color-3']};")
	
	def leaveEvent(self, _: QEvent) -> None:
		self.setStyleSheet(f"color: {config.returnBackgroundProperties()['text-color']}; background-color: {config.returnBackgroundProperties()['background-color-2']};")


class OptionsMenu(QPushButton):
	def __init__(self, parent, close_event=None, keyboard_viewer_event=None):
		super(OptionsMenu, self).__init__(parent=parent)
		self.setFixedSize(QSize(100, 25))
		self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color-2']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
		self.group_box, self.parent_widget, self.activated, self.group_box_layout, self.close_event = QGroupBox(parent), parent, False, QVBoxLayout(), close_event
		self.buttons = {
			"shut-down": MenuLabel(self.group_box, text=" Shut Down", mouse_pressed_event=lambda: self.closeMenu(self.close_event)),
			"keyboard-viewer": MenuLabel(self.group_box, text=" Show Keyboard", mouse_pressed_event=lambda: self.closeMenu(keyboard_viewer_event))
		}
		self.buttons["shut-down"].move(0, 25)
		self.group_box_layout.addWidget(self.buttons["shut-down"])
		self.group_box_layout.addWidget(self.buttons["keyboard-viewer"])
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.setText("Options")
		self.pressed.connect(self.mousePressed)
		self.group_box.resize(100, 50)
		self.group_box.setStyleSheet(f"QGroupBox {{ background-color: {config.returnBackgroundProperties()['background-color-2']}; border: none; }};")
		self.setFont(QFont(config.returnProperties()["font-family"], config.returnProperties()["font-size"]))
		self.group_box.hide()
	
	def updateStyleSheets(self):
		self.group_box.setStyleSheet(f"QGroupBox {{ background-color: {config.returnBackgroundProperties()['background-color-2']}; border: none; }};")
		self.setFont(QFont(config.returnProperties()["font-family"], config.returnProperties()["font-size"]))
		self.buttons["shut-down"].updateStyleSheets()
		self.buttons["keyboard-viewer"].updateStyleSheets()
	
	def updateMenuPosition(self, x: int or None = None, y: int or str or None = None):
		if x is None: x = self.group_box.pos().x()
		if y is None: y = self.group_box.pos().y()
		if y == "default": y = self.pos().y() + self.height() + 8
		self.group_box.move(QPoint(x, y))
	
	def closeMenu(self, run_event=None):
		self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color-3']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
		self.group_box.hide()
		self.buttons["shut-down"].hide()
		self.buttons["keyboard-viewer"].hide()
		self.activated = False
		if run_event is not None: run_event()
	
	def mousePressed(self):
		self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
		if self.activated: self.closeMenu()
		else:
			self.group_box.show()
			self.buttons["shut-down"].show()
			self.buttons["keyboard-viewer"].show()
			self.activated = True
	
	# def mouseReleaseEvent(self, _: QMouseEvent) -> None:
	# 	self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color-3']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
	
	def enterEvent(self, _: QEvent) -> None:
		self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color-3']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
	
	def leaveEvent(self, _: QEvent) -> None:
		self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color' + ('' if self.activated else '-2')]}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")

