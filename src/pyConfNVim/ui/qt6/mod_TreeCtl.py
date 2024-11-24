#!/usr/bin/env python
from myPyQt2.QLib import gnr
from myPyQt2.QLib.QBases import QModule
from myPyQt2.QLib.QModules import QHIncDec, QHSearch

from pyConfNVim.LocalContext import Ctx

@Ctx
def mod_TreeCtl(ctx,name):
	w = QModule.make(name,)
	w['Elements'] |= gnr.Element(QHIncDec.make('ColEx', wh=[20, 20]))
	w['Elements'] |= gnr.Element(QHSearch.make('TreeSearch', ))
	w = w['Fnx']['Run'](w)
	sfn = gnr.Short(w, 'Con')
	w['Con']['+']   = sfn['ColEx']['Inc']
	w['Con']['-']   = sfn['ColEx']['Dec']
	return w
