import logging
import json

class level:
	def __init__(self,size=(12,10)):
		self.size = size
		self.map = [[0] * self.size[1] for i in xrange(self.size[0])]
		
		self.tiles = []
	
	def add_object(self,object):
		self.tiles.append(object)
	
	def load(self,file):
		try:
			_file = open(file,'r')
		except:
			raise Exception('Could not find level \'%s\'!' % file)
		
		try:
			for tile in json.loads(_file.readline()):
				self.add_object(tile)
		except ValueError:
			print 'Could not load level: \'%s\' was empty.' % file
		
		_file.close()
		
		return self.tiles
	
	def save(self,file):
		try:
			_file = open(file,'w')
		except:
			raise Exception('Could not write to \'%s\'!' % file)
		
		_file.write(json.dumps(self.tiles))
		_file.close()
		
		logging.info('Saved level: %s' % file)