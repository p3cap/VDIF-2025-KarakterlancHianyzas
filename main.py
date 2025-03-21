import random, os, datetime, events, log_export
import city_data as info

menu_tree = {
    "desc": "Sziti építő OS",
    "actions": {
        "start simulation": {"desc": "interaktív szimuláció elkezdődött",
            "actions": {
				"info": [events.show_info, "Szimulációs Információk"],
				"jeln": [events.show_reports, "A jelenlegi kör jelentései [lakosok,panaszok,stb..] mutataja meg"],
				"epit": [events.build, "Épület építése"],
				"upgr": [events.upgrade_building, "Épület fejlesztése/felújjítása"],
				#"next": [events.next_round, "Következő kör leszimulálása x db nap"],
            }
        },
        "cvs adatok": {"desc": "CVS-file alapú, speciális épületek, városok importálása, exportálása",
            "actions": {
                "import_city": [log_export.import_city, "Importálja a város konfigurációt CVS-ből"],
                "export_city": [log_export.export_city, "Exportálja a jelenlegi város konfigurációt CVS-be"],
                "import_buildings": [log_export.import_buildings, "Importálja az épületeket CVS-ből"],
                "export_buildings": [log_export.export_buildings, "Exportálja a jelenlegi épületeket CVS-be"]
            }
        },
    }
}

def open_menu(menu):
    print(f"\n{info.Colors.OKGREEN}--{menu['desc']}--{info.Colors.ENDC}")
    while True:
        action_key = events.foolproof_input("Választás: ", menu["actions"])
        if action_key is None: return
        selected = menu["actions"][action_key]
        if isinstance(selected, list):  # Submenu
            selected[0]()
        else:  # Execute action
            open_menu(selected)

def checkEnd():
	global simulating
	if info.sim_data["hapiness"] < info.sim_const["min_hapiness"]: return True
	elif info.sim_data["currency_M"] <= 0: return True
	return False

def end_simulation():
	print(f"{info.info.Colors.FAIL}GAME OVER")

if __name__ == "__main__": #akkor indul csak el a program, ha egyenesn ezt a python filet indítjuk el és nem indul el ha csak hivatkozunk rá
	while not checkEnd():
		open_menu(menu_tree)