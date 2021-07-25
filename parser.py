import csv
import os
import re
import sys
import urllib.request
from typing import Type, Tuple

from baseParser import BaseParser
from monstat import MonStatParser
from property import Property
from property import PropertyParse
from skills import SkillParser
from utils import isdebugging

getSkillId = (lambda par, skills: [skill for skill in skills if skill.id == par])
getSkillSkill = (lambda par, skills: [skill for skill in skills if skill.skill.lower() == par.lower()])
getMonster = (lambda x, monsters: [mon for mon in monsters if mon.id == x.par])
class Parser:
	skills: [SkillParser] = []
	definedProperties: [PropertyParse] = []
	monsters: [MonStatParser] = []
	version: str = ""

	def __init__(self, version: str):
		self.skills = self.read(SkillParser)
		self.definedProperties = self.read(PropertyParse)
		self.monsters = self.read(MonStatParser)
		self.version = version

	def read(self, cls: Type[BaseParser], dl=False) -> [BaseParser]:
		return BaseParserCreator.read(cls, self, self.version, dl)

	def findInCommon(self, property: Property) -> str:
		classes = {}
		skillBeg = int(property.min)
		skillEnd = int(property.max)
		for skillI in range(skillBeg, skillEnd):
			sk = self.getSk(skillI)
			if sk.char not in classes and len(classes) == 0:
				classes[sk.char] = True
			else:
				return "Random Level {} skill ({} possibilities)".format(property.par, skillEnd-skillBeg)
		cls = classes.keys()[0]
		return "Random Level {} {} skill".format(property.par, cls)

	def getSk(self, skillId) -> SkillParser:
		skill = getSkillId(skillId, self.skills)
		if not skill:
			skill = getSkillSkill(skillId, self.skills)
		if not skill:
			print("Unable to get skill for property {}".format(skillId))
			sys.exit()
		return skill

	def parseSkill(self, property) -> str:
		global skills
		if property.prop == "skill-rand":
			return self.findInCommon(property)

		skill = self.getSk(property.par)

		if property.prop == "skill":
			if(len(skill)):
				skill = skill[0]
				#TODO
				return "+{} to {} ({} Only)".format(generateRange(property), skill.skill, skill.char)
			else:
				return "+{} to {} (Class Only)".format(generateRange(property), property.par)
		elif property.prop == "att-skill":
			return "{}% Chance To Cast Level {} {} On Attack".format(property.min, property.max, property.par)
		elif property.prop == "oskill":
			if len(skill):
				skill = skill[0]
			return "+{} to {}".format(generateRange(property), skill.skill)
			#return "Level {} {} ({} Charges)".format(int(int(property.min)/3), skill.skill, property.max)
		elif property.prop == "kill-skill":
			when = "Kill An Enemy"
		elif property.prop == "levelup-skill":
			when = "Level-Up"
		elif property.prop == "death-skill":
			when = "Die"
		else:
			print("Unknown skill property {}".format(property.prop))
			sys.exit()
		return "{}% Chance To Cast Level {} {} When you {}".format(property.min, property.max, property.par, when)

	def parseReanimate(self, property) -> str:
		if property.prop == "reanimate":
			monster = getMonster(property, self.monsters)[0]
			return "{} Reanimate As: {}".format(generateRange(property, "%"), monster)
		else:
			print("Unknown reanimate {}".format(property.prop))
			sys.exit()

	def validateProperty(self, property: Property) -> str:
		x = property
		matched = 0
		if x.prop.startswith("*"):
			if isdebugging():
				print("Got star prop " + x.prop)
			x.prop = x.prop[1:]
		for prop in self.definedProperties:
			if prop.code == x.prop:
				matched += 1
		if matched != 1:
			print("Property {} is not valid".format(property.prop))
			sys.exit()

	def parse(self, properties: [Property]):
		poisonDmgProps: [Tuple[Property, int]] = []
		coldDmgProps: [Tuple[Property, int]] = []
		for k, property in enumerate(properties):
			parsed = None
			minMax = re.compile("[A-Za-z]+\-(min|max)")
			dmg = re.compile("dmg\-[a-z]+")
			pierce = re.compile('pierce\-[A-Za-z]+')
			res = re.compile('res\-[A-Za-z]+')
			resLen = re.compile('res\-[A-Za-z]+\-len')
			abs = re.compile('abs\-[A-Za-z]+')
			red = re.compile('red\-[A-Za-z]+')
			extra = re.compile('extra\-[A-Za-z]+')
			star = re.compile('\*.+')
			dot = re.compile("(pois|cold)-len")
			self.validateProperty(property)
			if property.prop is None:
				print("cant")
			elif property.prop == "dmg":
				parsed = "{} Damage".format(generateRange(property))
			elif property.prop == "dmg%":
				parsed = "{} Enhanced Damage".format(generateRange(property, "%"))
			elif property.prop == "dmg%/lvl":
				parsed = "{} Enhanced Damage (Based on Character Level)".format(generateRange(property, "%"))
			elif re.match(dot, property.prop):
				property.mult(1/25)
				if property.prop.startswith("cold"):
					coldDmgProps.append((property, k))
				elif property.prop.startswith("pois"):
					poisonDmgProps.append((property, k))
				parsed = "This should not be seen"
			elif re.match(star, property.prop):

				print("Got star property: {}".format(property.prop))
			elif re.match(red, property.prop):
				ret = "{}Damage Reduced By {}"
				if property.prop == "red-mag":
					type = "Magic "
				else:
					type = ""
				parsed = ret.format(type, generateRange(property))
			elif re.match(minMax, property.prop):
				type=""
				if(property.prop.startswith("cold")):
					coldDmgProps.append((property, k))
				elif(property.prop.startswith("pois")):
					poisonDmgProps.append((property, k))
				elif(property.prop.endswith("max")):
					type = "Maximum"
				elif(property.prop.endswith("min")):
					type = "Minimum"
				parsed = "+{} To {} Damage".format(generateRange(property), type)
			elif re.match(abs, property.prop):
				type = tagToString(property.prop)
				parsed = "{} Absorb +{}".format(type, generateRange(property, "%"))
			elif re.match(resLen, property.prop):
				if property.prop == "res-pois-len":
					parsed = "Poison Length Reduced by {}".format(generateRange(property, "%"))
				else:
					print("Unknown reduce length {}".format(property.prop))
					sys.exit()
			elif re.match(res, property.prop):
				if property.prop == "res-all":
					parsed = "All Resistances +{}".format(generateRange(property))
				else:
					type = ""
					if property.prop == "res-all-max":
						type = "Maximum Poison/Fire/Cold/Lightning"
					elif "max" in property.prop:
						type = "Maximum "
					else:
						type += tagToString(property.prop)
					parsed = "{} Resistance +{}".format(type, generateRange(property, "%"))
					if "/lvl" in property.prop:
						parsed += " (Based on Character Level)"
			elif re.match(pierce, property.prop):
				type = tagToString(property.prop)
				parsed = "-{} To Enemy {} Resistance".format(generateRange(property, "%"), type)
			elif re.match(dmg, property.prop):
				if(property.prop == "dmg-undead"):
					parsed = "+{} Damage To Undead".format(generateRange(property, "%"))
				elif(property.prop == "dmg-und/lvl"):
					parsed = "+{} Damage To Undead (Based on Character Level)".format(generateRange(property, "%"))
				elif(property.prop == "dmg-demon"):
					parsed = "+{} Damage To Demons".format(generateRange(property, "%"))
				elif(property.prop == "dmg-dem/lvl"):
					parsed = "+{} Damage To Demons (Based On Character Level)".format(generateRange(property, "%"))
				elif property.prop == "dmg-to-mana":
					parsed = "{} Damage Taken Goes to Mana".format(generateRange(property, "%"))
				else:
					if (property.prop == "dmg-ac"):
						parsed = "{} To Monster Defense Per Hit".format(generateRange(property))
					elif property.prop == "dmg-elem":
						parsed = "+{} Fire/Cold/Lightning Damage".format(generateRange(property))
					else:
						ret = "Adds " + generateRange(property)
						if (property.prop == "dmg-ltng"):
							ret += "Lightning"
						elif (property.prop == "dmg-cold"):
							ret += "Cold"
						elif (property.prop == "dmg-fire"):
							ret += "Fire"
						elif (property.prop == "dmg-pois"):
							ret += "Poison"
						elif (property.prop == "dmg-mag"):
							ret += "Magic"
						elif (property.prop == "dmg-norm"):
							pass
						else:
							print("Unknown add damage: {}".format(property.prop))
							sys.exit()
						parsed = ret  + " Damage"
			elif re.match(extra, property.prop):
				if property.prop == "extra-pois":
					type = "Poison"
				elif property.prop == "extra-cold":
					type = "Cold"
				elif property.prop == "extra-fire":
					type = "Fire"
				elif property.prop == "extra-ltng":
					type = "Lightning"
				parsed = "+{} To {} Skill Damage".format(generateRange(property), type)

			elif property.prop in ["skill", "kill-skill", "levelup-skill", "death-skill", "att-skill", "oskill", "skill-rand"]:
				parsed = self.parseSkill(property)
			elif property.prop == "reanimate":
				self.parseReanimate(property)
			elif property.prop == "fireskill":
				parsed = "+{} To Fire Skills".format(generateRange(property))
			elif property.prop == "skilltab":
				parsed = "+{} To Skill Tab {} (TODO)".format(generateRange(property), property.par)
			elif property.prop in ["sor", 'nec', 'bar', 'pal', 'ass', 'dru', 'ama']:
				#TODO
				parsed = "+{} To Char skill".format(generateRange(property))
			elif property.prop == "res-all":
				parsed = "All Resistances +{}".format(generateRange(property))
			elif property.prop == "aura":
				parsed = "Level {} {} Aura When Equipped".format(generateRange(property), property.par)
			elif property.prop in ["swing1","swing2","swing3"]:
				parsed = "{} Increased Attack Speed".format(generateRange(property, "%"))
			elif property.prop == "all-stats":
				parsed = "+{} To All Attributes".format(generateRange(property))
			elif property.prop == "light":
				parsed = "+{} To Light Radius".format(generateRange(property))
			elif property.prop == "stupidity":
				parsed = "Hit Blinds Target"
			elif property.prop == "allskills":
				parsed = "+{} To All Skills".format(generateRange(property))
			elif property.prop == "":
				parsed = ""
			elif property.prop == "balance1":
				parsed = "+{} Faster Hit Recovery".format(generateRange(property, "%"))
			elif property.prop == "balance2":
				parsed = "+{} Faster Hit Recovery".format(generateRange(property, "%"))
			elif property.prop == "balance3":
				parsed = "+{} Faster Hit Recovery".format(generateRange(property, "%"))
			elif property.prop == "hit-skill":
				parsed = "{}% Chance To Cast Level {} {} On Striking".format(min, max, property.par)
			elif property.prop == "gethit-skill":
				parsed = "{}% Chance To Cast Level {} {} When Struck".format(min, max, property.par)
			elif property.prop == "ethereal":
				parsed = "Ethereal"
			elif property.prop == "indestruct":
				parsed = "Indestructible"
			elif property.prop == "rep-dur":
				parsed = "Repairs Durability {} in 4 Seconds".format(property.par)
			elif property.prop == "knock":
				parsed = "Knockback"
			elif property.prop == "mana/lvl":
				val = int(property.par) / 8
				parsed = "+{}-{} To Mana (Based On Character Level)".format(val, val * 111)
			elif property.prop == "regen-mana":
				parsed = "Regenerate Mana {}".format(generateRange(property, "%"))
			elif property.prop == "mana%":
				parsed = "Increase Maximum Mana {}".format(generateRange(property, "%"))
			elif property.prop in ["cast1", "cast2", "cast3"]:
				parsed = "{} Faster Cast Rate".format(generateRange(property, "%"))
			elif property.prop == "hp" or property.prop == "mana":
				if property.prop == "hp":
					type = "Life"
				else:
					type = "Mana"
				parsed = "+{} To {}".format(generateRange(property), type)
			elif property.prop == "hp/lvl":
				parsed = "+{} To Life (Based on Character Level)".format(generateRange(property))
			elif property.prop == "explosivearrow":
				parsed = "FIres Explosive Arrows or Bolts ({})".format(generateRange(property))
			elif property.prop == "cheap":
				parsed = "Reduces All Vendor Prices {}".format(generateRange(property, "%"))
			elif property.prop == "mag%":
				parsed = "{} Better Chance of Getting Magic Items".format(generateRange(property, "%"))
			elif property.prop == "mag%/lvl":
				parsed = "+{} Better Chance of Getting Magical Items (Based On Character Level)".format(
					generateRange(property))
			elif property.prop == "red-dmg%":
				parsed = "Damage Reduced By {}".format(generateRange(property, "%"))
			elif property.prop == "str":
				parsed = "+{} to Strength".format(generateRange(property))
			elif property.prop == "str/lvl":
				parsed = "+{} To Strength (Based On Character Level)".format(property)
			elif property.prop == "dex":
				parsed = "+{} to Dexterity".format(generateRange(property))
			elif property.prop == "dex/lvl":
				parsed = "+{} To Dexterity (Based On Character Level)".format(property)
			elif property.prop == "enr":
				parsed = "+{} to Energy".format(generateRange(property))
			elif property.prop == "enr/lvl":
				parsed = "+{} To Energy (Based On Character Level)".format(property)
			elif property.prop == "vit":
				parsed = "+{} to Vitality".format(generateRange(property))
			elif property.prop == "vit/lvl":
				parsed = "vit/lvl"
			elif property.prop == "slow":
				parsed = "Slows Target By {}".format(generateRange(property, "%"))
			elif property.prop == "ac":
				parsed = "+{} Defense".format(generateRange(property))
			elif property.prop == "ac/lvl":
				if(property.min == "" or property.max == ""):
					property.min = property.par
					property.max = property.par
				property.min=str(int(int(property.min)/8))
				property.max=str(int(int(property.max)/8))
				parsed = "+{} To Defense (Based On Character Level)".format(generateRange(property))
			elif property.prop == "ac%":
				parsed = "+{} Enhanced Defense".format(generateRange(property, "%"))
			elif property.prop == "ac-miss":
				parsed = "+{} Defense Vs. Missle".format(generateRange(property))
			elif property.prop == "ignore-ac":
				parsed = "Ignores Target's Defense"
			elif property.prop == "reduce-ac":
				parsed = "-{} Target Defense".format(generateRange(property, "%"))
			elif property.prop == "hp%":
				parsed = "Increase Maximum Life {}".format(generateRange(property, "%"))
			elif property.prop == "att%":
				parsed = "{} Bonus To Attack Rating".format(generateRange(property, "%"))
			elif property.prop == "att":
				parsed = "+{} To Attack Rating".format(generateRange(property))
			elif property.prop == "att-undead":
				parsed = "+{} To Attack Rating Against Undead".format(generateRange(property))
			elif property.prop == "att-und/lvl":
				parsed = "+{} To Attack Rating Against Undead (Based on Character Level)".format(
					generateRange(property))
			elif property.prop == "att-demon":
				parsed = "+{} Damage to Demons".format(generateRange(property, "%"))
			elif property.prop == "att-dem/lvl":
				parsed = "+{} Damage to Demons (Based on Character Level)".format(generateRange(property, "%"))
			elif property.prop == "demon-heal":
				parsed = "+{} Life After Each Demon Kill".format(generateRange(property))
			elif property.prop == "noheal":
				parsed = "Prevent Monster Heal"
			elif property.prop == "heal-kill":
				parsed = "+{} Life After Each Kill".format(generateRange(property))
			elif property.prop == "ease":
				parsed = "Requirements {}".format(generateRange(property, "%"))
			elif property.prop == "nofreeze":
				parsed = "Cannot be Frozen"
			elif property.prop == "freeze":
				parsed = "Freezes Target +{}".format(generateRange(property))
			elif property.prop == "half-freeze":
				parsed = "Half Freeze Duration"
			elif property.prop == "block1":
				parsed = "+{} Faster Block Rate".format(generateRange(property, "%"))
			elif property.prop == "block2":
				parsed = "+{} Faster Block Rate".format(generateRange(property, "%"))
			elif property.prop == "block3":
				parsed = "+{} Faster Block Rate".format(generateRange(property, "%"))
			elif property.prop == "block":
				parsed = "{} Increased Chance of Blocking".format(generateRange(property, "%"))
			elif property.prop == "howl":
				parsed = "Hit Causes Monster to Flee {}".format(generateRange(property, "%"))
			elif property.prop == "gold%":
				parsed = "{} Extra Gold From Monsters".format(generateRange(property, "%"))
			elif property.prop == "gold%/lvl":
				parsed = "{} Extra Gold From Monsters (Based on Character Level)".format(generateRange(property, "%"))
			elif property.prop == "manasteal":
				parsed = "{} Mana Stolen Per Hit".format(generateRange(property, "%"))
			elif property.prop == "lifesteal":
				parsed = "{} Life Stolen Per Hit".format(generateRange(property, "%"))
			elif property.prop == "deadly":
				parsed = "{} Deadly Strike".format(generateRange(property, "%"))
			elif property.prop == "deadly/lvl":
				parsed = "+{} Deadly Strike (Based on Character Level)".format(generateRange(property))
			elif property.prop == "regen":
				parsed = "Replenish Life {}".format(generateRange(property))
			elif property.prop == "regen-mana":
				parsed = "Regenerate Mana {}".format(generateRange(property, "%"))
			elif property.prop == "mana-kill":
				parsed = "+{} to Mana After Each Kill".format(generateRange(property))
			elif property.prop == "openwounds":
				parsed = "{} Chance of Open Wounds".format(generateRange(property, "%"))
			elif property.prop == "crush":
				parsed = "{} Chance of Crushing Blow".format(generateRange(property, "%"))
			elif property.prop == "thorns":
				parsed = "Attacker Takes Damage of {}".format(generateRange(property))
			elif property.prop == "rip":
				parsed = "Slain Monsters Rest in Peace"
			elif property.prop == "move2":
				parsed = "{} Faster Run Walk".format(generateRange(property, "%"))
			elif property.prop == "move3":
				parsed = "{} Faster Run Walk".format(generateRange(property, "%"))
			elif property.prop == "att/lvl":
				property.mult(.5)
				parsed = "{} to Attack Rating (Based on Chracter Level)".format(generateRange(property))
			elif property.prop == "dmg/lvl":
				property.mult(1/8)
				parsed = "{} to Maximum Damage (Based on Character Level)".format(generateRange(property))
			elif property.prop == "addxp":
				parsed = "{} to Experience Gained".format(generateRange(property, "%"))
			elif property.prop == "rep-quant":
				y = 100/int(property.par)
				z = y/int(property.par)
				property.mult(z)
				parsed = "Replenishes Quantity (1 in {} sec)".format(generateRange(property))
			elif property.prop  == "state":
				# TODO
				parsed = "Monster Set {} TODO".format(property.par.split("-")[-1])
			elif property.prop == "pierce":
				# TODO
				parsed = "Attacks Pierce target TODO"
			elif property.prop == "stack":
				parsed = "Increased stack size {}".format(generateRange(property))
			elif property.prop == "splash":
				# TODO
				if property.par == "proc_SplashDamage":
					parsed = "Attacks Spalsh TODO"
			elif property.prop == "magicarrow":
				parsed = "Fires Level {} Magic Arrows/Bolts".format(generateRange(property))
			elif property.prop == "ac-hth":
				parsed = "+{} Defense vs. Melee".format(generateRange(property))
			elif property.prop == "bloody":
				# TODO not visible
				parsed = "Extra Blood {}".format(generateRange(property))
			else:
				print("Unable to parse " + str(property))
				sys.exit()
			if parsed == "":
				print("Property {} did not get parsed!".format(property.prop))
				sys.exit()
			property.parsed = parsed
			properties[k] = property

		byType = (lambda typ, props: [x for x in props if typ in x[0].prop])
		validProp = re.compile("(pois|cold)-(len|min|max)")
		def mergeDmgProps(props: [Property], typ: str):
			if len(props) == 3 and len([x for x in props if re.match(validProp, x[0].prop)]) == 3:
				lenProp = byType("len", props)[0]
				minProp = byType("min", props)[0]
				maxProp = byType("max", props)[0]
				properties[lenProp[1]].parsed = "Adds {}-{} {} Damage, Duration: {} seconds".format(
					generateRange(minProp[0]), generateRange(maxProp[0]), typ, generateRange(lenProp[0]))
				properties.remove(minProp[0])
				properties.remove(maxProp[0])
			elif len(props) != 0:
				print("Mismatched number of poison properties " + len(props))

		mergeDmgProps(poisonDmgProps, "Poison")
		mergeDmgProps(coldDmgProps, "Cold")

		return properties

def tagToString(prop) -> str:
	if "ltng" in prop:
		return "Lightning"
	elif "cold" in prop:
		return "Cold"
	elif "fire" in prop:
		return "Fire"
	elif "pois" in prop:
		return "Poison"
	elif "mag" in prop:
		return "Magic"
	else:
		print("Unknown prop " + prop)
		sys.exit()


def generateRange(prop, append=""):
	if prop.min == "" and prop.max == "" and prop.par != "":
		return "{}{}".format(prop.par, append)
	else:
		if prop.min == prop.max:
			return prop.min + append
		return "{}-{}{}".format(prop.min, prop.max, append)

class BaseParserCreator:
	@staticmethod
	def read(cls: Type[BaseParser], parser: Parser, version: str, dl=False) -> [BaseParser]:
		items = []
		path = os.path.join(os.getcwd(), "versions", version, cls.getName()+".txt")
		try:
			with open(path, 'r') as file:
				reader = csv.DictReader(file, delimiter='\t')
				for line in reader:
					item = cls(dict(line))
					item.parse(parser)
					if item.verify():
						items.append(item)
						if dl:
							BaseParserCreator.Download(item)
					else:
						print("bad ({})".format(item.name) + str(item))
		except FileNotFoundError:
			print("Unable to find %s" % path)
			sys.exit()


		return items

	@staticmethod
	def Download(cls: Type[BaseParser]):
		name = cls.fileName()
		url = "http://classic.battle.net/images/battle/diablo2exp/images/{}".format(name) + "/{}.gif"
		gemName = cls.Name().replace(" ", "")
		nurl = url.format(gemName)
		try:
			try:
				os.mkdir(os.path.join('Images', name))
			except:
				pass
			imgName = os.path.join("Images", name, cls.FileName)
			urllib.request.urlretrieve(nurl, imgName)
			cls.img = imgName
		except Exception:
			print("Unable to parse {} url {}".format(gemName, nurl))
