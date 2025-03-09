@tool
extends Area2D
class_name building

@onready var shape = $Shape
@onready var collision = $Collision
@onready var label = $Label

enum type {
	ROAD,
	PANEL
}

func _ready():
	child_entered_tree.connect(func():
		for e in get_children():
			if e is ColorRect:
				pass
				#when clicked move it
		)

func _process(delta):
	var children = get_children()
	if len(children) > 4: #has at least 1 Dot
		var points:PackedVector2Array = []
		var label_pos = Vector2.ZERO
		for dot in children:
			if dot is ColorRect:
				var dot_pos = dot.position+Vector2(dot.size.x/2,dot.size.y/2)
				points.append(dot_pos)
				label_pos += dot_pos
		label.position = label_pos / Vector2(len(children),len(children)) #+1 for zero
		label.text = name
		shape.polygon = points
		collision.polygon = points
