# -*- coding: utf-8 -*-
"""
System/config.py
Checks if config values in config.json are valid and returns them
Made by Daniel M using Python 3
"""

import json.decoder
import os
from json import dump, load


class Config:
	def __init__(self):
		ThemeConfig.formatJSON()
		FontConfig.formatJSON()

	@staticmethod
	def appendJSON(values: dict, file_name: str) -> None:
		with open(file_name, "r+") as file:
			data = load(file)
			for i in values.keys():
				data[i] = values[i]
			file.seek(0)
			dump(data, file, indent=2)


class ThemeConfig:
	"""
	Theme Configuration
	DO NOT MODIFY THIS FILE DIRECTLY. TO MODIFY THEME COLORS, EDIT System/config/themes/dark.json or System/config/themes/light.json
	TO CREATE A NEW THEME, ADD A JSON FILE AT System/config/themes.
	"""
	@staticmethod
	def formatJSON() -> None:
		with open("System/config/theme.json") as file:
			try: load(file)
			except json.decoder.JSONDecodeError: open("System/config/theme.json", "w").write("{\"theme\": \"light\"}\n")
			file = open("System/config/theme.json")
			loaded_file = load(file)
			if open("System/config/theme.json", "r+").read() == "":
				open("System/config/theme.json", "w").write("{ }")
			if "theme" not in loaded_file:
				Config.appendJSON({"theme": "light"}, "System/config/theme.json")
			if open("System/config/theme.json", "r+").read().splitlines()[-1] != "":
				open("System/config/theme.json", "a").write("\n")
	
	@staticmethod
	def returnConfig() -> bool or dict:
		ThemeConfig.formatDefault()
		if not os.path.exists("System/config/theme.json"):
			open("System/config/theme.json", "w").write(f"{{\"theme\": \"{ThemeConfig.returnDefault()['default']}\"}}\n")
		return load(open("System/config/theme.json"))
	
	@staticmethod
	def returnDefault() -> dict:
		ThemeConfig.formatDefault()
		return load(open("System/default_config/themes.json"))
	
	@staticmethod
	def formatDefault() -> None:
		if not os.path.exists("System/default_config/themes.json"):
			open("System/config/themes.json", "w").write("{\n  \"default\": \"light\"\n}\n")



class FontConfig:
	"""
	Font Configuration
	DO NOT MODIFY THIS FILE DIRECTLY. TO MODIFY FONT DEFAULTS, EDIT System/default_config/font.json
	"""
	@staticmethod
	def formatJSON() -> None:
		with open("System/config/font.json") as file:
			try: load(file)
			except json.decoder.JSONDecodeError: open("System/config/font.json", "w").write("{\n  \"fonts\": [\n    \"Arial\",\n    \"Gill Sans\",\n    \"Times\",\n    \"Courier\",\n    \"Symbol\",\n    \"Calibri\",\n    \"Cambria\",\n    \"Candara\",\n    \"Comic Sans MS\",\n    \"Consolas\",\n    \"Constantia\",\n    \"Corbel\",\n    \"Courier New\",\n    \"Gabriola\",\n    \"Georgia\",\n    \"Helvetica\",\n    \"Impact\",\n    \"MS Gothic\",\n    \"Rockwell\",\n    \"SimSun\",\n    \"SimSun-ExtB\",\n    \"Tahoma\",\n    \"Times New Roman\",\n    \"Trebuchet MS\",\n    \"Verdana\",\n    \"Webdings\",\n    \"Wingdings\"\n  ],\n  \"font-family\": \"Helvetica\",\n  \"font-size\": \"12\"\n}")
			file = open("System/config/font.json")
			loaded_file = load(file)
			if open("System/config/font.json", "r+").read() == "":
				open("System/config/font.json", "w").write("{ }")
			if "font-family" not in loaded_file:
				Config.appendJSON({"font-family": "Arial"}, "System/config/font.json")
			if "font-size" not in loaded_file:
				Config.appendJSON({"font-size": "12"}, "System/config/font.json")
			if "fonts" not in loaded_file:
				Config.appendJSON({"fonts": ["Arial", "Gill Sans", "Times", "Courier", "Symbol", "Calibri", "Cambria", "Candara", "Comic Sans MS", "Consolas", "Constantia", "Corbel", "Courier New", "Gabriola", "Georgia", "Helvetica", "Impact", "MS Gothic", "Rockwell", "SimSun", "SimSun-ExtB", "Tahoma", "Times New Roman", "Trebuchet MS", "Verdana", "Webdings", "Wingdings"]}, "System/config/font.json")
			if open("System/config/font.json", "r+").read().splitlines()[-1] != "":
				open("System/config/font.json", "a").write("\n")
	
	@staticmethod
	def returnConfig() -> bool or dict:
		FontConfig.formatDefault()
		if not os.path.exists("System/config/font.json"):
			open("System/config/font.json", "w").write(f"{{\n  \"fonts\": [\n    \"Arial\",\n    \"Gill Sans\",\n    \"Times\",\n    \"Courier\",\n    \"Symbol\",\n    \"Calibri\",\n    \"Cambria\",\n    \"Candara\",\n    \"Comic Sans MS\",\n    \"Consolas\",\n    \"Constantia\",\n    \"Corbel\",\n    \"Courier New\",\n    \"Gabriola\",\n    \"Georgia\",\n    \"Helvetica\",\n    \"Impact\",\n    \"MS Gothic\",\n    \"Rockwell\",\n    \"SimSun\",\n    \"SimSun-ExtB\",\n    \"Tahoma\",\n    \"Times New Roman\",\n    \"Trebuchet MS\",\n    \"Verdana\",\n    \"Webdings\",\n    \"Wingdings\"\n  ],\n  \"font-family\": \"{FontConfig.returnDefault()['default-font']}\",\n  \"font-size\": \"{FontConfig.returnDefault()['default-size']}\"\n}}")
		return load(open("System/config/font.json"))
	
	@staticmethod
	def returnDefault() -> dict:
		FontConfig.formatDefault()
		return load(open("System/default_config/font.json"))
	
	@staticmethod
	def formatDefault() -> None:
		if not os.path.exists("System/default_config/font.json"):
			open("System/config/font.json", "w").write("{\n  \"default-font\": \"Helvetica\",\n  \"default-size\": 12\n}\n")
	

class WindowConfig:
	"""
	Window Configuration
	DO NOT MODIFY THIS FILE DIRECTLY. TO MODIFY DEFAULT WINDOW CONFIGURATIONS, EDIT System/default_config/window.json
	"""
	@staticmethod
	def formatJSON() -> None:
		with open("System/config/window.json") as file:
			try: load(file)
			except json.decoder.JSONDecodeError: open("System/config/window.json", "w").write("{\n  \"size\": \"full\"\n}")
			file = open("System/config/window.json")
			loaded_file = load(file)
			if open("System/config/window.json", "r+").read() == "":
				open("System/config/window.json", "w").write("{\n  \n}")
			if "size" not in loaded_file:
				Config.appendJSON({"size": "full"}, "System/config/window.json")
			if open("System/config/window.json", "r+").read().splitlines()[-1] != "":
				open("System/config/window.json", "a").write("\n")
			
	@staticmethod
	def returnConfig() -> dict:
		WindowConfig.formatDefault()
		if not os.path.exists("System/config/window.json"):
			open("System/config/window.json", "w").write(f"{{\n  \"size\": \"{WindowConfig.returnDefault()['default-size']}\"\n}}")
		return load(open("System/config/window.json"))
	
	@staticmethod
	def returnDefault() -> dict:
		WindowConfig.formatDefault()
		return load(open("System/default_config/window.json"))
	
	@staticmethod
	def formatDefault() -> None:
		if not os.path.exists("System/default_config/window.json"):
			open("System/config/window.json", "w").write("{\n  \"default-size\": [1440, 720]\n}")


class Themes:
	@staticmethod
	def getThemes() -> dict:
		themes = {}
		for i in os.listdir("System/config/themes"):
			themes[i[:-5]] = load(open(f"System/config/themes/{i}"))
		return themes


def returnProperties() -> dict:
	return {**ThemeConfig.returnConfig(), **FontConfig.returnConfig(), **WindowConfig.returnConfig()}


def returnBackgroundProperties() -> dict:
	return Themes.getThemes()[ThemeConfig.returnConfig()["theme"]]
