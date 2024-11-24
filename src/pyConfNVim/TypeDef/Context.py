#!/usr/bin/env python
from Clict import Clict
class LocalContext(Clict):
	def __init__(s,name='ctx'):
		s._name=name
		super().__init__()
	def __getitem__(s, i):
		return super().__getitem__(i)
	def __getattr__(s, i):
		return super().__getattr__(i)
	def __setitem__(s, k,v):
		super().__setitem__(k,v)
	def __setattr__(s, k,v):
		s.__setitem__(k,v)