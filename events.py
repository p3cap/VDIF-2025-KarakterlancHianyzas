import city_data as info, random as rng, log_export, sys

#input, formatting
def format_number(amount):
    for unit in ["M", "B", "T", "P", "E", "Z"]:
        if abs(amount) < 1000:
            return f"{amount:.2f}{unit}".rstrip("0").rstrip(".")
        amount /= 1000

def format_date(days):
	year = info.sim_data["start_year"] + (days // 365)
	day_of_year = days % 365
	return f"{year} - Day {day_of_year}"

def number_input(prompt:str):
	inp = input ("[number] "+prompt)
	while not inp.isnumeric(): inp = input ("[number] "+prompt)
	return int(inp)

def choice_input(prompt:str, choices:dict): #dict: "choice name": {"return_value":, "desc":}
	shortcuts = {str(i): key for i, key in enumerate(choices)}
	shortcut_ext=shortcuts.copy()
	shortcut_ext.update({"h": "help", "x": "exit"})
	options = ", ".join([f"{act} [{shortcut}]" for shortcut, act in shortcut_ext.items()])

	while True:
		inp = input(f"\n{info.Colors.BOLD}Opciók: {options}{info.Colors.ENDC}\n{prompt}").lower()
		if inp in ["x", "exit"]:#exit
			exit_action()
			return None, None
		elif inp in ["h", "help"]: #help
			for shortcut, act in shortcuts.items():
				print(f"{act} [{shortcut}]: {choices[act]["desc"]}")
		
		elif inp in choices: return choices[inp]["return_value"], choices[inp]["desc"] #valid
		elif inp in shortcuts: return choices[shortcuts[inp]]["return_value"], choices[shortcuts[inp]]["desc"] #valid shortcut
		else: print(f"{info.Colors.WARNING}Invalid opció{info.Colors.ENDC}")

#lekérdezések
def show_info():
	currency_type = info.sim_const["currency_type"]
	print(info.Colors.HEADER, "-" * 15, "INFO", "-" * 15, info.Colors.ENDC)  
	print(f"{"Maximum nap:":<30} {info.sim_const["max_days"]}")
	print(f"{"Eltelt napok száma:":<30} {info.sim_data["day"]}")
	print(info.Colors.HEADER, "-" * 40, info.Colors.ENDC)  

def show_reports():
	currency_type = info.sim_const["currency_type"]
	print(info.Colors.HEADER, "-" * 12, "JELENTÉSEK", "-" * 12, info.Colors.ENDC)  
	print(f"{"Valuta:":<20} {format_number(info.sim_data["currency_M"])} {currency_type}")
	print(f"{"Boldogság:":<20} {info.sim_data["happiness"]}%")
	print(f"{"Épületek:":<20} {len(info.sim_data["buildings"])} db")
	print(f"{"Polgárok:":<20} {len(info.sim_data["citizens"])} db")
	print("Panaszok:")
	for e in info.sim_data["complaints"]: print(e["desc"])  
	print(info.Colors.HEADER, "-" * 40, info.Colors.ENDC)  


def list_citizens():
	print(f"{"ID":<20} {"Born":<20} {"Job":<20} {"HouseID":<20} \n{"-" * 90}")
	for Id,c in info.sim_data["citizens"].items():
		print(f"{Id:<20}{format(c)}")
def list_buildings():
	print(f"{"ID":<20} {"Épület neve":<20} {"Tipus":<20} {"Szolgáltatások":<20} \n{"-" * 90}")
	for Id,b in info.sim_data["buildings"].items():
		print(f"{Id:<20}{format(b)}")
def list_projects():
	print(info.sim_data["projects"])
	print(f"{"ID":<20} {"Projekt neve:":<20} {"Befejezéshez szükséges napok:":<20} \n{"-" * 90}")
	for Id,p in info.sim_data["projects"].items(): 
		print(f"{Id:<20}{p.name:<20}{p.finish_days-(p.start_date-info.sim_data["day"]):<20}")

#buildings
def build():
	buildings_choices = {bld.name: {"return_value":bld, "desc":f"Tipus: {bld.type}, Ár: {format_number(bld.cost)}{info.sim_const["currency_type"]}"} for bld in info.buildings}
	new_building, _ = choice_input("Mit akarsz építeni:",buildings_choices)
	if not new_building: return None
	info.sim_data["projects"].update({info.make_id(info.sim_data["projects"]) :new_building})
	info.sim_data["currency_M"] -= new_building.cost
	print(f"Új projekt: {new_building.name},{new_building.type}",f"Befejezési idő: {new_building.finish_days} nap",sep="\n")
	print(f"Megmaradt valuta: {format_number(info.sim_data["currency_M"])}")

def upgrade_building():
	placed_builds = info.sim_data["buildings"]
	build_choices = {bld.name: {"return_value": bld,"desc":f"ID:{Id}{format(bld)}"} for Id,bld in placed_builds.items()}
	if len(placed_builds) <= 0: # no buildings
		print(f"{info.Colors.FAIL}-Nincsen fejleszthető épület a városban-{info.Colors.ENDC}")
		return None

	building_inp, _ = choice_input("Melyik épületet fejleszted:",build_choices)
	if not building_inp: return None
	valid_upgs = {upg.name: {"return_value": upg, "desc":f"Ár: {upg.cost_M}, Hatások: {upg.effects}, Projekt idő: {upg.build_days} nap"} for upg in building_inp.get_valid_upgs()}
	if len(valid_upgs) > 0:
		upg_inp, _ = choice_input("Megfizethető fejlesztések:", valid_upgs)
		if not upg_inp: return None
		new_upg = info.upgrades[upg_inp]
		new_upg.finish_dict = building_inp.services #when finished goes into the builds upg dict
		info.sim_data["currency_M"] -= new_upg.cost
		print(f"Új projekt: {new_upg.name},{new_upg.type}",f"Befejezési idő: {new_upg.finish_days} nap",sep="\n")
		print(f"Megmaradt valuta: {format_number(info.sim_data["currency_M"])}")
	else:
		print("Nincsenek elérhető fejlesztések ehhez az épülethez.")
		return None

def custom_building():
	info.buildings.append(info.Building(
		_cost_M=number_input("Épület ára (Milliókba): "),
		_area=number_input("Épület területe (m2-be): "),
		_stories=number_input("Emeletek száma: "),
		_reliability=number_input("Megbízhatósági érték (0-100): "),
		_type=choice_input("Épület fajtája: ", {e:{"return_value":e,"desc":"Épület típus"} for e in info.Building.building_types})[0] or info.Building.building_types[0]
	))
	#add services while true input

#random events handling
def disaster():
	chances = [dis.chance for dis in info.disasters]
	dis = rng.choices(info.disasters, weights=chances)[0]
	if dis.name != "nincs katasztrófa": return dis
	else: return None

#forduló_szimulálása (should be a city class.....)
def calculate_happiness():
	if len(info.sim_data["citizens"]) < 1: return 100
	const = info.sim_const
	service_req = const["service_requirements"]
	happiness = 0
	service_rate = {}
	for Id, bld in info.sim_data["buildings"].items():
		for service in bld.services:
			if service not in service_rate.keys():
				service_rate.update({service: 0})
			service_rate[service] += float(bld.area // const["area_per_service"]) * float(bld.quality / 5)

	for key, req in service_req.items():
		if not service_rate.get(key): 
			happiness *= 0.5
			info.sim_data["complaints"].append({"desc": f"Nincsen {key} szolgáltatás!", "day": info.sim_data["day"]})
		else:
			service_happiness = min(service_rate[key] / req, const["max_happiness"] / len(service_req))
			if service_happiness < const["max_happiness"] / len(service_req):
				info.sim_data["complaints"].append({"desc": f"Kevés a(z) {key} szolgáltatás! ({service_rate[key]}/{req})", "day": info.sim_data["day"]})
			happiness += service_happiness
	return happiness


def next_round():
  #under 18 wont pay tax, based on happiness
	simulated_days = number_input("Hány napot akarsz leszimulálni?: ")
	const = info.sim_const
	data = info.sim_data

	for i in range(simulated_days):
		projects = data["projects"]
		buildings = data["buildings"]
		citizens = data["citizens"]
		info.sim_data["complaints"] = []
		data["day"]+=1
		new_disaster = disaster()
		if new_disaster:
			dis_info = new_disaster.activate()
			print(f"{info.Colors.WARNING}Természeti katasztrófa történt: {new_disaster.name}, méret:{dis_info['size']}")
			print(f"Érintett épületek száma: {len(dis_info['damaged_builds'])} ,kár mennyisége: {format_number(dis_info['repair_cost_M'])}{info.sim_const['currency_type']}")
			damaged_buildings_desc = ", ".join(f"{Id}: {info.sim_data['buildings'][Id].name}" for Id in dis_info["damaged_builds"])
			if choice_input("Megjavítod?", {"igen": {"return_value": True, "desc": damaged_buildings_desc}}): 
				new_disaster.repair(dis_info)
				print(f"Megmaradt valuta: {format_number(info.sim_data["currency_M"])}")
		#updating, citiznes, buildings
		for Id,bld in buildings.items():
			current_residents = [c for key,c in citizens.items() if c.houseID == Id]
			free_space = (bld.area // info.sim_const["area_for_citizen"]) - len(current_residents)
			for _ in range(free_space):
				new_citizen = info.Citizen(_houseID=Id)
				new_citizen.assign_job()
				citizens.update({info.make_id(citizens): new_citizen})

		for Id,proj in projects.items(): #some reason citizens wont get added
			if not proj.finished:
				if proj.check_done(): #it will aslo automatically put the project into the right data dict
					del projects[Id]
		#tax
		data["happiness"] = calculate_happiness()
		total_tax = 0
		for Id,c in citizens.items():
			if c.job not in const["no_tax_jobs"]:
				tax = const["tax_per_citizen"]*(data["happiness"]/const["max_happiness"])
				data["currency_M"] += tax
				total_tax += tax
		
		print(f"{info.Colors.OKCYAN}Day {i+1} simulated.{info.Colors.ENDC}")
		print(f"{info.Colors.OKCYAN}	Adó bevétel: {total_tax}{info.sim_const["currency_type"]}{info.Colors.ENDC}")
		print(f"{info.Colors.OKCYAN}	Panaszok száma: {len(info.sim_data["complaints"])}db{info.Colors.ENDC}")
	show_reports()

#end
def exit_action():
  print(f"{info.Colors.FAIL}-megszakítva-{info.Colors.ENDC}")

def checkEnd():
	if info.sim_data["happiness"] < info.sim_const["min_happiness"]: 
		return True
	elif info.sim_data["currency_M"] <= 0: 
		return True
	return False

def end_simulation():
	log_export.export_city()
	print(f"{info.Colors.FAIL}SIMULATION OVER, file saved")
	sys.exit()