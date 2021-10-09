from __future__ import annotations
from typing import List

from py_ts_interfaces import Interface, Parser
from dataclasses import dataclass

@dataclass
class TypeInterface(Interface):
	name: str
	children: List[TypeInterface]

@dataclass
class RunewordInterface(Interface):
	name: str
	classRestriction: str
	Runes: List[str]
	Version: str
	Properties: List[str]
	Type: List[TypeInterface]

@dataclass
class SocketableInterface(Interface):
	name: str
	letter: str
	transform: str
	code: str
	mods: List[str]
