import datetime

#simuláció konstansok
sim_const = {
"currency_type": "HUF",
	"days_per_round": 30,
	"min_hapiness": 50,
	"max_hapiness": 100,
	"illnes_rate": 0.1,
	"max_days": 300
}

#simuláció adatai
sim_data = {
	"hapiness": sim_const["min_hapiness"],
	"currency_M": 1000,
	"buildings": {},
	"citizens": {},
	"current_date": None,

	"round": 0,
}
#feljegyzések
logbook = []


class Building: #épület azonosító, név, típus (pl. lakóház, iskola), építés éve, hasznos terület. 
	building_types = ["lakóház","munkahely","egészségügy","iskola","közlekedés"]
	def __init__(self, _cost_M:int, _area:int, _stories:int, _reliability:float, _type:str, _restauration_cost:dict, _restauration_days:int):
		self.built = None
		self.cost = _cost_M
		self.area = _area
		self.stories = _stories
		self.reliability = _reliability
		self.type = _type
		self.age = 0
		self.name = "N/A"
		self.quality = 5.0
		self.restauration_cost = _restauration_cost
		self.restauration_days = _restauration_days
		self.upgrades = {}
	def update(self):
		self.age = self.built - None
		for upg in self.upgrades:
			upg.build_days = upg.started - 0 #timehere
	def upgrade(self,upg):
		for key in self.upgrades:
			if self.upgrades[key]["time_remains"] > 0: return "egszerre csak egy fejleszést lehet csinálni."

	def get_valid_upgs(self):
		valid_upgrades = []
		dict_building = vars(self)
		for key, upg in upgrades.items():
			dict_upg = vars(upg)
			if dict_upg[key] <= dict_building[key]:
				valid_upgrades.append(key)
		return valid_upgrades


class Upgrade:#szolgáltatás azonosító, név, típus (pl. egészségügy, közlekedés), kapcsolódó épület azonosítója. 
#					^ will be in the buildigs upgarde list ^
	def __init__(self, _cost_M:int, _build_days:int, _per_100:bool, _min_requirements:dict, _effects:dict):
		self.cost = _cost_M
		self.build_days = _build_days
		self.per_100 = _per_100
		self.min_req = _min_requirements
		self.effect = _effects
		self.started = 0

class Disaster:
	def __init__(self, _hapiness_decrease:int, _per_100:bool, _stranght:dict, _chance:float):
		self.per_100 = _per_100
		self.stranght = _stranght
		self.hapiness_decrease = _hapiness_decrease
		self.chance = _chance

class Citizen: #lakos azonosító, név, születési év, foglalkozás, lakóhely (kapcsolat az Épületek táblával). 
	def __init__(self, _ID:int, _born:int, _job:str, _houseID:int):
		self.ID = _ID
		self.born = _born
		self.job = _job
		self.houseID = _houseID

buildings = { #_cost_M(millikba):int, _area(m2):int, _stories:int, _reliability(megbizhatóság), _type:str
	"ház": Building(_cost_M=60, _area=150, _stories=1, _reliability=98.8, _type="lakossági"),
	"ikerház": Building(_cost_M=75, _area=300, _stories=1, _reliability=98.8, _type="lakossági"),
	"lakótelep": Building(_cost_M=900, _area=60000, _stories=10, _reliability=89.2, _type="lakossági"),

	"mini rendelő": Building(_cost_M=90, _area=100, _stories=1, _reliability=92.8, _type="egészségügy"),
	"kórház": Building(_cost_M=2800, _area=5000, _stories=4, _reliability=89.9, _type="egészségügy"),

	"óvoda": Building(_cost_M=325, _area=500, _stories=2, _reliability=93.9, _type="iskola"),
	"egyetem": Building(_cost_M=3000, _area=5500, _stories=4, _reliability=95.0, _type="iskola"),
}

upgrades = {#_cost_M(millio), _build_days(napban), _per_100(méretarányos), _effects(hatásai)
	"energetikai korszerűsítés": Upgrade(_cost_M=3, _build_days=150, _per_100=True, _min_requirements={"age":5}, _effects={"quality": 3, "reliability": 20}),
	"bővítés": Upgrade(_cost_M=3, _build_days=30, _per_100=True, _min_requirements={}, _effects={"space": 30}),
	"szigetelés": Upgrade(_cost_M=3, _build_days=30, _per_100=True, _min_requirements={}, _effects={"quality": 2.5}),
	"tetőcsere": Upgrade(_cost_M=3, _build_days=30, _per_100=True, _min_requirements={}, _effects={"reliability": 30}),
	"lift beépítés": Upgrade(_cost_M=5, _build_days=60, _per_100=False, _min_requirements={"stories":2}, _effects={"quality": 2.5})
}
disasters = {# _stranght(a katasztrófa mértéke), _hapiness_decrease(boldogság csökkenése), _chance(esély a bekövetkezésre)
	"cunami": Disaster( _stranght=4, _hapiness_decrease=28, _chance=0.22),
	"tornádó": Disaster( _stranght=3, _hapiness_decrease=30, _chance=0.33),
	"tűz": Disaster( _stranght=2, _hapiness_decrease=10,_chance=0.80),
	"bombázás": Disaster( _stranght=4, _hapiness_decrease=35, _chance=0.41),
	"vulkán": Disaster( _stranght=5, _hapiness_decrease=25, _chance=0.09),
	"nincs katasztrófa": Disaster(_chance=2)
	}

