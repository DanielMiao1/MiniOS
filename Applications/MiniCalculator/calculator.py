# -*- coding: utf-8 -*-
"""
Applications/MiniCalculator/calculator.py
Mini Calculator
Application made by Daniel M using Python 3 for the MiniOS project: https://github.com/DanielMiao1/MiniOS
"""

# from PyQt5.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class Button(QPushButton):
	def __init__(self, text, parent):
		super().__init__(text, parent=parent)
		self.setCursor(Qt.CursorShape.PointingHandCursor)
		self.setStyleSheet("Button { border: none; background-color: #eee; } Button:hover { background-color: #ddd; }")


class Calculator(QMainWindow):
	"""Main Window"""
	def __init__(self) -> None:
		super(Calculator, self).__init__()
		self.result = QTextEdit(self)
		self.result.move(QPoint(10, 10))
		self.result.setStyleSheet("border: none; background-color: #eee;")
		self.open_parentheses = Button("(", self)
		self.close_parentheses = Button(")", self)
		self.backspace = Button("⌫", self)
		self.clear = Button("⇤", self)
		self.number_7 = Button("7", self)
		self.number_8 = Button("8", self)
		self.number_9 = Button("9", self)
		self.division = Button("÷", self)
		self.number_4 = Button("4", self)
		self.number_5 = Button("5", self)
		self.number_6 = Button("6", self)
		self.multiplication = Button("×", self)
		self.number_1 = Button("1", self)
		self.number_2 = Button("2", self)
		self.number_3 = Button("3", self)
		self.subtraction = Button("-", self)
		self.number_0 = Button("0", self)
		self.decimal = Button(".", self)
		self.equal = Button("=", self)
		self.addition = Button("+", self)
		
	def resizeEvent(self, event) -> None:
		self.result.resize(QSize(event.size().width() - 20, 50))
		for i in [self.open_parentheses, self.close_parentheses, self.backspace, self.clear, self.number_7, self.number_8, self.number_9, self.number_4, self.number_5, self.number_6, self.number_1, self.number_2, self.number_3, self.number_0, self.decimal, self.equal, self.addition, self.subtraction, self.multiplication, self.division]:
			i.resize(QSize((self.width() - 50) // 4, (self.width() - 50) // 4))
		self.open_parentheses.move(QPoint(10, self.result.height() + 20))
		self.close_parentheses.move(QPoint(self.open_parentheses.width() + 20, self.result.height() + 20))
		self.backspace.move(QPoint(self.open_parentheses.width() + self.close_parentheses.width() + 30, self.result.height() + 20))
		self.clear.move(QPoint(self.open_parentheses.width() + self.close_parentheses.width() + self.backspace.width() + 40, self.result.height() + 20))
		self.number_7.move(QPoint(10, self.open_parentheses.height() + self.open_parentheses.y() + 10))
		self.number_8.move(QPoint(self.number_7.width() + 20, self.open_parentheses.height() + self.open_parentheses.y() + 10))
		self.number_9.move(QPoint(self.number_7.width() + self.number_8.width() + 30, self.open_parentheses.height() + self.open_parentheses.y() + 10))
		self.division.move(QPoint(self.number_7.width() + self.number_8.width() + self.number_9.width() + 40, self.open_parentheses.height() + self.open_parentheses.y() + 10))
		self.number_4.move(QPoint(10, self.number_7.height() + self.number_7.y() + 10))
		self.number_5.move(QPoint(self.number_4.width() + 20, self.number_7.height() + self.number_7.y() + 10))
		self.number_6.move(QPoint(self.number_4.width() + self.number_5.width() + 30, self.number_7.height() + self.number_7.y() + 10))
		self.multiplication.move(QPoint(self.number_4.width() + self.number_5.width() + self.number_6.width() + 40, self.number_7.height() + self.number_7.y() + 10))
		self.number_1.move(QPoint(10, self.number_4.height() + self.number_4.y() + 10))
		self.number_2.move(QPoint(self.number_1.width() + 20, self.number_4.height() + self.number_4.y() + 10))
		self.number_3.move(QPoint(self.number_1.width() + self.number_2.width() + 30, self.number_4.height() + self.number_4.y() + 10))
		self.subtraction.move(QPoint(self.number_1.width() + self.number_2.width() + self.number_3.width() + 40, self.number_4.height() + self.number_4.y() + 10))
		self.number_0.move(QPoint(10, self.number_1.height() + self.number_1.y() + 10))
		self.decimal.move(QPoint(self.number_0.width() + 20, self.number_1.height() + self.number_1.y() + 10))
		self.equal.move(QPoint(self.number_0.width() + self.decimal.width() + 30, self.number_1.height() + self.number_1.y() + 10))
		self.addition.move(QPoint(self.number_0.width() + self.decimal.width() + self.equal.width() + 40, self.number_1.height() + self.number_1.y() + 10))
		super(Calculator, self).resizeEvent(event)


if __name__ == "__main__":
	app = QApplication([])
	calc = Calculator()
	calc.show()
	app.exec()
