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
			data.updateElements()
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
		if __import__("os").path.exists("System/config/colors.json"): return load(open("System/config/colors.json"))
		return False

class FontConfig:
	@staticmethod
	def formatJSON() -> None:
		with open("System/config/font.json") as file:
			loaded_file = load(file)
			if open("System/config/font.json", "r+").read() == "": open("System/config/font.json", "w").write("{ }")
			if "font-family" not in loaded_file: Config.appendJSON({"font-family": "Arial"}, "System/config/font.json")
			if "font-size" not in loaded_file: Config.appendJSON({"font-size": "15"}, "System/config/font.json")
			if "fonts" not in loaded_file: Config.appendJSON({"fonts": ["Arial", "Gill Sans", "Times", "Courier", "Symbol", "Calibri", "Cambria", "Candara", "Comic Sans MS", "Consolas", "Constantia", "Corbel", "Courier New", "Franklin Gothic Medium", "Gabriola", "Georgia", "Helvetica", "Impact", "MS Gothic", "Rockwell", "SimSun", "SimSun-ExtB", "Tahoma", "Times New Roman", "Trebuchet MS", "Verdana", "Webdings", "Wingdings"]}, "System/config/font.json")
			if open("System/config/font.json", "r+").read().splitlines()[-1] != "": open("System/config/font.json", "a").write("\n")
	
	@staticmethod
	def returnConfig() -> bool or dict:
		if __import__("os").path.exists("System/config/font.json"): return load(open("System/config/font.json"))
		return False

def returnProperties() -> dict: return {**ColorConfig.returnConfig(), **FontConfig.returnConfig()}