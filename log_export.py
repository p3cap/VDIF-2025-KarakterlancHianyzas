import pickle, os,time, events, city_data as info

save_dir = "saves"

def save_simulation():
	filename = input("Mentési fájl neve: ") + ".pkl"
	save_path = os.path.join(save_dir, filename)
	with open(save_path, "wb") as f:
		pickle.dump({
			"sim_const": info.sim_const,
			"sim_data":  info.sim_data,
			"buildings": info.buildings
		}, f)
	print(f"Szimuláció elmentve {filename} néven a saves mappába.")

def load_simulation():
	save_files = [f for f in os.listdir(save_dir) if f.endswith(".pkl")]
	if not save_files:
		print("Nem található mentés.")
		return None

	load_file = events.choice_input("Mentési fájl betöltése: ",{os.path.basename(file_path):{"return_value":os.path.join(save_dir, file_path),"desc":file_path} for file_path in save_files})
	print(load_file)
	with open(load_file[0], "rb") as f:
		save_file = pickle.load(f)

		info.sim_const = save_file["sim_const"]
		info.sim_data = save_file["sim_data"]
		info.buildings = save_file["buildings"]
	
	print(f"Mentés betöltve!")