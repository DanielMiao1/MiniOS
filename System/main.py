# The Simplifyc Operating System main script
# Made by Daniel M using Python 3

# Imports
import os
import sys

try:
	from PyQt5.QtGui import *
	from PyQt5.QtCore import *
	from PyQt5.QtWidgets import *
except ImportError:
	if input("The PyQt5 Library is not installed. Enter 'install' to install the module, or anything else to stop the process. ").lower() == "install":
		os.system("pip install PyQt5")

print("Starting the Simplifyc Operating System...") # Print startup message

class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()


(application, window) = (QApplication(sys.argv), Window())
application.exec_()
