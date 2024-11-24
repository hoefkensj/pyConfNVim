#!/usr/bin/env python
from pathlib import Path
from pyConfNVim.LocalContext import GlobalContext,NewContext
from pyConfNVim.__configure__ import loadConfig
CTX=GlobalContext()
NewContext(Path(__file__).parent.name)
loadConfig()
