import random, log_export, os
import city_data as info

#alap defek
def format_number(amount):
  for unit in ["","k","M","B","T","P","E","Z"]:
        if abs(amount) < 1000:
            return f"{amount:.2f}{unit}".rstrip('0').rstrip('.')
        amount /= 1000

def foolproof_input(text:str,choices:list):
  shortcuts = {key[0]: key for key in choices+["x -> exit"]}
  while True:
    options = ', '.join([f"{act} [{shortcut}]" for shortcut, act in shortcuts.items()])
    inp = input(f"\n{info.colors.BOLD}Opciók: {options}{info.colors.ENDC}\n{text}").lower()
    if inp == "x": 
      exit_action()
      return None
    elif inp in choices: return inp
    elif inp in shortcuts: return shortcuts[inp] 
      
    print(f"{info.colors.WARNING}Please choose one of the options{info.colors.ENDC}")

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
  print("Valuta:",format_number(info.sim_data["currency"]),currency_type)
  print(f"Boldogság: {format_number(info.sim_data["hapiness"])}%")
  print("Épületek(db):",format_number(len(info.sim_data["buildings"])),"db")
  print("Polgárok(db):",format_number(len(info.sim_data["citizens"])),"db")
  print("Adó bevétel:"     )#WIP
  print("Panaszok:"        )#WIP
  print(info.colors.HEADER,  "-"*26  ,info.colors.ENDC) #line

def build():
  new_building = foolproof_input("Mit akarsz építeni:",info.buildings.keys())
  if new_building: 
    print(info.buildings[new_building])

def help_actions():
  for key, (func, description) in choices.items(): print(f"{key} [{key[0]}] {description}")

#round
def exit_action():
  #os.system('cls' if os.name == 'nt' else 'clear')
  print(f"{info.colors.FAIL}-megszakítva-{info.colors.ENDC}")

def next_round():
  action = foolproof_input("What to do:",list(choices.keys()))
  if action: choices[action][0]()

choices = {
  "help": [help_actions, "Segít a paracsok magyarázásban"],
  "info": [show_info, "Szimulációs Információk"],
  "jeln": [show_reports, "A jelenlegi kör jelentései (lakosok,panaszok,stb..) mutataja meg"],
  "epit": [build, "Épület építése"],
  "next": [next_round, "Következő kör"],
}
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
    next_round()
