# -*- coding: utf-8 -*-
"""
System/widgets/__init__.py
Main file for custom Qt widgets
Made by Daniel M using Python 3
"""

from datetime import datetime

from PyQt6.QtWebEngineWidgets import *

from .menu import *


class Widget(QWidget):
	pressed = pyqtSignal(int)
	released = pyqtSignal(int)

	def __init__(self, parent=None):
		super(Widget, self).__init__(parent)
		self.label = None
		# self.context_menu = Menu(self)

	def contextMenu(self):
		pass
	
	def mousePressEvent(self, event) -> None:
		self.pressed.emit(event.button())
	
	def mouseReleaseEvent(self, event) -> None:
		self.released.emit(event.button())

	def setText(self, text):
		if self.label is None:
			self.label = QLabel(self)

		self.label.setText(text)
		self.resizeLabel(self.size())

	def resizeLabel(self, size):
		self.label.resize(size)

	def resizeEvent(self, event):
		if self.label is not None:
			self.resizeLabel(event.size())
		super(Widget, self).resizeEvent(event)

# class Widget(QPushButton):
# 	pressed = pyqtSignal()
# 	released = pyqtSignal()
# 	context_pressed = pyqtSignal()
# 	context_released = pyqtSignal()
#
# 	def __init__(self, parent, text="", context_menu=None):
# 		super(Widget, self).__init__(parent=parent)
# 		self.setText(text) if text else None
# 		self.context_menu = context_menu
# 		self.context_widget = None
#
# 	def mousePressEvent(self, event) -> None:
# 		if event.buttons() == Qt.LeftButton:
# 			self.pressed.emit()
# 		if event.buttons() == Qt.RightButton:
# 			self.context_pressed.emit()
#
# 	def mouseReleaseEvent(self, event) -> None:
# 		if event.button() == Qt.LeftButton:
# 			self.released.emit()
# 		elif event.button() == Qt.RightButton:
# 			self.context_released.emit()
# 			self.context()
#
# 	def context(self) -> None:
# 		if self.context_menu:
# 			for i in QApplication.instance().topLevelWidgets():
# 				if isinstance(i, QMainWindow):
# 					self.context_widget = Menu(i, **self.context_menu)
# 					self.context_widget.move(QCursor.pos())
# 					self.context_widget.show()
# 					break
#
# 	def contextMenuEvent(self, event) -> None:
# 		return None


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
		self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
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
		length = style.pixelMetric(QStyle.PixelMetric.PM_SliderLength, style_slider, self.slider)
		available = style.pixelMetric(QStyle.PixelMetric.PM_SliderSpaceAvailable, style_slider, self.slider)
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
		# super(Clock, self).__init__(parent=parent, context_menu={})
		super(Clock, self).__init__(parent=parent)
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
