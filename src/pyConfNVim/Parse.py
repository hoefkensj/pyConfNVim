#!/usr/bin/env python
from Clict import Clict
from pyConfNVim.LocalContext import Ctx
from pyConfNVim.TypeDef import Mappings
def cleanstr(string):
	string = string.strip()
	string = string.strip('"')
	string = string.strip("'")
	string = string.strip(" ")
	return string

@Ctx
def Values(ctx,val):
	res=Clict()
	tplmodes=ctx.config.lib.templates['MODES-shorts']
	vals = val.split(',')
	val_mode=cleanstr(vals.pop(0))
	val_opts=[cleanstr(v) for v in vals]
	modes=[]
	for mode in val_mode:
		modes+=[tplmodes.get(mode)]
	opts=Clict()
	for opt in val_opts:
		if not opt== '':
			opts[opt] = True
	if not 'desc' in opts:
		opts['desc']=None
	res.modestr=val_mode
	res.modes=modes
	res.opts=opts
	return res



def conf_keymaps(config,reg):
	kms=Clict()
	for section in config:
		if section == 'DEFAULT':
			continue
		kms[section] = Mappings.KeyMap(section, config[section])
		kms[section].__type__ = 'keymap'
		if not section == 'unmap':
			for mp in kms[section].hkey:
				if mp.hotkey in reg:
					print('DUPLICATE', mp.hotkey, reg)
				else:
					reg += [f'{mp.hotkey}.{mp.mode}']
	kms.__registered=reg
	return kms
