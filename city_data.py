#simuláció konstansok
sim_const = {
	"illnes_chance": 0.01,
	"days_per_round": 30,
}
#simuláció adatai
sim_data = {
	"happiness": 70,
	"currency": 1000000000,
	"buildings": [],
	"citizens": [],

	"round": 0,
}
#feljegyzések
logbook = []


class Building: #épület azonosító, név, típus (pl. lakóház, iskola), építés éve, hasznos terület. 
	building_types = ["lakóház","munkahely","egészségügy","iskola","közlekedés"]
	def __init__(self, _cost:int, _space:int, _stories:int, _reliability:float, _type:str):
		self.ID = None
		self.built = None
		self.cost = _cost
		self.space = _space
		self.stories = _stories
		self.reliability = _reliability
		self.type = _type
		self.name = "N/A"
		self.age = 0 #_built??
		self.quality = 100
		self.upgrades = {}

class Upgrade:#szolgáltatás azonosító, név, típus (pl. egészségügy, közlekedés), kapcsolódó épület azonosítója. 
#					            ^               will be in the buildigs upgarde list           ^
	def __init__(self, _cost:int, _build_days:int, _per_100:bool, _min_requirements:dict, _effects:dict):
		self.cost = _cost
		self.build_days = _build_days
		self.per_100 = _per_100
		self.min_req = _min_requirements
		self.effect = _effects

class Citizen: #lakos azonosító, név, születési év, foglalkozás, lakóhely (kapcsolat az Épületek táblával). 
	def __init__(self, _ID:int, _born:int, _job:str, _houseID:int):
		self.ID = _ID
		self.born = _born
		self.job = _job
		self.houseID = _houseID

buildings = { #_cost:int, _space:int, _stories:int, _reliability(megbizhatóság), _type:str
	"kádárkocka": Building(_cost=4000000, _space=150, _stories=1, _reliability=98.8, _type="lakossági"),
	"ikerház": Building(_cost=7500000, _space=300, _stories=1, _reliability=98.8, _type="lakossági"),
	"lakótelep": Building(_cost=900000000, _space=60000, _stories=10, _reliability=89.2, _type="lakossági"),

	"kis rendelő": Building(_cost=340000, _space=100, _stories=1, _reliability=92.8, _type="egészségügy"),
  "kórház": Building(_cost=280000000, _space=5000, _stories=4, _reliability=89.9, _type="egészségügy"),
  
  "óvoda": Building(_cost=325000000, _space=500, _stories=2, _reliability=93.9, _type="iskola"),
  "egyetem": Building(_cost=3000000000, _space=5500, _stories=4, _reliability=95.0, _type="iskola"),
}

upgrades = {#_cost(ft), _build_days(napban), _per_100(méretarányos), _effects(hatásai)
	"energetikai korszerűsítés": Upgrade(_cost=3000000, _build_days=150, _per_100=True, _min_requirements={"age":5}, _effects={"quality": 10, "reliability": 20}),
	"bővítés": Upgrade(_cost=300000, _build_days=30, _per_100=True, _min_requirements={}, _effects={"space": 30}),
	"szigetelés": Upgrade(_cost=300000, _build_days=30, _per_100=True, _min_requirements={}, _effects={"quality": 50}),
	"tetőcsere": Upgrade(_cost=300000, _build_days=30, _per_100=True, _min_requirements={}, _effects={"reliability": 30}),
	"lift beépítés": Upgrade(_cost=5000000, _build_days=60, _per_100=False, _min_requirements={"stories":2}, _effects={"quality": 50})
}
