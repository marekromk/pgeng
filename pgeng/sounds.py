'A simple class for loading and playing sounds and music'
import pygame
from pathlib import Path
from errno import ENOENT as _ENOENT
from os import strerror as _strerror

class Sounds:
	'''A class for playing sounds or music
	It uses a boolean variable to know if it should play sound
	It will not if PlaySoundVariable is False
	The volume will be set to 1 automatically

	Channels is for setting the amount of channels in pygame.mixer if it is initialised

	Attributes:

	play_sound_variable

	sounds

	volume'''
	def __init__(self, channels=64):
		'Initialising the class, it should only be done once'
		if channels < 0:
			raise ValueError('channels can not be less than 0')
		if pygame.mixer.get_init():
			pygame.mixer.set_num_channels(channels)
		self.sounds = {}
		self.play_sound_variable = True
		self.volume = 1

	def __repr__(self):
		'''Returns a string representation of the object

		Returns: str'''
		return f'pgeng.Sounds{pygame.mixer.get_num_channels(), self.volume}'

	def add_sound(self, path, name, volume=-1):
		'''Adding sounds to the Sounds dictionary
		The volume will be set by the volume variable if volume is -1'''
		self.sounds[name] = pygame.mixer.Sound(f'{Path(path).resolve()}')
		self.sounds[name].set_volume(self.volume if volume == -1 else volume)

	def set_play_sound(self, play_sound_boolean, affect_music=True):
		'''Setting the play_sound_variable to True or False
		It will also pause music if it is False and unpause if it is True'''
		self.play_sound_variable = play_sound_boolean
		if affect_music and self.play_sound_variable and not pygame.mixer.get_busy():
			pygame.mixer.music.unpause()
		elif affect_music:
			pygame.mixer.music.pause()

	def set_volume(self, volume, music=True, specific_sound=None):
		'''Set the volume of the sounds
		It also sets the volume variable for new sounds in the future

		It will not change the volume of the music if music is False
		It will set the volume of a specific sound in the dictionary if a specific_sound is given
		Than it will not change the volume variable'''
		if not 0 <= volume <= 1:
			raise ValueError('Volume must be between 0 and 1')
		if music:
			pygame.mixer.music.set_volume(volume)
		if specific_sound is None:
			self.volume = volume
			for sound in self.sounds:
				self.sounds[sound].set_volume(volume)
		else:
			self.sounds[specific_sound].set_volume(volume)

	def play_sound(self, sound):
		'Plays the specified sound in the sounds dictionary if play_sound_variable is True'
		if self.play_sound_variable:
			self.sounds[sound].play()

	def play_music(self, path, amount=-1, volume=-1):
		'''This will play the music file if play_sound_variable is True
		The volume will be the volume variable if volume is -1
		amount is the amount of times played, it will be indefinitely if amount is -1'''
		path = Path(path).resolve()
		if not path.is_file():
			raise FileNotFoundError(_ENOENT, _strerror(_ENOENT), f'{path}')
		if self.play_sound_variable:
			pygame.mixer.music.load(path)
			pygame.mixer.music.set_volume(self.volume if volume == -1 else volume)
			pygame.mixer.music.play(amount)