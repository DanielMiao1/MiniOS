# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ToolButton(QToolButton):
	def __init__(self, parent):
		super(ToolButton, self).__init__(parent)


class PushButton(QPushButton):
	"""Add QPushButton Animation"""
	def __init__(self, text="", color="black") -> None:
		super().__init__()
		self.color = color
		self.setText(text)
		self._animation = QVariantAnimation(startValue=QColor("black"), endValue=QColor("white"), valueChanged=self.valueChanged, duration=200)
		self.updateStylesheet(QColor("white"))
		self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
	
	def valueChanged(self, color: QColor) -> None:
		self.updateStylesheet(color)
	
	def updateStylesheet(self, background: QColor) -> None:
		self.setStyleSheet(f"QPushButton {{background-color: {background.name()}; color: #888888; padding: 16px 32px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; border: 2px solid white;}}")
	
	def enterEvent(self, event: QEvent) -> None:
		self._animation.setDirection(QAbstractAnimation.Backward)
		self._animation.start()
		super().enterEvent(event)
	
	def leaveEvent(self, event: QEvent) -> None:
		self._animation.setDirection(QAbstractAnimation.Forward)
		self._animation.start()
		super().leaveEvent(event)
	
	def updateColor(self, color="black") -> None:
		self.color = color