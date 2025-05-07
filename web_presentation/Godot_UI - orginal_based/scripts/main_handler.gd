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
	var chance = randi_range(0,100)
	if chance > 98:
		var disaster = Data.disasters.pick_random()
		var damaged_builds = []
		for bld in user_data["buildings"]:
			if randi_range(1,5) == 5:
				damaged_builds.append(bld)
		UI.action("Természeti katasztrófa: "+str(disaster.dst_name)+". Javási költség: "+Global.format_number(len(damaged_builds)*1000))
		var action = await Global.disaster
		if action:
			user_data["currency_M"] -= len(damaged_builds)*1000
		else:
			for e in user_data["buildings"]:
				if e in damaged_builds:
					user_data["buildings"][e].finish_days += 200

func simulate_days(days):
	var user_data = Data.user_data
	for e in days:
		user_data["day"] += 1
		var tax = snapped(Data.sim_const["tax_payer_spektrum"][1]*(user_data["happiness"]/100),0.1)
		if user_data["happiness"] < 30:
			tax = -100
		for citizen in range(user_data["citizens"]):
			user_data["currency_M"] += tax
		
		random_disaster()
		
		user_data["citizens"] = 0
		for bld_ID in user_data["buildings"]:
			user_data["buildings"][bld_ID].finish_days -= 1
			if user_data["buildings"][bld_ID].finish_days <= 0:
				for i in range(user_data["buildings"][bld_ID].area/30):
					user_data["citizens"] += 1
		
	$Map.load_map()
		
		
