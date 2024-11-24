#!/usr/bin/env python

import sys
from textwrap import shorten
# from src.isPyPackage.ansi_colors import reset,rgb,yellow,red
def hasDict(d):
	return any([True for key in d if isinstance(d[key], dict)])

yellow=[255,255,0]
red=[255,0,0]
reset='\x1b[m'
def rgb(color,string,last=[0,0,0]):
	ansi='\x1b[38;2;{};{};{}m'
	c=ansi.format(*color)
	result='{C}{S}{R}'.format(C=c,S=string,R=reset)
	last=c
	return result

def overview(d):
	dicts=[item for item in d if isinstance(d[item], dict)]
	sd=len(dicts)
	ld=len(d)-sd
	sd=rgb(yellow,sd)
	ld=rgb(red,ld)
	print( f'({sd}Groups+{ld}items){reset}',end='')
def pTree(*a, **k):
	fstr= ''
	d = a[0]
	maxd = a[1] if len(a) > 1 else 0
	limi = k.get("limit") or (a[2] if len(a) > 2 else 0)
	depth = k.get("depth") or 0
	keys = len(d.keys())
	depthstop = True if (maxd == depth and not maxd <= 0) else False
	limstop = True if (len(d) >= limi and not limi <= 0) else False
	if limstop or depthstop:
		overview(d)
	else:
		for key in d:
			dkey = shorten(	f"\x1b[32m{d[key]}\x1b[0m" if callable(d[key]) else str(d[key]), 80	)
			keys -= 1
			if isinstance(d[key], dict):
				fstr+="\n"
				fstr+="  ┃  " * (depth)
				fstr+="  ┗━━ " if keys == 0 else "  ┣━━ "
				fstr+=f"\x1b[1;34m{str(key)}\t:\x1b[0m\t"
				fstr+=pTree(d[key], maxd, limi, depth=depth + 1)
			else:
				fstr+="\n"
				fstr+="  ┃  " * (depth)
				fstr+="  ┗━━ " if keys == 0 else "  ┣━━ "
				fstr+=f"{str(key)}\t:\t{dkey}"
	return fstr