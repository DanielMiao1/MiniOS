# -*- coding: utf-8 -*-
"""
Applications/.ApplicationSupport/get_properties.py
returnProperties function returns dictionary with values from System/config JSON files
Made by Daniel M using Python 3 for Application Support in the MiniOS project: https://github.com/DanielMiao1/MiniOS
"""

from System.core.config import *


def returnProperties() -> dict:
	return {**ThemeConfig.returnConfig(), **FontConfig.returnConfig(), **WindowConfig.returnConfig()}


def returnBackgroundProperties() -> dict:
	return Themes.getThemes()[ThemeConfig.returnConfig()["theme"]]
