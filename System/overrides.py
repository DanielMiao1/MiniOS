"""
System/overrides.py
PyQt widget overrides
Made by Daniel M using Python 3
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class PushButton(QPushButton):
	"""Add QPushButton Animation"""
	def __init__(self, text = "") -> None:
		super().__init__()
		self.setText(text)
		self._animation = QVariantAnimation(startValue = QColor("white"), endValue = QColor("black"), valueChanged = self.valueChanged, duration = 200)
		self.updateStylesheet(QColor("black"), QColor("white"))
		self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

	def valueChanged(self, color: QColor) -> None:
		"""If value changed"""
		self.updateStylesheet(color, QColor("white") if self._animation.direction() == QAbstractAnimation.Forward else QColor("black"))

	def updateStylesheet(self, background: QColor, foreground: QColor) -> None:
		"""Update style sheet"""
		self.setStyleSheet(f"QPushButton {{background-color: {background.name()}; color: {foreground.name()}; padding: 16px 32px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; border: 2px solid white;}}")

	def enterEvent(self, event: QEvent) -> None:
		"""Display backward color animation on mouse hover"""
		self._animation.setDirection(QAbstractAnimation.Backward)
		self._animation.start()
		super().enterEvent(event)

	def leaveEvent(self, event: QEvent) -> None:
		"""Display forward color animation on mouse leave"""
		self._animation.setDirection(QAbstractAnimation.Forward)
		self._animation.start()
		super().leaveEvent(event)
