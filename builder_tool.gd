@tool
extends Node2D

@onready var line = $Line2D

func _process(delta):
	print("Wjat")
	if len(get_children()) > 2:
		var points:PackedVector2Array = []
		var children = get_children()
		for e in children:
			if e is ColorRect:
				points.append(e.position)
		points.append(children[0].position)
		line.points = points
