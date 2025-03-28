import sys
import events, log_export
import city_data as info

# megjegyzés: a city maga lehetett volna egy külön class... but no time to do it now

menu_tree = {  # return_value -> actions volt, a choice_input egyszerűségének érdekében lett megváltoztatva
	"desc": "Sziti építő OS",
	"return_value": {
		"belépés a szimulációba": {"desc": "interaktív szimuláció elkezdődött",
			"return_value": {
				"epit": {"return_value": events.build, "desc": "Épület építése"},
				"upgr": {"return_value": events.upgrade_building, "desc": "Épület fejlesztése/felújítása"},
				"next_round": {"return_value": events.next_round, "desc": "Következő kör (választott mennyiségű nap) le szimulálása."},
				"stat": {"desc": "Statisztika kimutatási opciók",
					"return_value": {
						"info": {"return_value": events.show_info, "desc": "Szimulációs Információk"},
						"jelentés": {"return_value": events.show_reports, "desc": "A jelenlegi kör jelentései [lakosok, pénz, stb..] mutatja meg"},
						"list projects": {"return_value": events.list_projects, "desc": "Összes projekt statisztikáit mutatja ki"},
						"list citizens": {"return_value": events.list_citizens, "desc": "Összes lakos statisztikáit mutatja ki"},
						"list buildings": {"return_value": events.list_buildings, "desc": "Összes épület statisztikáit mutatja ki"},
					}
				}
			}
		},
		"szimuláció mentések": {"desc": "Szimulációs adatok mentése, betöltése",
			"return_value": {
				"szimuláció mentése": {"return_value": log_export.save_simulation, "desc": "Elmenti a szimulációt a saves mappába"},
				"mentett szimuláció betöltése": {"return_value": log_export.load_simulation, "desc": "A saves mappából betölhető mentések."},
				"make_custom_building": {"return_value": events.custom_building, "desc": "Saját típusú épület létrehozása"},
			}
		},
	}
}

def open_menu(menu, desc=""):
	print(f"\n{info.Colors.OKGREEN}--{desc}--{info.Colors.ENDC}")
	while True:
		choice, next_desc = events.choice_input("Választás: ", menu)
		if not choice: 
			return None
		if isinstance(choice, dict): 
			open_menu(choice, next_desc)  # submenu
		else: 
			choice()  # call the return value func
	

if __name__ == "__main__":
	with open("README.md", encoding="UTF-8") as file:
		for e in file.readlines(): 
			print(e)
	while not events.checkEnd():
		open_menu(menu_tree["return_value"], menu_tree["desc"])
	events.end_simulation()