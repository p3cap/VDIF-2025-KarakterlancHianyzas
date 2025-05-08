extends Panel

func _ready():
	$enter.pressed.connect(func():
		$Button.pause()
		$Anim.play("enter")
		)
