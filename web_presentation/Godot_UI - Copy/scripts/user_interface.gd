extends CanvasLayer


# Called when the node enters the scene tree for the first time.
func _ready():
	for e in get_children():
		var btn = e.find_child("close_button")
		if not btn: return
		
		btn.pressed.connect(func():
			var anim = e.find_child("Anim")
			if btn.button_pressed and anim:
				anim.play_backwards("close")
			elif anim:
				anim.play("close")
			)

func _process(delta):
	pass
