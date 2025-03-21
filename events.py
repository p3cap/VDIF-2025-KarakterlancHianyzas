import city_data as info, random

#others
def format_number(amount):
    for unit in ["", "k", "M", "B", "T", "P", "E", "Z"]:
        if abs(amount) < 1000:
            return f"{amount:.2f}{unit}".rstrip('0').rstrip('.')
        amount /= 1000

def foolproof_input(prompt, choices, shortcuts=None):
	if not shortcuts: shortcuts = {key[0]: key for key in choices.keys()}  # Shortcut (first letter)
	shortcut_ext=shortcuts.copy()  # Add help and exit shortcuts
	shortcut_ext.update({"h": "help", "x": "exit"})
	options = ', '.join([f"{act} [{shortcut}]" for shortcut, act in shortcut_ext.items()])
	
	while True:
		inp = input(f"\n{info.Colors.BOLD}Opciók: {options}{info.Colors.ENDC}\n{prompt}").lower()
		if inp in ["x", "exit"]:  # Exit
			exit_action()
			return None
		elif inp in ["h", "help"]:  # Help
			for shortcut, act in shortcuts.items():
				value = choices[act]
				description = value[1] if isinstance(value, list) else value["desc"]
				print(f"{act} [{shortcut}]: {description}")
		
		elif inp in choices: return inp # Valid choice
		elif inp in shortcuts: return shortcuts[inp] #valid shortcut
		else: print(f"{info.Colors.WARNING}Please choose one of the options{info.Colors.ENDC}")  # Invalid choice

#választható dologok
def show_info():
	currency_type = info.sim_const["currency_type"]
	print(info.Colors.HEADER,  "-"*10,"info","-"*10  ,info.Colors.ENDC) #line
	print("Maximum nap:",info.sim_const["max_days"])
	print("Egy körben eltelő napok száma:",info.sim_const["days_per_round"])
	print("Eltelt körök száma:",info.sim_data["round"],f"({info.sim_data["round"]*info.sim_const["days_per_round"]}nap)")
	print("Hátralévő körök száma:",info.sim_const["max_days"]//info.sim_const["days_per_round"]-info.sim_data["round"])
	print(info.Colors.HEADER,  "-"*26  ,info.Colors.ENDC) #line

def show_reports():
	currency_type = info.sim_const["currency_type"]
	print(info.Colors.HEADER,  "-"*7,"jelentések","-"*7  ,info.Colors.ENDC) #line
	print("Valuta:",format_number(info.sim_data["currency_M"]),currency_type)
	print(f"Boldogság: {format_number(info.sim_data["hapiness"])}%")
	print("Épületek(db):",format_number(len(info.sim_data["buildings"])),"db")
	print("Polgárok(db):",format_number(len(info.sim_data["citizens"])),"db")
	print("Adó bevétel:"     )#WIP
	print("Panaszok:"        )#WIP
	print(info.Colors.HEADER,  "-"*26  ,info.Colors.ENDC) #line

def build():
	new_building = foolproof_input("Mit akarsz építeni:",info.buildings)
	if new_building:
		new_building = info.buildings[new_building]
		new_building.name = input("Épület neve: ") or info.buildings
		info.sim_data["buildings"].update({str(len(info.sim_data["buildings"])): new_building})
		print("added",new_building.type,new_building.name)

def upgrade_building(): #NOT WORKING YET!!!!!
	placed_builds = info.sim_data["buildings"]
	build_choices = {}
	for key in placed_builds: build_choices.update({key: [None, placed_builds[key].type]}) #adds desc info, instea do full func, but it will still retuen the right ID
	if len(placed_builds) <= 0: 
		print(f"{info.Colors.FAIL}-No buildings were found-{info.Colors.ENDC}")
		return None
	shortcuts = {}
	for Id, blding in placed_builds.items(): 
		shortcuts.update( {blding.name: str(Id)} )#make id shortcuts

	building_inp = foolproof_input("Melyik épületet fejleszted (ID):",build_choices,shortcuts)
	if not building_inp: return None
	print(building_inp)
	building = placed_builds[building_inp]
	valid_upgs = building.get_valid_upgs()
	if len(valid_upgs) > 0:
		for e in valid_upgs: print(info.Colors.BOLD, "Megfizethető fejlesztések:",info.Colors.ENDC)
		upg_inp = foolproof_input("Melyik fejleszést szeretnéd alkalmazni?", valid_upgs)
		if not upg_inp: return None
		
	else:
		print("Nincsenek elérhető fejlesztések ehhez az épülethez.")
		return None

def disaster():
	chances = [info.disaster.chance for info.disaster in info.disasters.values()]
	dis = random.choices(list(info.disasters.keys()), weights=chances)[0]
	if dis != "nincs katasztrófa":
		print("szia")

#end

def exit_action():
    print(f"{info.Colors.FAIL}-megszakítva-{info.Colors.ENDC}")
