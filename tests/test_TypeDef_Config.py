import unittest
from pathlib import Path
import pyConfNVim
from pyConfNVim.TypeDef.Config import Config
from pyConfNVim.TypeDef.NVimConfig import KeyMaps
from pyConfNVim.tools import  pTree
class test_Config(unittest.TestCase):
	def test_NewConfig(self):
		# breakpoint()

		testroot=Path(Path (__file__).parent,'testdata','config')

		testConf=Config(testroot)
		print(testConf)

		self.assertEqual('value1',testConf['testcat']['test_Config']['SECTION1']['KEY1'])  # add assertion here
		self.assertEqual('value1',testConf.testcat.test_Config.SECTION1['KEY1'])  # add assertion here
		# print(testConf.keymaps.startup.testkeymap.line.current_move_up.CMD)  # add assertion here
		self.assertEqual('<Cmd>m +1<CR>',testConf.keymaps.startup.testkeymap.line.current_move_down.CMD)


if __name__ == '__main__':
	unittest.main()
