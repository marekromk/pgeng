'A Flame class'
#IMPORTS
import pygame
from random import uniform, randint
from .particle import Particle
#IMPORTS

#VARIABLES
__all__ = ['set_flame_attributes', 'Flame']
#VARIABLES

#SET_FLAME_ATTRIBUTES
def set_flame_attributes(alpha_layers=2, alpha_glow_difference=2):
    '''Set the attributes for the FlameParticle
    alpha_layers is basically how many layers a particle has
    alpha_glow_difference is how much the radius of each layer should change for every layer'''
    if type(alpha_layers) is not int or type(alpha_glow_difference) is not int:
        raise TypeError('Attributes have to be integers')
    if alpha_layers < 2:
        raise ValueError('alpha_layers can not be less than 2')
    if alpha_glow_difference < 1:
        raise ValueError('alpha_glow_difference can not be less than 1')
    FlameParticle.alpha_layers = alpha_layers
    FlameParticle.alpha_glow_difference_constant = alpha_glow_difference
#SET_FLAME_ATTRIBUTES

#FLAMEPARTICLE
class FlameParticle(Particle):
    '''A single particle for the flame
    Look at Particle for more information
    It gets renders with alpha layers

    Attributes:

    alpha_glow

    alpha_layers

    burn_rate

    surface'''
    #VARIABLES
    alpha_layers = 2
    alpha_glow_difference_constant = 2
    #VARIABLES

    #__INIT__
    def __init__(self, location, size, burn_rate, colour):
        'Initialising a FlameParticle'
        super().__init__(location, [0, 0], size, colour)
        self.burn_rate = burn_rate
        self.alpha_layers = FlameParticle.alpha_layers
        self.alpha_glow = FlameParticle.alpha_glow_difference_constant
        surface_size = self.size * 2 * self.alpha_layers ** 2 * self.alpha_glow
        self.surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
    #__INIT__

    #MOVE
    def move(self, y_momentum, delta_time=1):
        '''Move the FlameParticle
        y_momentum is how much it should move vertically'''
        self.momentum = [uniform(round(-self.size), round(self.size)) / delta_time, y_momentum]
        super().move(self.burn_rate, delta_time=delta_time)
    #MOVE

    #RENDER
    def render(self, surface, scroll=(0, 0)):
        '''Render the FlameParticle with alpha layers on top of it
        scroll is position of the camera, it will render it at the location of the FlameParticle minus scroll'''
        if self.alive:
            surface_size = round(self.size) * 2 * self.alpha_layers ** 2 * self.alpha_glow
            self.surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
            for i in range(self.alpha_layers, -1, -1):
                alpha = max(0, 255 - i * (255 // self.alpha_layers - 5))
                radius = round(self.size) * i ** 2 * self.alpha_glow
                pygame.draw.circle(self.surface, (self.colour[0], self.colour[1], self.colour[2], alpha), (self.surface.get_width() / 2, self.surface.get_height() / 2), radius)
            surface.blit(self.surface, [self.location[i] - self.surface.get_size()[i] / 2 - scroll[i] for i in range(2)])
    #RENDER
#FLAMEPARTICLE

#FLAME
class Flame:
    '''A flame effect
    It is basically a lot FlameParticles
    They all get created around one location
    They are not all the same size, it is random, with the maximum size being max_particle_size and the minimum being max_particle_size / 5
    The intensity means how many particles the flame has at once

    Attributes:

    burn_rate

    colour

    intensity

    location

    max_particle_size

    particles'''
    #__INIT__
    def __init__(self, location, max_particle_size, burn_rate, colour, intensity=2):
        'Initialising a flame'
        if max_particle_size <= 1:
            raise ValueError(f'max_particle_size can not be less than 1')
        self.location = list(location)
        self.max_particle_size = max_particle_size
        self.burn_rate = burn_rate
        self.intensity = intensity
        self.colour = colour
        self.particles = []
        for i in range(round(intensity * 25)):
            self.particles.append(FlameParticle([self.location[0] + randint(round(-self.max_particle_size * 2), round(self.max_particle_size * 2)), self.location[1] + randint(round(-self.max_particle_size * 2), round(self.max_particle_size * 2))], max(1, uniform(self.max_particle_size / 5, self.max_particle_size)), self.burn_rate, self.colour))
    #__INIT__

    #SET_INTENSITY
    def set_intensity(self, intensity=2):
        '''Set the intensity of the flame
        All the particles get removed and the correct amount of new ones get added'''
        self.intensity = intensity
        self.particles = []
        for i in range(round(intensity * 25)):
            self.particles.append(FlameParticle([self.location[0] + randint(round(-self.max_particle_size * 2), round(self.max_particle_size * 2)), self.location[1] + randint(round(-self.max_particle_size * 2), round(self.max_particle_size * 2))], max(1, uniform(self.max_particle_size / 5, self.max_particle_size)), self.burn_rate, self.colour))
    #SET_INTENSITY

    #RENDER
    def render(self, surface, y_momentum, scroll=(0, 0), delta_time=1):
        '''Update and render the flame and every FlameParticle that it has
        y_momentum is how much each FlameParticle should move vertically
        scroll is position of the camera, it will render it at the location of the Flame minus scroll'''
        for i, particle in sorted(enumerate(self.particles), reverse=True):
            particle.move(y_momentum, delta_time)
            particle.render(surface, scroll)
            if not particle.alive:
                self.particles.pop(i)
                self.particles.append(FlameParticle([self.location[0] + randint(round(-self.max_particle_size * 2), round(self.max_particle_size * 2)), self.location[1] + randint(round(-self.max_particle_size), round(self.max_particle_size))], max(1, uniform(self.max_particle_size / 5, self.max_particle_size)), self.burn_rate, self.colour))
    #RENDER
#FLAME