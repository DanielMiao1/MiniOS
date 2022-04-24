"""
Applications/.ApplicationSupport/get_properties.py
returnProperties function returns dictionary with values from System/config JSON files
Made by Daniel M using Python 3 for Application Support in the MiniOS project: https://github.com/DanielMiao1/MiniOS
"""

__import__("sys").path.insert(1, "System/")
import config


def returnProperties() -> dict:
	return {**config.ThemeConfig.returnConfig(), **config.FontConfig.returnConfig()}


def returnBackgroundProperties() -> dict:
	return config.Themes.getThemes()[config.ThemeConfig.returnConfig()["theme"]]
