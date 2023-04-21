'An Entity class'
import pygame
from .animations import Animations

def tiles_collision(rect, tiles):
	'''A function used by the Entity class to check collisions with tiles

	Returns: list'''
	return [tile for tile in tiles if rect.colliderect(tile)]

class Entity:
	'''An entity with usefull functions
	It needs a position and a size for the pygame.Rect object
	Use Entity.location.x and Entity.location.y instead of Entity.rect.x and Entity.rect.y
	Entity.location is a pygame.math.Vector2 object
	It has an animation class

	Attributes:

	alpha

	animations

	flips

	location

	rect

	rotation

	scale'''
	def __init__(self, location, size):
		'Initialising an Entity object'
		self.rect = pygame.Rect(location, size)
		self.location = pygame.Vector2(location) #rect uses truncated integers, Vector2 is more precise

		self.flips = [False, False] #x, y
		self.rotation = 0
		self.scale = [1, 1] #x, y
		self.alpha = 255

		self.animations = Animations(None)

	def __repr__(self):
		'''Returns a string representation of the object

		Returns: str'''
		return f'pgeng.Entity{tuple(self.location), self.rect.size}'

	@property
	def center(self):
		'''Returns the center location of the Entity

		Returns: pygame.math.Vector2'''
		return pygame.Vector2([self.location[i] + self.rect.size[i] * 0.5 for i in range(2)])

	def get_angle(self, target):
		'''Get the angle to a target
		target can be an Entity object, a list/tuple or pygame.math.Vector2
		It will go from the center of the Entity
		It will returns the angle in degrees

		Returns: float'''
		if isinstance(target, Entity):
			return pygame.Vector2().angle_to(target.center - self.center)
		return pygame.Vector2().angle_to(target - self.center)

	def get_distance(self, target):
		'''Get the distance to a target
		target can be an Entity object, a list/tuple or pygame.math.Vector2

		Returns: float'''
		if isinstance(target, Entity):
			return self.location.distance_to(target.location)
		return self.location.distance_to(target)

	def in_range(self, target, range):
		'''This will check if a target is in a specified range
		target can be an Entity object, a list/tuple or pygame.math.Vector2
		This uses get_distance

		Returns: bool'''
		return self.get_distance(target) <= range

	def set_scale(self, scale=1):
		'''This sets the scale for the image
		It can be a list or tuple with the scale for the width and the scale for the height
		If it is a number, than it will be set for the width and height'''
		if (type(scale) is list or type(scale) is tuple) and len(scale) != 2:
			raise ValueError('scale should have 2 values')
		self.scale = list(scale) if type(scale) is list or type(scale) is tuple else [scale, scale]

	def current_image(self, delta_time=1):
		'''Get the current image in the animation
		delta_time is how much the frame should update, usually it would be 1
		It also get transformed with transform_image

		Returns: pygame.Surface'''
		return self.transform_image(self.animations.current_image(delta_time))

	def transform_image(self, image):
		'''This will transform the image with the current values of the variables

		It will scale it according to the scale variable
		It will flip it horizontal and vertical according to the flips variable
		It will rotate it according to the rotation variable
		It will also set and alpha according to the alpha variable

		For more information about transforming, go to https://www.pygame.org/docs/ref/transform.html

		Returns: pygame.Surface'''
		transformed_image = image.copy()
		if (type(self.scale) is list or type(self.scale) is tuple) and len(self.scale) != 2:
			raise ValueError('scale should have 2 values')
		if len(self.flips) != 2:
			raise ValueError('flips should have 2 values')
		if list(self.scale) != [1, 1]:
			transformed_image = pygame.transform.scale(transformed_image, [round(image.get_size()[i] * self.scale[i]) for i in range(2)])
		if any(self.flips):
			transformed_image = pygame.transform.flip(transformed_image, self.flips[0], self.flips[1])
		if self.rotation % 360:
			transformed_image = pygame.transform.rotate(transformed_image, self.rotation % 360)
		if self.alpha != 255:
			transformed_image.set_alpha(self.alpha)
		return transformed_image

	def movement(self, momentum, tiles):
		'''Changing the position of the Entity object
		momentum must be a list/tuple with how much it should move horizontally and vertically
		It also needs a list with Tile objects in it

		It returns a dictionary with booleans to show what part of the rect is colliding with the Tile objects
		It also shows the rect is colliding with a ramp
		{'top': False, 'bottom': False, 'right': False, 'left': False, 'ramp': False}

		Returns: dict'''
		self.location = pygame.Vector2(self.location)
		collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False, 'ramp': False}
		normal_tiles = [tile.rect for tile in tiles if not tile.ramp]
		ramp_tiles = [tile for tile in tiles if tile.ramp]

		#check left and right side first
		self.location.x += momentum[0]
		self.rect.x = round(self.location.x) #round it, because a rect normally truncates
		hit_list = tiles_collision(self.rect, normal_tiles)
		for tile in hit_list:
			if momentum[0] > 0: #going to the right
				self.rect.right = tile.left
				collision_types['right'] = True
			elif momentum[0] < 0: #going to the left
				self.rect.left = tile.right
				collision_types['left'] = True
			self.location.x = self.rect.x

		#check top and bottom second
		self.location.y += momentum[1]
		self.rect.y = round(self.location.y) #round it, because a rect normally truncates
		hit_list = tiles_collision(self.rect, normal_tiles)
		for tile in hit_list:
			if momentum[1] > 0: #going down
				self.rect.bottom = tile.top
				collision_types['bottom'] = True
			elif momentum[1] < 0: #going up
				self.rect.top = tile.bottom
				collision_types['top'] = True
			self.location.y = self.rect.y

		#check ramps last
		for ramp in ramp_tiles:
			ramp_hitbox = ramp.rect
			if self.rect.colliderect(ramp_hitbox):
				delta_x = self.rect.x - ramp_hitbox.x #difference between entity's and ramp's x
				if ramp.ramp == 1 or ramp.ramp == 4: #left side of the entity touches the ramp
					height_position = ramp_hitbox.w - delta_x
				else: #right side of the entity touches the ramp
					height_position = delta_x + self.rect.w

				height_position = min(height_position, ramp_hitbox.w) #horizontal position should not be more than width of ramp
				height_position = max(height_position, 0) #horizontal position should not be less that 0 compared to the ramp

				if ramp.ramp == 1 or ramp.ramp == 2: #top of the entity touches the ramp
					y_position = ramp_hitbox.y + height_position
				else: #bottom of the entity touches the ramp
					y_position = ramp_hitbox.bottom - height_position

				if (ramp.ramp == 3 or ramp.ramp == 4) and self.rect.bottom > y_position:
					self.rect.bottom = y_position
					self.location.y = self.rect.y
					collision_types['bottom'] = True
					collision_types['ramp'] = True
				elif (ramp.ramp == 1 or ramp.ramp == 2) and self.rect.top < y_position:
					self.rect.top = y_position
					self.location.y = self.rect.y
					collision_types['top'] = True
					collision_types['ramp'] = True

		return collision_types