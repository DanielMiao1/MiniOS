# The Simplifyc Operating System
# Made by Daniel M using PyQt5

try: import os # Import OS module
except ImportError(name = "os"):
	print("An error occurred while trying to import the os module.")
	exit() # If OS module is not found

try:
	from PyQt5.QtGui import *
	from PyQt5.QtWidgets import *
except ImportError:
	if input("The PyQt5 Library is not installed. Enter 'install' to install the module, or anything else to stop the process. ").lower() == "install": os.system("pip install PyQt5")

