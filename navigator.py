import main, log_export

# menu tree
menu_tree = {
    "desc":"Sziti építő OS", 
    "actions":{
        "new_save": [log_export.import_city, "Create a new save"],
            "cvs adatok": {
                "desc": "Adatok importálása, exportálása",
                "actions": {
                    "city import": [log_export.import_city, "Importálja a város konfigurációt CVS file-ba"],
                    "export city": [log_export.export_city, "Exportálja a város konfigurációt CVS file-ból"],
                    "make buildings": [log_export.import_buildings, "Speciális épület létrehozása"],
                    "buildings import": [log_export.import_buildings, "Importálja a létrehozható épületeket CVS file-ba"],
                    "_export buildings": [log_export.export_buildings, "Exportálja a létrehozható épületeket CVS file-ból"]
                }
            }
        }
    }

#treminal colors
class colors:
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

def exit_action(): print(f"{colors.FAIL}-megszakítva-{colors.ENDC}")

def foolproof_input(text:str, choices:dict):
    shortcuts = {key[0]: key for key in choices.keys()}  # shortcut (első betű)
    shortcuts.update({"h": "help", "x": "exit"})  # Kilépés, help
    options = ', '.join([f"{act} [{shortcut}]" for shortcut, act in shortcuts.items()])
    while True:
        inp = input(f"\n{colors.BOLD}Opciók: {options}{colors.ENDC}\n{text}").lower()

        if inp in ["x", "exit"]: #kilepes
            print(f"{colors.FAIL}-megszakítva-{colors.ENDC}")
            return None
        elif inp in ["h", "help"]: #help
            for key, (_ , description) in choices.items():
                print(f"{key} [{key["desc"]}] {description}")
        elif inp in choices:  return inp # valid
        elif inp in shortcuts: return choices[shortcuts[inp]] # shortcut valid
        else:print(f"{colors.WARNING}Please choose one of the options{colors.ENDC}") #invalid


def open_menu(menu):
    print(f"{colors.OKGREEN}{menu["desc"]}{colors.ENDC}")
    action = foolproof_input("What to do:", menu["actions"])
    if not action: return
    action = menu["action"][action]
    if action is list:
        action[0]()
    elif action is dict:
        open_menu(action)

open_menu(menu_tree)
