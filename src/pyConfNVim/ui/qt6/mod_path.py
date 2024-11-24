#!/usr/bin/env python

#!/usr/bin/env python
from myPyQt2.QLib.QModules import QHSingleChoice,QHMultiChoice
from myPyQt2.QLib.QElements import QTextButton, QCheckBox
from pathlib import Path
from myPyQt2.QLib.QBases import QModule
from pyConfNVim.LocalContext import Ctx

from myPyQt2.QLib import gui, gnr
from Clict import Clict


@Ctx
def mod_Path(ctx,name,choices,options):
	w = QModule.make(name,t='H',margin=[5,0,5,0])
	w['Elements'] |= gnr.Element(QHSingleChoice.make('Choices',lbl=f'{name}:',name=name,choices=choices ))
	w['Elements'] |= gnr.Element(QHMultiChoice.make('Options',lbl=f'{name}:',name=name,choices=options ))


	w = w['Fnx']['Run'](w)
	sfn=gnr.Short(w, 'Fnx')
	sCon=gnr.Short(w,'Con')
	w['Con']['Choices']=sCon['Choices']
	w['Con']['Options']=sCon['Options']
	w['Fnx']['Choices']=sfn['Choices']
	w['Fnx']['Options']=sfn['Options']


	def MakePath():
		if ctx.state.selected[name]['conf']:
			lang='conf'
		if ctx.state.selected[name]['lua']:
			lang='lua'
		testing=ctx.state.selected[name]['test']
		mybase='test' if testing else 'user'
		base=ctx.config.lib.paths.base.get(mybase)
		if testing:
			base=Path(ctx.pkgroot,base).absolute()
		else:
			base=Path(base).expanduser().absolute()
		user=ctx.config.lib.paths.user.get('user')
		ctx.state[name].path=Path(base,'nvim')
		ctx.state[name].full=Path(base,'nvim')
		ctx.state[name].lang=lang
	def GetState():
		def getstate():
			STATE={**sfn['Choices']['GetState'](),**sfn['Options']['GetState']()}
			ctx.state.selected[name]=STATE
			MakePath()
			return STATE
		return getstate
	w['Fnx']['GetState']=GetState()

	for choice in choices:
		w['Con']['Choices'][choice]['Changed'](GetState()) #'(lambda
	# : STATE())# ChangeSelected(w,name,choices))
	for opt in options:
		w['Con']['Options'][opt]['Changed'](GetState())#ChangeSelected(w,name,choices))
	return w
