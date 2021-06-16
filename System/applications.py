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
	if "name" not in load(open(f"{rel_path}/application.json")) or "run" not in load(open(f"{rel_path}/application.json")) or "run_class" not in load(open(f"{rel_path}/application.json")): return {"valid": False}
	if not exists(f"{rel_path}/" + load(open(f"{rel_path}/application.json"))["run"]): return {"valid": False}
	return {"valid": True, "name": load(open(f"{rel_path}/application.json"))["name"], "path": f"{rel_path}/" + load(open(f"{rel_path}/application.json"))["run"], "run_class": load(open(f"{rel_path}/application.json"))["run_class"]}

def returnApplications() -> dict:
	"""Returns a dictionary of valid applications"""
	applications = {}
	for i in sorted(__import__("os").listdir("Applications"))[1:]:
		properties = getApplicationProperties(f"Applications/{i}")
		if properties["valid"]: applications[i] = {"name": properties["name"], "path": properties["path"], "file": properties["path"].split("/")[-1], "run_class": properties["run_class"]}
	return applications
