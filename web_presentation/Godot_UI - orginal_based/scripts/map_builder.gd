extends GridContainer


@onready var build_sample = $UI_build_sample
@onready var UI = $"../UserInterface"
@onready var action_panel = UI.find_child("ActionPanel")

func _ready():
	load_map()

func _process(delta):
	pass

func building_click(buildID:int):
	var build = Data.user_data["buildings"].get(str(buildID))
	Global.selected = build if Global.selected != build else null

	$"../UserInterface".toggle_info(false if Global.selected else true)


func load_map():
	for e in get_children():
		if e != $UI_build_sample: e.queue_free()
	var user_data = Data.user_data
	for ID in user_data["buildings"].keys():
		var building = find_child(str(ID))
		var bld_data = user_data["buildings"][ID]
		if not building:
			build_sample.find_child("build_name").text = bld_data.bld_name
			build_sample.find_child("build_name").tooltip_text = "ID: "+str(ID)
			building = build_sample.duplicate()
		
		var icon = load("res://Assets/building_icons/"+bld_data.get("type")+".png") if bld_data.finish_days == 0 else load("res://Assets/building_icons/build_project.png")
		building.texture_normal = icon
		var upg_conatiner = building.find_child("upgrades")
		var build_time_label = upg_conatiner.find_child("Build_time")
		if bld_data.finish_days > 0:
			build_time_label.visible = true
			build_time_label.text = str(bld_data.finish_days)+":00:00"
		else:
			var sample = upg_conatiner.find_child("UI_upg_sample")
			build_time_label.visible = false
			for upg in bld_data.upgrades:
				var new_upg:TextureRect = sample.duplicate()
				new_upg.texture = load("res://Assets/upg_icons/"+upg.name+".png")
				new_upg.tooltip_text = upg.name
				upg_conatiner.add_child(new_upg)
				
		add_child(building)
		building.name = str(ID)
		building.pressed.connect(func():
			building_click(int(building.name))
			)
		building.visible = true
