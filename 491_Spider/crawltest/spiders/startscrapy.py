from scrapy.cmdline import execute
import traceback
import os
from os import path
from mltools import sett

class Exec:         
	def __init__( self, newPath ):  
		self.savedPath = os.getcwd()
		os.chdir(sett.spider_dir)
		execute(['scrapy', 'crawl', 'news'])

	def __del__( self ):
		os.chdir(self.savedPath )

try:
	Exec(path.abspath('491_Spider'))
except Exception as e:
	pass
traceback.print_exc()

