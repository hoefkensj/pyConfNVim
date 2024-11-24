#!/usr/bin/env python
from pathlib import Path
from Clict import Clict
from myPyQt2.QLib.QModules import QHSingleChoice,QHMultiChoice
from myPyQt2.QLib.QElements import QTextButton, QCheckBox
from myPyQt2.QLib.QBases import QModule
from myPyQt2.QLib import gui, gnr
from pyConfNVim.LocalContext import Ctx
from pyConfNVim.TypeDef.Config import Config
from pyConfNVim.ui.qt6.mod_path import mod_Path

@Ctx
def WalkFile(ctx,config):
	filestr=[]
	for section in config:
		header=f'-- {section}'
		luaset=makelua(config[section])
		filestr+=[header]
		for lua in luaset:
			filestr+=[luaset[lua].LINE]
	return '\n'.join(filestr)
@Ctx
def WalkFolder(ctx,folder):
	strfolder = Clict()
	for item in folder:
		if folder[item].__type__ == 'container':
			strfolder[item] = WalkFolder(folder[item])
		elif folder[item].__type__ == 'config':
			strfolder[item] = WalkFile(folder[item])
	return strfolder




@Ctx
def mod_Nvim(ctx,name):
	w = QModule.make(name,t='V',margin=[5,10,5,10])
	choices = ['conf', 'lua', ]
	options = ['all','test']
	w['Elements'] |= gnr.Element(mod_Path('Source',choices,options ))
	w['Elements'] |= gnr.Element(mod_Path('Target',choices , options))
	w['Elements'] |= gnr.Element(mod_ConfCtl('ConfCtl' ))
	w = w['Fnx']['Run'](w)
	sfn=gnr.Short(w, 'Fnx')
	sCon=gnr.Short(w,'Con')
	target=sfn['Target']
	source=sfn['Source']
	w['Con']['Load']=sCon['ConfCtl']['Load']
	w['Con']['Parse']=sCon['ConfCtl']['Parse']
	w['Con']['Print']=sCon['ConfCtl']['Print']
	w['Con']['Write']=sCon['ConfCtl']['Write']
	w['Con']['Del']=sCon['ConfCtl']['Del']
	def GetState():
		def getstate():
			ctx.state.selected.Source=sfn['Source']['GetState']()
			ctx.state.selected.Target=sfn['Target']['GetState']()
			return ctx.state.selected
		return getstate

	w['Fnx']['GetState']=GetState()

	# w['Con']['Print'](GetState())
	# w['Con']['Write'](Write(w))

	return w



@Ctx
def Write(ctx,w):
	def write():
		rootstr=ctx.Target.path
		root=Path(rootstr).expanduser().absolute()
		pkeymaps=Path(root,'keymaps')
		ctx.keymaps.target=pkeymaps
		for folder in ctx.keymaps.strings:
			targetdir=Path(ctx.keymaps.target,folder)
			init=[]
			if targetdir.exists():
				for file in targetdir.glob('*'):
					file.unlink()
			targetdir.mkdir(parents=True,exist_ok=True)
			for file in ctx.keymaps.strings[folder]:
				targetfile=Path(ctx.keymaps.target,folder,f'{file}.lua')
				init+=['.'.join([*Path(str(Path(*[*targetfile.parts][[*targetfile.parts].index('lua')+1:])).removesuffix('.lua')).parts])]
				targetfile.touch(exist_ok=True)
				targetfile.write_text(ctx.keymaps.strings[folder][file])
			initfile=Path(ctx.keymaps.target, folder, f'init.lua')
			tplinit=gettpl('MASK_luainit')['base']
			strinit=[]
			for line in init:
				strinit+=[tplinit.format(LUAFILE=line)]
			initfile.write_text('\n'.join(strinit))

	return write

@Ctx
def mod_ConfCtl(ctx,name):

	w = QModule.make(name)
	w['Elements'] |= gnr.Element(QTextButton.make('Load', pol='E.P' ))
	w['Elements'] |= gnr.Element(QTextButton.make('Parse', pol='E.P' ))
	w['Elements'] |= gnr.Element(QTextButton.make('Print', pol='E.P' ))
	w['Elements'] |= gnr.Element(QTextButton.make('Write', pol='E.P' ))
	w['Elements'] |= gnr.Element(QTextButton.make('Del', pol='E.P' ))

	w = w['Fnx']['Run'](w)
	sfn = gnr.Short(w, 'Con')
	w['Con']['Load'] = sfn['Load']['clicked']
	w['Con']['Parse'] = sfn['Parse']['clicked']
	w['Con']['Print'] = sfn['Print']['clicked']
	w['Con']['Write'] = sfn['Write']['clicked']
	w['Con']['Del'] = sfn['Del']['clicked']
	return w

@Ctx
def Tester(ctx):

	b=Clict()
	b.gui=gui.make('Tester')
	ctx.b=b
	b.gui['Elements']|=	gnr.Element(mod_Nvim('Nvim'))
	b.s = gnr.Short(b.gui)

	b.sCon = Clict(gnr.Short(b.gui, 'Con'))
	b.sFnx = Clict(gnr.Short(b.gui, 'Fnx'))
	b.GUI = b.gui
	b.GUI['Main'] = b.gui['Tester']['Fnx']['Run'](b.GUI['Tester'])
	b.GUI['Run'](b.GUI)

if __name__ == '__main__':
	Tester()
