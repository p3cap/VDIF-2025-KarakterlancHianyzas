extends Node2D

@onready var UI = $UserInterface

func _ready():
	pass # Replace with function body.


func _process(delta):
	pass

func build(building_info):
	if building_info.cost > Data.user_data["currency_M"]:
		UI.warn("Not enough money!")
		return
	Data.user_data["currency_M"] -=  building_info.cost
	var builds = Data.user_data["buildings"]
	builds.merge({str(len(builds)-1):building_info})
	$Map.load_map()

func upg_building(building, upg):
	if upg.cost > Data.user_data["currency_M"]:
		UI.warn("Not enough money!")
		return
	Data.user_data["currency_M"] -=  upg.cost

func random_disaster():
	var user_data = Data.user_data
	var chance = randi_range(0,1000)
	if chance > 990:
		var disaster = Data.disasters.pick_random()
		var damaged_builds = []
		for bld in user_data["buildings"]:
			if randi_range(1,5) == 5:
				damaged_builds.append(bld)
		var action = UI.action("Természeti katasztrófa: "+str(disaster.name),len(damaged_builds))
		if action:
			pass
		else:
			for e in user_data["buildings"]:
				if e in damaged_builds:
					e.area = 0

func simulate_days(days):
	var user_data = Data.user_data
	for e in days:
		user_data["day"] += 1
		for citizen in user_data["citizens"]:
			user_data["currncy_M"] += Data.sim_const["tax_payer_spektrum"][1]
		
		random_disaster()
		
	for bld in user_data["buildings"]:
		bld.finish_days -= days
		
	$Map.load_map()
		
		
