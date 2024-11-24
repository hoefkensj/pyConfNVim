#!/usr/bin/env python
from Clict import Clict
from pathlib import Path
import re

def makelua(mapping):
	def mask(tpl,**parts):
		return tpl.format(**parts)

	luaset=Clict()
	luastr=[]
	luaMASK=gettpl('MASK_keymap.lua')
	luaMODE=gettpl('MODES-mapping')
	print(mapping.desc)
	luaDesc=mapping.desc if mapping.desc != 'None' else mapping.name
	hotkeys=mapping.hkey
	for i,hotkey in enumerate(hotkeys):
		lua=Clict()
		lua.FUNC = f"'{mapping.func}'".ljust(30)
		lua.NAME = mapping.name
		lua.KEYS = f"'{hotkey['hotkey']}'".ljust(30)
		lua.MODE=luaMODE.get(hotkey['mapmode'])
		lua.OPTS=luaMASK['opts'].format(OPTS=optlist(hotkey['opts'],luaDesc), O='{', C='}').ljust(40)
		lua.DESC=luaDesc
		lua.LINE=mask(luaMASK['base'],**lua)
		luaset[lua.KEYS]=lua
	return luaset




class QLuaFlat(Clict):
	"""stores the tree structure of of luafiles"""
	def __init__(__s, p):
		__s._path=Path(p).expanduser().resolve().absolute()
		__s._read__()
	def __read__(__s):
		for i,item in enumerate(__s._path.rglob('*.lua')):
			name=item.name.removesuffix('.lua')
			__s[i].tree = item.relative_to(__s._path).parts[:-1]
			__s[i].name = name
			__s[i].type = 'lua'
			__s[i].lines = __s._readfile__(item)
		# s.lines = s.luafile.lines
		# s.parsed = s.__parselines__()
		# s.maps[s.name].mappings = s.parsed
	def __readfile__(__s, file):
		with open(file, 'r') as l:
			return l.readlines()


class QLuaPackageTree(Clict):
	def __init__(__s, p, init=None, root=None):
		__s._name=p.stem
		__s._root=p.resolve().absolute() if root is None else root
		__s._path=p.resolve().absolute().relative_to(__s._root)
		__s._isroot=False if root else True
		__s._type= 'config'
		__s._subp=Path(__s._path, 'lua' if __s._isroot else '')
		__s._pkgs=[item for item in Path(__s._root, __s._path).glob('*') if item.is_dir()]
		__s._modules=[item for item in Path(__s._root, __s._path).glob('*') if item.is_file() and item.suffix == '.lua']
		__s._other=[item for item in Path(__s._root, __s._path).glob('*') if item not in __s._childpkgs and item not in __s._modules]
		__s._recurse__()

	def __recurse__(__s):
		# print(s.__pkgs)
		# print(s.__modules)
		# print(s.__other)
		for pkg in __s._pkgs:
			if pkg.name.startswith('_'):
				continue
			__s[pkg.stem]=QLuaPackageTree(pkg.absolute())
		for mod in __s._modules:
			__s[mod.stem]=QLuaMod(mod, root=__s._root)
	def __str__(s):
		string=''
		for item in s:
			string+=f'{item}:\n'
			string+=f'    -{s[item]}\n'
		return string

# def __str__(s):
# 	return '\n'.join([f'    {s.__name}: {s[item].__name}' for item in s])


class QLuaPkg(Clict):
	def	__init__(__s, p, init=None, root=None):
		super().__init__()
		__s._tree=QLuaPackageTree(p, init=init, root=root)
		# print(s.__tree)
		__s._name=p.stem
		__s._root=p.resolve().absolute() if root is None else root
		__s._path=p.expanduser().resolve().absolute().relative_to(__s._root)
		__s._isroot=False if root else True
		__s._type= 'config'
		__s._subp=Path(__s._path, 'lua' if __s._isroot else '')
		__s._init=Path(__s._root, __s._path, 'init.lua') if init is None else Path(p, init, 'init.lua')
		__s._lists= Init(__s._init)
		__s._settype__()
		__s._loadlist__()
	def __settype__(__s):
		if 'keymaps' in __s._path.parts:
			__s._type= 'keymap'


	def __loadlist__(__s):
		__s._lists.missing=[]
		__s._children.pkgs = []
		__s._children.mods = []
		for item in __s._lists.active:

			pkgpath=Path(__s._root, 'lua', item.replace('.', os.sep))
			modpath=Path(__s._root, 'lua', f'{item.replace(".", os.sep)}.lua')
			# print(modpath)
			if not pkgpath.exists()and not modpath.exists():
				__s._lists.missing+=[item]

			if pkgpath.is_dir():
				__s._children.pkgs += [pkgpath.stem]
				__s[pkgpath.stem]=QLuaPkg(pkgpath, root=__s._root)

			if modpath.is_file():
				__s._children.mods += [modpath.stem]
				__s[modpath.stem]=QLuaMod(modpath, root=__s._root)
	def __str__(__s):
		string=''
		string+='---------------\n\n'

		string+=f'Package: {__s._name}\n'
		string+=f'Root: {__s._root}\n'
		string+=f'type: {__s._type}\n'
		string+=f'SubPkgs: {",".join(__s._children.pkgs)}\n'
		string+=f'Modules: {",".join(__s._children.mods)}\n'
		for item in __s:
			string+=f'{item}:\n{__s[item]}\n'
		string+='---------------\n\n'
		return string

	def Init(__s, p):
		rex = Clict()
		rex.initspec = r'require\(\'(?P<MOD>.*)\'\)(?P<COMM>.*)$'
		rex.require = re.compile(rex.initspec, re.M | re.S | re.X)
		with open(p, 'r') as l:
			lines = l.readlines()
		active = []
		inactive = []
		for line in lines:
			if not 'require' in line:
				continue
			line = line.strip()
			if line.startswith('--'):
				line = line.removeprefix('--')
				rexfind = rex.require.search(line)
				inactive += [rexfind.groupdict()['MOD']]
			else:
				rexfind = rex.require.search(line)
				active += [rexfind.groupdict()['MOD']]
		print(f'{active=}')
		lists = Clict
		lists.active = active
		lists.inactive = inactive
		return lists


class QLuaMod(Clict):
	def __init__(__s, p, init=None, root=None):

		__s._name=p.stem
		__s._root=root
		__s._path=p.resolve().absolute().relative_to(__s._root)
		__s._type= 'config'
		__s._settype__()
		__s._read__()
		__s._parse__()


	def __settype__(__s):
		if 'keymaps' in __s._path.parts:
			__s._type= 'keymap'

	def __read__(__s):
		p=Path(__s._root, __s._path)
		with open(p, 'r') as l:
			lines=l.readlines()
		__s._data=[line.strip('\n') for line in lines if line != '']
	def __parse__(__s):
		if __s._type== 'keymap':
			__s|= KeyMap(__s._data)
	def __str__(__s):
		return '\n'.join(__s._data)


class LuaMap(Clict):

	def __init__(__s, **k):
		__s.meta.tpl = None
		__s.hotkeys = Clict()
		__s.conf = k.get('conf', k.get('cfg', None))
		__s.lua = Clict()
		__s.lua.lines = []
		__s.name = None
		__s.cmd = None
		__s.desc = None
		__s.part.func = None
		__s.part.name = None
		__s.part.desc = None
		__s.part.mode = None
		__s.part.opts = None

	def parse(__s):
		__s.cmd = __s.conf['CMD']
		__s._parse_hkeys__()
		__s._constructlua__()

	def __parse_hkeys__(__s):
		keys = {**__s.conf}
		keys.pop('CMD', None)
		keys.pop('desc', None)
		for i, k in enumerate(keys):
			valuestr = __s.conf[k]
			values = valuestr.split(',')
			__s.meta.hotkey[i].key = k
			__s.meta.hotkey[i].value = valuestr
			__s.meta.hotkey[i].modes = values.pop(0)
			if len(values) > 0:
				if 'desc' in values[-1]:
					__s.meta.hotkey[i].desc = values.pop(-1).split('=')[2]
				else:
					__s.meta.hotkey[i].desc = __s.desc
				for v in values:
					__s.meta.hotkey[i].opts[v] = True

	def __constructlua__(__s):
		for hk in __s.meta.hotkey:
			hotkey = __s.meta.hotkey[hk].key
			__s.hotkeys[hotkey].lua = __s.makeluamap(hk)
			__s.hotkeys[hotkey].len = len(__s.hotkeys[hotkey].lua)
			__s.lua[f'hotkey{hk}'] = __s.hotkey[hk].lua
			__s.lua.lines += [__s.hotkey[hk].lua]


def KeyMap(luafile):
	def clean_ckv(string):
		return string.strip().strip("'").removeprefix('--')

	def clean_modes(string):
		return [c for c in string if c in 'nvxsoict']

	def Opts(string):
		cleaned = Clict()
		opts = string.split(',')
		for opt in opts:
			key = opt.split('=')[0]
			val = '='.join(opt.split('=')[1:])
			cleaned[clean_ckv(key)] = clean_ckv(val)
		return cleaned

	def File(luafile):
		rex = Clict()
		tpl=gettpl('RE_lua')
		rex.mapping = fr'{tpl.kmap}'
		rex.option = fr'{tpl.opts}'
		rex.luamap = re.compile(rex.mapping, re.M | re.S | re.X)
		rex.reargs = re.compile(rex.option, re.M | re.S | re.X)
		args = None

		parsed = Clict()
		for line in luafile:
			rexmap = rex.luamap.search(line)
			if rexmap:
				with suppress(AttributeError):
					ARGS = rexmap.groupdict()['ARGS']
					COMM = rexmap.groupdict()['COMM']
					NAME = clean_ckv(COMM)
					if ARGS is not None:
						rexargs = rex.reargs.search(ARGS)
						grargs = rexargs.groupdict()
						modes = grargs['MODES']
						cmd = grargs['CMD']
						opts = grargs['OPTS']
						key = grargs['KEY']

						MODES = clean_modes(modes)
						CMD = clean_ckv(cmd)
						OPTS = Opts(opts)
						KEY = clean_ckv(key)
						parsed[NAME][CMD][KEY].modes = MODES
						parsed[NAME][CMD][KEY].opts = OPTS
		return parsed

	return File(luafile)


def Tree(LuaPkg):
	branch=Clict()
	for pkg in LuaPkg:
		if isinstance(LuaPkg[pkg],QLuaPkg):
			branch[pkg]=Tree(LuaPkg[pkg])
		elif isinstance(LuaPkg[pkg],QLuaMod):
			if LuaPkg[pkg].__type__=='keymap':
				branch[pkg]=KeyMap(LuaPkg[pkg])

	return branch


def Init(p):
	rex=Clict()
	rex.initspec = r'require\(\'(?P<MOD>.*)\'\)(?P<COMM>.*)$'
	rex.require = re.compile(rex.initspec, re.M | re.S | re.X)
	with open(p, 'r') as l:
		lines=l.readlines()
	active=[]
	inactive=[]
	for line in lines:
		if not 'require' in line:
			continue
		line=line.strip()
		if line.startswith('--'):
			line=line.removeprefix('--')
			rexfind = rex.require.search(line)
			inactive+=[rexfind.groupdict()['MOD']]
		else:
			rexfind = rex.require.search(line)
			active+=[rexfind.groupdict()['MOD']]
	print(f'{active=}')
	lists=Clict
	lists.active=active
	lists.inactive=inactive
	return lists
