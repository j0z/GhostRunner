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
somber = somber_engine.somber(name='%s - %s' % (__name__,__version__),win_size=(640,480))
somber.resource_dir = os.path.join('Art','Tiles','mayan')
somber.solid_objects = somber.create_group()

class platform(somber_engine.active):
	def __init__(self,sprite):
		somber_engine.active.__init__(self,sprite,somber=somber)
		
		somber.solid_objects.add(self)

class character(somber_engine.active):
	def __init__(self):
		somber_engine.active.__init__(self,'mario.png',somber=somber)
		
		self.on_ground = False
	
	def jump(self):
		if self.on_ground:
			self.vspeed = -10
	
	def update(self):
		somber_engine.active.update(self)
		
		_collides = self.collides_with_group(somber.solid_objects)
		
		if _collides:
			for object in _collides:
				#Left
				if self.collide_at((self.rect.topleft[0],self.rect.topleft[1]+1),object):
					self.hspeed = 0
					self.rect.move_ip(-(self.rect.topleft[0]-object.rect.topright[0]),0)
				elif self.collide_at((self.rect.bottomleft[0],
					self.rect.bottomleft[1]-(self.vspeed+1)),object):
					self.hspeed = 0
					self.rect.move_ip(-(self.rect.bottomleft[0]-object.rect.bottomright[0]),0)
				
				#Right
				elif self.collide_at((self.rect.topright[0],self.rect.topright[1]+1),object):
					self.hspeed = 0
					self.rect.move_ip(-(self.rect.topright[0]-object.rect.topleft[0]),0)
				elif self.collide_at((self.rect.bottomright[0],
					self.rect.bottomright[1]-(self.vspeed+1)),object):
					self.hspeed = 0
					self.rect.move_ip(-(self.rect.bottomright[0]-object.rect.bottomleft[0]),0)
				
				#Down
				elif self.vspeed>=0:
					if self.collide_at((self.rect.bottomleft[0],self.rect.bottomleft[1]+1),object):
						self.vspeed = 0
						self.rect.move_ip(0,-(self.rect.bottomleft[1]-object.rect.topleft[1]))
					elif self.collide_at((self.rect.bottomright[0]-1,self.rect.bottomright[1]+1),object):
						self.vspeed = 0
						self.rect.move_ip(0,-(self.rect.bottomright[1]-object.rect.topright[1]))
					
				if self.collide_at((self.rect.bottomleft[0],self.rect.bottomleft[1]+3),object):
					self.on_ground = True
				elif self.collide_at((self.rect.bottomright[0]-1,self.rect.bottomright[1]+3),object):
					self.on_ground = True
				else:
					self.on_ground = False
		
		if self.vspeed>=1 or self.vspeed<0: self.on_ground = False

def callback():
	pass

for x in range(864/64):
	#if x == 3: continue
	_plat = platform('platform-2.png')
	_plat.set_pos((x*64,350))
	somber.add_active(_plat)

_plat = platform('wall-1.png')
_plat.set_pos((128,246))
somber.add_active(_plat)
_plat = platform('wall-1.png')
_plat.set_pos((128,300))
somber.add_active(_plat)

_player = character()
_player.x_limit_min = 0
_player.x_limit_max = 800
_player.y_limit_max = 600
_player.set_pos((80,250))
_player.gravity = 0.3
_player.set_movement('horizontal')
_player.hspeed_max = 3

somber.bind_key('z',_player.jump)

somber.add_active(_player)

somber.set_background('temp_background.png')
somber.run(callback)