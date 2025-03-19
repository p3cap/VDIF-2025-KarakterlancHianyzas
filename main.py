import random, log_export, os, datetime
import city_data as info
import navigator as ui

#választható dologok
def show_info():
	currency_type = info.sim_const["currency_type"]
	print(info.colors.HEADER,  "-"*10,"info","-"*10  ,info.colors.ENDC) #line
	print("Maximum nap:",info.sim_const["max_days"])
	print("Egy körben eltelő napok száma:",info.sim_const["days_per_round"])
	print("Eltelt körök száma:",info.sim_data["round"],f"({info.sim_data["round"]*info.sim_const["days_per_round"]}nap)")
	print("Hátralévő körök száma:",info.sim_const["max_days"]//info.sim_const["days_per_round"]-info.sim_data["round"])
	print(info.colors.HEADER,  "-"*26  ,info.colors.ENDC) #line

def show_reports():
	currency_type = info.sim_const["currency_type"]
	print(info.colors.HEADER,  "-"*7,"jelentések","-"*7  ,info.colors.ENDC) #line
	print("Valuta:",ui.format_number(info.sim_data["currency"]),currency_type)
	print(f"Boldogság: {ui.format_number(info.sim_data["hapiness"])}%")
	print("Épületek(db):",ui.format_number(len(info.sim_data["buildings"])),"db")
	print("Polgárok(db):",ui.format_number(len(info.sim_data["citizens"])),"db")
	print("Adó bevétel:"     )#WIP
	print("Panaszok:"        )#WIP
	print(info.colors.HEADER,  "-"*26  ,info.colors.ENDC) #line

def build():
	new_building = ui.ui.foolproof_input("Mit akarsz építeni:",list(info.buildings.keys()))
	if new_building:
		new_building = info.buildings[new_building]
		new_building.name = input("Épület neve: ") or info.buildings
		info.sim_data["buildings"].update({len(info.sim_data["buildings"]): new_building})
		print("added",new_building.type,new_building.name)

def upgrade_building(): #NOT WORKING YET!!!!!
	building_inp = ui.foolproof_input("Melyik épületet fejleszted (ID):",list(info.buildings.keys())) 
	if not building_inp: return None
	building = info.sim_data["buildings"].get(building_inp)
	valid_upgs = building.get_valid_upgs()
	if len(valid_upgs) > 0:
		for e in valid_upgs: print(ui.colors.BOLD, "Megfizethető fejlesztések:",ui.colors.ENDC)
		upg_inp = ui.foolproof_input("Melyik fejleszést szeretnéd alkalmazni?", valid_upgs)
		if not upg_inp: return None
		
	else:
		print("Nincsenek elérhető fejlesztések ehhez az épülethez.")
		return None



#end
def checkEnd():
	global simulating
	if info.sim_data["hapiness"] < info.sim_const["min_hapiness"]: return True
	elif info.sim_data["currency"] <= 0: return True
	return False

def end_simulation():
	print(f"{info.colors.FAIL}GAME OVER")

if __name__ == "__main__": #akkor indul csak el a program, ha egyenesn ezt a python filet indítjuk el és nem indul el ha csak hivatkozunk rá
	while not checkEnd():
		ui.open_menu()
