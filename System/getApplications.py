# -*- coding: utf-8 -*-
"""
System/getApplications.py
Gets all applications
Made by Daniel M using Python 3
"""

from json import load
from os.path import exists

def getApplicationProperties(rel_path: str) -> dict:
	"""Returns the application properties if the application at the given path is valid, otherwise return False"""
	if not exists(f"{rel_path}/application.json"): return {"valid": False}
	if "name" not in load(open(f"{rel_path}/application.json")) or "run" not in load(open(f"{rel_path}/application.json")): return {"valid": False}
	if not exists(f"{rel_path}/" + load(open(f"{rel_path}/application.json"))["run"]): return {"valid": False}
	return {"valid": True, "name": load(open(f"{rel_path}/application.json"))["name"], "path": f"{rel_path}/" + load(open(f"{rel_path}/application.json"))["run"]}

def returnApplications() -> dict:
	"""Returns a dictionary of valid applications"""
	applications = {}
	for i in __import__("os").listdir("Applications"):
		properties = getApplicationProperties(f"Applications/{i}")
		if properties["valid"]: applications[i] = {"name": properties["name"].title(), "path": properties["path"], "file": properties["path"].split("/")[-1]}
	return applications
