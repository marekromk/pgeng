'''A class for animations'''
#IMPORTS
import pygame
from pathlib import Path
from .Core import load_image, most_used
#IMPORTS

#ANIMATIONS
class Animations:
	'''A class for animations
	Not all the animations should be done in one Animations class, it is good to create one for Entities and such
	It needs a action to begin with

	Attributes:

	action

	animation_frames

	animations_data

	frame'''
	#__INIT__
	def __init__(self, action):
		'''Initialising an Animations class'''
		self.animations_data = {}
		self.animation_frames = {}
		self.action = action
		self.frame = 0
	#__INIT__

	#ADD_ANIMATION
	def load_animation(self, path, frame_durations, repeat=True, colourkey=None, file_type=None, animation_name=None):
		'''A function for loading still images for a animation

		It loads all images in a directory, the last character before the file type needs to be a number
		The name of the directory it is in needs to be in the file name (directories above that don't matter),
		The file type of the frames should be the most used file type in the directory
		Example:
			'run/run1.png'
			'run/run2.png'

		Or you can use file_type variable
		Example:
			file_type='.png'

		If you don't want the name of the directory to be the name of the animation, you could use animation_name
		If you do that, the file name should still be the same as the directory

		frame_durations is a list or tuple with how long each frame should last, it has to be in order
		repeat is if the animation should loop, if it is False, the image would stay on the last one
		The images will be added to animation_frames'''
		path = Path(path)
		if not path.is_dir():
			raise FileNotFoundError(f'Directory \'{path}\' does not exist')
		animation_name = path.name if animation_name is None else animation_name
		self.animations_data[animation_name] = ([], repeat)
		if not file_type:
			file_type = most_used([file.suffix for file in path.glob('*.*')])[0]
		for i, frame_duration in enumerate(frame_durations):
			if not path.joinpath(f'{path.name}{i + 1}{file_type}').is_file():
				raise pygame.error(f'Too many non image files in \'{path}\' or the image file is not named \'{path.name}{i + 1}{file_type}\'')
			animation_frame_id = f'{animation_name}{i + 1}'
			self.animation_frames[animation_frame_id] = load_image(path.joinpath(f'{path.name}{i + 1}{file_type}'), colourkey)
			self.animations_data[animation_name][0].append((animation_frame_id, frame_duration))
	#ADD_ANIMATION

	#ADD_IMAGE
	def add_image(self, image, name, duration, repeat=True):
		'''Manually add an image to an animation
		If this name does not yes exist, it will be created
		The image will be added to animation_frames with a number, so it has to be added in the correct order'''
		if name not in self.animations_data:
			self.animations_data[name] = ([], repeat)
		animation_frame_id = f'{name}{len(self.animations_data[name][0]) + 1}'
		self.animation_frames[animation_frame_id] = image
		self.animations_data[name][0].append((animation_frame_id, duration))
	#ADD_IMAGE

	#CURRENT_IMAGE
	def current_image(self, delta_time=1):
		'''Get the current image in the animation
		delta_time is how much the frame should update, usually it would be 1

		Returns: pygame.Surface'''
		if self.action not in self.animations_data:
			raise KeyError(f'Animation \'{action}\' is not defined')
		animation_data = self.animations_data[self.action]
		self.frame += delta_time
		reset_frame = round(self.frame) > sum([frame_duration[1] for frame_duration in animation_data[0]][:len(animation_data[0])])
		if reset_frame and animation_data[1]:
			self.frame = 0
		elif reset_frame and not animation_data[1]:
			self.frame = sum([frame_duration[1] for frame_duration in animation_data[0]][:len(animation_data[0])])
		for i, frame_data in enumerate(animation_data[0]):
			if sum([frame_duration[1] for frame_duration in animation_data[0]][:i + 1]) >= round(self.frame):
				return self.animation_frames[frame_data[0]]
	#CURRENT_IMAGE

	#SET_ACTION
	def set_action(self, action):
		'''Set the current action, the frame will also be reset to 0'''
		if action not in self.animations_data:
			raise KeyError(f'Animation \'{action}\' is not defined')
		if self.action != action:
			self.action = action
			self.frame = 0
	#SET_ACTION
#ANIMATIONS