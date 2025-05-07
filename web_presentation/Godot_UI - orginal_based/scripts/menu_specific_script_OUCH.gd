extends Panel

@onready var grid = $Build_menu/Scroll/Grid
@onready var main = $"../.."


func _ready():
	$Build.pressed.connect(func():
		$Build_menu.visible = true)
	$Build_menu/Back.pressed.connect(func():
		$Build_menu.visible = false)
	$Report.pressed.connect(func():
		$"../Report/Anim".play_backwards("close"))
	$"../Report/Back".pressed.connect(func():
		$"../Report/Anim".play("close"))
	$Simulate_1.pressed.connect(func():
		main.simulate_days(1))
	$Simulate_10.pressed.connect(func():
		main.simulate_days(10))
	
	for bld in Data.buildings:
		var new_sample = $Build_menu/Scroll/Grid/UI_building_sample.duplicate()
		new_sample.texture_normal = load("res://Assets/building_icons/"+bld.get("type")+".png")
		for e in new_sample.get_children():
			if bld.get(e.name):
				e.text = str(bld.get(e.name))+e.text
		new_sample.pressed.connect(func(): 
			main.build(bld)
			)
		new_sample.visible = true
		grid.add_child(new_sample)
