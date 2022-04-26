# -*- coding: utf-8 -*-
"""
System/overrides.py
PyQt widget overrides
Made by Daniel M using Python 3
"""
import config

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

import typing


class ApplicationWindowToolBar(QToolBar):
	def __init__(self, background_color, mouse_move_event=None, window_name="Window", close_application_window_function=None):
		super(ApplicationWindowToolBar, self).__init__()
		self.setStyleSheet(f"background-color: {background_color}; border: 4px solid {background_color}; color: {config.returnBackgroundProperties()['text-color']};")
		self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
		self.setCursor(Qt.ArrowCursor)
		self.mouse_move_event = mouse_move_event
		self.close = QAction("×", self)
		if close_application_window_function is not None: self.close.triggered.connect(close_application_window_function)
		self.spacer = QWidget()
		self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.window_name = QAction(window_name, self)
		self.addAction(self.close)
		self.addWidget(self.spacer)
		self.addAction(self.window_name)
	
	def mouseMoveEvent(self, event):
		if self.mouse_move_event is not None: self.mouse_move_event(event)
		super(ApplicationWindowToolBar, self).mouseMoveEvent(event)
	
	def contextMenuEvent(self, _: QContextMenuEvent) -> None: pass


class ToolButton(QToolButton):
	def __init__(self, parent):
		super(ToolButton, self).__init__(parent)


class GroupBox(QGroupBox):
	def __init__(self, parent):
		super(GroupBox, self).__init__(parent=parent)
		self.setFixedHeight(20)
		# self.setStyleSheet("background-color: white; border: none;")


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
		
		def enterEvent(self, event: QEvent) -> None:
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
		
		def enterEvent(self, event: QEvent) -> None:
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
			if icon is None: self.setText(text)
			else: self.setIcon(icon)
			self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
			self.setFont(QFont(config.returnProperties()["font-family"], config.returnProperties()["font-size"]))
		
		def mousePressEvent(self, event: QMouseEvent) -> None:
			self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color-3']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
			super().mousePressEvent(event)
		
		def mouseReleaseEvent(self, event: QMouseEvent) -> None:
			self.setStyleSheet(f"background-color: {config.returnBackgroundProperties()['background-color-2']}; color: {config.returnBackgroundProperties()['text-color']}; border: none;")
			super().mouseReleaseEvent(event)
		
		def enterEvent(self, event: QEvent) -> None:
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
		self.setStyleSheet(f"QPushButton {{background-color: {background.name()}; color: #888888; padding: 16px 32px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; border: 2px solid white;}}")

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
	
	def updateColor(self, color="black") -> None:
		"""Update the color"""
		self.color = color


class Slider(QWidget):
	def __init__(self, minimum, maximum, value, update_function, interval=1, labels=None) -> None:
		super(Slider, self).__init__()
		levels = range(minimum, maximum + interval, interval)
		self.update_function = update_function
		self.levels = list(zip(levels, labels)) if labels is not None else list(zip(levels, map(str, levels)))
		self.layout = QVBoxLayout(self)
		self.right_margin, self.bottom_margin, self.top_margin, self.left_margin = 10, 10, 10, 10
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
	
	def updateMenuPosition(self, x: typing.Optional[int] = None, y: typing.Optional[typing.Union[int, str]] = None):
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
