#!/usr/bin/env python
import os
from pathlib import Path
from Clict import Clict
from configparser import ConfigParser,ExtendedInterpolation

def dummy(*a, **k):pass
def DBug(enabled=False):
	def dbug(*a):
		print(*a)
		return enabled

	def dummy(*a):
		return enabled
	if enabled:
		return dbug
	else:
		return dummy

def getFileType(c):
	def isconfig(): return bool(
		(	c._path.suffix.casefold() in ['.conf','.config','.init', '.ini', '.cfg'])+
		(	c._path.stem.casefold() in ['conf','config','.config','init','.conf','.settings'])
	)
	r=Clict()
	r.file=bool(c._path.is_file())
	r.folder=bool(c._path.is_dir())
	r.config=bool(isconfig())
	return r



def newConfig():
	cfg = ConfigParser(interpolation=ExtendedInterpolation(),
	                   delimiters=':',
	                   allow_no_value=True)  # create empty config
	cfg.optionxform = lambda option: option
	return cfg

class Config(Clict):

	def __init__(s,p,cat=None,parent=None,debug=False):
		s._path=Path(p)
		s._name=s._path.stem
		s._parent= parent or None
		s._cat=cat or []
		s._type=getFileType(s)

		s._self=s.__self__()
		s.__read__()

	def __self__(s):
		self=Clict()
		self.name=s._name
		self.path=s._path
		self.file=s._type.file
		self.folder=s._type.folder
		self.config=s._type.config
		parent=s.get('_parent')
		if parent:
			self.parent=parent.get('_name')

		return self

	def __read__(s):
		if s._type.folder:
			for item in [*s._path.glob('*')]:
				name=item.stem
				cat=[*s._cat,s._name]
				if '_' in name:
					if name.split('_')[0].isnumeric():
						name='_'.join(name.split('_')[1:])
				s[name]=Config(item,cat=cat ,parent=s)
		elif s._type.file:
			if s._type.config:
				cfg = newConfig()
				cfg.read(s._path)
				for section in cfg:
					if '-' in section:
						for key in cfg[section]:
							s[section.split('-')[0]]['-'.join(section.split('-')[1:]).replace('-', '.')][key]= cfg[section][key]
					else:
						for key in cfg[section]:
							s[section][key] = cfg[section][key]










