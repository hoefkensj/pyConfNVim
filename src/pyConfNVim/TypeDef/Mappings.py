#!/usr/bin/env python
import os
from Clict import Clict
from pyConfNVim import Parse



class KeyMap(Clict):
	"""stores the tree structure of configparser elements"""
	def __init__(s,name,mapping,cat=None,conf=None,parent=None):
		s._mapping=mapping
		s._workmap={**mapping}
		s._cat=cat
		s._conf=conf
		s.name=name
		s.__extract__('CMD')
		s.__extract__('desc',name)

	def __extract__(s,key,default=None):
		if key in s._workmap:
			s[key.lower]=s._workmap.pop(key)
		else:
			s[key.lower]=default



class HotKey(Clict):
	def __init__(s,hk,vals):
		s._type='hotkey'
		s.hotkey = hk
		s.parse_valstr(vals)

	def parse_valstr(s,valstr):
		vals=Parse.Values(valstr)
		s.mode = vals.modes
		s.mapmode=vals.modestr
		s.opts = vals.opts

	def __str__(s):
		return s.__fancy__()


