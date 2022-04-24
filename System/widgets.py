"""
System/widgets.py
Widgets
Made by Daniel M using Python 3
"""

# Local imports
from config import returnBackgroundProperties
from overrides import ApplicationWindowToolBar

# PyQt imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


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

	
class ApplicationWindow(QWidget):
	mode = None
	position = None
	focus_signal = pyqtSignal(bool)
	out_focus_signal = pyqtSignal(bool)
	new_geometry_signal = pyqtSignal(QRect)
	
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
	
	def closeWindow(self): self.setParent(None)
	
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
					try: self.child_widget.parent_widget_resize_event(event)
					except AttributeError: pass
		super(ApplicationWindow, self).resizeEvent(event)
	
	def contextMenuEvent(self, event: QContextMenuEvent) -> None: self.child_widget.contextMenuEvent(event)
