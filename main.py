from gems import GemsParser
from itemTypes import ItemTypeParser
from parseAggregate import ParseAggregate
from parser import Parser
from runeword import RunewordParser
from setItem import SetItemParser
from unique import UniqueParser

if __name__ == "__main__":
	psr = Parser()
	print("Loading Item Types")
	types = psr.read(ItemTypeParser)
	typesByCode = dict()
	for t in types:
		typesByCode[t.code] = t
	master = "weap"
	weapon = typesByCode[master]

	print("Loading Gems/Runes")
	gems = psr.read(GemsParser, True)
	print("Downloading Images")

	print("Loading Runewords")
	items = psr.read(RunewordParser)
	itemAggregate = ParseAggregate(items, RunewordParser, psr)

	print("Loading Uniq")
	otherItems = psr.read(UniqueParser)
	itmAggregate = ParseAggregate(otherItems, UniqueParser, psr)

	print("Loading Set")
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

	d = 2
