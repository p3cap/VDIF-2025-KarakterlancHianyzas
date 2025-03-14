import random, log_export
import city_data as info

def format_number(amount):
  for unit in ["","k","M","B","T","P","E","Z"]:
        if abs(amount) < 1000:
            return f"{amount:.2f}{unit}".rstrip('0').rstrip('.')
        amount /= 1000

def foolproof_input(text,choices):
  while True:
    inp = input(f"Opciók: {choices} \n{text}")
    if inp in choices: return inp
    print(info.colors.WARNING+"Please choose one of the options"+info.colors.ENDC)

def show_info():
  currency_type = info.sim_const["currency_type"]
  print("-"*10,"info","-"*10)
  print("Currency:",format_number(info.sim_data["currency"]),currency_type)
  print("Hapiness:",format_number(info.sim_data["happiness"]),currency_type)
  print("Number of buildings:",format_number(len(info.sim_data["buildings"])),"db")
  print("Number of citizens:",format_number(len(info.sim_data["citizens"])),"db")

choices = {
  "info": show_info
}

def round():
  choices[foolproof_input("What to do:",list(choices.keys()))]()
  
  round()

if __name__ == "__main__":
  round()
