import somber as somber_engine
import logging
import time
import sys
import os

__name__ = 'Ghost Runner'

if os.path.exists('release.lock'):
	__version__ = open('release.lock','r').readline()
else:
	__version__ = time.strftime('%m.%d.%Y')


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
	def __init__(self,sprite):
		somber_engine.active.__init__(self,sprite,somber=somber)
		
		somber.solid_objects.add(self)

class character(somber_engine.active):
	def __init__(self):
		somber_engine.active.__init__(self,'mario.png',somber=somber)
		
		somber.add_active(self)
	
	def jump(self):
		self.vspeed = -8
		#self.gravity = 0.3
	
	def update(self):
		somber_engine.active.update(self)
		
		_collides = self.collides_with_group(somber.solid_objects)
		
		if _collides:
			for object in _collides:
				_xoffset_right_mid = (self.rect.midright[0]-object.rect.midleft[0])
				_xoffset_left_mid = (object.rect.midright[0]-self.rect.midleft[0])
				_yoffset_bottom = (self.rect.midbottom[1]-object.rect.topleft[1])
				
				if _xoffset_right_mid<30 and _yoffset_bottom>1 and self.vspeed<=1:
					self.rect.move_ip(-_xoffset_right_mid,0)
					self.hspeed = 0
				
				if _xoffset_left_mid<30 and _yoffset_bottom>1 and self.vspeed<=1:
					self.rect.move_ip(_xoffset_left_mid,0)
					self.hspeed = 0
				
				if _yoffset_bottom<30 and self.vspeed>=0:
					self.rect.move_ip(0,-_yoffset_bottom)
					self.vspeed = 0

def callback():
	pass

for x in range(864/64):
	#if x == 3: continue
	_plat = platform('platform-2.png')
	_plat.set_pos((x*64,364))
	somber.add_active(_plat)

_plat = platform('wall-1.png')
_plat.set_pos((128,300))
somber.add_active(_plat)

_player = character()
_player.x_limit_min = 0
_player.x_limit_max = 800
_player.y_limit_max = 600
_player.set_pos((80,100))
_player.gravity = 0.3
_player.set_movement('horizontal')
_player.hspeed_max = 3

somber.bind_key('z',_player.jump)

somber.add_active(_player)

somber.set_background('temp_background.png')
somber.run(callback)