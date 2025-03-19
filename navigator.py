import log_export, main
# Menu tree

menu_tree = {
    "desc": "Sziti építő OS",
    "actions": {
        "start simulation": {"desc": "interaktív szimuláció elkezdődött",
            "actions": {
				"info": [main.show_info, "Szimulációs Információk"],
				"jeln": [main.show_reports, "A jelenlegi kör jelentései (lakosok,panaszok,stb..) mutataja meg"],
				"epit": [main.build, "Épület építése"],
				"upgr": [main.upgrade_building, "Épület fejlesztése/felújjítása"],
				"next": [main.next_round, "Következő kör leszimulálása x db nap"],
            }
        },
        "cvs adatok": {"desc": "CVS-file alapú, speciális épületek, városok importálása, exportálása",
            "actions": {
                "import_city": (log_export.import_city, "Importálja a város konfigurációt CVS-ből"),
                "export_city": (log_export.export_city, "Exportálja a jelenlegi város konfigurációt CVS-be"),
                "import_buildings": (log_export.import_buildings, "Importálja az épületeket CVS-ből"),
                "export_buildings": (log_export.export_buildings, "Exportálja a jelenlegi épületeket CVS-be")
            }
        },
    }
}

# Terminal colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def format_number(amount):
    for unit in ["", "k", "M", "B", "T", "P", "E", "Z"]:
        if abs(amount) < 1000:
            return f"{amount:.2f}{unit}".rstrip('0').rstrip('.')
        amount /= 1000

def exit_action():
    print(f"{Colors.FAIL}-megszakítva-{Colors.ENDC}")

def foolproof_input(prompt, choices):
    shortcuts = {key[0]: key for key in choices.keys()}  # Shortcut (first letter)
    shortcuts.update({"h": "help", "x": "exit"})  # Add help and exit shortcuts
    options = ', '.join([f"{act} [{shortcut}]" for shortcut, act in shortcuts.items()])
    
    while True:
        inp = input(f"\n{Colors.BOLD}Opciók: {options}{Colors.ENDC}\n{prompt}").lower()
        if inp in ["x", "exit"]:  # Exit
            exit_action()
            return None
        elif inp in ["h", "help"]:  # Help
            for key, value in choices.items():
                description = value[1] if value is tuple else value.get("desc", "")
                print(f"{key} [{key[0]}]: {description}")
        
        elif inp in choices: return inp # Valid choice
        elif inp in shortcuts: return shortcuts[inp] #valid shortcut
        else: print(f"{Colors.WARNING}Please choose one of the options{Colors.ENDC}")  # Invalid choice

def open_menu(menu):
    print(f"{Colors.OKGREEN}{menu['desc']}{Colors.ENDC}")
    while True:
        action_key = foolproof_input("Választás: ", menu["actions"])
        if action_key is None:
            return
        selected = menu["actions"][action_key]
        if selected is dict:  # Submenu
            open_menu(selected)
        else:  # Execute action
            selected[0]()

open_menu(menu_tree)