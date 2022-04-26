# -*- coding: utf-8 -*-
"""
System/desktop_files.py
Gets all Desktop files/directories
Made by Daniel M using Python 3
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def getFileIcon(file_extension: str, file_type: str) -> QIcon:
	if file_type == "directory":
		return QIcon("System/images/file_icons/directory.png")
	if file_extension == "txt":
		return QIcon("System/images/file_icons/txt.png")
	elif file_extension == "rtf":
		return QIcon("System/images/file_icons/rtf.png")
	elif file_extension == "png":
		return QIcon("System/images/file_icons/png.png")
	elif file_extension == "jpg":
		return QIcon("System/images/file_icons/jpg.png")
	elif file_extension == "gif":
		return QIcon("System/images/file_icons/gif.png")
	return QIcon("System/images/file_icons/document.png")


def returnItems() -> dict:
	"""Returns a dictionary of valid applications"""
	items = {}
	for i in __import__("os").listdir("Home/Desktop"):
		if i.split(".")[-1].lower() not in ["minios", "miniosdir"] or i.count(".") == 0 or i.startswith("."):
			continue
		if i.split(".")[-1] == "minios":
			file_type, file_name, file_extension = "file", ".".join(i.split(".")[:-2]), i.split(".")[-2]
		elif i.split(".")[-1] == "miniosdir":
			file_type, file_name, file_extension = "directory", ".".join(i.split(".")[:-1]), i.split(".")[-2] if len(i.split(".")) > 2 else None
		else:
			file_type, file_name, file_extension = "unknown", "unknown", "unknown"
		items[i] = {"filename": file_name, "extension": file_extension, "type": file_type, "displayname": f"{file_name}.{file_extension}" if file_type == "file" else file_name}
	return items


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