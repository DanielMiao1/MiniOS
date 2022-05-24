# -*- coding: utf-8 -*-
"""
System/widgets/__init__.py
Menu widgets
Made by Daniel M using Python 3
"""

from .. import config

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


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
	
	def contextMenuEvent(self, event) -> None:
		pass


class MenuItem(QPushButton):
	def __init__(self, parent, text, action):
		super(MenuItem, self).__init__(parent=parent)
		self.setText(text)
		self.pressed.connect(action)
		self.setStyleSheet("MenuItem { border: none; background-color: #ccc; } MenuItem:hover { background-color: #888; }")

	def contextMenuEvent(self, event) -> None:
		pass


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
	
	def contextMenuEvent(self, event) -> None:
		pass


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

	def contextMenuEvent(self, event) -> None:
		pass
