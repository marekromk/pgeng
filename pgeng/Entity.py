'''An Entity class'''
#IMPORTS
import pygame, math
#IMPORTS

#COLLISIONTEST
def CollisionTest(RectObject, CollisionList):
	'''A function used by the PhysicsObject class to check collisions with tiles'''
	return [Rect for Rect in CollisionList if RectObject.colliderect(Rect)]
#COLLISIONTEST

#ENTITY
class Entity:
	'''A physics object with a function for movement and collision
	It needs a position and a width and height for the pygame.Rect object
	Use self.Location[0] and self.Location[1] instead of self.rect.x and self.rect.y

	Attributes:

	Alpha

	Flips

	Location

	rect

	Rotation

	Scale'''
	#__INIT__
	def __init__(self, Location, Size):
		'''Initialising an Entity Object'''
		self.rect = pygame.Rect(Location, Size)
		self.Location = list(Location)

		self.Flips = [False, False]
		self.Rotation = 0
		self.Scale = [1, 1]
		self.Alpha = 255
	#__INIT__

	#CENTER
	@property
	def Center(self):
		'''Returns the center location of the Entity'''
		return [self.Location[0] + self.rect.w / 2, self.Location[1] + self.rect.h / 2]
	#CENTER

	#GETANGLE
	def GetAngle(self, Target):
		'''Get the angle to a target
		Target can be an Entity object or a list or tuple of an x and y coordinate
		It will go from the center of the Entity
		It will returns the angle in radians, not degrees

		Returns: Float'''
		if isinstance(Target, Entity):
			return math.atan2(Target.Center[1] - self.Center[1], Target.Center[0] - self.Center[0])
		return math.atan2(Target[1] - self.Center[1], Target[0] - self.Center[0])
	#GETANGLE

	#GETDISTANCE
	def GetDistance(self, Target):
		'''Get the distance to a target
		Target can be an Entity object or a list or tuple of an x and y coordinate

		Returns: Float'''
		if isinstance(Target, Entity):
			return math.sqrt((Target.Location[0] - self.Location[0]) ** 2 + (Target.Location[1] - self.Location[1]) ** 2)
		return math.sqrt((Target[0] - self.Location[0]) ** 2 + (Target[1] - self.Location[1]) ** 2)
	#GETDISTANCE

	#INRANGE
	def InRange(self, Target, Range):
		'''This will check if a target is in a specified range
		This uses GetDistance, so check GetDistance() for Target argument

		Returns: Boolean'''
		return self.GetDistance(Target) <= Range
	#INRANGE

	#SETSCALE
	def SetScale(self, Scale):
		'''This sets the scale for the image
		It can be a list or tuple with the scale for the width and the scale for the height
		If it is a number, than it will be set for the width and height'''
		if type(Scale) is list or type(Scale) is tuple:
			self.Scale = list(Scale)
		else:
			self.Scale = [Scale, Scale]
	#SETSCALE

	#TRANSFORMIMAGE
	def TransformImage(self, Surface):
		'''This will transform the image with the current values of the variables

		It will scale it according to the Scale variable
		It will flip it horizontal and vertical according to the Flips variable
		It will rotate it according to the Rotation variable, pygame will rotate it in the other direction compared to degrees in math
		It will also set and alpha according to the Alpha variable

		For more information about the rotation, go to https://www.pygame.org/docs/ref/transform.html#pygame.transform.rotate

		Returns: pygame.Surface'''
		Image = Surface
		if self.Scale != [1, 1]:
			Image = pygame.transform.scale(Image, (int(Image.get_width() * self.Scale[0]), int(Image.get_height() * self.Scale[1])))
		if any(self.Flips):
			Image = pygame.transform.flip(Image, self.Flips[0], self.Flips[1])
		if self.Rotation:
			Image = pygame.transform.rotate(Image, self.Rotation)
		if self.Alpha != 255:
			Image.set_alpha(self.Alpha)
		return Image
	#TRANSFORMIMAGE

	#MOVEMENT
	def Movement(self, Momentum, Tiles):
		'''Changing the position of the Entity object
		It needs a list that has the location change since last frame [x, y] not the actual x and y coordinates
		It also needs a list with Tile objects in it

		It returns a dictionary with booleans to show what part of the rect collide with the tiles:
		{'Top': False, 'Bottom': False, 'Right': False, 'Left': False}

		Returns: Dictionary'''
		#VARIABLES
		self.Location = list(self.Location)
		CollisionTypes = {'Top': False, 'Bottom': False, 'Right': False, 'Left': False}
		NormalTiles = [Tile.rect for Tile in Tiles if not Tile.Ramp]
		RampTiles = [Tile for Tile in Tiles if Tile.Ramp]
		#VARIABLES

		#NORMALTILES
		self.Location[0] += Momentum[0]
		self.rect.x = self.Location[0]
		HitList = CollisionTest(self.rect, NormalTiles)
		for Tile in HitList:
			if Momentum[0] > 0:
				self.rect.right = Tile.left
				CollisionTypes['Right'] = True
			elif Momentum[0] < 0:
				self.rect.left = Tile.right
				CollisionTypes['Left'] = True
			self.Location[0] = self.rect.x

		self.Location[1] += Momentum[1]
		self.rect.y = self.Location[1]
		HitList = CollisionTest(self.rect, NormalTiles)
		for Tile in HitList:
			if Momentum[1] > 0:
				self.rect.bottom = Tile.top
				CollisionTypes['Bottom'] = True
			elif Momentum[1] < 0:
				self.rect.top = Tile.bottom
				CollisionTypes['Top'] = True
			self.Location[1] = self.rect.y
		#NORMALTILES

		#RAMPS
		for Ramp in RampTiles:
			RampHitBox = Ramp.rect
			if self.rect.colliderect(RampHitBox):
				RelativeX = self.rect.x - RampHitBox.x
				if Ramp.Ramp == 1 or Ramp.Ramp == 4:
					HeightPosition = Ramp.Size - RelativeX
				else:
					HeightPosition = RelativeX + self.rect.w

				HeightPosition = min(HeightPosition, Ramp.Size)
				HeightPosition = max(HeightPosition, 0)

				if Ramp.Ramp == 1 or Ramp.Ramp == 2:
					YPosition = RampHitBox.y + HeightPosition
				else:
					YPosition = RampHitBox.y + Ramp.Size - HeightPosition

				if (Ramp.Ramp == 3 or Ramp.Ramp == 4) and self.rect.bottom > YPosition:
					self.rect.bottom = YPosition
					self.Location[1] = self.rect.y
					CollisionTypes['Bottom'] = True
				elif (Ramp.Ramp == 1 or Ramp.Ramp == 2) and self.rect.top < YPosition:
					self.rect.top = YPosition
					self.Location[1] = self.rect.y
					CollisionTypes['Top'] = True
		#RAMPS

		return CollisionTypes
	#MOVEMENT
#ENTITY