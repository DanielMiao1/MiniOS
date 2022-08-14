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
	def __init__(self, text="", color="black") -> None:
		super().__init__()
		self.color = color
		self.setText(text)
		self._animation = QVariantAnimation()
		self._animation.setStartValue(QColor("black"))
		self._animation.setEndValue(QColor("white"))
		self._animation.valueChanged.connect(self.valueChanged)
		self._animation.setDuration(200)
		self.updateStylesheet(QColor("white"))
		self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
	
	def valueChanged(self, color: QColor) -> None:
		"""If value changed"""
		self.updateStylesheet(color)
	
	def updateStylesheet(self, background: QColor) -> None:
		"""Update style sheet"""
		self.setStyleSheet(
			f"QPushButton {{background-color: {background.name()}; color: #888888; padding: 16px 32px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; border: 2px solid "
			f"white;}}")
	
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
