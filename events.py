import city_data as info, random as rng

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
	print(f"{"Panaszok:":<20} {"WIP"}")  
	print(info.Colors.HEADER, "-" * 40, info.Colors.ENDC)  


def list_citizens():
	print(f"{"ID":<10} {"Born":<10} {"Job":<10} {"HouseID":<10} \n{"-" * 45}")
	for Id,c in info.sim_data["citizens"].items():
		print(f"{Id:<10}{format(c)}")
def list_buildings():
	print(f"{"ID":<10} {"Épület neve":<10} {"Tipus":<10} {"Szolgáltatások":<10} \n{"-" * 45}")
	for Id,b in info.sim_data["buildings"].items():
		print(f"{Id:<10}{format(b)}")
def list_projects():
	print(info.sim_data["projects"])
	print(f"{"ID":<10} {"Start day":<10} {"Befejezéshez szükséges napok:":<10} \n{"-" * 45}")
	for Id,p in info.sim_data["projects"].items(): 
		print(f"{Id:<10}{p.start_date:<10}{p.finish_days:<10}")

#buildings
def build():
	buildings_choices = {bld.name: {"return_value":bld, "desc":f"Tipus: {bld.type}, Minőség: {bld.quality}"} for bld in info.buildings}
	new_building, _ = choice_input("Mit akarsz építeni:",buildings_choices)
	if not new_building: return None
	info.sim_data["projects"].update({info.make_id(info.sim_data["projects"]) :new_building})#Finish ID GIVER!!!
	print(f"Új projekt: {new_building.name},{new_building.type}",f"Befejezési idő: {new_building.finish_days} nap",sep="\n")

def upgrade_building():
	placed_builds = info.sim_data["buildings"]
	build_choices = {bld.name: {"return_value": bld,"desc":f"Tipus: {bld.type}, Minőség: {bld.quality}"} for bld in placed_builds}
	if len(placed_builds) <= 0: # no buildings
		print(f"{info.Colors.FAIL}-No buildings were found-{info.Colors.ENDC}")
		return None

	building_inp, _ = choice_input("Melyik épületet fejleszted:",build_choices)
	if not building_inp: return None
	building = placed_builds[building_inp]
	valid_upgs = {upg.name: {"return_value": upg.name, "desc":f"Ár: {upg.cost_M}, Hatások: {upg.effects}, Projekt idő: {upg.build_days} nap"} for upg in building.get_valid_upgs()}
	if len(valid_upgs) > 0:
		upg_inp, _ = choice_input("Megfizethető fejlesztések:", valid_upgs)
		if not upg_inp: return None
		new_upg = info.upgrades[upg_inp]
		new_upg.finish_dict = building.upgrades #when finished goes into the builds upg dict
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

#random events handling
def disaster():
	chances = [dis.chance for dis in info.disasters]
	dis = rng.choices(info.disasters, weights=chances)[0]
	if dis.name != "nincs katasztrófa": return None

#forduló_szimulálása (should be a city class.....)
def calcualte_happiness():
	const = info.sim_const
	service_req = const["serice_requirements"]
	happiness = 0
	service_rate = {}
	for Id,bld in info.sim_data["buildings"].items():
		for service in bld.services:
			if service not in service_rate.keys(): service_rate.update({service:0})
			service_rate[service] += float(bld.area//const["area_per_service"])*float(bld.quality/5)

	for key,req in service_req.items():
		if not service_req.get(key): 
			happiness *= 0.8
			info.sim_data["complaints"].update({"desc":f"Nincsen {key} szolgáltatás!","day":info.sim_data["day"]})
		else:
			service_happiness = min(req/service_req[key], len(service_req)/const["max_happiness"])
			if service_happiness < len(service_req)/const["max_happiness"]:
				info.sim_data["complaints"].update({"desc":f"Kevés a(z) {key} szolgáltatás! ({req/service_req[key]}/{len(service_req)/const["max_happiness"]})","day":info.sim_data["day"]})
			happiness += service_happiness


def next_round():
  #under 18 wont pay tax, based on happiness
	simulated_days = number_input("Hány napot akarsz leszimulálni?: ")
	const = info.sim_const
	data = info.sim_data
	projects = data["projects"]
	buildings = data["buildings"]
	citizens = data["citizens"]

	for i in range(simulated_days):
		new_disaster = disaster()
		data["happiness"] = calcualte_happiness()
		
		data["day"]+=1
		
		#updateing, citiznes, buildings
		for Id,bld in buildings.items():
			current_residents = [c for key,c in citizens.items() if c.houseID == Id]
			free_space = (bld.area // info.sim_const["area_for_citizen"]) - len(current_residents)

			for _ in range(free_space):
				#make job (0.1% cahnce to be jobless), FINISH, spktrum age (0,80)
				new_citizen = info.Citizen( _born=data["day"], _job="munkanélküli", _houseID=Id)
				citizens.update({info.make_id(citizens): new_citizen})
			bld.update()

		for Id,proj in projects.items():
			if not proj.finished:
				proj.check_done()

	#tax
		total_tax = 0
		for Id,c in citizens.items():
			#if over 18 assign job, if over 6 assign, DOIT
			if c.job and data["day"] - c.born > 18*365.25:
				data["currency_M"] += const["tax_per_citizen"]*(data["happiness"]/const["max_happiness"])
		
		print(f"{info.Colors.OKCYAN}Day {i+1} simulated.{info.Colors.ENDC}")
	show_reports()

#end
def exit_action():
  print(f"{info.Colors.FAIL}-megszakítva-{info.Colors.ENDC}")