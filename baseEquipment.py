import logging

from baseParser import BaseParser
from property import Property
from utils import isdebugging

logger = logging.getLogger(__name__)

class BaseEquipment(BaseParser):
	name: str
	itypes: []
	props: [Property]

	def __init__(self, line):
		self.name = ""
		self.itypes = []
		self.props = []
		BaseParser.__init__(self, line)

	def add(self, property: Property, parser):
		for prop in self.props:
			if prop.equiv(property):
				prop.add(property, parser)
				return
		self.props.append(property)

	def parseProperties(self, maxProps: int, propFmtStr: str, parFmtStr: str, minFmtStr: str, maxFmtStr: str, parser):
		for i in range(1, maxProps):
			if self.raw[propFmtStr.format(str(i))] != "":
				self.props.append(Property(self.raw[propFmtStr.format(str(i))], self.raw[parFmtStr.format(str(i))],
										   self.raw[minFmtStr.format(str(i))], self.raw[maxFmtStr.format(str(i))]))
		if self.verify():
			if isdebugging():
				logger.debug(self.name)
			parser.parse(self.props)
