'''An Entity class'''
#IMPORTS
import pygame, math
from .Animations import Animations
#IMPORTS

#COLLISION_TEST
def collision_test(rect, collision_list):
	'''A function used by the Entity class to check collisions with tiles'''
	return [list_rect for list_rect in collision_list if rect.colliderect(list_rect)]
#COLLISION_TEST

#ENTITY
class Entity:
	'''An entity with usefull functions
	It needs a position and a size for the pygame.Rect object
	Use Entity.location[0] and Entity.location[1] instead of Entity.rect.x and Entity.rect.y
	It has an animation class

	Attributes:

	alpha

	animations

	flips

	location

	rect

	rotation

	scale'''
	#__INIT__
	def __init__(self, location, size):
		'''Initialising an Entity object'''
		self.rect = pygame.Rect(location, size)
		self.location = list(location)

		self.flips = [False, False]
		self.rotation = 0
		self.scale = [1, 1]
		self.alpha = 255

		self.animations = Animations(None)
	#__INIT__

	#CENTER
	@property
	def center(self):
		'''Returns the center location of the Entity'''
		return [self.location[0] + self.rect.w / 2, self.location[1] + self.rect.h / 2]
	#CENTER

	#GET_ANGLE
	def get_angle(self, target):
		'''Get the angle to a target
		target can be an Entity object or a list or tuple with an x and y coordinate
		It will go from the center of the Entity
		It will returns the angle in radians, not degrees

		Returns: Float'''
		if isinstance(target, Entity):
			return math.atan2(target.center[1] - self.center[1], target.center[0] - self.center[0])
		return math.atan2(target[1] - self.center[1], target[0] - self.center[0])
	#GET_ANGLE

	#GET_DISTANCE
	def get_distance(self, target):
		'''Get the distance to a target
		target can be an Entity object or a list or tuple with an x and y coordinate

		Returns: Float'''
		if isinstance(target, Entity):
			return math.sqrt((target.location[0] - self.location[0]) ** 2 + (target.location[1] - self.location[1]) ** 2)
		return math.sqrt((target[0] - self.location[0]) ** 2 + (target[1] - self.location[1]) ** 2)
	#GET_DISTANCE

	#IN_RANGE
	def in_range(self, target, range):
		'''This will check if a target is in a specified range
		target can be an Entity object or a list or tuple with an x and y coordinate
		This uses get_distance

		Returns: Boolean'''
		return self.get_distance(target) <= range
	#IN_RANGE

	#SET_SCALE
	def set_scale(self, scale):
		'''This sets the scale for the image
		It can be a list or tuple with the scale for the width and the scale for the height
		If it is a number, than it will be set for the width and height'''
		if type(scale) is list or type(scale) is tuple:
			self.scale = list(scale)
		else:
			self.scale = [scale, scale]
	#SET_SCALE

	#IMAGE
	def current_image(self, delta_time=1):
		'''Get the current image in the animation
		delta_time is how much the frame should update, usually it would be 1
		It also get transformed with transform_image

		Returns: pygame.Surface'''
		return self.transform_image(self.animations.current_image(delta_time))
	#IMAGE

	#TRANSFORM_IMAGE
	def transform_image(self, image):
		'''This will transform the image with the current values of the variables

		It will scale it according to the scale variable
		It will flip it horizontal and vertical according to the flips variable
		It will rotate it according to the rotation variable, pygame will rotate it in the other direction compared to degrees in math
		It will also set and alpha according to the alpha variable

		For more information about the rotation, go to https://www.pygame.org/docs/ref/transform.html#pygame.transform.rotate

		Returns: pygame.Surface'''
		image = image.copy()
		if self.scale != [1, 1]:
			image = pygame.transform.scale(image, (int(image.get_width() * self.scale[0]), int(image.get_height() * self.scale[1])))
		if any(self.flips):
			image = pygame.transform.flip(image, self.flips[0], self.flips[1])
		if self.rotation:
			image = pygame.transform.rotate(image, self.rotation)
		if self.alpha != 255:
			image.set_alpha(self.alpha)
		return image
	#TRANSFORM_IMAGE

	#MOVEMENT
	def movement(self, momentum, tiles):
		'''Changing the position of the Entity object
		It needs a list that has the location change since last frame [x, y] not the actual x and y coordinates
		It also needs a list with Tile objects in it

		It returns a dictionary with booleans to show what part of the rect collide with the tiles:
		{'top': False, 'bottom': False, 'right': False, 'left': False}

		Returns: Dictionary'''
		#VARIABLES
		self.location = list(self.location)
		collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
		normal_tiles = [tile.rect for tile in tiles if not tile.ramp]
		ramp_tiles = [tile for tile in tiles if tile.ramp]
		#VARIABLES

		#NORMAL_TILES
		self.location[0] += momentum[0]
		self.rect.x = self.location[0]
		hit_list = collision_test(self.rect, normal_tiles)
		for tile in hit_list:
			if momentum[0] > 0:
				self.rect.right = tile.left
				collision_types['right'] = True
			elif momentum[0] < 0:
				self.rect.left = tile.right
				collision_types['left'] = True
			self.location[0] = self.rect.x

		self.location[1] += momentum[1]
		self.rect.y = self.location[1]
		hit_list = collision_test(self.rect, normal_tiles)
		for tile in hit_list:
			if momentum[1] > 0:
				self.rect.bottom = tile.top
				collision_types['bottom'] = True
			elif momentum[1] < 0:
				self.rect.top = tile.bottom
				collision_types['top'] = True
			self.location[1] = self.rect.y
		#NORMAL_TILES

		#RAMPS
		for ramp in ramp_tiles:
			ramp_hitbox = ramp.rect
			if self.rect.colliderect(ramp_hitbox):
				delta_x = self.rect.x - ramp_hitbox.x
				if ramp.ramp == 1 or ramp.ramp == 4:
					height_position = ramp.size - delta_x
				else:
					height_position = delta_x + self.rect.w

				height_position = min(height_position, ramp.size)
				height_position = max(height_position, 0)

				if ramp.ramp == 1 or ramp.ramp == 2:
					y = ramp_hitbox.y + height_position
				else:
					y = ramp_hitbox.y + ramp.size - height_position

				if (ramp.ramp == 3 or ramp.ramp == 4) and self.rect.bottom > y:
					self.rect.bottom = y
					self.location[1] = self.rect.y
					collision_types['bottom'] = True
				elif (ramp.ramp == 1 or ramp.ramp == 2) and self.rect.top < y:
					self.rect.top = y
					self.location[1] = self.rect.y
					collision_types['top'] = True
		#RAMPS

		return collision_types
	#MOVEMENT
#ENTITY