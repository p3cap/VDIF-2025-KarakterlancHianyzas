import city_data as info, random as rng

#others
def format_number(amount):
    for unit in ["", "k", "M", "B", "T", "P", "E", "Z"]:
        if abs(amount) < 1000:
            return f"{amount:.2f}{unit}".rstrip("0").rstrip(".")
        amount /= 1000

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
	print(f"{"Egy körben eltelő napok száma:":<30} {info.sim_const["days_per_round"]}")
	print(f"{"Eltelt körök száma:":<30} {info.sim_data["day"]}")
	print(f"{"Max napok:":<30} {info.sim_data["day"]}")
	print(info.Colors.HEADER, "-" * 40, info.Colors.ENDC)  

def show_reports():
	currency_type = info.sim_const["currency_type"]
	print(info.Colors.HEADER, "-" * 12, "JELENTÉSEK", "-" * 12, info.Colors.ENDC)  
	print(f"{"Valuta:":<20} {format_number(info.sim_data["currency_M"])} {currency_type}")
	print(f"{"Boldogság:":<20} {format_number(info.sim_data["hapiness"])}%")
	print(f"{"Épületek:":<20} {format_number(len(info.sim_data["buildings"]))} db")
	print(f"{"Polgárok:":<20} {format_number(len(info.sim_data["citizens"]))} db")
	print(f"{"Panaszok:":<20} {"WIP"}")  
	print(info.Colors.HEADER, "-" * 40, info.Colors.ENDC)  


def list_citizens():
	print(f"{"ID":<5} {"Born":<6} {"Job":<20} {"HouseID":<8} \n{"-" * 45}")
	for key,c in info.sim_data["citizens"].items(): print(f"{c.ID:<5} {c.born:<6} {c.job:<20} {c.houseID:<8}")
def list_buildings():
	print(f"{"ID":<5} {"Born":<6} {"Job":<20} {"HouseID":<8} \n{"-" * 45}")
	for key,c in info.sim_data["buildings"].items(): print(f"{c.ID:<5} {c.born:<6} {c.job:<20} {c.houseID:<8}")
def list_projects():
	print(info.sim_data["projects"])
	print(f"{"ID":<5} {"Start day":<6} {"Time reamins":<20} {"building ID":<8} \n{"-" * 45}")
	for key,p in info.sim_data["projects"].items(): 
		print(f"{key:<5} {p.start_date:<6} {(info.sim_data["day"]-p.finish_days):<20} {"unassigned":<8}")#finish fromat date

#buildings
def build():
	buildings_choices = {bld.name: {"return_value":bld, "desc":f"Tipus: {bld.type}, Minőség: {bld.quality}"} for bld in info.buildings}
	new_building, _ = choice_input("Mit akarsz építeni:",buildings_choices)
	if not new_building: return None
	info.sim_data["projects"].update({0:new_building})#Finish ID GIVER!!!
	print(f"Új projekt: {new_building.name},{new_building.type}",f"Befejezési idő: {new_building.finish_days} nap",sep="\n")

def upgrade_building():
	placed_builds = info.sim_data["buildings"]
	build_choices = {bld.name: {"return_value": bld,"desc":f"Tipus: {bld.type}, Minőség: {bld.quality}"} for bld in placed_builds}
	if len(placed_builds) <= 0: 
		print(f"{info.Colors.FAIL}-No buildings were found-{info.Colors.ENDC}")
		return None
	shortcuts = {}
	for Id, blding in placed_builds.items(): 
		shortcuts.update( {blding.name: str(Id)} )#make id shortcuts

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
	for bld in info.sim_data["buildings"]:
		if bld.type not in service_rate.keys(): service_rate.update({bld.type:0})
		service_rate[bld.type] += float(bld.area//const["area_per_service"])*float(bld.quality/5)

	for key,req in service_req:
		if not service_req.get(key): happiness *= 0.2
		happiness += min(req/service_req[key], len(service_req)/const["max_happiness"])


def next_round():
  #under 18 wont pay tax, based on happiness
	simulated_days = number_input("Hány napot akarsz leszimulálni?: ")
	const = info.sim_const
	data = info.sim_data
	projects = data["projects"]
	buildings = data["buildings"]
	citizens = data["citizens"]
	new_disaster = disaster()
	
	data["day"]+=simulated_days
	
	#updateing, citiznes, buildings
	print(f"{info.Colors.OKCYAN}Lakosok kalkulálása...{info.Colors.ENDC}")
	for bld in buildings:
		current_residents = [c for c in citizens if c.houseID == bld.ID]
		free_space = (bld.area // 30) - len(current_residents)

		for _ in free_space:
			new_id = max(c.ID for c in citizens) + 1 if citizens else 1
			#make job (0.1% cahnce to be jobless), FINISH, spktrum age (0,80)
			new_citizen = info.Citizen(_ID=new_id, _born=data["day"], _job="munkanélküli", _houseID=bld.ID)
			citizens.append(new_citizen)
		bld.update()

	print(f"{info.Colors.OKCYAN}Projektek engedélyezése...{info.Colors.ENDC}")
	for Id,proj in projects.items():
		if not proj.finished:
			proj.check_done()

#tax
	print(f"{info.Colors.OKCYAN}Adók begyűjtése...{info.Colors.ENDC}")
	for c in citizens:
		#if over 18 assign job, if over 6 assign
		if c.job and data["day"] - c.born > 18*365.25:
			data["currency_M"] += const["tax_per_citizen"]
	show_reports()

#end
def exit_action():
  print(f"{info.Colors.FAIL}-megszakítva-{info.Colors.ENDC}")