extends Camera2D

var dragging := false
var last_mouse_pos := Vector2.ZERO

func _unhandled_input(event):
	if event is InputEventMouseButton:
		if event.button_index in [MOUSE_BUTTON_LEFT, MOUSE_BUTTON_MIDDLE]:
			dragging = event.pressed
			last_mouse_pos = get_viewport().get_mouse_position()

	elif event is InputEventMouseMotion and dragging:
		var current_mouse_pos = get_viewport().get_mouse_position()
		var delta = last_mouse_pos - current_mouse_pos
		position += delta/zoom.y
		last_mouse_pos = current_mouse_pos

func _process(delta):
	zoom = Vector2(Global.zoom/100,Global.zoom/100)
	if Input.is_action_just_pressed("zoom_in"):
		Global.zoom *= 1.2
	elif Input.is_action_just_pressed("zoom_out"):
		Global.zoom *= 0.8
