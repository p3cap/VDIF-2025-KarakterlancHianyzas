import csv, datetime, city_data as info

def export_buildings():
  save_name = input("Save file name():")
  with open('saves//save_01.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["ID", "nev", "tipus"])


def import_buildings():
  print("Buildings imported from CVS.")

def import_city():
  print("City configuration imported from CVS.")

def export_city():
  print("City configuration exported to CVS.")

if __name__ == "__main__":
  print("spd")
  export_buildings()