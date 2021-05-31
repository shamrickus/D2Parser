from gems import Socketable
from itemTypes import ItemType
from parseAggregate import ParseAggregate
from parser import Parser
from runeword import Runeword, Uniq, SetItem

if __name__ == "__main__":
	psr = Parser()
	print("Loading Item Types")
	types = psr.read(ItemType)
	typesByCode = dict()
	for t in types:
		typesByCode[t.code] = t
	master = "weap"
	weapon = typesByCode[master]

	# getChildren = lambda code: [x for x in types if x.equiv1 == code or x.equiv == code]
	# children = getChildren(weapon.code)
	# weapon.children = []
	# weapon.children.extend(children)
	# for c in children:
	# 	c.parents.append(weapon)
	# 	child = getChildren(c.code)
	# 	if len(child) > 0:
	# 		c.children.extend(child)
	# 		children.extend(child)
	# 	for d in child:
	# 		d.parents.append(c)
	#
	# for typ in children:
	# 	print(typ.name)
	# 	for c in typ.children:
	# 		print("\t" + c.name)
	#
	# with open("asdf.json", "w") as s:
	# 	s.write(weapon.json())
	#
	# with open("parents.json", "w") as s:
	# 	out = "["
	# 	for c in types:
	# 		out += "{\"name\": \"%ss\", \"parents\": [" % c.name
	# 		parents = c.allParents()
	# 		for p in set(parents):
	# 			out += "\"%ss\"," % p.name
	# 		if len(parents) > 0:
	# 			out = out[:-1]
	# 		out += "]},"
	# 	out += "]"
	# 	s.write(out)
	#
	# with open("children.json", "w") as s:
	# 	out = "["
	# 	for c in children:
	# 		out += "{\"name\": \"%ss\", \"children\": [" % (c.name)
	# 		for tc in c.allChildren():
	# 			out += "\"%ss\"," % tc.name
	# 		out += "]},"
	# 	out += "]"
	# 	s.write(out)
	#
	# exit()

	print("Loading Gems/Runes")
	gems = psr.read(Socketable, True)
	print("Downloading Images")

	print("Loading Runewords")
	items = psr.read(Runeword)
	itemAggregate = ParseAggregate(items, Runeword, psr)

	print("Loading Uniq")
	otherItems = psr.read(Uniq)
	itmAggregate = ParseAggregate(otherItems, Uniq, psr)

	print("Loading Set")
	setItems = psr.read(SetItem)
	setAgg = ParseAggregate(setItems, SetItem, psr)

	runes: [Socketable] = [x for x in gems if x.isRune()]
	byName: [Socketable] = (lambda x: [rune for rune in runes if rune.code == x])
	byCode: [ItemType] = (lambda x: [type for type in types if type.code == x])

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

	#itemAggregate.writeJSON()
	d = 2
