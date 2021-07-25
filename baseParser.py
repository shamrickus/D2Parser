from utils import headerParse

class BaseParser:
	def __init__(self, line):
		self.raw = {}
		for prop in line:
			self.raw[headerParse(prop)] = line[prop]

	@staticmethod
	def getName():
		raise NotImplementedError()

	def verify(self):
		raise NotImplementedError()

	def json(self):
		raise NotImplementedError()

	def parse(self, parser):
		raise NotImplementedError()

	def format(self, list):
		return "[\"" + "\",\"".join(x for x in list) + "\"]"

	def formatObj(self, listObj):
		return "[" + ', '.join(x for x in listObj) + "]"
