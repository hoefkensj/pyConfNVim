#!/usr/bin/env python
import sys
from myPyQt2.QLib import gui, gnr
from myPyQt2.QLib.QElements import QTextButton
from myPyQt2.QLib.QBases import QModule
from pyConfNVim.LocalContext import Ctx
from Clict import Clict
@Ctx
def addself(ctx,**k):
	slf={**ctx.b.gui}
	def self():
		ctx.b.gui['Main']['Elements']['trw_Tree']['Fnx']['Add'](self=slf)
	return self
def AddCtx(ctx):


	def addctx():
		copy = Clict()
		keys = ctx.keys()
		keys.remove('b')
		for key in keys:
			copy[key] = ctx[key]
		ctx.b.gui['Main']['Elements']['trw_Tree']['Fnx']['Add'](ctx=copy)
	return addctx


@Ctx
def mod_AppCtl(ctx,name):
	w = QModule.make(name)
	w['Elements'] |= gnr.Element(QTextButton.make('*self', pol='P.P', ))
	w['Elements'] |= gnr.Element(QTextButton.make('*ctx', pol='P.P', ))
	w['Elements'] |= gnr.Element(QTextButton.make('Print', pol='E.P', ))
	w['Elements'] |= gnr.Element(QTextButton.make('Exit', pol='E.P', ))
	w = w['Fnx']['Run'](w)
	sfn = gnr.Short(w, 'Con', 'clicked')
	w['Con']['self'] = sfn['*self']
	w['Con']['ctx'] = sfn['*ctx']
	w['Con']['Print'] = sfn['Print']
	w['Con']['Exit'] = sfn['Exit']
	w['Con']['Exit'](sys.exit)
	# w['Con']['Update'](Update(ctx.b.gui))
	return w
