"""
System/rerun.py
Rerun main.py script for imports
Made by Daniel M
"""
def rerun():
	print("Successfully installed required packages.")
	__import__("os").system("python3 System/main.py")
