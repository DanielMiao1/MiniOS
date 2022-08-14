from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from typing import Optional

from ..config import returnBackgroundProperties


class ApplicationWindowToolBar(QToolBar):
	def __init__(self, background_color, mouse_move_event=None, window_name="Window", close_application_window_function=None):
		super(ApplicationWindowToolBar, self).__init__()
		self.setStyleSheet(f"background-color: {background_color}; border: 4px solid {background_color}; color: {returnBackgroundProperties()['text-color']};")
		self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
		self.setCursor(Qt.CursorShape.ArrowCursor)
		self.mouse_move_event = mouse_move_event
		self.close = QAction("×", self)
		if close_application_window_function is not None:
			self.close.triggered.connect(close_application_window_function)
		self.spacer = QWidget()
		self.spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.window_name = QAction(window_name, self)
		self.addAction(self.close)
		self.addWidget(self.spacer)
		self.addAction(self.window_name)

	def mouseMoveEvent(self, event):
		if self.mouse_move_event is not None:
			self.mouse_move_event(event)
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
		self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
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
		if self.restart_window_function is not None:
			self.restart_window_function(self.pos())

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
		if not self.is_editing:
			return
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
		self.position = QPoint(event.globalPosition().x() - self.geometry().x(), event.globalPosition().y() - self.geometry().y())
		super(ApplicationWindow, self).mousePressEvent(event)

	def setCursorShape(self, position):
		if not self.allow_resize:
			return
		if ((position.y() > self.y() + self.height() - 3) and (position.x() < self.x() + 3)) or ((position.y() > self.y() + self.height() - 3) and (position.x() > self.x() + self.width() - 3)) or ((position.y() < self.y() + 3) and (position.x() < self.x() + 3)) or (position.y() < self.y() + 3) and (position.x() > self.x() + self.width() - 3):
			if (position.y() > self.y() + self.height() - 3) and (position.x() < self.x() + 3):
				self.mode = "resize-bottom-left"
				self.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
			if (position.y() > self.y() + self.height() - 3) and (position.x() > self.x() + self.width() - 3):
				self.mode = "resize-bottom-right"
				self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
			if (position.y() < self.y() + 3) and (position.x() < self.x() + 3):
				self.mode = "resize-top-left"
				self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
			if (position.y() < self.y() + 3) and (position.x() > self.x() + self.width() - 3):
				self.mode = "resize-top-right"
				self.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
		elif (position.x() < self.x() + 3) or (position.x() > self.x() + self.width() - 3):
			if position.x() < self.x() + 3:
				self.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
				self.mode = "resize-left"
			else:
				self.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
				self.mode = "resize-right"
		elif (position.y() > self.y() + self.height() - 3) or (position.y() < self.y() + 3):
			if position.y() < self.y() + 3:
				self.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
				self.mode = "resize-top"
			else:
				self.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
				self.mode = "resize-bottom"
		else:
			self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
			self.mode = None

	def mouseReleaseEvent(self, event: QMouseEvent) -> None:
		self.mode = None
		super(ApplicationWindow, self).mouseReleaseEvent(event)

	def mouseMoveEvent(self, event: QMouseEvent):
		super(ApplicationWindow, self).mouseMoveEvent(event)
		if not self.is_editing or not self.focus or not self.allow_resize:
			return
		if not event.buttons():
			self.setCursorShape(QPoint(event.pos().x() + self.geometry().x(), event.pos().y() + self.geometry().y()))
			return
		if self.mode == "resize-top-left":
			new_width = event.globalPosition().x() - self.position.x() - self.geometry().x()
			new_height = event.globalPosition().y() - self.position.y() - self.geometry().y()
			new_position = event.globalPosition() - self.position
			self.resize(self.geometry().width() - new_width, self.geometry().height() - new_height)
			self.move(new_position.x(), new_position.y())
		elif self.mode == "resize-top-right":
			new_height = event.globalPosition().y() - self.position.y() - self.geometry().y()
			new_position = event.globalPosition() - QPointF(self.position)
			self.resize(event.pos().x(), self.geometry().height() - new_height)
			self.move(self.x(), new_position.y())
		elif self.mode == "resize-bottom-left":
			new_width = event.globalPosition().x() - self.position.x() - self.geometry().x()
			new_position = event.globalPosition() - QPointF(self.position)
			self.resize(self.geometry().width() - new_width, event.pos().y())
			self.move(new_position.x(), self.y())
		elif self.mode == "resize-bottom":
			self.resize(self.width(), event.pos().y())
		elif self.mode == "resize-left":
			new_width = event.globalPosition().x() - self.position.x() - self.geometry().x()
			new_position = event.globalPosition() - QPointF(self.position)
			self.resize(self.geometry().width() - new_width, self.height())
			print(new_position.x(), new_position.y())
			self.move(new_position.x(), self.y())
		elif self.mode == "resize-top":
			new_height = event.globalPosition().y() - self.position.y() - self.geometry().y()
			new_position = event.globalPosition() - QPointF(self.position)
			self.resize(self.width(), self.geometry().height() - new_height)
			self.move(self.x(), new_position.y())
		elif self.mode == "resize-right":
			self.resize(event.pos().x(), self.height())
		elif self.mode == "resize-bottom-right":
			self.resize(event.pos().x(), event.pos().y())
		self.parentWidget().repaint()
		self.new_geometry_signal.emit(self.geometry())

	def toolBarMouseMoveEvent(self, event: Optional[QMouseEvent] = None):
		if event is None:
			return
		try:
			self.new_position = event.globalPosition() - QPointF(self.position)
		except TypeError:
			return
		if self.new_position.x() < 0 or self.new_position.y() < 0 or self.new_position.x() > self.parentWidget().width() - self.width():
			return
		self.move(QPoint(round(self.new_position.x()), round(self.new_position.y())))
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
		try:  # TODO: use hasattr() instead
			self.child_widget.parentResizeEvent(event)
		except AttributeError:
			try:
				self.child_widget.parent_resize_event(event)
			except AttributeError:
				try:
					self.child_widget.parentWidgetResizeEvent(event)
				except AttributeError:
					try:
						self.child_widget.parentWidgetResizeEvent(event)
					except AttributeError:
						try:
							self.child_widget.parent_widget_resize_event(event)
						except AttributeError:
							pass
