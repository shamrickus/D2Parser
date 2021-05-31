from baseParser import BaseParser

class PropertyParse(BaseParser):
	def __init__(self, line):
		self.code = ""
		BaseParser.__init__(self, line)

	def parse(self, parser):
		self.code = self.raw["code"]

	@staticmethod
	def getName():
		return "properties"

class Property:
	def generateRange(self, append=""):
		self.min = 0
		self.max = 0
		self.par = 0
		self.prop = ""
		self.parsed = ""
		if (self.min == self.max):
			return self.min + append
		return "{}-{}{}".format(self.min, self.max, append)

	def __str__(self):
		return ("prop: {}, par: {}, min: {}, max: {}, parsed: {}".format(self.prop, self.par, self.min, self.max,
																		 self.parsed))

	def json(self):
		return "{" + "\"prop\":\"{}\",\"par\":\"{}\",\"min\":\"{}\",\"max\":\"{}\",\"parsed\":\"{}\"".format(self.prop,
																											 self.par,
																											 self.min,
																											 self.max,
																											 self.parsed) + "}"

	def __init__(self, prop, par, min, max):
		if (prop is None or prop == ""):
			self.prop = None
			return
		self.parsed = ""
		self.prop = prop
		self.par = par
		self.min = min
		self.max = max

	def equiv(self, prop):
		return self.prop == prop.prop and \
			   self.par == prop.par

	def add(self, prop, parser):
		if self.min.isnumeric():
			self.min = str(int(self.min) + int(prop.min))
		if self.max.isnumeric():
			self.max = str(int(self.max) + int(prop.max))
		if self.par.isnumeric() and prop.par.isnumeric():
			self.par = str(int(self.par) + int(prop.par))
		parser.parse([self])

	def mult(self, amount: int):
		if self.min.isnumeric():
			self.min = str(round((int(self.min)*amount), 1))
		if self.max.isnumeric():
			self.max = str(round(int(self.max)*amount, 1))
		if self.par.isnumeric():
			self.par = str(round(int(self.par)*amount, 1))
