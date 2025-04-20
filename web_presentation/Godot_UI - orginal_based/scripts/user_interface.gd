extends CanvasLayer

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
	$Values/currency.text = str(Global.format_number(Data.user_data["currency_M"]))+Global.sim_const["currency_type"]
	$Values/happiness.text = str(Data.user_data["happiness"])+"%"
	$Values/citizens.text = str(len(Data.user_data["citizens"]))
	$Values/day.text = str(Data.user_data["day"])+"."
	
	if not Global.selected: return

	
