import random, log_export, os
import city_data as info

def format_number(amount):
  for unit in ["","k","M","B","T","P","E","Z"]:
        if abs(amount) < 1000:
            return f"{amount:.2f}{unit}".rstrip('0').rstrip('.')
        amount /= 1000

def foolproof_input(text:str,choices:list):
  while True:
    inp = input(f"\n{info.colors.BOLD}Opciók: {choices}{info.colors.ENDC}\n'x'->kilépés \n{text}").lower()
    if inp in choices: return inp
    if inp == "x": exit_action(); return
    print(f"{info.colors.WARNING}Please choose one of the options{info.colors.ENDC}")

def show_info():
  currency_type = info.sim_const["currency_type"]
  print(info.colors.HEADER,  "-"*10,"info","-"*10  ,info.colors.ENDC) #line
  print("Valuta:",format_number(info.sim_data["currency"]),currency_type)
  print(f"Boldogság: {format_number(info.sim_data["happiness"])}/{info.sim_const['max_hapiness']}")
  print("Épületek(db):",format_number(len(info.sim_data["buildings"])),"db")
  print("Polgárok(db):",format_number(len(info.sim_data["citizens"])),"db")
  print(info.colors.HEADER,  "-"*26  ,info.colors.ENDC) #line

def show_reports():
  currency_type = info.sim_const["currency_type"]
  print(info.colors.HEADER,  "-"*7,"jelentések","-"*7  ,info.colors.ENDC) #line
  print("Adó bevétel:"     )#WIP
  print("Panaszok:"        )#WIP
  print(info.colors.HEADER,  "-"*26  ,info.colors.ENDC) #line

def build():
  new_building = foolproof_input("Mit akarsz építeni:",info.buildings.keys())
  if new_building: print(info.buildings[new_building])

def exit_action():
  #os.system('cls' if os.name == 'nt' else 'clear')
  print(f"{info.colors.FAIL}-megszakítva-{info.colors.ENDC}")

choices = {
  "info": show_info,
  "jelentes": show_reports,
  "epit": build,
}

def round():
  action = foolproof_input("What to do:",list(choices.keys()))
  if action: choices[action]()
  
  round()

if __name__ == "__main__": #akkor indul csak el a program, ha egyenesn ezt a filet indítjuk
  round()
