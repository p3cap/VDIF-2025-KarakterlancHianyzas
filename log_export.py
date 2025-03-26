import csv, datetime, city_data as info

def export_buildings():
  print("Buildings exported to CVS.")
  with open('saves//save_01.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["az", "nev", "tipus"])
    """for key, value in test.items():#city_data.sim_data[]
      writer.writerow([key, value.name, value.type])"""

def import_buildings():
  print("Buildings imported from CVS.")

def import_city():
  print("City configuration imported from CVS.")

def export_city():
  print("City configuration exported to CVS.")

if __name__ == "__main__":
  print("spd")
  export_buildings()