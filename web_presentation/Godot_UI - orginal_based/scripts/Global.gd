extends Node

var selected = null

func format_number(amount):
	for unit in ["M", "B", "T", "P", "E", "Z"]:
		if abs(amount) < 1000:
			return str(amount)+unit
		amount /= 1000
