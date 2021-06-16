# -*- coding: utf-8 -*-
"""
System/config.py
Checks if config values in config.json are valid and returns them
Made by Daniel M using Python 3
"""

from json import load, dump

class Config:
	def __init__(self):
		self.color_config = ColorConfig()
		self.color_config.formatJSON(False)

	@staticmethod
	def appendJSON(values: dict, file_name: str) -> None:
		with open(file_name, "r+") as file:
			data = load(file)
			data.update(values)
			file.seek(0)
			dump(data, file, indent = 2)

class ColorConfig:
	def __init__(self): pass
	
	@staticmethod
	def formatJSON(return_value: bool) -> dict:
		if all(True for i in list(open("System/config/colors.json", "r").read()) if i == " ") or open("System/config/colors.json", "r").read() == "": open("System/config/colors.json", "w").write("{ }")
		if "background-color" not in load(open("System/config/colors.json")).keys(): Config.appendJSON({"background-color": "#ffffff"}, "System/config/colors.json")
		if "secondary-background-color" not in load(open("System/config/colors.json")).keys(): Config.appendJSON({"secondary-background-color": "#ffffff"}, "System/config/colors.json")
		if return_value: return load(open("System/config/colors.json"))
	
	def returnConfig(self) -> bool or dict:
		if not __import__("os").path.exists("System/config/colors.json"): return False
		return self.formatJSON(True)
