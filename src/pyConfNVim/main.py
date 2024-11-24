# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import multiprocessing
from pathlib import Path
from Clict import Clict
from inspect import getsourcefile
# import builtins
import pyConfNVim
from pyConfNVim.TypeDef.Config import Config
from pyConfNVim.LocalContext import NewContext,Ctx
from pyConfNVim.Parse import conf_keymaps
# from pyConfNVim.ui.qt6.qtbrowser import browser


def loadConfig(ctx):
	self=Path(__file__).parent
	configdir=Path(self,'config')
	ctx.config=Config(configdir)

	ctx.pkgroot = Path(__file__).absolute().parent
	return ctx
def unpack(conf,parsed):
	if conf._type.folder:
		for folder in conf:
			unpack(conf[folder],parsed)
	elif conf._type.config and conf._type.file:
		parsed[conf._name]=conf_keymaps(conf, [])
	return parsed

@Ctx
def main(ctx):
	loadConfig(ctx)
	parsed = Clict()
	nvimroot = Path('~/.config/nvim/conf/').expanduser()
	nvimconf = Config(nvimroot)
	ctx.nvimconf=nvimconf
	parsed=unpack(nvimconf,parsed)
	ctx.parsed.nvimconf=parsed
	print(repr(ctx))

# proc = multiprocessing.Process(target=browser)
	# proc.start()

if __name__ == '__main__':
	main()
