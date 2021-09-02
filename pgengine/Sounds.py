'''A simple class for loading and playing sounds and music'''
#IMPORTS
import pygame
#IMPORTS

#SOUNDS
class Sounds:
	'''A class for playing sounds or music
	It uses a boolean variable to know if it should play sound
	It will not if PlaySoundVariable is False

	Channels is for setting the amount of channels in pygame.mixer if it is initialised'''
	#__INIT__
	def __init__(self, Channels=64):
		'''Initialising the class, it should only be done once'''
		pygame.mixer.set_num_channels(Channels)
		self.Sounds = {}
		self.PlaySoundVariable = True
	#__INIT__

	#ADDSOUND
	def AddSound(self, File, Name, Volume=1):
		'''Adding sounds to the Sounds dictionary, set the volume of the sound with Volume
		Set the file type of the sound you are loading with FileType (.wav is recommended)'''
		self.Sounds[Name] = pygame.mixer.Sound(File)
		self.Sounds[Name].set_volume(Volume)
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

	#PLAYSOUND
	def PlaySound(self, Sound):
		'''Plays the specified sound in the Sounds dictionary if PlaySoundVariable is True'''
		if self.PlaySoundVariable:
			self.Sounds[Sound].play()
	#PLAYSOUND

	#PLAYMUSIC
	def PlayMusic(self, File, Volume=1, Amount=-1):
		'''This will play the music file if PlaySoundVariable is True, you can set the volume and amount of times played
		Amount=-1 is indefinitely
		Set the file type of the sound you are loading with FileType (.wav is recommended)'''
		if self.PlaySoundVariable:
			pygame.mixer.music.load(File)
			pygame.mixer.music.set_volume(Volume)
			pygame.mixer.music.play(Amount)
	#PLAYMUSIC
#SOUNDS