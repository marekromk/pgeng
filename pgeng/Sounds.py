'''A simple class for loading and playing sounds and music'''
#IMPORTS
import pygame
#IMPORTS

#SOUNDS
class Sounds:
	'''A class for playing sounds or music
	It uses a boolean variable to know if it should play sound
	It will not if PlaySoundVariable is False
	The volume will be set to 1 automatically

	Channels is for setting the amount of channels in pygame.mixer if it is initialised

	Attributes:

	PlaySoundVariable

	Sounds

	Volume'''
	#__INIT__
	def __init__(self, Channels=64):
		'''Initialising the class, it should only be done once'''
		if pygame.mixer.get_init():
			pygame.mixer.set_num_channels(Channels)
		self.Sounds = {}
		self.PlaySoundVariable = True
		self.Volume = 1
	#__INIT__

	#ADDSOUND
	def AddSound(self, File, Name, SetVolume=True):
		'''Adding sounds to the Sounds dictionary
		The volume will be set by the Volume variable if SetVolume is True'''
		self.Sounds[Name] = pygame.mixer.Sound(File)
		if SetVolume:
			self.Sounds[Name].set_volume(self.Volume)
	#ADDSOUND

	#SETPLAYSOUND
	def SetPlaySound(self, PlaySoundBoolean):
		'''Setting the PlaySoundVariable to True or False
		It will also pause music if it is False and unpause if it is True'''
		self.PlaySoundVariable = PlaySoundBoolean
		if self.PlaySoundVariable and not pygame.mixer.get_busy():
			pygame.mixer.music.unpause()
		else:
			pygame.mixer.music.pause()
	#SETPLAYSOUND

	#SETVOLUME
	def SetVolume(self, Volume, Music=True, SpecificSound=None):
		'''Set the volume of the sounds
		It also sets the Volume variable for new sounds in the future

		It will not change the volume of the music if Music is False
		It will set the volume of a specific sound in the dictionary if a SpecificSound is given
		Than it will not change the Volume variable'''
		if 0 > Volume > 1:
			raise ValueError('Volume must be between 0 and 1')
		if Music:
			pygame.mixer.music.set_volume(Volume)
		if not SpecificSound:
			self.Volume = Volume
			for Sound in self.Sounds:
				self.Sounds[Sound].set_volume(Volume)
		else:
			self.Sounds[SpecificSound].set_volume(Volume)
	#SETVOLUME

	#PLAYSOUND
	def PlaySound(self, Sound):
		'''Plays the specified sound in the Sounds dictionary if PlaySoundVariable is True'''
		if self.PlaySoundVariable:
			self.Sounds[Sound].play()
	#PLAYSOUND

	#PLAYMUSIC
	def PlayMusic(self, File, Amount=-1, Volume=-1):
		'''This will play the music file if PlaySoundVariable is True
		The volume will be the Volume variable if Volume is -1
		Amount will be and amount of times played
		Amount=-1 is indefinitely'''
		if self.PlaySoundVariable:
			pygame.mixer.music.load(File)
			pygame.mixer.music.set_volume(self.Volume if Volume == -1 else Volume)
			pygame.mixer.music.play(Amount)
	#PLAYMUSIC
#SOUNDS