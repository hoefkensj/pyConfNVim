#!/usr/bin/env python
from pathlib import Path
from pyConfNVim.LocalContext import Ctx
from pyConfNVim.TypeDef.Config import Config
@Ctx
def loadConfig(ctx):
	self=Path(__file__).parent
	configdir=Path(self,'config')
	ctx.config=Config(configdir)

	ctx.pkgroot = Path(__file__).absolute().parent
	return ctx