"""
Applications/.ApplicationSupport/get_properties.py
returnProperties function returns dictionary with values from System/config JSON files
Made by Daniel M using Python 3 for Application Support in the SimplifycOS project: https://github.com/DanielMiao1/SimplifycOS
"""

__import__("sys").path.insert(1, "System/")
import config

def returnProperties() -> dict: return {**config.ColorConfig.returnConfig(), **config.FontConfig.returnConfig()}