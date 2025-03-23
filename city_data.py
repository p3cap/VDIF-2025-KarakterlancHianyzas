import datetime

#simuláció konstansok
sim_const = {
	"currency_type": "HUF",
	"days_per_round": 30,
	"min_hapiness": 20,
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
	"projects": {},
	"current_date": None,

	"round": 0,
}
#others
def func_check():pass #used for isinstance(object, type(func(check))) to differanciate func from varubles in classes, to make them easier to systemize
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
	def __init__(self, _finish_dict:dict):
		self.finished = False
		self.finish_dict = _finish_dict
		self.start_date = datetime.datetime.now()
		sim_data["projects"].update({len(sim_data["projects"]):self})
	def check_done(self):
		if self.start_date - datetime.datetime.now() <= 0:
			self.finished = True
			self.finish_dict.update({len(self.finish_dict)})


class Building(Project): #épület azonosító, név, típus (pl. lakóház, iskola), építés éve, hasznos terület. 
	building_types = ["lakóház","munkahely","egészségügy","iskola","közlekedés"]
	def __init__(self, _cost_M:int=0, _area:int=0, _stories:int=0, _reliability:int=0, _finish_days:int=0,_type:str="",_name:str=""):
		self.built = datetime.datetime.now()
		self.cost = _cost_M
		self.area = _area
		self.stories = _stories
		self.reliability = _reliability
		self.finish_days = _finish_days
		self.type = _type
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

	def get_valid_upgs(self):
		valid_upgrades = []
		for key, upg in upgrades.items():
			for key,req in upg.min_req:
				value = getattr(self, key)
				if isinstance(value,type(func_check)) and value() > req or value > req: #makes sure it's a function and then calls it with () to return value
					valid_upgrades.append(upg)

		return valid_upgrades

class Upgrade(Project):#szolgáltatás azonosító, név, típus (pl. egészségügy, közlekedés), kapcsolódó épület azonosítója. 
#					^ will be in the buildigs upgarde list ^
	def __init__(self, _cost_M:int, _finish_days:int, _per_100:bool, _min_requirements:dict, _effects:dict):
		self.cost = _cost_M
		self._finish_days = _finish_days
		self.per_100 = _per_100
		self.min_req = _min_requirements
		self.effect = _effects
		self.started = 0
		self.finish_dict = None #in this case the builduings upgrade dict



class Disaster:
	def __init__(self, _hapiness_decrease:int=0, _per_100:bool=False, _stranght:dict=1, _chance:float=0):
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
	"ház": Building(_cost_M=60, _area=150, _stories=1, _reliability=98, _type="lakossági", _name="ház"),
	"ikerház": Building(_cost_M=75, _area=300, _stories=1, _reliability=98, _type="lakossági", _name="ikerház"),
	"lakótelep": Building(_cost_M=900, _area=60000, _stories=10, _reliability=89, _type="lakossági", _name="lakótelep"),

	"mini rendelő": Building(_cost_M=90, _area=100, _stories=1, _reliability=92, _type="egészségügy", _name="mini rendelő"),
	"kórház": Building(_cost_M=2800, _area=5000, _stories=4, _reliability=89.9, _type="egészségügy", _name="kórház"),

	"óvoda": Building(_cost_M=325, _area=500, _stories=2, _reliability=93, _type="iskola", _name="óvoda"),
	"egyetem": Building(_cost_M=3000, _area=5500, _stories=4, _reliability=95, _type="iskola", _name="egyetem"),
}

upgrades = {#_cost_M(millio), _finish_days(napban), _per_100(méretarányos), _effects(hatásai)
	"energetikai korszerűsítés": Upgrade(_cost_M=3, _finish_days=150, _per_100=True, _min_requirements={"age":5}, _effects={"quality": 3, "reliability": 20}),
	"bővítés": Upgrade(_cost_M=3, _finish_days=30, _per_100=True, _min_requirements={}, _effects={"space": 30}),
	"szigetelés": Upgrade(_cost_M=3, _finish_days=30, _per_100=True, _min_requirements={}, _effects={"quality": 2.5}),
	"tetőcsere": Upgrade(_cost_M=3, _finish_days=30, _per_100=True, _min_requirements={}, _effects={"reliability": 30}),
	"lift beépítés": Upgrade(_cost_M=5, _finish_days=60, _per_100=False, _min_requirements={"stories":2}, _effects={"quality": 2.5})
}
disasters = {# _stranght(a katasztrófa mértéke), _hapiness_decrease(boldogság csökkenése), _chance(esély a bekövetkezésre)
	"cunami": Disaster( _stranght=4, _hapiness_decrease=28, _chance=0.22),
	"tornádó": Disaster( _stranght=3, _hapiness_decrease=30, _chance=0.33),
	"tűz": Disaster( _stranght=2, _hapiness_decrease=10,_chance=0.20),
	"bombázás": Disaster( _stranght=4, _hapiness_decrease=35, _chance=0.41),
	"vulkán": Disaster( _stranght=5, _hapiness_decrease=25, _chance=0.09),
	"nincs katasztrófa": Disaster(_chance=2)
	}