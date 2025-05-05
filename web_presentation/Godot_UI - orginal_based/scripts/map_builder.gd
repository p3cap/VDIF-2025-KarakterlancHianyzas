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
			var icon = load("res://Assets/building_icons/"+bld_data.get("type")+".png")
			building = build_sample.duplicate()
			building.texture_normal = icon
			add_child(building)
			building.name = str(ID)
			building.pressed.connect(func():
				building_click(int(building.name))
				)
			building.visible = true
