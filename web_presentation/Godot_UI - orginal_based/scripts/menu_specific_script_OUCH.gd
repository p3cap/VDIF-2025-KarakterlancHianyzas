extends Panel

@onready var grid = $Build_menu/Scroll/Grid
@onready var main = $"../.."


func _ready():
	$Report_menu/Back.pressed.connect(func():
		$Report_menu.visible = false)
	$Report.pressed.connect(func():
		$Report_menu.visible = true)
	$Build.pressed.connect(func():
		$Build_menu.visible = true)
	$Build_menu/Back.pressed.connect(func():
		$Build_menu.visible = false)
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

func _process(delta):
	var user_data = Data.user_data
	$Report_menu/builds.text = str(len(user_data["buildings"]))+"db"
	
	$Report_menu/complaints.text = str(len(user_data["complaints"]))+"db"
	for e in $Report_menu/Scroll/Grid.get_children():
		if e != $Report_menu/Scroll/Grid/sample: e.queue_free()

	for comp in user_data["complaints"]:
		var new = $Report_menu/Scroll/Grid/sample.duplicate()
		new.name = comp["desc"]
		new.text = comp["desc"]
		new.visible = true
		$Report_menu/Scroll/Grid.add_child(new)
