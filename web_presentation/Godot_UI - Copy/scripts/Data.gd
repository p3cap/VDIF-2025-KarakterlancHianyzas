extends Node

var default_data = {
	"happiness": 30,
	"currency_M": 100000,
	"buildings": {"0":Global.buildings[0]},
	"citizens": {},
	"projects": {},
	"complaints": [],
	"start_year": 2025,
	"day": 0,
}

var user_data := {}

var save_path := "user://save_data.json"

func _ready():
	load_data()

func load_data():
	if FileAccess.file_exists(save_path):
		var file = FileAccess.open(save_path, FileAccess.READ)
		user_data = JSON.parse_string(file.get_as_text())
	else:
		user_data = default_data.duplicate(true)
		save_data()

func save_data():
	var file = FileAccess.open(save_path, FileAccess.WRITE)
	file.store_string(JSON.stringify(user_data))
