import os, sys, pygame
from pygame.locals import *

__author__  = 'flags'
__contact__ = 'jetstarforever@gmail.com'
__license__ = 'WTFPLv2'
__version__ = '0.1'
__about__   = '2d game engine using PyGame'

class ActiveGroup(pygame.sprite.Group):
	"""'Give me $20' -flags, 2012"""
	def draw(self,surface):
		spritedict = self.spritedict
		surface_blit = surface.blit
		dirty = self.lostsprites
		self.lostsprites = []
		dirty_append = dirty.append
		for s in self.sprites():
			r = spritedict[s]
			
			if s.static:
				newrect = surface_blit(s.image, s.rect)
			else:
				_pos = (s.rect.topleft[0]-s.somber.camera_pos[0],
					s.rect.topleft[1]-s.somber.camera_pos[1])
				newrect = surface_blit(s.image, _pos)
			
			if r is 0:
				dirty_append(newrect)
			else:
				if newrect.colliderect(r):
					dirty_append(newrect.union(r))
				else:
					dirty_append(newrect)
					dirty_append(r)
			spritedict[s] = newrect
		return dirty

class Somber:
	def __init__(self,name='Somber Engine',win_size=(320,240),fps=60):
		self.name = name
		self.win_size = win_size
		self.fps = fps
		self.state = 'running'
		
		#Various
		self.resource_dir = ''
		self.input = {'up':False,
			'down':False,
			'left':False,
			'right':False}
		self.mouse_pos = (0,0)
		self.camera_pos = [0,0]
		
		#Lists
		self.fonts = []
		self.dirty_rects = []
		self.sprites = []
		self.keybinds = []
		
		#Start Pygame
		pygame.init()

		#Set up our clocks here
		self.clock_fps = pygame.time.Clock()

		#Define the surfaces we'll be drawing to
		self.window = pygame.display.set_mode(self.win_size)
		self.buffer = pygame.Surface(self.win_size)
		self.background = pygame.Surface(self.win_size)
		
		#Set caption
		pygame.display.set_caption(self.name)
		
		#Create our sprite groups
		self.active_objects = ActiveGroup()
	
	def get_all_resources(self):
		_ret = []
		
		for root, dirs, files in os.walk(self.resource_dir):
			for infile in files:
				_fname = os.path.join(root, infile)
				file, ext = os.path.splitext(_fname)
				if ext in ['.jpg','.JPG','.png','.PNG']:
					_ret.append(_fname.replace(self.resource_dir+os.sep,''))
		
		return _ret
	
	def create_group(self):
		return pygame.sprite.RenderUpdates()
	
	def bind_key(self,key,callback):
		self.keybinds.append({'key':key,'callback':callback})
	
	def add_active(self,object):
		self.active_objects.add(object)
	
	def add_sprite(self,name):
		try:
			_surface = load_image(os.path.join(self.resource_dir,name))
		except:
			raise Exception('Sprite not found: %s' % os.path.join(self.resource_dir,name))
		
		self.sprites.append({'name':name,'surface':_surface})
		
		return _surface
	
	def get_sprite(self,name):
		for sprite in self.sprites:
			if sprite['name'] == name:
				return sprite['surface']
		
		print 'Cached new sprite: \'%s\'' % (name)
		return self.add_sprite(name)
	
	def add_font(self,font,size):
		self.fonts.append({'name':font,'size':size,'font':pygame.font.Font(font,size)})
	
	def get_font(self,name):
		for font in self.fonts:
			if font['name']==name:
				return font
		
		return None
	
	def set_background_image(self,name):
		self.background_image = self.get_sprite(name)
		self.background.blit(self.background_image,(0,0))
		self.window.blit(self.background,(0,0))
		
		pygame.display.update()
	
	def set_background_color(self,color):
		self.background.fill(color)
		self.window.blit(self.background,(0,0))
		
		pygame.display.update()
	
	def write(self,font,pos,text,color=(0,0,0),aa=True):
		_font = self.get_font(font)['font']
		
		self.dirty_rects.append(self.window.blit(_font.render(text, aa, color),pos))
	
	def get_input(self):
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key in [K_ESCAPE,K_q]:
				pygame.quit()
				sys.exit()
			
			elif event.type == KEYDOWN:
				if event.key == K_UP or event.key == K_KP8:
					self.input['up'] = True
				elif event.key == K_DOWN or event.key == K_KP2:
					self.input['down'] = True
				elif event.key == K_LEFT or event.key == K_KP4:
					self.input['left'] = True
				elif event.key == K_RIGHT or event.key == K_KP6:
					self.input['right'] = True
				elif event.key == K_KP7:
					self.input['upleft'] = True
				elif event.key == K_KP9:
					self.input['upright'] = True
				elif event.key == K_KP1:
					self.input['downleft'] = True
				elif event.key == K_KP3:
					self.input['downright'] = True
				
				for entry in self.keybinds:
					if len(entry['key'])==1 and ord(entry['key']) == event.key:
						entry['callback']()
			
			elif event.type == KEYUP:
				if event.key == K_UP or event.key == K_KP8:
					self.input['up'] = False
				elif event.key == K_DOWN or event.key == K_KP2:
					self.input['down'] = False
				elif event.key == K_LEFT or event.key == K_KP4:
					self.input['left'] = False
				elif event.key == K_RIGHT or event.key == K_KP6:
					self.input['right'] = False
				elif event.key == K_KP7:
					self.input['upleft'] = False
				elif event.key == K_KP9:
					self.input['upright'] = False
				elif event.key == K_KP1:
					self.input['downleft'] = False
				elif event.key == K_KP3:
					self.input['downright'] = False
			
			elif event.type == MOUSEMOTION:
				self.mouse_pos = tuple(event.pos)
			
			elif event.type == MOUSEBUTTONDOWN:
				for entry in self.keybinds:
					if entry['key']=='m1':
						entry['callback'](event.button)
	
	def run(self,callback):
		while self.state=='running':
			#Grab input
			self.get_input()
			
			#Update all groups
			self.active_objects.update()
			self.active_objects.clear(self.window,self.background)
			
			callback()
			
			#Draw all groups
			self.dirty_rects.extend(self.active_objects.draw(self.window))
			
			#Update the screen
			pygame.display.update(self.dirty_rects)
			self.clock_fps.tick(self.fps)
			
			self.dirty_rects = []

class general(pygame.sprite.Sprite):
	def __init__(self,sprite,pos=None):
		self.sprite = sprite
		
		self.pos = list(pos)
		self.start_pos = list(pos)
		self.static = False
		
		self.movement = None
		
		self.alpha = 255
		self.last_alpha = 255
		
		self.image = self.sprite
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos
		self.image.blit(self.sprite,self.rect)

		pygame.sprite.Sprite.__init__(self)
	
	def set_pos(self,pos,set_start=False):
		self.rect.topleft = list(pos)
		if set_start: self.start_pos = list(pos)
	
	def set_movement(self,type):
		if type in ['horizontal','vertical','ortho']:
			self.movement = type
		elif type == None:
			self.movement = None
		else:
			self.movement = None
			
			raise Exception('Invalid movement type: \'%s\'' % type)
		
		self.movement
	
	def destroy(self):
		pass

class static(general):
	def __init__(self,sprite=None,pos=(0,0)):		
		general.__init__(self,sprite=sprite,pos=pos)
		
		static.add(self)

class active(general):
	def __init__(self,sprite,pos=(0,0),somber=None):
		if not somber:
			raise Exception('No somber callback set!')
		
		self.somber = somber
		self.sprite = somber.get_sprite(sprite)
		
		general.__init__(self,sprite=self.sprite,pos=pos)
		
		self.hspeed = 0
		self.hspeed_max = 0
		self.hspeed_min = 0
		self.hfriction_move = 0
		self.hfriction_stop = 0
		
		self.vspeed = 0
		self.vspeed_max = 0
		self.vspeed_min = 0
		
		self.x_limit_min = None
		self.x_limit_max = None
		
		self.y_limit_min = None
		self.y_limit_max = None
		
		self.gravity = 0
	
	def set_sprite(self,sprite):
		self.sprite = self.somber.get_sprite(sprite)
		self.image = self.sprite
		self.image.blit(self.sprite,(0,0))
	
	def set_alpha(self,val):
		self.image = self.sprite.copy()
		self.image.set_alpha(val)
	
	def update(self):
		self.pos = list(self.rect.topleft)
		
		if self.movement=='horizontal':
			if self.somber.input['right']:
				if self.hfriction_move and self.hspeed<self.hspeed_max:
					self.hspeed += self.hfriction_move
				else:
					self.hspeed = self.hspeed_max
			elif self.somber.input['left']:
				if self.hfriction_move and self.hspeed>-self.hspeed_max:
					self.hspeed -= self.hfriction_move
				else:
					self.hspeed = -self.hspeed_max
			else:
				if self.hfriction_stop:
					if self.hspeed>0:
						self.hspeed -= self.hfriction_stop
					elif self.hspeed<0:
						self.hspeed += self.hfriction_stop
				else:
					self.hspeed = self.hspeed_min
		elif self.movement=='vertical':
			if self.somber.input['right']: self.vspeed = self.vspeed_max
			elif self.somber.input['left']: self.vspeed = -self.vspeed_max
			else: self.vspeed = self.vspeed_min
		
		if not self.x_limit_max == None:
			if self.rect.topright[0]>self.x_limit_max:
				if self.hspeed>0:
					self.hspeed = 0
		
		if not self.x_limit_min == None:	
			if self.pos[0]<self.x_limit_min:
				if self.hspeed<0:
					self.hspeed = 0
					
		if not self.y_limit_max == None:
			if self.rect.bottomleft[1]>self.y_limit_max:
				if self.vspeed>0:
					self.vspeed = 0
		
		if not self.y_limit_min == None:	
			if self.pos[1]<self.y_limit_min:
				if self.vspeed<0:
					self.vspeed = 0
		
		self.vspeed+=self.gravity
		
		if not self.alpha == self.last_alpha:
			self.set_alpha(self.alpha)
		
		self.last_alpha = self.alpha
		
		self.rect.topleft = [self.rect.topleft[0]+round(self.hspeed),
			self.rect.topleft[1]+round(self.vspeed)]
	
	def collide_at(self,pos,other):
		return other.rect.collidepoint((pos))
	
	def collides_with(self,object):
		if self.rect.colliderect(object.rect): return True
		
		return False
	
	def collides_with_group(self,group):
		_collides = pygame.sprite.spritecollide(self,group,False)
		if _collides:
			return _collides
		
		return False
	
	def destroy(self):
		active.remove(self)
		
		general.destroy(self)

class particle(active):
	def __init__(self,sprite=None,pos=(0,0),gravity=0.05,alpha=255,velocity=(0,0)):
		active.__init__(self,sprite=sprite,pos=pos)
		
		self.set_alpha(alpha)
		self.gravity = gravity
		
		self.hspeed = velocity[0]
		self.vspeed = velocity[1]
	
	def update(self):
		self.alpha-=2
		
		if self.alpha<=0: self.destroy()
		
		if self.pos[0]<0 or self.pos[0]>win_size[0]\
			or self.pos[1]<0 or self.pos[1]>win_size[1]:
			self.destroy()
		
		active.update(self)

def load_image(name):
	try:
		image = pygame.image.load(name)
	except:
		print 'Could not find: %s' % name
		sys.exit()
	
	if name.count('.png'):
		image=image.convert_alpha()
	else:
		image=image.convert()
		image.set_colorkey((255,255,255))
	
	return image