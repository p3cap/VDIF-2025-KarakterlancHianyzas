extends Node

signal disaster

var selected = null
var zoom = 100

func format_number(amount):
	var units = ["M", "B", "T", "P", "E", "Z"]
	var i = 0
	while abs(amount) >= 1000.0 and i < units.size() - 1:
		amount /= 1000.0
		i += 1
	return "%.2f%s" % [amount, units[i]]
