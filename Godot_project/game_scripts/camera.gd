extends Camera2D

var zoom_speed = 0.1
var min_zoom = 0.5
var max_zoom = 2.0

var is_dragging = false
var last_mouse_position = Vector2.ZERO

func _input(event):
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_WHEEL_UP and zoom.x > min_zoom:
		zoom -= Vector2(zoom_speed, zoom_speed)
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_WHEEL_DOWN and zoom.x < max_zoom:
		zoom += Vector2(zoom_speed, zoom_speed)
	
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_MIDDLE:
			if event.pressed:
				is_dragging = true
				last_mouse_position = get_global_mouse_position()
			else:
				is_dragging = false
	elif event is InputEventMouseMotion and is_dragging:
		var mouse_delta = get_global_mouse_position() - last_mouse_position
		position -= mouse_delta
		last_mouse_position = get_global_mouse_position()
