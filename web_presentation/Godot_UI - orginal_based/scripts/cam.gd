extends Camera2D

var dragging := false
var last_mouse_pos := Vector2.ZERO

func _input(event):
	if event is InputEventMouseButton:
		if event.button_index in [MOUSE_BUTTON_LEFT, MOUSE_BUTTON_MIDDLE]:
			dragging = event.pressed
			last_mouse_pos = get_viewport().get_mouse_position()

		elif event.button_index == MOUSE_BUTTON_WHEEL_UP:
			zoom *= 1.1
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			zoom *= 0.9

	elif event is InputEventMouseMotion and dragging:
		var current_mouse_pos = get_viewport().get_mouse_position()
		var delta = last_mouse_pos - current_mouse_pos
		position += delta/zoom.y
		last_mouse_pos = current_mouse_pos
