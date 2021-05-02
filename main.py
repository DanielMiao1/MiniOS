try: import os # Import OS module
except ImportError(name = "os"):
	print("An error occurred while trying to import the os module.")
	exit() # If OS module is not found, print error message and exit

os.system("python3 System/main.py") # Run main script in System/main.py
