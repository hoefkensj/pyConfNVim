#!/usr/bin/env python
import os
from Clict import Clict
from pyConfNVim import Parse
from pyConfNVim.TypeDef.Mappings import KeyMap



class KeyMaps(Clict):
	def __init__(s,config,cat=None,conf=None,parent=None):
		s._config=config
		s._path=config._path
		s._name=s._path.name
		s._cat=cat
		s._conf=conf
		s._parent= parent or None
		s._isconf=False
		s._iscat=False
		s._type=None
		s._registered=[]
		s.__selfid__()
		s.__parse__()

	def __selfid__(s):
		c = s._config
		# print(f'\n\n\n\n{c._self}\n\n')
		if c._isfolder:
			s._iscat=True
		elif c._isfile:
			s._isconf=True
			if c._type == 'conf':
				s._type = 'keymaps'

	def __parse__(s):
		c = s._config
		if s._iscat:
			for key in c:
				s[key]=KeyMaps(c[key],cat=s._name,parent=s)
				s._registered+=s[key]._registered
		elif s._isconf:
			for key in c:
				if key == 'DEFAULT':
					continue
				s[key]=KeyMap(key,c[key],cat=s._cat,conf=s._name,parent=s)
				s._registered+=[s[key].hkey[i].hotkey for i in s[key].hkey ]