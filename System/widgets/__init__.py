# -*- coding: utf-8 -*-
"""
System/widgets.py
Widgets
Made by Daniel M using Python 3
"""

import widgets.dock

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
	

class SelectionRectangle(QWidget):
	def __init__(self):
		super().__init__()
		self.setGeometry(30, 30, 600, 400)
		self.begin = QPoint()
		self.end = QPoint()
	
	def paintEvent(self, _):
		painter = QPainter(self)
		brush = QBrush(QColor(100, 10, 10, 40))
		painter.setBrush(brush)
		painter.drawRect(QRect(self.begin, self.end))
	
	def mousePressEvent(self, event):
		self.begin = event.pos()
		self.end = event.pos()
		self.update()
	
	def mouseMoveEvent(self, event):
		self.end = event.pos()
		self.update()
	
	def mouseReleaseEvent(self, event):
		self.begin = event.pos()
		self.end = event.pos()
		self.update()


class GroupBox(QGroupBox):
	def __init__(self, parent):
		super(GroupBox, self).__init__(parent=parent)
		self.setFixedHeight(20)
		# self.setStyleSheet("background-color: white; border: none;")


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


class ApplicationWindow(QWidget):
	mode = None
	position = None
	focus_signal = pyqtSignal(bool)
	out_focus_signal = pyqtSignal(bool)
	new_geometry_signal = pyqtSignal(QRect)
	window_closed = pyqtSignal()
	
	def __init__(self, parent, point, child_widget, background_color="default", window_name="Window", toolbar_background_color=returnBackgroundProperties()['background-color-3'], custom_stylesheet="", window_size=QSize(800, 350), restart_window_function=None, allow_resize=True):
		super(ApplicationWindow, self).__init__(parent=parent)
		if isinstance(window_size, list):
			if len(window_size) == 2: window_size = QSize(window_size[0], window_size[1])
		self.resize(window_size)
		self.setStyleSheet(custom_stylesheet)
		self.background_color, self.focus, self.is_editing, self.old_position, self.new_position, self.layout, self.shadow, self.restart_window_function, self.toolbar_background_color, self.allow_resize = background_color, True, True, None, None, QVBoxLayout(self), QGraphicsDropShadowEffect(), restart_window_function, toolbar_background_color, allow_resize
		self.setGraphicsEffect(self.shadow)
		self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
		self.setVisible(True)
		self.setAutoFillBackground(False)
		self.setMouseTracking(True)
		self.setFocusPolicy(Qt.ClickFocus)
		self.setFocus()
		self.move(point)
		self.tool_bar = ApplicationWindowToolBar(self.toolbar_background_color, mouse_move_event=self.toolBarMouseMoveEvent, window_name=window_name, close_application_window_function=self.closeWindow)
		self.layout.addWidget(self.tool_bar)
		self.child_widget = child_widget
		self.setChildWidget(child_widget)
		self.installEventFilter(parent)
	
	def closeWindow(self):
		self.setParent(None)
		self.window_closed.emit()
	
	def restartWindow(self):
		self.closeWindow()
		if self.restart_window_function is not None: self.restart_window_function(self.pos())
	
	def setChildWidget(self, child_widget):
		if child_widget:
			child_widget.setParent(self)
			child_widget.setCursor(Qt.CursorShape.ArrowCursor)
			child_widget.releaseMouse()
			self.layout.addWidget(child_widget)
			self.layout.setContentsMargins(1, 1, 1, 1)
	
	def focusInEvent(self, event: QFocusEvent):
		self.focus = True
		self.mode = None
		parent = self.parentWidget()
		parent.installEventFilter(self)
		parent.repaint()
		self.focus_signal.emit(True)
		super(ApplicationWindow, self).focusInEvent(event)
	
	def focusOutEvent(self, event: QFocusEvent):
		if not self.is_editing: return
		self.mode = None
		self.out_focus_signal.emit(False)
		self.focus = False
		super(ApplicationWindow, self).focusOutEvent(event)
	
	def paintEvent(self, event: QPaintEvent):
		painter = QPainter(self)
		painter.fillRect(event.rect(), QColor(self.background_color if self.background_color.lower() != "default" else returnBackgroundProperties()["background-color"]))
		rect = event.rect()
		rect.adjust(0, 0, -1, -1)
		painter.setPen(QColor(self.toolbar_background_color))
		painter.drawRect(rect)
		super(ApplicationWindow, self).paintEvent(event)
	
	def mousePressEvent(self, event: QMouseEvent):
		self.position = QPoint(event.globalX() - self.geometry().x(), event.globalY() - self.geometry().y())
		super(ApplicationWindow, self).mousePressEvent(event)
	
	def setCursorShape(self, position):
		if not self.allow_resize: return
		if ((position.y() > self.y() + self.height() - 3) and (position.x() < self.x() + 3)) or ((position.y() > self.y() + self.height() - 3) and (position.x() > self.x() + self.width() - 3)) or ((position.y() < self.y() + 3) and (position.x() < self.x() + 3)) or (position.y() < self.y() + 3) and (position.x() > self.x() + self.width() - 3):
			if (position.y() > self.y() + self.height() - 3) and (position.x() < self.x() + 3):
				self.mode = "resize-bottom-left"
				self.setCursor(QCursor(Qt.SizeBDiagCursor))
			if (position.y() > self.y() + self.height() - 3) and (position.x() > self.x() + self.width() - 3):
				self.mode = "resize-bottom-right"
				self.setCursor(QCursor(Qt.SizeFDiagCursor))
			if (position.y() < self.y() + 3) and (position.x() < self.x() + 3):
				self.mode = "resize-top-left"
				self.setCursor(QCursor(Qt.SizeFDiagCursor))
			if (position.y() < self.y() + 3) and (position.x() > self.x() + self.width() - 3):
				self.mode = "resize-top-right"
				self.setCursor(QCursor(Qt.SizeBDiagCursor))
		elif (position.x() < self.x() + 3) or (position.x() > self.x() + self.width() - 3):
			if position.x() < self.x() + 3:
				self.setCursor(QCursor(Qt.SizeHorCursor))
				self.mode = "resize-left"
			else:
				self.setCursor(QCursor(Qt.SizeHorCursor))
				self.mode = "resize-right"
		elif (position.y() > self.y() + self.height() - 3) or (position.y() < self.y() + 3):
			if position.y() < self.y() + 3:
				self.setCursor(QCursor(Qt.SizeVerCursor))
				self.mode = "resize-top"
			else:
				self.setCursor(QCursor(Qt.SizeVerCursor))
				self.mode = "resize-bottom"
		else:
			self.setCursor(QCursor(Qt.ArrowCursor))
			self.mode = None
	
	def mouseReleaseEvent(self, event: QMouseEvent) -> None:
		self.mode = None
		super(ApplicationWindow, self).mouseReleaseEvent(event)
	
	def mouseMoveEvent(self, event):
		super(ApplicationWindow, self).mouseMoveEvent(event)
		if not self.is_editing or not self.focus or not self.allow_resize: return
		if not event.buttons():
			self.setCursorShape(QPoint(event.x() + self.geometry().x(), event.y() + self.geometry().y()))
			return
		if self.mode == "resize-top-left":
			new_width = event.globalX() - self.position.x() - self.geometry().x()
			new_height = event.globalY() - self.position.y() - self.geometry().y()
			new_position = event.globalPos() - self.position
			self.resize(self.geometry().width() - new_width, self.geometry().height() - new_height)
			self.move(new_position.x(), new_position.y())
		elif self.mode == "resize-top-right":
			new_height = event.globalY() - self.position.y() - self.geometry().y()
			new_position = event.globalPos() - self.position
			self.resize(event.x(), self.geometry().height() - new_height)
			self.move(self.x(), new_position.y())
		elif self.mode == "resize-bottom-left":
			new_width = event.globalX() - self.position.x() - self.geometry().x()
			new_position = event.globalPos() - self.position
			self.resize(self.geometry().width() - new_width, event.y())
			self.move(new_position.x(), self.y())
		elif self.mode == "resize-bottom": self.resize(self.width(), event.y())
		elif self.mode == "resize-left":
			new_width = event.globalX() - self.position.x() - self.geometry().x()
			new_position = event.globalPos() - self.position
			self.resize(self.geometry().width() - new_width, self.height())
			self.move(new_position.x(), self.y())
		elif self.mode == "resize-top":
			new_height = event.globalY() - self.position.y() - self.geometry().y()
			new_position = event.globalPos() - self.position
			self.resize(self.width(), self.geometry().height() - new_height)
			self.move(self.x(), new_position.y())
		elif self.mode == "resize-right": self.resize(event.x(), self.height())
		elif self.mode == "resize-bottom-right": self.resize(event.x(), event.y())
		self.parentWidget().repaint()
		self.new_geometry_signal.emit(self.geometry())
	
	def toolBarMouseMoveEvent(self, event=None):
		if event is None: return
		try: self.new_position = event.globalPos() - self.position
		except TypeError: pass
		else:
			if self.new_position.x() < 0 or self.new_position.y() < 0 or self.new_position.x() > self.parentWidget().width() - self.width(): return
			self.move(self.new_position)
			self.parentWidget().repaint()
			self.new_geometry_signal.emit(self.geometry())
	
	def resizeEvent(self, event: QResizeEvent) -> None:
		"""
		Try to call resize function (if available) from child widget
		Supported child widget functions names:
			parentResizeEvent
			parent_resize_event
			parentWidgetResizeEvent
			parent_widget_resize_event
		With argument:
			event[: (QtGui.)QResizeEvent]
		"""
		try: self.child_widget.parentResizeEvent(event)
		except AttributeError:
			try: self.child_widget.parent_resize_event(event)
			except AttributeError:
				try: self.child_widget.parentWidgetResizeEvent(event)
				except AttributeError:
					try: self.child_widget.parentWidgetResizeEvent(event)
					except AttributeError:
						try: self.child_widget.parent_widget_resize_event(event)
						except AttributeError: pass


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

