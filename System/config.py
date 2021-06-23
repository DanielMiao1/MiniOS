# -*- coding: utf-8 -*-
"""
System/config.py
Checks if config values in config.json are valid and returns them
Made by Daniel M using Python 3
"""
import json.decoder
from json import load, dump

class Config:
	def __init__(self):
		ColorConfig.formatJSON()
		FontConfig.formatJSON()
		WindowConfig.formatJSON()

	@staticmethod
	def appendJSON(values: dict, file_name: str) -> None:
		with open(file_name, "r+") as file:
			data = load(file)
			for i in values.keys(): data[i] = values[i]
			print(data)
			file.seek(0)
			dump(data, file, indent = 2)

class ColorConfig:
	@staticmethod
	def formatJSON() -> None:
		with open("System/config/colors.json") as file:
			try: load(file)
			except json.decoder.JSONDecodeError: open("System/config/colors.json", "w").write("{\n  \"background-color\": \"#ffffff\",\n  \"secondary-background-color\": \"#ffffff\",\n  \"text-color\": \"#000000\"\n}\n")
			file = open("System/config/colors.json")
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
			try: load(file)
			except json.decoder.JSONDecodeError: open("System/config/font.json", "w").write("{\n  \"fonts\": [\n    \"Arial\",\n    \"Gill Sans\",\n    \"Times\",\n    \"Courier\",\n    \"Symbol\",\n    \"Calibri\",\n    \"Cambria\",\n    \"Candara\",\n    \"Comic Sans MS\",\n    \"Consolas\",\n    \"Constantia\",\n    \"Corbel\",\n    \"Courier New\",\n    \"Franklin Gothic Medium\",\n    \"Gabriola\",\n    \"Georgia\",\n    \"Helvetica\",\n    \"Impact\",\n    \"MS Gothic\",\n    \"Rockwell\",\n    \"SimSun\",\n    \"SimSun-ExtB\",\n    \"Tahoma\",\n    \"Times New Roman\",\n    \"Trebuchet MS\",\n    \"Verdana\",\n    \"Webdings\",\n    \"Wingdings\"\n  ],\n  \"font-family\": \"Helvetica\",\n  \"font-size\": \"12\"\n}")
			file = open("System/config/font.json")
			loaded_file = load(file)
			if open("System/config/font.json", "r+").read() == "": open("System/config/font.json", "w").write("{ }")
			if "font-family" not in loaded_file: Config.appendJSON({"font-family": "Arial"}, "System/config/font.json")
			if "font-size" not in loaded_file: Config.appendJSON({"font-size": "12"}, "System/config/font.json")
			if "fonts" not in loaded_file: Config.appendJSON({"fonts": ["Arial", "Gill Sans", "Times", "Courier", "Symbol", "Calibri", "Cambria", "Candara", "Comic Sans MS", "Consolas", "Constantia", "Corbel", "Courier New", "Franklin Gothic Medium", "Gabriola", "Georgia", "Helvetica", "Impact", "MS Gothic", "Rockwell", "SimSun", "SimSun-ExtB", "Tahoma", "Times New Roman", "Trebuchet MS", "Verdana", "Webdings", "Wingdings"]}, "System/config/font.json")
			if open("System/config/font.json", "r+").read().splitlines()[-1] != "": open("System/config/font.json", "a").write("\n")
	
	@staticmethod
	def returnConfig() -> bool or dict:
		if __import__("os").path.exists("System/config/font.json"): return load(open("System/config/font.json"))
		return False

class WindowConfig:
	@staticmethod
	def formatJSON() -> None:
		with open("System/config/window.json") as file:
			try: load(file)
			except json.decoder.JSONDecodeError: open("System/config/window.json", "w").write("{\n  \"size\": \"full\"\n}")
			file = open("System/config/window.json")
			loaded_file = load(file)
			if open("System/config/window.json", "r+").read() == "": open("System/config/window.json", "w").write("{\n  \n}")
			if "size" not in loaded_file: Config.appendJSON({"size": "full"}, "System/config/window.json")
			if open("System/config/window.json", "r+").read().splitlines()[-1] != "": open("System/config/window.json", "a").write("\n")
			
	@staticmethod
	def returnConfig() -> bool or dict:
		if __import__("os").path.exists("System/config/window.json"): return load(open("System/config/window.json"))
		return False

def returnProperties() -> dict: return {**ColorConfig.returnConfig(), **FontConfig.returnConfig(), **WindowConfig.returnConfig()}
