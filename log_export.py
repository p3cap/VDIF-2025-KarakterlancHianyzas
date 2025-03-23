import csv, city_data as info

test = {"1":info.Building()}

def export_buildings():
  with open('saves//save_01.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in test.items():#city_data.sim_data[]
      writer.writerow([key, value.name, value.type])

def import_buildings():
  pass

def import_city():
  pass

def export_city():
  pass

if __name__ == "__main__":
  export_buildings()