# -*- coding: utf-8 -*-
"""
System/import_modules.py
Check if modules are installed
Made By Daniel M using Python 3
"""

from os import system
from sys import executable

from rerun import rerun as rerun_program


def checkModules() -> None:
	rerun = False
	try:
		import PyQt6
	except ImportError:
		rerun = True
		if input("The PyQt6 library for graphics is not installed. Enter 'install' to install the module, or anything else to stop the process: ").lower() == "install":
			system(f"{executable} -m pip install PyQt6")
		else:
			print("You can manually install the PyQt6 library by running the 'pip3 install PyQt6' command in the terminal")
			exit()
			
	try:
		import PyQt6.QtWebEngineWidgets
	except ImportError:
		rerun = True
		if input("The PyQt6-WebEngine library (responsible for displaying webpages) is not installed. Enter 'install' to install the module, or anything else to stop the process: ").lower() == "install":
			system(f"{executable} -m pip install PyQt6-WebEngine")
		else:
			print("You can manually install the PyQt6-WebEngine Library by running the 'pip3 install PyQt6-WebEngine' command in the terminal")
			exit()
	
	if rerun:
		rerun_program()
