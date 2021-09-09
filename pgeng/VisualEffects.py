'''Functions and classes for visual effects in PyGame'''
#IMPORTS
import pygame, math
#IMPORTS

#CIRCLELIGHTING
def CircleLighting(Radius, Colour):
	'''Creates a surface twice as big as the given radius
	It draws a circle with the radius on it
	Recommended to blit with the special_flag pygame.BLEND_RGBA_ADD

	Returns: pygame.Surface'''
	LightingSurface = pygame.Surface((Radius * 2, Radius * 2))
	LightingSurface.set_colorkey((0, 0, 0))
	pygame.draw.circle(LightingSurface, Colour, (Radius, Radius), Radius)
	return LightingSurface
#CIRCLELIGHTING

#PARITCLE
class Particle:
	'''A particle to move and render
	It can also have gravity and a 'lighting' for the rendering'''
	#__INIT__
	def __init__(self, Location, Momentum, Size, Colour):
		'''Initialising a particle'''
		self.Location = list(Location)
		self.Momentum = Momentum
		self.Size = Size
		self.Colour = Colour
		self.Alive = True
	#__INIT__

	#MOVE
	def Move(self, SizeChange, YMomentum=0, DeltaTime=1):
		'''Move the location of the particle and change the size
		If the size is smaller or equal to 0, it will no longer be alive
		It also has gravity (YMomentum)'''
		self.Location = list(self.Location)
		self.Momentum[1] += YMomentum * DeltaTime
		self.Location[0] += self.Momentum[0] * DeltaTime
		self.Location[1] += self.Momentum[1] * DeltaTime
		self.Size -= SizeChange * DeltaTime
		if self.Size <= 0:
			self.Alive = False
	#MOVE

	#RENDER
	def Render(self, Surface, Scroll=[0, 0], LightingColour=None):
		'''Render the particle
		It can also render a lighting circle around the particle with a pygame.BLEND_RGBA_ADD flag'''
		if self.Alive:
			pygame.draw.circle(Surface, self.Colour, (self.Location[0] - Scroll[0], self.Location[1] - Scroll[1]), int(self.Size))
			if LightingColour:
				LightingRadius = self.Size * 2
				Surface.blit(CircleLighting(LightingRadius, LightingColour), (self.Location[0] - LightingRadius - Scroll[0], self.Location[1] - LightingRadius - Scroll[1]), special_flags=pygame.BLEND_RGBA_ADD)
	#RENDER
#PARTICLE

#SHOCKWAVE
class ShockWave:
	'''A shockwave to get smaller or bigger
	The radius needs to be decreased'''
	#__INIT__
	def __init__(self, Location, Colour, Radius, Width):
		'''Initialising a shockwave'''
		self.Location = list(Location)
		self.Colour = Colour
		self.Radius = Radius
		self.Width = Width
		self.Alive = True
	#__INIT__

	#UPDATE
	def Update(self, Surface, RadiusChange, WidthChange, Scroll=[0, 0], DeltaTime=1):
		'''The move and render function of the shockwave if the width is smaller or 1, it will no longer be alive'''
		self.Radius += RadiusChange * DeltaTime
		self.Width -= WidthChange * DeltaTime
		if self.Width <= 1:
			self.Alive = False
		else:
			pygame.draw.circle(Surface, self.Colour, (self.Location[0] - Scroll[0], self.Location[1] - Scroll[1]), self.Radius, int(self.Width))
	#UPDATE
#SHOCKWAVE

#SPARK
class Spark:
	'''A spark to draw and move
	A spark is a polygon so checking collision with it is not possible'''
	#__INIT__
	def __init__(self, Location, Angle, Speed, Size, Colour):
		'''Initialising a spark
		It will change the angle to radians'''
		self.Location = list(Location)
		self.Angle = math.radians(Angle) #ANGLE IS IN RADIANS
		self.Speed = Speed
		self.Size = Size
		self.Colour = Colour
		self.Alive = True
	#__INIT__

	#NORMALMOVEMENT
	def NormalMovement(self, SpeedChange, DeltaTime=1, AngleChange=0):
		'''A function to move the spark normal
		It will decrease the speed and if it is lower or equal to 0, it is no longer alive
		AngleChange will change the angly by that amount every time this runs'''
		self.Location = list(self.Location)
		self.Location[0] += math.cos(self.Angle) * self.Speed * DeltaTime
		self.Location[1] += math.sin(self.Angle) * self.Speed * DeltaTime
		self.Speed -= SpeedChange * DeltaTime
		self.Angle += AngleChange * DeltaTime
		if self.Speed <= 0:
			self.Alive = False
	#NORMALMOVEMENT

	#GRAVITYMOVEMENT
	def GravityMovement(self, SpeedChange, YMomentum, MaximumYMomentum, DeltaTime=1):
		'''A function to move the particle, but it also includes gravity
		It will change the angle a little bit down every frame
		It will decrease the speed and if it is lower or equal to 0, it is no longer alive'''
		self.Location = list(self.Location)
		Momentum = [math.cos(self.Angle) * self.Speed * DeltaTime, math.sin(self.Angle) * self.Speed * DeltaTime]
		self.Location[0] += Momentum[0]
		self.Location[1] += Momentum[1]
		Momentum[1] = min(Momentum[1] + YMomentum * DeltaTime, MaximumYMomentum)
		self.Angle = math.atan2(Momentum[1], Momentum[0])
		self.Speed -= SpeedChange * DeltaTime
		if self.Speed <= 0:
			self.Alive = False
	#GRAVITYMOVEMENT

	#RENDER
	def Render(self, Surface, Scroll=[0, 0], LightingColour=None):
		'''A function to render the spark
		It will calculate every point for the polygon (there are 4 points) it looks like a rhombus, but the back one is longer
		If LightingColour is turned on, it will blit a bigger polygon on top of it with BLEND_RGBA_ADD'''
		if self.Alive:
			Points = [[self.Location[0] + math.cos(self.Angle) * self.Speed * self.Size, self.Location[1] + math.sin(self.Angle) * self.Speed * self.Size], #FRONT POINT
			[self.Location[0] + math.cos(self.Angle + math.pi / 2) * self.Speed * self.Size * 0.4, self.Location[1] + math.sin(self.Angle + math.pi / 2) * self.Speed * self.Size * 0.4], #RIGHT POINT
			[self.Location[0] - math.cos(self.Angle) * self.Speed * self.Size * 2.5, self.Location[1] - math.sin(self.Angle) * self.Speed * self.Size * 2.5], #BOTTOM POINT
			[self.Location[0] + math.cos(self.Angle - math.pi / 2) * self.Speed * self.Size * 0.4, self.Location[1] + math.sin(self.Angle - math.pi / 2) * self.Speed * self.Size * 0.4]] #LEFT POINT

			pygame.draw.polygon(Surface, self.Colour, [[Point[0] - Scroll[0], Point[1] - Scroll[1]] for Point in Points])
			if LightingColour:
				LightingPosition = [abs(min([Point[0] for Point in Points]) - self.Location[0] + (min([Point[0] for Point in Points]) - max([Point[0] for Point in Points])) * 0.5),
				abs(min([Point[1] for Point in Points]) - self.Location[1] + (min([Point[1] for Point in Points]) - max([Point[1] for Point in Points])) * 0.5)]
				Surface.blit(self.Lighting(Points, LightingPosition, LightingColour), (self.Location[0] - LightingPosition[0] - Scroll[0], self.Location[1] - LightingPosition[1] - Scroll[1]), special_flags=pygame.BLEND_RGBA_ADD)
	#RENDER

	#LIGHTING
	def Lighting(self, Points, LightingPosition, Colour):
		'''A function used by Render to draw a bigger polygon on top of the normal one'''
		LightingSurfaceWidth = (max([Point[0] for Point in Points]) - min([Point[0] for Point in Points])) * 2
		LightingSurfaceHeight = (max([Point[1] for Point in Points]) - min([Point[1] for Point in Points])) * 2
		LightingSurface = pygame.Surface((LightingSurfaceWidth, LightingSurfaceHeight)) #DIFFERENCE BETWEEN LOWEST AND HIGHTEST POINTS
		LightingSurface.set_colorkey((0, 0, 0))

		#EVERYTHING * 2 FOR MAKING THE POLYGON LARGER
		LargerPoints = [[LightingPosition[0] + math.cos(self.Angle) * self.Speed * self.Size * 2, LightingPosition[1] + math.sin(self.Angle) * self.Speed * self.Size * 2], #FRONT POINT
		[LightingPosition[0] + math.cos(self.Angle + math.pi / 2) * self.Speed * self.Size * 0.8, LightingPosition[1] + math.sin(self.Angle + math.pi / 2) * self.Speed * self.Size * 0.8], #RIGHT POINT
		[LightingPosition[0] - math.cos(self.Angle) * self.Speed * self.Size * 5, LightingPosition[1] - math.sin(self.Angle) * self.Speed * self.Size * 5], #BOTTOM POINT
		[LightingPosition[0] + math.cos(self.Angle - math.pi / 2) * self.Speed * self.Size * 0.8, LightingPosition[1] + math.sin(self.Angle - math.pi / 2) * self.Speed * self.Size * 0.8]] #LEFT POINT
		pygame.draw.polygon(LightingSurface, Colour, LargerPoints)
		return LightingSurface
		#LIGHTING
#SPARK