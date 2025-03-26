import random as rng

#simuláció konstansok
sim_const = { #area calcuated in m2
	"currency_type": "HUF",
	"area_for_citizen": 30,
	"citizen_age_skpektrum": (0,80),
	"min_happiness": 20,
	"max_happiness": 100,
	"max_days": 30000,
	"tax_per_citizen": 50000,
	"area_per_service": 5, #mekkore terület után számít fel szolgáltatást egy meberre
	"serice_requirements": { #%of pupultion, these will accumlate happiness
		"egészségügy": 0.1,#10%
		"munkahely": 0.9,
		"oktatás": 0.25,
		"közlekedés": 0.8,
		"rendőrség": 0.4,
	}
}

#simuláció adatai
sim_data = {
	"happiness": 30,
	"currency_M": 1000,
	"buildings": {},
	"citizens": {},
	"projects": {},
	"complaints": {},
	"start_year": 2025,
	"day": 0,
}
#others
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

#classes
class Project:
	services = ["egészségügy","munka","oktatás","közlekedés","rendőrség","bolt"]
	def __init__(self):
		self.finished = False
		self.start_date = sim_data["day"]
		self.finish_days = 100
	def check_done(self):
		if sim_data["day"] - self.start_date  >= self.finish_days:
			self.finished = True
			print(self.finish_dict)
			self.finish_dict.update({len(sim_data["buildings"]):self})

class Building(Project): #épület azonosító, név, típus (pl. lakóház, iskola), építés éve, hasznos terület. 
	building_types = ["lakóház","munkahely","kórház","iskola","rendőrség","bolt"]
	def __init__(self, _cost_M:int=0, _area:int=0, _stories:int=0, _reliability:int=0, _finish_days:int=0,_type="lakóház",_services:list=[],_name:str=""):
		super().__init__()
		self.built = sim_data["day"]
		self.cost = _cost_M
		self.area = _area
		self.stories = _stories
		self.reliability = _reliability
		self.finish_days = _finish_days
		self.type = _type
		self.services = _services
		self.name = _name or input("Épület neve: ") or "N/A"
		self.quality = 2.5
		self.upgrades = {}
		self.finish_dict = sim_data["buildings"]
		self.age = 0
	def upgrade(self,upg):
		if not upg:return
		for key, value in upg.effects:
			print(key, value)
			setattr(self, key, getattr(self, key) + value)
	def update(self):
		self.age = sim_data["day"] - self.built

	def get_valid_upgs(self):
		valid_upgrades = []
		for key, upg in upgrades.items():
			for key,req in upg.min_req:
				value = getattr(self, key)
				if value > req:
					valid_upgrades.append(upg)

		return valid_upgrades
	def __format__(self, format_spec):
		return f"{self.name:<10}{self.type:<10}{self.services}"

class Upgrade(Project):#szolgáltatás azonosító, név, típus (pl. egészségügy, közlekedés), kapcsolódó épület azonosítója. 
#					^ will be in the buildigs upgarde list ^
	def __init__(self, _name, _cost_M:int, _finish_days:int, _per_100:bool, _min_requirements:dict, _effects:dict):
		super().__init__()
		self.name = _name
		self.cost = _cost_M
		self._finish_days = _finish_days
		self.per_100 = _per_100
		self.min_req = _min_requirements
		self.effect = _effects
		self.started = 0
		self.finish_dict = None #in this case the builduings upgrade dict
	def __format__(self, format_spec):
		return f"upg"

class Disaster:
	def __init__(self, _name, _strength: dict = 0, _chance: float = 0):
		super().__init__()
		self.name = _name
		self.strength = _strength
		self.chance = _chance

	def activate_disaster(self):
		dis_info = {
			"size": rng.randint(1, 5),
			"damaged_builds": [],
			"repair_cost_M": 0
		}
		buildings = list(sim_data["buildings"].values())  # Convert dictionary values to a list
		if not buildings:
			return dis_info  # Return early if there are no buildings

		min_affected = max(1, len(buildings) // 10)
		max_affected = min(len(buildings), rng.randint(min_affected, len(buildings)))

		for building in rng.sample(buildings, rng.randint(min_affected, max_affected)):
			if building.type in self.strength:
				damage = self.strength[building.type]
				new_quality = max(0, building.quality - damage)
				dis_info["damaged_builds"].append(building.name)
				dis_info["repair_cost_M"] += (building.quality - new_quality) * 0.05 * building.cost
				building.quality = new_quality  # Correctly update the building's quality

		return dis_info

	def __format__(self, format_spec):
		return f"Disatser"

class Citizen: #lakos azonosító, név, születési év, foglalkozás, lakóhely (kapcsolat az Épületek táblával). 
	def __init__(self, _born:int, _job:str, _houseID:int):
		super().__init__()
		self.born = _born
		self.job = _job
		self.houseID = _houseID
	def __format__(self, format_spec):
		return f"{self.born:<10}{self.job:<10}{self.houseID:<10}"

def make_id(data_dict):
	if not data_dict:return 1
	return max(data_dict.keys()) + 1


buildings = [
	# Lakó
	Building(_name="családi ház", _cost_M=60, _area=150, _stories=1, _reliability=98, _type="lakóház"),
	Building(_name="ikerház", _cost_M=75, _area=300, _stories=2, _reliability=98, _type="lakóház"),
	Building(_name="társasház", _cost_M=250, _area=1000, _stories=4, _reliability=95, _type="lakóház"),
	Building(_name="lakótelepi épület", _cost_M=900, _area=6000, _stories=10, _reliability=89, _type="lakóház"),
	
	# Egészség
	Building(_name="mini rendelő", _cost_M=90, _area=100, _stories=1, _reliability=92, _type="egészség"),
	Building(_name="szakorvosi rendelő", _cost_M=600, _area=1200, _stories=2, _reliability=90, _type="egészség"),
	Building(_name="kórház", _cost_M=2800, _area=5000, _stories=4, _reliability=90, _type="egészség"),
	Building(_name="klinikai központ", _cost_M=6000, _area=10000, _stories=6, _reliability=88, _type="egészség"),

	# Oktatás
	Building(_name="óvoda", _cost_M=325, _area=500, _stories=2, _reliability=93, _type="oktatás"),
	Building(_name="általános iskola", _cost_M=1200, _area=3000, _stories=3, _reliability=94, _type="oktatás"),
	Building(_name="középiskola", _cost_M=2000, _area=4000, _stories=4, _reliability=95, _type="oktatás"),
	Building(_name="egyetem", _cost_M=3000, _area=5500, _stories=4, _reliability=95, _type="oktatás"),

	# Munka
	Building(_name="kisbolt", _cost_M=250, _area=300, _stories=1, _reliability=97, _type="munka"),
	Building(_name="irodaház", _cost_M=1500, _area=10000, _stories=5, _reliability=95, _type="munka"),
	Building(_name="bevásárlóközpont", _cost_M=5000, _area=20000, _stories=3, _reliability=90, _type="munka"),
	Building(_name="ipari park", _cost_M=10000, _area=50000, _stories=2, _reliability=85, _type="munka"),

	# Közlekedés
	Building(_name="autóbusz megálló", _cost_M=50, _area=50, _stories=1, _reliability=99, _type="közlekedés"),
	Building(_name="buszpályaudvar", _cost_M=800, _area=3000, _stories=1, _reliability=85, _type="közlekedés"),
	Building(_name="vasútállomás", _cost_M=1200, _area=5000, _stories=2, _reliability=88, _type="közlekedés"),
	Building(_name="repülőtér", _cost_M=20000, _area=100000, _stories=3, _reliability=80, _type="közlekedés")
]

upgrades = [
	Upgrade(_name="energetikai korszerűsítés", _cost_M=0.3, _finish_days=150, _per_100=True, _min_requirements={"age": 5}, _effects={"quality": 3, "reliability": 20}),
	Upgrade(_name="bővítés", _cost_M=0.3, _finish_days=30, _per_100=True, _min_requirements={"area": 200}, _effects={"space": 30}),
	Upgrade(_name="szigetelés", _cost_M=0.3, _finish_days=30, _per_100=True, _min_requirements={"age": 3}, _effects={"quality": 2.5}),
	Upgrade(_name="tetőcsere", _cost_M=0.3, _finish_days=30, _per_100=True, _min_requirements={"age": 10}, _effects={"reliability": 30}),
	Upgrade(_name="lift beépítés", _cost_M=5, _finish_days=60, _per_100=False, _min_requirements={"stories": 3}, _effects={"quality": 2.5}),
	Upgrade(_name="napkollektor telepítés", _cost_M=0.5, _finish_days=45, _per_100=False, _min_requirements={"stories": 1}, _effects={"quality": 4, "reliability": 10}),
	Upgrade(_name="okosotthon rendszer", _cost_M=0.7, _finish_days=60, _per_100=False, _min_requirements={"type": "lakó"}, _effects={"quality": 5, "reliability": 5}),
	
	Upgrade(_name="hőszivattyú", _cost_M=1, _finish_days=45, _per_100=False, _min_requirements={"type": "lakó", "age": 2}, _effects={"quality": 3, "reliability": 5}),
	Upgrade(_name="biztonsági rendszer", _cost_M=0.6, _finish_days=30, _per_100=False, _min_requirements={"type": "munka"}, _effects={"reliability": 10}),
	Upgrade(_name="térfigyelő kamerák", _cost_M=0.4, _finish_days=25, _per_100=False, _min_requirements={"type": "közlekedés"}, _effects={"reliability": 7}),
	Upgrade(_name="környezetbarát burkolatok", _cost_M=0.3, _finish_days=20, _per_100=True, _min_requirements={"area": 500}, _effects={"quality": 2}),
	Upgrade(_name="zöldtető", _cost_M=1.5, _finish_days=90, _per_100=False, _min_requirements={"stories": 2, "age": 5}, _effects={"quality": 5, "reliability": 3}),
	Upgrade(_name="elektromos töltőállomás", _cost_M=2, _finish_days=60, _per_100=False, _min_requirements={"type": "munka"}, _effects={"quality": 4}),
	Upgrade(_name="intelligens világítás", _cost_M=0.5, _finish_days=40, _per_100=False, _min_requirements={"age": 3}, _effects={"quality": 3, "reliability": 2}),
	Upgrade(_name="modern csatornarendszer", _cost_M=1, _finish_days=60, _per_100=True, _min_requirements={"age": 10, "area": 1000}, _effects={"reliability": 8}),
	Upgrade(_name="hangszigetelés", _cost_M=0.8, _finish_days=50, _per_100=True, _min_requirements={"type": "lakó", "age": 3}, _effects={"quality": 3}),
	Upgrade(_name="faültetés", _cost_M=0.2, _finish_days=10, _per_100=True, _min_requirements={"area": 200}, _effects={"quality": 1})
]
disasters = [
	Disaster(_name="cunami", _strength=4, _chance=0.22),
	Disaster(_name="tornádó", _strength=3, _chance=0.33),
	Disaster(_name="tűz", _strength=2, _chance=0.20),
	Disaster(_name="bombázás", _strength=4, _chance=0.41),
	Disaster(_name="vulkán", _strength=5, _chance=0.09),
	Disaster(_name="nincs katasztrófa", _strength=0, _chance=2)
]
