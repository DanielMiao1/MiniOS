"""
System/import_modules.py
Check if modules are installed
Made By Daniel M using Python 3
"""

# Module imports
from os import system

# Local file imports
from rerun import rerun as rerun_program

def checkModules() -> None:
	rerun = False
	try: import PyQt5
	except ImportError:
		rerun = True
		if input("The PyQt5 Library is not installed. Enter 'install' to install the module, or anything else to stop the process: ").lower() == "install": system("pip3 install PyQt5")
		else:
			print("You can manually install the PyQt5 Library by running the 'pip3 install PyQt5' command in the terminal")
			exit()
			
	# Check if PyQt5.QtWebEngineWidgets is installed for the browser application; and if the module is not installed using pip, ask the user to install it
	try: import PyQt5.QtWebEngineWidgets
	except ImportError:
		rerun = True
		if input("The PyQtWebEngineWidgets Library is not installed. Enter 'install' to install the module, or anything else to stop the process: ").lower() == "install": system("pip3 install PyQtWebEngine")
		else:
			print("You can manually install the PyQtWebEngineWidgets Library by running the 'pip3 install PyQtWebEngine' command in the terminal")
			exit()
	
	if rerun: rerun_program()
