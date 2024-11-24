# !/usr/bin/env python
# Auth
import sys
from myPyQt2.QLib import gui, gnr
from myPyQt2.QLib.QElements import QTree
from Clict import Clict
from pathlib import Path
from pyConfNVim.LocalContext import Ctx

from pyConfNVim.TypeDef.Config import Config
from pyConfNVim.ui.qt6.mod_AppCtl import mod_AppCtl,addself,AddCtx
from pyConfNVim.ui.qt6.mod_TreeCtl import mod_TreeCtl
from pyConfNVim.ui.qt6.mod_nvim import mod_Nvim
# from pyConfNVim.read import read

# from pyConfNVim.main import  CURRENTCTX
@Ctx
def ABTestCtx(ctx,test,stoA,fnA,stoB,fnB):
	lang=ctx.state[test].lang
	if lang == 'conf':
		stoA=fnA()
	elif lang == 'lua':
		stoB=fnB()

def Allign(GUI):
	s = gnr.Short(GUI['Main'])
	wMax = max(s['Key']['Fnx']['wLbl'](), s['Val']['Fnx']['wLbl']()) + 10
	s['Key']['Fnx']['Allign'](wMax)
	s['Val']['Fnx']['Allign'](wMax)
@Ctx
def Remove(ctx):
	def remove():
		ctx.b.gui['Main']['Elements']['trw_Tree']['Fnx']['Mtd']['takeTopLevelItem'](0)
	return remove


@Ctx
def Parse(ctx):
	def parse():

		ABTestCtx('Source',ctx.parsed.conf,ctx.nvim.conf.parsed,ctx.parsed.lua,lambda:pyConfNVim.Typedefs.QLua.Tree(ctx.source.lua)  )
		# SourceType = ctx.state.Source.lang
		#
		#
		# if SourceType == 'conf':
		# 	ctx.parsed.conf=ctx.nvim.conf.parsed()
		# elif SourceType == 'lua':
		# 	ctx.parsed.lua = pyConfNVim.Typedefs.QLua.Tree(ctx.source.lua)
			# ctx.parsed.current=ctx.parsed.lua
		sFn=gnr.Short(ctx.b.gui,'Fnx')
		sFn['Tree']['Add'](Parsed=ctx.parsed.conf)
	return parse
@Ctx
def PrintLines(ctx):
	def printlines():

		SourceType = ctx.state.Source.lang
		if SourceType == 'conf':
			ctx.converted.conf=ctx.nvim.conf.converted()
		elif SourceType == 'lua':
			ctx.converted.lua = pyConfNVim.Typedefs.QLua.Tree(ctx.source.lua)
			# ctx.converted.current=ctx.converted.lua
		sFn=gnr.Short(ctx.b.gui,'Fnx')
		sFn['Tree']['Add'](Converted=ctx.converted)
	return printlines
# @Ctx
# def Write(ctx):
# 	def write():
#
# 		TargetType = ctx.state.Target.lang
# 		if TargetType == 'conf':
# 				print(ctx.parsed.current)
# 		elif TargetType == 'lua':
# 			print(ctx.parsed.current)
#
# 		sCon=gnr.Short(ctx.b.gui,'Con')
# 		ctx.b.gui['Main']['Elements']['trw_Tree']['Fnx']['Add'](Parsed=ctx.parsed)
# 	return write

@Ctx
def Load(ctx):
	def load():
		if ctx.state.Source.lang=='lua':
			ctx.source.lua = QLuaPkg(Path(ctx.state.Source.full))
		elif ctx.state.Source.lang =='conf':
			ctx.nvim.conf = QNvimConfig(Path(ctx.state.Source.full,'conf'))
			ctx.source.conf=ctx.nvim.conf.sourced()
		sFn=gnr.Short(ctx.b.gui,'Fnx')
		sFn['Tree']['Add'](Source=ctx.source)
	return load

# @Ctx
# def Write(ctx):
#
# 		def write():
# 			source=ctx.parsed.current
# 			if ctx.state.Target.lang=='conf':
# 				target=Path(ctx.state.Target.full, 'conf')
# 			elif ctx.state.Target.lang=='lua':
# 				target=Path(ctx.state.Target.full)
#
# 			root = Path(target).expanduser().absolute()
# 			pkeymaps = Path(root, 'keymaps')
# 			ctx.keymaps.target = pkeymaps
# 			for folder in ctx.keymaps.strings:
# 				targetdir = Path(ctx.keymaps.target, folder)
# 				init = []
# 				if targetdir.exists():
# 					for file in targetdir.glob('*'):
# 						file.unlink()
# 				targetdir.mkdir(parents=True, exist_ok=True)
# 				for file in ctx.keymaps.strings[folder]:
# 					targetfile = Path(ctx.keymaps.target, folder, f'{file}.lua')
# 					init += ['.'.join([*Path(str(Path(*[*targetfile.parts][[*targetfile.parts].index('lua') + 1:])).removesuffix('.lua')).parts])]
# 					targetfile.touch(exist_ok=True)
# 					targetfile.write_text(ctx.keymaps.strings[folder][file])
# 				initfile = Path(ctx.keymaps.target, folder, f'init.lua')
# 				tplinit = gettpl('MASK_luainit')['base']
# 				strinit = []
# 				for line in init:
# 					strinit += [tplinit.format(LUAFILE=line)]
# 				initfile.write_text('\n'.join(strinit))
#
# 		return write
@Ctx
def browser(ctx):
	b=Clict()
	b.gui=gui.make('Browser')
	ctx.b=b
	b.gui['Elements']|=	gnr.Element(QTree.make('Tree', cols=5, hidecols=[2, 3, 4]))
	b.gui['Elements']|=	gnr.Element(mod_TreeCtl('TreeCtl'))
	b.gui['Elements']|=	gnr.Element(mod_Nvim('Nvim'))
	b.gui['Elements']|= gnr.Element(mod_AppCtl('AppCtl'))
	b.s = gnr.Short(b.gui)
	sFnx=gnr.Short(b.gui, 'Fnx')
	sCon=gnr.Short(b.gui,'Con')
	# b.sCon['Nvim']['Load']

	sCon['Nvim']['Load'](Load())
	sCon['Nvim']['Parse'](Parse())
	sCon['Nvim']['Print'](PrintLines())
	# sCon['Nvim']['Parse'](Write())
	sCon['TreeCtl']['+'](sFnx['Tree']['Mtd']['expandAll'])
	sCon['TreeCtl']['-'](sFnx['Tree']['Mtd']['collapseAll'])
	# b.sCon['AppCtl']['Update'](addself())
	sCon['AppCtl']['self'](addself())
	sCon['AppCtl']['ctx'](AddCtx(ctx))
	sCon['AppCtl']['Exit'](sys.exit)

	b.GUI = b.gui
	b.GUI['Main'] = b.gui['Browser']['Fnx']['Run'](b.GUI['Browser'])
	# Allign(b.GUI)
	b.GUI['Run'](b.GUI)
browser()

# GUI = gui.make('Main')
# # GUI['Elements']|=gnr.Element(component)
# GUI['Elements'] |= gnr.Element(QTree.make('Tree', cols=5, hidecols=[2, 3, 4]))
# GUI['Elements'] |= gnr.Element(mod_TreeCtl('TreeCtl'))
# GUI['Elements'] |= gnr.Element(QEditProp.make('Key', ))
# GUI['Elements'] |= gnr.Element(QEditProp.make('Val', ))
# # GUI['Elements'] |= gnr.Element(QComboBox.make('test', ))
# GUI['Elements'] |= gnr.Element(QAppCtl.make('AppCtl'))
# s=gnr.Short(GUI)
# sCon = Clict(gnr.Short(GUI, 'Con'))
# sFnx = Clict(gnr.Short(GUI, 'Fnx'))
# sCon['TreeCtl']['+'](sFnx['Tree']['Mtd']['expandAll'])
# sCon['TreeCtl']['-'](sFnx['Tree']['Mtd']['collapseAll'])
# sCon['AppCtl']['Update'](Update(gui={**GUI}))
# sCon['AppCtl']['Exit'](sys.exit)
#
# GUI=GUI
# GUI['Main'] = GUI['Main']['Fnx']['Run'](GUI['Main'])
# Allign(GUI)
# GUI['Run'](GUI)
#
# print('After')

# def MProc():
# 	def mproc()
