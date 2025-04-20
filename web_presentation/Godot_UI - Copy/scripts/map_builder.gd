extends GridContainer


@onready var build_sample = $UI_build_sample
@onready var UI = $"../UserInterface"

func _ready():
	pass # Replace with function body.

func _process(delta):
	pass

func building_click(buildID:int):
	var build = Data.user_data["buildings"][buildID]
	var action_panel = UI.find_child("ActionPanel")
	action_panel.find_child("bld_name").text = build.bld__name
	action_panel.find_child("bld_type").text = build.type
	action_panel.find_child("bld_area").text = str(build.area)
	action_panel.visible = true

func load_map():
	for ID in Data.user_data["buildings"].keys():
		var building = find_child(str(ID))
		if not building:
			building = build_sample.duplicate()
			building.pressed.connect(func():
				building_click(int(building.name)))
			add_child(building)
