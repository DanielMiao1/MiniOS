# -*- coding: utf-8 -*-
"""
System/config.py
Checks if config values in config.json are valid and returns them
Made by Daniel M using Python 3
"""

from json import load, dump

class Config:
	def __init__(self):
		ColorConfig.formatJSON()

	@staticmethod
	def appendJSON(values: dict, file_name: str) -> None:
		with open(file_name, "r+") as file:
			data = load(file)
			data.update(values)
			file.seek(0)
			dump(data, file, indent = 2)

class ColorConfig:
	@staticmethod
	def formatJSON() -> None:
		with open("System/config/colors.json") as file:
			loaded_file = load(file)
			if open("System/config/colors.json", "r+").read() == "": open("System/config/colors.json", "w").write("{ }")
			if "background-color" not in loaded_file: Config.appendJSON({"background-color": "#ffffff"}, "System/config/colors.json")
			if "secondary-background-color" not in loaded_file: Config.appendJSON({"secondary-background-color": "#ffffff"}, "System/config/colors.json")
			if "text-color" not in loaded_file: Config.appendJSON({"text-color": "#000000"}, "System/config/colors.json")
			if open("System/config/colors.json", "r+").read().splitlines()[-1] != "": open("System/config/colors.json", "a").write("\n")
	
	@staticmethod
	def returnConfig() -> bool or dict:
		if not __import__("os").path.exists("System/config/colors.json"): return False
		return load(open("System/config/colors.json"))
