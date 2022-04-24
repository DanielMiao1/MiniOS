# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../")

from config import returnBackgroundProperties
from datetime import datetime

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


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


class ApplicationWindowToolBar(QToolBar):
	def __init__(self, background_color, mouse_move_event=None, window_name="Window", close_application_window_function=None):
		super(ApplicationWindowToolBar, self).__init__()
		self.setStyleSheet(f"background-color: {background_color}; border: 4px solid {background_color};")
		self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
		self.setCursor(Qt.ArrowCursor)
		self.mouse_move_event = mouse_move_event
		self.close = QAction("×", self)
		if close_application_window_function is not None:
			self.close.triggered.connect(close_application_window_function)
		self.spacer = QWidget()
		self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.window_name = QAction(window_name, self)
		self.addAction(self.close)
		self.addWidget(self.spacer)
		self.addAction(self.window_name)
	
	def mouseMoveEvent(self, event):
		if self.mouse_move_event is not None:
			self.mouse_move_event(event)
		super(ApplicationWindowToolBar, self).mouseMoveEvent(event)
	
	
class ApplicationWindow(QWidget):
	mode = None
	position = None
	focus_signal = pyqtSignal(bool)
	out_focus_signal = pyqtSignal(bool)
	new_geometry_signal = pyqtSignal(QRect)
	
	def __init__(self, parent, point, child_widget, background_color="default", window_name="Window", toolbar_background_color=returnBackgroundProperties()['background-color-3'], custom_stylesheet="", window_size=QSize(800, 350), restart_window_function=None, allow_resize=True):
		super(ApplicationWindow, self).__init__(parent=parent)
		if isinstance(window_size, list):
			if len(window_size) == 2:
				window_size = QSize(window_size[0], window_size[1])
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
	
	def restartWindow(self):
		self.closeWindow()
		if self.restart_window_function is not None:
			self.restart_window_function(self.pos())
	
	def setChildWidget(self, child_widget):
		if child_widget:
			child_widget.setParent(self)
			child_widget.releaseMouse()
			self.layout.addWidget(child_widget)
			self.layout.setContentsMargins(1, 1, 1, 1)
	
	def focusInEvent(self, _):
		self.focus = True
		parent = self.parentWidget()
		parent.installEventFilter(self)
		parent.repaint()
		self.focus_signal.emit(True)
	
	def focusOutEvent(self, _):
		if not self.is_editing:
			return
		self.mode = None
		self.out_focus_signal.emit(False)
		self.focus = False
	
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.fillRect(event.rect(), QColor(self.background_color if self.background_color.lower() != "default" else returnBackgroundProperties()["background-color"]))
		rect = event.rect()
		rect.adjust(0, 0, -1, -1)
		painter.setPen(QColor(self.toolbar_background_color))
		painter.drawRect(rect)
	
	def mousePressEvent(self, event):
		self.position = QPoint(event.globalX() - self.geometry().x(), event.globalY() - self.geometry().y())
		if not event.buttons():
			self.setCursorShape(event.pos())
			return
		super(ApplicationWindow, self).mousePressEvent(event)
	
	def setCursorShape(self, position):
		if not self.allow_resize:
			return
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
	
	def mouseReleaseEvent(self, event):
		QWidget.mouseReleaseEvent(self, event)
	
	def mouseMoveEvent(self, event):
		QWidget.mouseMoveEvent(self, event)
		if not self.is_editing or not self.focus or not self.allow_resize:
			return
		if not event.buttons() and Qt.LeftButton:
			p = QPoint(event.x() + self.geometry().x(), event.y() + self.geometry().y())
			self.setCursorShape(p)
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
		elif self.mode == "resize-bottom":
			self.resize(self.width(), event.y())
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
		elif self.mode == "resize-right":
			self.resize(event.x(), self.height())
		elif self.mode == "resize-bottom-right":
			self.resize(event.x(), event.y())
		self.parentWidget().repaint()
		self.new_geometry_signal.emit(self.geometry())
		
	def toolBarMouseMoveEvent(self, event=None):
		if event is None:
			return
		try: self.new_position = event.globalPos() - self.position
		except TypeError: pass
		else:
			if self.new_position.x() < 0 or self.new_position.y() < 0 or self.new_position.x() > self.parentWidget().width() - self.width():
				return
			self.move(self.new_position)
			self.parentWidget().repaint()
			self.new_geometry_signal.emit(self.geometry())
	
	def resizeEvent(self, event: QResizeEvent) -> None:
		"""
		Try to call resize function (if available) from child widget
		Supported child widget function names:
			parentResizeEvent(event: QResizeEvent, *args)
			resizeEvent(event: QResizeEvent, *args)
			parent_resize_event(event: QResizeEvent, *args)
			parentWidgetResizeEvent(event: QResizeEvent, *args)
			parent_widget_resize_event(event: QResizeEvent, *args)
		"""
		try: self.child_widget.parentResizeEvent(event)
		except AttributeError:
			try: self.child_widget.resizeEvent(event)
			except AttributeError:
				try: self.child_widget.parent_resize_event(event)
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


class Clock(QLabel):
	def __init__(self, parent):
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
