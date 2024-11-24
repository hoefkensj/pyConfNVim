#!/usr/bin/env python

from Clict import  Clict
from pyConfNVim.TypeDef.Context import LocalContext


def GlobalContext():
	if not 'CTX' in globals():
		globals()['CTX']=Clict()

	return  globals()['CTX']

def NewContext(newctx=__name__):
	CTX=GlobalContext()
	CTX[newctx]=LocalContext(newctx)
	CTX.current=CTX[newctx]
	return CTX[newctx]



def Ctx(fn):
	CTX=GlobalContext()
	return lambda *a,**k :  fn(CTX.current,*a,**k)