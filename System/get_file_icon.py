"""
System/get_file_icon.py
Function getFileIcon returns PyQt5.QtGui.QIcon for files or directories
Made by Daniel M using Python 3
"""

# from PyQt5.QtCore import *
from PyQt5.QtGui import *


def getFileIcon(file_extension: str, file_type: str) -> QIcon:
	if file_type == "directory": return QIcon("System/images/file_icons/directory.png")
	if file_extension == "txt": return QIcon("System/images/file_icons/txt.png")
	elif file_extension == "rtf": return QIcon("System/images/file_icons/rtf.png")
	return QIcon("System/images/file_icons/document.png")
