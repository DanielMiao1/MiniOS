# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Dock(QGroupBox):
	def __init__(self, parent):
		super(Dock, self).__init__(parent=parent)
		self.setLayout(QHBoxLayout())
		self.background = None
		self.color = None
		self.font_family = None
		self.font_size = None
		self.layout().setContentsMargins(2, 2, 2, 2)
		self.layout().setSpacing(0)
		self.layout().addStretch()
		self.layout().addStretch()
	
	def addItem(self, name, icon, run_class):
		self.layout().insertWidget(self.layout().count() - 1, DockItem(self, name, icon, run_class))
	
	def adjustGeometry(self):
		self.move(0, self.parent().height() - self.height())
		self.resize(self.parent().width(), 50)
	
	def setStyles(self, **styles):
		self.background = styles["background_color"] if "background_color" in styles else None
		self.color = styles["text_color"] if "text_color" in styles else None
		self.font_family = styles["font_family"] if "font_family" in styles else None
		self.font_size = styles["font_size"] if "font_size" in styles else None
		self.setStyleSheet(f"background-color: {self.background}; color: {self.color}; border: none;")


class DockItem(QLabel):
	def __init__(self, parent, name, icon_path, run_class):
		super(DockItem, self).__init__(parent=parent)
		self.setContentsMargins(5, 0, 5, 0)
		self.setPixmap(QPixmap(icon_path).scaled(QSize(35, 35)))
		self.name = name
		self.icon_path = icon_path
		self.run_class = run_class
		self.label = QLabel(self.name, self.parent().parent())
		self.label.setStyleSheet(f"background-color: {self.parent().background}; color: {self.parent().color}; font-family: {self.parent().font_family}; font-size: {self.parent().font_size}; padding: 5px;")
		self.label.adjustSize()
		self.label.hide()
	
	def enterEvent(self, event):
		self.label.move(QPoint(event.globalPos().x() - event.pos().x() + (self.width() // 2) - (self.label.width() // 2), self.parent().parent().height() - self.parent().height() - self.label.height() - 10))
		self.label.show()
		super(DockItem, self).enterEvent(event)
	
	def leaveEvent(self, event):
		self.label.hide()
		super(DockItem, self).leaveEvent(event)
	
	def mousePressEvent(self, event):
		# self.
		self.parent().parent().openApplication(self.run_class)
		super(DockItem, self).mousePressEvent(event)
