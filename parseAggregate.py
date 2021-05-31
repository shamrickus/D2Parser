import os
from typing import Type

from baseEquipment import BaseEquipment
from parser import Parser


class ParseAggregate:
	def __init__(self, items: [BaseEquipment], itemClass: Type[BaseEquipment], parser: Parser):
		self.items = items
		self.cls = itemClass
		self.parser = parser

	def parse(self, runes):
		for item in self.items:
			itemRunes = [r for r in runes if r.letter in item.runes]
			for itype in item.itypes:
				if itype.isShield():
					type = "Shield"
				elif itype.isWeapon():
					type = "Weapon"
				elif itype.isArmor():
					type = "Armor"

			for rune in itemRunes:
				for runeProp in rune._props[type]:
					item.add(runeProp, self.parser)

	def writeJSON(self):
		with open(os.getcwd() + self.cls.getName().replace("csv", "ts"), "w") as file:
			file.write("[")
			for item in self.items:
				file.write(item.json() + ",")
			file.write("];")
