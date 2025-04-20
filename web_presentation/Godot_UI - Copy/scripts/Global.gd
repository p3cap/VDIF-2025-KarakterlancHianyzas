extends Node

var sim_const = { #area calcuated in m2
	"currency_type": "HUF",
	"area_for_citizen": 30,
	"citizen_age_skpektrum": [0,80],
	"tax_payer_spektrum": [18,60],
	"no_tax_jobs":["munkanélküli","tanuló","nyugdíjas"],
	"min_happiness": 20,
	"max_happiness": 100,
	"max_days": 30000,
	"tax_per_citizen": 50000,
	"area_per_service": 5, #mekkore terület után számít fel szolgáltatást egy meberre
	"service_requirements": { #%of pupultion, that will accumlate happiness
		"egészségügy": 0.3,#10%
		"munkahely": 0.9,
		"oktatás": 0.25,
		"közlekedés": 0.8,
		"rendőrség": 0.4,
		"bolt": 0.4,
	}
}

class Building:
	var built: int
	var cost: int
	var area: int
	var stories: int
	var reliability: int
	var finish_days: int
	var type: String
	var services: Array
	var bld_name: String
	var quality: int
	var finish_dict: Dictionary

	func _init(_name: String = "",_cost_M: int = 0, _area : int = 0, _stories: int = 0, _reliability: int = 0, _type: String = "lakóház", _services: Array = [],_finish_days: int = 100):
		cost = _cost_M
		area = _area
		stories = _stories
		reliability = _reliability
		finish_days = _finish_days
		type = _type
		services = _services
		bld_name = _name if _name != "" else "N/A"
		quality = 5
		finish_dict = Data.user_data["buildings"]

	func Upgrade(upg):
		if upg == null:
			return
		for key in upg.effects.keys():
			var value = upg.effects[key]
			self.key = self.get(key) + value

	func get_valid_upgs(upgrades) -> Array:
		var valid_upgrades = []
		for upg in upgrades:
			for key in upg.min_req.keys():
				var req = upg.min_req[key]
				var value = self.key
				if value >= req:
					valid_upgrades.append(upg)
		return valid_upgrades

class Upgrade:
	var upg_name : String
	var cost : int
	var finish_days : int
	var per_100 : bool
	var min_req : Dictionary
	var effects : Dictionary
	var started : int = 0
	var finish_dict = null

	func _init(_name: String, _cost_M: int, _finish_days: int, _per_100: bool, _min_requirements: Dictionary, _effects: Dictionary):
		upg_name = _name
		cost = _cost_M
		finish_days = _finish_days
		per_100 = _per_100
		min_req = _min_requirements
		effects = _effects

class Disaster:
	var dst_name : String
	var strength : float
	var chance : float

	func _init(_name: String, _strength: float, _chance: float = 0.0):
		dst_name = _name
		strength = _strength
		chance = _chance

	func activate() -> Dictionary:
		var dis_info = {
			"size": randi_range(1,5),
			"damaged_builds": {},
			"repair_cost_M": 0
		}

		for Id in Data.user_data["buildings"].keys():
			var bld = Data.user_data["buildings"][Id]
			if randi_range(1, 5) <= dis_info["size"]:
				var new_quality = max(0, bld.quality - randi_range(0, strength))
				dis_info["damaged_builds"][Id] = bld.quality
				dis_info["repair_cost_M"] += (bld.quality - new_quality) * 0.05 * bld.cost
				bld.quality = new_quality

		return dis_info

	func repair(dis_info: Dictionary) -> void:
		print("%d buildings repaired, %fM cost..." % [dis_info["damaged_builds"].size(), dis_info["repair_cost_M"]])
		Data.user_data["currency_M"] -= dis_info["repair_cost_M"]
		for Id in dis_info["damaged_builds"].keys():
			var org_quality = dis_info["damaged_builds"][Id]
			Data.user_data["buildings"][Id].quality = org_quality

var buildings
var upgrades
var disasters
func _ready():
	buildings = [
		# Lakó
		Building.new("családi ház", 60, 150, 1, 98, "lakóház", [], 200),
		Building.new("ikerház", 75, 300, 2, 98, "lakóház", [], 250),
		Building.new("társasház", 250, 1000, 4, 95, "lakóház", [], 400),
		Building.new("lakótelepi épület", 900, 6000, 10, 89, "lakóház", [], 700),

		# Egészség
		Building.new("mini rendelő", 90, 100, 1, 92, "kórház", ["egészségügy"], 250),
		Building.new("szakorvosi rendelő", 600, 1200, 2, 90, "kórház", ["egészségügy"], 400),
		Building.new("kórház", 2800, 5000, 4, 90, "kórház", ["egészségügy"], 800),
		Building.new("klinikai központ", 6000, 10000, 6, 88, "kórház", ["egészségügy"], 1000),

		# Oktatás
		Building.new("óvoda", 325, 500, 2, 93, "oktatás", ["oktatás"], 300),
		Building.new("általános iskola", 1200, 3000, 3, 94, "oktatás", ["oktatás"], 500),
		Building.new("középiskola", 2000, 4000, 4, 95, "oktatás", ["oktatás"], 700),
		Building.new("egyetem", 3000, 5500, 4, 95, "oktatás", ["oktatás"], 900),

		# Munka
		Building.new("kisbolt", 250, 300, 1, 97, "munka", ["munkahely", "bolt"], 150),
		Building.new("irodaház", 1500, 10000, 5, 95, "munka", ["munkahely"], 600),
		Building.new("bevásárlóközpont", 5000, 20000, 3, 90, "munka", ["munkahely", "bolt"], 800),
		Building.new("ipari park", 10000, 50000, 2, 85, "munka", ["munkahely"], 1200),

		# Közlekedés
		Building.new("autóbusz megálló", 50, 50, 1, 99, "közlekedés", ["közlekedés"], 50),
		Building.new("buszpályaudvar", 800, 3000, 1, 85, "közlekedés", ["közlekedés"], 400),
		Building.new("vasútállomás", 1200, 5000, 2, 88, "közlekedés", ["közlekedés"], 600),
		Building.new("repülőtér", 20000, 100000, 3, 80, "közlekedés", ["közlekedés"], 1500),

		# Rendőrség
		Building.new("rendőrőrs", 1200, 1500, 2, 95, "rendőrség", ["rendőrség"], 500),
		Building.new("rendőrkapitányság", 5000, 8000, 4, 90, "rendőrség", ["rendőrség"], 800)
	]

	upgrades = [
		Upgrade.new("energetikai korszerűsítés", 0.3, 150, true, {}, {"quality": 3, "reliability": 20}),
		Upgrade.new("bővítés", 0.3, 30, true, {"area": 200}, {"space": 30}),
		Upgrade.new("szigetelés", 0.3, 30, true, {}, {"quality": 2.5}),
		Upgrade.new("tetőcsere", 0.3, 30, true, {}, {"reliability": 30}),
		Upgrade.new("lift beépítés", 5, 60, false, {"stories": 3}, {"quality": 2.5}),
		Upgrade.new("napkollektor telepítés", 0.5, 45, false, {"stories": 1}, {"quality": 4, "reliability": 10}),
		Upgrade.new("okosotthon rendszer", 0.7, 60, false, {"type": "lakó"}, {"quality": 5, "reliability": 5}),
		
		Upgrade.new("hőszivattyú", 1, 45, false, {"type": "lakó"}, {"quality": 3, "reliability": 5}),
		Upgrade.new("biztonsági rendszer", 0.6, 30, false, {"type": "munka"}, {"reliability": 10}),
		Upgrade.new("térfigyelő kamerák", 0.4, 25, false, {"type": "közlekedés"}, {"reliability": 7}),
		Upgrade.new("környezetbarát burkolatok", 0.3, 20, true, {"area": 500}, {"quality": 2}),
		Upgrade.new("zöldtető", 1.5, 90, false, {"stories": 2}, {"quality": 5, "reliability": 3}),
		Upgrade.new("elektromos töltőállomás", 2, 60, false, {"type": "munka"}, {"quality": 4}),
		Upgrade.new("intelligens világítás", 0.5, 40, false, {}, {"quality": 3, "reliability": 2}),
		Upgrade.new("modern csatornarendszer", 1, 60, true, {"area": 1000}, {"reliability": 8}),
		Upgrade.new("hangszigetelés", 0.8, 50, true, {"type": "lakó"}, {"quality": 3}),
	]
	disasters = [
		Disaster.new("cunami",4, 0.22),
		Disaster.new("tornádó",3, 0.33),
		Disaster.new("tűz",2, 0.20),
		Disaster.new("bombázás",4, 0.41),
		Disaster.new("vulkán",5, 0.09),
		Disaster.new("nincs katasztrófa",0, 800)
	]
