import city_data as info, random

def disaster():
	chances = [info.disaster.chance for info.disaster in info.disasters.values()]
	dis = random.choices(list(info.disasters.keys()), weights=chances)[0]
	if dis != "nincs katasztrófa":
		return dis

print(disaster())