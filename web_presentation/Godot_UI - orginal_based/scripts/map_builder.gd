extends GridContainer


@onready var build_sample = $UI_build_sample
@onready var UI = $"../UserInterface"
@onready var action_panel = UI.find_child("ActionPanel")

func _ready():
	load_map()

func _process(delta):
	pass

func building_click(buildID):
	var build = Data.user_data["buildings"].get(int(buildID))
	Global.selected = build
	print(build,Data.user_data["buildings"],buildID)

func load_map():
	for e in get_children():
		if e != $UI_build_sample: e.queue_free()
	var user_data = Data.user_data
	for ID in user_data["buildings"].keys():
		var building = build_sample.duplicate()
		var bld_data = user_data["buildings"][ID]
		building.find_child("build_name", true, false).text = bld_data.bld_name
		building.find_child("build_name", true, false).tooltip_text = "ID: "+str(ID)
	
		var icon = load("res://Assets/building_icons/"+bld_data.get("type")+".png") if bld_data.finish_days <= 0 else load("res://Assets/building_icons/build_project.png")
		building.texture_normal = icon
		var upg_conatiner = building.find_child("upgrades", true, false)
		var build_time_label = upg_conatiner.find_child("Build_time", true, false)
		if bld_data.finish_days > 0:
			build_time_label.visible = true
			build_time_label.text = str(bld_data.finish_days)+":00:00"
		else:
			"""var sample = upg_conatiner.find_child("UI_upg_sample", true, false)"""
			build_time_label.visible = false
			"""for upg in bld_data.services:
				var new_upg:TextureRect = sample.duplicate()
				new_upg.texture = load("res://Assets/upg_icons/upg_placeholder.png")
				new_upg.tooltip_text = upg
				upg_conatiner.add_child(new_upg)"""
				
		add_child(building)
		building.name = str(ID)
		building.pressed.connect(func():
			building_click(building.find_child("build_name", true, false).tooltip_text)
			)
		building.visible = true
