# -*- coding: utf-8 -*-

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

import typing
import sys
sys.path.insert(0, "../")
import config


class Buttons:
	class CancelButton(QPushButton):
		def __init__(self, parent, text="", size=QSize(100, 25)):
			super().__init__(parent=parent)
			self.setFixedSize(size)
			self.setCursor(Qt.CursorShape.PointingHandCursor)
			self.setText(text)
			self.setFont(QFont(config.returnProperties()['font-family'], config.returnProperties()['font-size']))
			self.setStyleSheet("background-color: #FF0044; color: white; border: none;")
		
		def mousePressEvent(self, event: QMouseEvent) -> None:
			self.setStyleSheet("background-color: #FF0000; color: white; border: none;")
			super().mousePressEvent(event)
		
		def mouseReleaseEvent(self, event: QMouseEvent) -> None:
			self.setStyleSheet("background-color: #FF4800; color: white; border: none;")
			super().mouseReleaseEvent(event)
		
		def enterEvent(self, event: QEnterEvent) -> None:
			self.setStyleSheet("background-color: #FF4800; color: white; border: none;")
			super().enterEvent(event)
		
		def leaveEvent(self, event: QEvent) -> None:
			self.setStyleSheet("background-color: #FF0044; color: white; border: none;")
			super().leaveEvent(event)
	
	class ContinueButton(QPushButton):
		def __init__(self, parent, text="", size=QSize(100, 25)):
			super().__init__(parent=parent)
			self.setFixedSize(size)
			self.setCursor(Qt.CursorShape.PointingHandCursor)
			self.setText(text)
			self.setFont(QFont(config.returnProperties()['font-family'], config.returnProperties()['font-size']))
			self.setStyleSheet("background-color: #44E200; color: black; border: none;")
		
		def mousePressEvent(self, event: QMouseEvent) -> None:
			self.setStyleSheet("background-color: #0BF260; color: black; border: none;")
			super().mousePressEvent(event)
		
		def mouseReleaseEvent(self, event: QMouseEvent) -> None:
			self.setStyleSheet("background-color: #41DB24; color: black; border: none;")
			super().mouseReleaseEvent(event)
		
		def enterEvent(self, event: QEnterEvent) -> None:
			self.setStyleSheet("background-color: #41DB24; color: black; border: none;")
			super().enterEvent(event)
		
		def leaveEvent(self, event: QEvent) -> None:
			self.setStyleSheet("background-color: #44E200; color: black; border: none;")
			super().leaveEvent(event)
	
	class KeyboardButton(QPushButton):
		def __init__(self, parent, text: str = "", size: QSize = QSize(20, 20), icon: typing.Union[QIcon, None] = None):
			super().__init__(parent=parent)
			self.setFixedSize(size)
			self.setCursor(Qt.CursorShape.PointingHandCursor)
			if icon is None:
				self.setText(text)
			else:
				self.setIcon(icon)
			self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
			self.setFont(QFont(config.returnProperties()["font-family"], config.returnProperties()["font-size"]))
		
		def mousePressEvent(self, event: QMouseEvent) -> None:
			self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color-3']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
			super().mousePressEvent(event)
		
		def mouseReleaseEvent(self, event: QMouseEvent) -> None:
			self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color-2']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
			super().mouseReleaseEvent(event)
		
		def enterEvent(self, event: QEnterEvent) -> None:
			self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color-2']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
			super().enterEvent(event)
		
		def leaveEvent(self, event: QEvent) -> None:
			self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
			super().leaveEvent(event)


class PushButton(QPushButton):
	"""Add QPushButton Animation"""
	def __init__(self, text="", parent=None, color="black", padding="15px", background="#F5F5F5", hover="#E6E6E6") -> None:
		if parent is None:
			super(PushButton, self).__init__()
		else:
			super(PushButton, self).__init__(parent)
		self.color = color
		self.padding = padding
		self.setText(text)
		self._animation = QVariantAnimation()
		self._animation.setStartValue(QColor(hover))
		self._animation.setEndValue(QColor(background))
		self._animation.valueChanged.connect(self.valueChanged)
		self._animation.setDuration(200)
		self.updateStylesheet(QColor(background))
		self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
	
	def valueChanged(self, color: QColor) -> None:
		"""If value changed"""
		self.updateStylesheet(color)
	
	def updateStylesheet(self, background: QColor) -> None:
		"""Update style sheet"""
		self.setStyleSheet(f"background-color: {background.name()}; color: {self.color}; border: none; padding: {self.padding};")
	
	def enterEvent(self, event: QEvent) -> None:
		"""Display backward color animation on mouse hover"""
		self._animation.setDirection(QAbstractAnimation.Direction.Backward)
		self._animation.start()
		super().enterEvent(event)
	
	def leaveEvent(self, event: QEvent) -> None:
		"""Display forward color animation on mouse leave"""
		self._animation.setDirection(QAbstractAnimation.Direction.Forward)
		self._animation.start()
		super().leaveEvent(event)
	
	def updateColor(self, color="black") -> None:
		"""Update the color"""
		self.color = color


class ToolButton(QToolButton):
	def __init__(self, parent):
		super(ToolButton, self).__init__(parent)


class TabButton(PushButton):
	def __init__(self, parent, action, text=""):
		super(TabButton, self).__init__(text, parent, padding="5px")
		self.action = action
	
	def mousePressEvent(self, event):
		self.action()
		super(TabButton, self).mousePressEvent(event)


class ActionPushButton(PushButton):
	def __init__(self, parent, text="", action=None):
		super(ActionPushButton, self).__init__(text, parent, padding="0px")
		self.action = action
		self.pressed.connect(lambda self=self: self.action() if self.action is not None else None)
		self.setFixedSize(QSize(75, 75))
	