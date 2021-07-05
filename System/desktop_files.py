"""
System/desktop_files.py
Gets all Desktop files/directories
Made by Daniel M using Python 3
"""

def returnItems() -> dict:
	"""Returns a dictionary of valid applications"""
	items = {}
	for i in __import__("os").listdir("Home/Desktop"):
		if i.split(".")[-1].lower() not in ["minios", "miniosdir"] or i.count(".") == 0 or i.startswith("."): continue
		if i.split(".")[-1] == "minios": file_type, file_name, file_extension = "file", ".".join(i.split(".")[:-2]), i.split(".")[-2]
		elif i.split(".")[-1] == "miniosdir": file_type, file_name, file_extension = "directory", ".".join(i.split(".")[:-1]), i.split(".")[-2] if len(i.split(".")) > 2 else None
		else: file_type, file_name, file_extension = "unknown", "unknown", "unknown"
		items[i] = {"filename": file_name, "extension": file_extension, "type": file_type, "displayname": f"{file_name}.{file_extension}" if file_type == "file" else file_name}
	return items
