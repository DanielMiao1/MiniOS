"""
System/calculations.py
Performs mathematical calculations
Made by Daniel M
"""

hex_keys = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}

rgb_keys = {str(y).lower(): str(x) for x, y in hex_keys.items()}

def getRgbFromHex(hex_color: str) -> list:
	for i in ["a", "b", "c", "d", "e", "f"]: hex_color = hex_color.replace(i, rgb_keys[i])
	return [int(list(hex_color)[0]) * 16 + int(list(hex_color)[1]), int(list(hex_color)[2]) * 16 + int(list(hex_color)[3]), int(list(hex_color)[4]) * 16 + int(list(hex_color)[5])]

def getHexFromRgb(rgb_value: list) -> str:
	return str(hex_keys[int(rgb_value[0]) // 16]) + str(hex_keys[((int(rgb_value[0]) / 16) - (int(rgb_value[0]) // 16)) * 16]) + str(hex_keys[int(rgb_value[1]) // 16]) + str(hex_keys[((int(rgb_value[1]) / 16) - (int(rgb_value[1]) // 16)) * 16]) + str(hex_keys[int(rgb_value[2]) // 16]) + str(hex_keys[((int(rgb_value[2]) / 16) - (int(rgb_value[2]) // 16)) * 16])

def getAdjustedColor(color: str) -> str:
	"""Gets the inverse of the given color"""
	return "#" + getHexFromRgb([128 - int(getRgbFromHex(color)[0]), 128 - int(getRgbFromHex(color)[1]), 128 - int(getRgbFromHex(color)[2])])
