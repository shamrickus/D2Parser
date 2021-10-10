import os
import sys
import logging

from gems import GemsParser
from itemTypes import ItemTypeParser
from parseAggregate import ParseAggregate
from parser import Parser
from runeword import RunewordParser
from setItem import SetItemParser
from unique import UniqueParser

if __name__ == "__main__":
	logging.basicConfig(stream=sys.stdout, level=logging.INFO)
	logger = logging.getLogger("main")

	mods = {}
	for modName in os.listdir(os.path.join(os.getcwd(), "versions")):
		mods[modName] = []
		for version in os.listdir(os.path.join(os.getcwd(), "versions", modName)):
			mods[modName].append(version)

	logger.info("Mods detected")
	for modName in mods.keys():
		logger.info('%s' % modName)
		for version in mods[modName]:
			logger.info("\t%s" % version)

	psr: Parser = None
	if len(sys.argv) == 3:
		psr = Parser(sys.argv[1], sys.argv[2])
	else:
		psr = Parser(list(mods.keys())[0], mods[list(mods.keys())[0]][0])
	logger.info("Loading Item Types")
	types = psr.read(ItemTypeParser)
	typesByCode = dict()
	for t in types:
		typesByCode[t.code] = t
	master = "weap"
	weapon = typesByCode[master]

	logger.info("Loading Gems/Runes")
	gems = psr.read(GemsParser)

	logger.info("Loading Runewords")
	items = psr.read(RunewordParser)
	itemAggregate = ParseAggregate(items, RunewordParser, psr)

	logger.info("Loading Uniq")
	otherItems = psr.read(UniqueParser)
	itmAggregate = ParseAggregate(otherItems, UniqueParser, psr)

	logger.info("Loading Set")
	setItems = psr.read(SetItemParser)
	setAgg = ParseAggregate(setItems, SetItemParser, psr)

	runes: [GemsParser] = [x for x in gems if x.isRune()]
	byName: [GemsParser] = (lambda x: [rune for rune in runes if rune.code == x])
	byCode: [ItemTypeParser] = (lambda x: [type for type in types if type.code == x])

	def replaceRunes(itemsAgg: ParseAggregate):
		for i, item in enumerate(itemsAgg.items):
			for j, rune in enumerate(item.runes):
				itemsAgg.items[i].runes[j] = byName(rune)[0].letter

	def replaceItems(itemsAgg: ParseAggregate):
		for i, item in enumerate(itemsAgg.items):
			for j, type in enumerate(item.itypes):
				itemsAgg.items[i].itypes[j] = byCode(type)[0]


	replaceRunes(itemAggregate)
	replaceItems(itemAggregate)
	replaceItems(itmAggregate)
	replaceItems(setAgg)
	itemAggregate.parse(runes)

	itemAggregate.writeJSON(items[0].getOutputName())

	d = 2
