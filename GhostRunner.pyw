import somber as somber_engine
import logging
import time
import sys
import os

__name__ = 'Ghost Runner'

if os.path.exists('release.lock'):
	__version__ = time.strftime('%m.%d.%Y')
else:
	__version__ = 'Stable'


#Setup logging
logger = logging.getLogger()

if '-debug' in sys.argv:
	logger.setLevel(logging.DEBUG)
else:
	logger.setLevel(logging.INFO)

file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_formatter = logging.Formatter('%(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(console_formatter)
logger.addHandler(ch)
logging.info('%s - %s' % (__name__,__version__))


#Setup Somber
somber = somber_engine.somber(name='%s - %s' % (__name__,__version__),win_size=(800,600))
somber.resource_dir = os.path.join('Art','Tiles','mayan')
somber.solid_objects = somber.create_group()

class platform(somber_engine.active):
	def __init__(self):
		somber_engine.active.__init__(self,'platform-2.png',somber=somber)
		
		somber.solid_objects.add(self)

class character(somber_engine.active):
	def __init__(self):
		somber_engine.active.__init__(self,'mario.png',somber=somber)
	
	def jump(self):
		self.vspeed = -8
	
	def update(self):
		somber_engine.active.update(self)
		
		_collides = self.collides_with_group(somber.solid_objects)
		if _collides:
			_yoffset = (self.rect.midbottom[1]-_collides.rect.topleft[1])
			self.rect.move_ip(0,-_yoffset)
			self.vspeed = 0

def callback():
	pass

for x in range(864/64):
	_plat = platform()
	_plat.set_pos((x*64,350))
	somber.add_active(_plat)

_player = character()
_player.set_pos((80,100))
_player.gravity = 0.3
_player.set_movement('horizontal')
_player.hspeed_max = 3

somber.bind_key('z',_player.jump)

somber.add_active(_player)

somber.set_background('temp_background.png')
somber.run(callback)