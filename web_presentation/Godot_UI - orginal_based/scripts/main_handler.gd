extends Node2D

@onready var UI = $UserInterface

func _ready():
	Global.disaster.connect(func(huh):
		print("dail")
		if Data.user_data["currency_M"] <= 0:
			get_tree().reload_current_scene()
			Data.load_data()
	)


func _process(delta):
	pass

func build(building_info):
	if building_info.cost > Data.user_data["currency_M"]:
		UI.warn("Not enough money!")
		return
	Data.user_data["currency_M"] -=  building_info.cost
	var builds = Data.user_data["buildings"]
	builds[len(builds)] = building_info
	$Map.load_map()

func upg_building(building, upg):
	if upg.cost > Data.user_data["currency_M"]:
		UI.warn("Not enough money!")
		return
	Data.user_data["currency_M"] -=  upg.cost

func calculate_happiness() -> float:
	if Data.user_data["citizens"] <= 0:
		return 0

	var c = Data.sim_const
	var reqs = c["service_requirements"]
	var rates = {}
	var hap = 0.0

	for b in Data.user_data["buildings"].values():
		if b.finish_days <= 0:
			for s in b.services:
				rates[s] = rates.get(s, 0.0) + float(b.area / c["area_per_service"]) * (b.quality / 5.0)

	for s in reqs:
		var r = reqs[s]
		var max = c["max_happiness"] / reqs.size()
		var rate = rates.get(s, 0.0)
		var h = min(rate / r, 1.0) * max
		hap += h

		if rate <= 0.0:
			Data.user_data["complaints"].append({ "desc": "Nincsen %s szolgáltatás!" % s, "day": Data.user_data["day"] })
		elif h < max:
			Data.user_data["complaints"].append({ "desc": "Kevés a(z) %s szolgáltatás! (%.2f/%.2f)" % [s, rate, r], "day": Data.user_data["day"] })
	return hap



func random_disaster():
	var user_data = Data.user_data
	var chance = randi_range(0,100)
	if chance > 98:
		var disaster = Data.disasters.pick_random()
		var damaged_builds = []
		for bld in user_data["buildings"]:
			if randi_range(1,2) == 2:
				damaged_builds.append(bld)
		if len(damaged_builds) <= 0: return
		var fix_cost = Global.format_number(len(damaged_builds)*80)
		UI.action("Természeti katasztrófa: "+str(disaster.dst_name)+". Sérült épületek: "+str(len(damaged_builds)),"Instant javítás: "+fix_cost,"100 napos javítás")
		var action = await Global.disaster
		if action:
			user_data["currency_M"] -= len(damaged_builds)*80
		else:
			for e in damaged_builds:
				user_data["buildings"][e].finish_days += 100
			$Map.load_map()

func simulate_days(days):
	var user_data = Data.user_data
	for e in days:
		user_data["complaints"] = []
		user_data["day"] += 1
		user_data["happiness"] = calculate_happiness()
		var tax = snapped(0.05*(user_data["happiness"]/100),0.01)
		if user_data["happiness"] < 30:
			tax = -(30-user_data["happiness"])
		for citizen in range(user_data["citizens"]):
			user_data["currency_M"] += tax
		
		random_disaster()
		
		user_data["citizens"] = 0
		for bld_ID in user_data["buildings"]:
			if user_data["buildings"][bld_ID].finish_days > 0:
				user_data["buildings"][bld_ID].finish_days -= 1
			if user_data["buildings"][bld_ID].finish_days <= 0 and user_data["buildings"][bld_ID].type == "lakóház":
				for i in range(user_data["buildings"][bld_ID].area/30):
					user_data["citizens"] += 1
		
	$Map.load_map()
		
	
	if user_data["currency_M"] <= 0:
		UI.action("Csődbe mentél.","újra kezdés","újra kezdés")
		
