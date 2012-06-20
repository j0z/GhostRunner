import somber as somber_engine
import logging
import level
import time
import sys
import os

__name__ = 'Ghost Runner'

if os.path.exists('release.lock'):
	__version__ = open('release.lock','r').readline()
else:
	__version__ = time.strftime('%m.%d.%Y')

##TODO: Remove
#To prevent crashes on non-dev machines
try:
	os.mkdir('levels')
except:
	pass

#Setup logging
logger = logging.getLogger()

if '-debug' in sys.argv:
	logger.setLevel(logging.DEBUG)
else:
	logger.setLevel(logging.INFO)

if '-editor' in sys.argv:
	win_size = (768,832)
else:
	win_size = (768,640)

file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_formatter = logging.Formatter('%(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(console_formatter)
logger.addHandler(ch)
logging.info('%s - %s' % (__name__,__version__))


#Setup Somber
somber = somber_engine.Somber(name='%s - %s' % (__name__,__version__),
	win_size=win_size)
somber.resource_dir = os.path.join('Art')
somber.solid_objects = somber.create_group()
somber.selector_objects = somber.create_group()
somber.add_font('ProggyClean.ttf',16)

#Create a level object
level = level.level()

#General gamestate stuff
gamestate = 'playing'
ghost = None
ghost_selector = None

class ghost_selector(somber_engine.active):
	def __init__(self,sprite):
		somber_engine.active.__init__(self,sprite,somber=somber)
		self.sprite_name = sprite
		self.static = True
		
		somber.selector_objects.add(self)
		
	def set_sprite(self,sprite):
		##TODO: Make this is function of Somber
		somber_engine.active.set_sprite(self,sprite)
		self.sprite_name = sprite

class ghost_placer(somber_engine.active):
	def __init__(self,sprite):
		somber_engine.active.__init__(self,sprite,somber=somber)
		self.sprite_name = sprite
		self.static = True
		self.level_pos = (0,0)
	
	def set_sprite(self,sprite):
		somber_engine.active.set_sprite(self,sprite)
		self.sprite_name = sprite
	
	def place(self):
		_collides = ghost.collides_with_group(somber.selector_objects)
		
		if _collides:
			self.set_sprite(_collides[0].sprite_name)
		elif (somber.mouse_pos[1]/64)<=9:
			_plat = platform(self.sprite_name)
			_pos = (self.pos[0]+somber.camera_pos[0],self.pos[1]+somber.camera_pos[1])
			_plat.set_pos(_pos,set_start=True)
			somber.add_active(_plat)

class platform(somber_engine.active):
	def __init__(self,sprite):
		somber_engine.active.__init__(self,sprite,somber=somber)
		self.sprite_name = sprite
		
		#Make the object collide with the player
		somber.solid_objects.add(self)
	
	def save(self):
		_save = {}
		_save['sprite'] = self.sprite_name
		_save['pos'] = tuple(self.rect.topleft)
		
		return _save

class character(somber_engine.active):
	def __init__(self):
		somber_engine.active.__init__(self,os.path.join('Characters','stand.png'),somber=somber)
		
		self.on_ground = False
	
	def jump(self):
		if self.on_ground:
			self.vspeed = -10
	
	def update(self):
		somber_engine.active.update(self)
		
		_collides = self.collides_with_group(somber.solid_objects)
		
		if _collides:
			for object in _collides:
				#Up
				if self.vspeed<0:
					if self.collide_at((self.rect.topleft[0]+5,self.rect.topleft[1]-1),object):
						self.vspeed = 0
						self.rect.move_ip(0,-(self.rect.topleft[1]-object.rect.bottomleft[1]))
					elif self.collide_at((self.rect.topright[0]-5,self.rect.topright[1]+1),object):
						self.vspeed = 0
						self.rect.move_ip(0,-(self.rect.topright[1]-object.rect.bottomright[1]))

				#Left
				if self.collide_at((self.rect.topleft[0]+1,self.rect.topleft[1]+1),object):
					self.hspeed = 0
					self.rect.move_ip(-(self.rect.topleft[0]-object.rect.topright[0]),0)
				elif self.collide_at((self.rect.bottomleft[0]+1,
					self.rect.bottomleft[1]-(self.vspeed+1)),object):
					self.hspeed = 0
					self.rect.move_ip(-(self.rect.bottomleft[0]-object.rect.bottomright[0]),0)
				
				#Right
				if self.collide_at((self.rect.topright[0],self.rect.topright[1]+1),object):
					self.hspeed = 0
					self.rect.move_ip(-(self.rect.topright[0]-object.rect.topleft[0]),0)
				elif self.collide_at((self.rect.bottomright[0],
					self.rect.bottomright[1]-(self.vspeed+1)),object):
					self.hspeed = 0
					self.rect.move_ip(-(self.rect.bottomright[0]-object.rect.bottomleft[0]),0)
				
				#Down
				if self.vspeed>=0:
					if self.collide_at((self.rect.bottomleft[0]+3,self.rect.bottomleft[1]+1),object):
						self.vspeed = 0
						self.rect.move_ip(0,-(self.rect.bottomleft[1]-object.rect.topleft[1]))
					elif self.collide_at((self.rect.bottomright[0]-4,self.rect.bottomright[1]+1),object):
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
	if gamestate=='designer':
		ghost.rect.topleft = ((somber.mouse_pos[0]/64)*64,
			(somber.mouse_pos[1]/64)*64)
		
		ghost.level_pos = (ghost.pos[0]+somber.camera_pos[0],
			ghost.pos[1]+somber.camera_pos[1])
	
	if _player.pos[0]>=win_size[0]/2:
		somber.camera_pos[0]=_player.pos[0]-(win_size[0]/2)
	if _player.pos[1]>=win_size[1]/2:
		somber.camera_pos[1]=_player.pos[1]-(win_size[1]/2)

def mouse_down(button):	
	if gamestate=='designer':
		if button==1:
			ghost.place()
		elif button==3:
			for object in somber.solid_objects:				
				if ghost.level_pos == object.rect.topleft:
					object.kill()

def move_cam_left():
	if gamestate=='designer' and self.camera_:
		somber.camera_pos[0]-=64

def move_cam_right():
	if gamestate=='designer':
		somber.camera_pos[0]+=64

def move_cam_up():
	if gamestate=='designer':
		somber.camera_pos[1]-=64
	
def move_cam_down():
	if gamestate=='designer':
		somber.camera_pos[1]+=64

def load(file):
	for object in level.load(file):
		_plat = platform(object['sprite'])
		_plat.set_pos(object['pos'],set_start=True)
		somber.add_active(_plat)

def save():
	if gamestate=='designer':
		level.tiles = []
		
		for object in somber.solid_objects:
			level.add_object(object.save())
		
		level.save(os.path.join('levels','test_level.dat'))

def enter_designer():
	#Since this is called externally, we have to set a global
	global gamestate, ghost
	
	#Stop all current movement
	reset_level()
	_player.gravity = 0
	_player.vspeed = 0
	_player.hspeed = 0
	_player.set_movement(None)
	
	#Create our ghost if we haven't already
	if not ghost:
		ghost = ghost_placer(os.path.join('Tiles','platform-1.png'))
		ghost.set_pos(somber.mouse_pos)
		somber.add_active(ghost)
		ghost.set_alpha(150)
		
		_x = 0
		_y = 12
		for resource in somber.get_all_resources():
			_ghost_selector = ghost_selector(resource)
			_ghost_selector.set_pos((_x*64,_y*64))
			somber.add_active(_ghost_selector)
			if _x>=12:
				_x=-1
				_y-=1
			_x+=1
	else:
		ghost.set_alpha(150)
		for object in somber.selector_objects:
			object.set_alpha(255)
	
	somber.write('ProggyClean.ttf',(0,0),'Designer',color=(90,90,90),aa=False)
	
	gamestate = 'designer'

def reset_level():
	global gamestate
	
	for object in somber.solid_objects:
		object.rect.topleft = object.start_pos
	
	if ghost:
		ghost.set_alpha(0)
		for object in somber.selector_objects:
			object.set_alpha(0)
	
	somber.camera_pos = [0,0]
	_player.set_pos((80,250))
	_player.gravity = 0.3
	_player.set_movement('horizontal')
	gamestate = 'playing'

_player = character()
_player.x_limit_min = 0
_player.x_limit_max = 1000
_player.y_limit_max = 1000
_player.set_pos((80,250))
_player.hspeed_max = 4
_player.hfriction_move = 0.2
_player.hfriction_stop = 0.4

load(os.path.join('levels','test_level.dat'))
reset_level()

somber.bind_key('z',_player.jump)
somber.bind_key('c',reset_level)
somber.bind_key('a',move_cam_left)
somber.bind_key('d',move_cam_right)
somber.bind_key('s',move_cam_down)
somber.bind_key('w',move_cam_up)
somber.bind_key('m1',mouse_down)
somber.bind_key('p',save)

if win_size == (768,832):
	somber.bind_key('x',enter_designer)

somber.add_active(_player)
somber.set_background_color((150,150,150))
somber.run(callback)