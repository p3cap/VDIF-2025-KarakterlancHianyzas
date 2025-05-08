extends CanvasLayer

@onready var main = $".."

func _ready():
	$Warning/Accept.pressed.connect(func():
		Global.disaster.emit(true)
		)
	$Warning/Decline.pressed.connect(func():
		Global.disaster.emit(false)
		)
	$Cam/out.pressed.connect(func():
		Global.zoom *= 1.1
		)
	$Cam/in.pressed.connect(func():
		Global.zoom *= 0.9
		)
	
	for e in get_children():
		var btn = e.find_child("close_button")
		if btn:
			btn.pressed.connect(func():
				var anim = e.find_child("Anim")
				if btn.button_pressed and anim:
					anim.play_backwards("close")
				elif anim:
					anim.play("close")
				)

func warn(msg):
	$Warning/msg.text = msg
	$Warning/Anim.play("warn")

func action(msg):
	$Warning/msg.text = msg
	$Warning/Anim.play("event")
	await Global.disaster
	$Warning/Anim.play_backwards("event")
	
	

func _process(delta):
	$Values/currency.text = Global.format_number(Data.user_data["currency_M"])+" "+Data.sim_const["currency_type"]
	$Values/happiness.text = str(Data.user_data["happiness"])+"%"
	$Values/citizens.text = str(Data.user_data["citizens"])
	$Values/day.text = str(Data.user_data["day"])+"."
	
	$Cam/zoom.text = str(snapped(Global.zoom,0.1))+"%"
	
	if not Global.selected: return
	$Info/bld_name.text = Global.selected.bld_name
	$Info/_type.text = Global.selected.type
	$Info/area.text = str(Global.selected.area)+"m2"
	$Info/people.text = str(snapped(Global.selected.area/30,1))
	$Info/quality.text = str(Global.selected.quality)+"/5"
	
	var upg_continer = $Info/Scroll/Grid
	var upg_sample = $Info/Scroll/Grid/UI_building_sample
	for upg in Data.upgrades:
		upg_sample.find_child("_name").text = upg.upg_name
		upg_sample.find_child("price_M").text = str(upg.cost)+" m2"
		var new_upg = upg_sample.duplicate()
		$Info/Scroll/Grid.add_child(new_upg)
		new_upg.pressed.connect(func():
			main.upg_build(Global.selected,upg)
			)
		new_upg.visible = true
	
