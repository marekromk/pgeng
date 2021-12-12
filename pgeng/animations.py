'A class for animations'
import pygame
from pathlib import Path
from errno import ENOENT as _ENOENT
from os import strerror as _strerror
from .core import load_image, most_used

class Animations:
	'''A class for animations
	Not all the animations should be done in one Animations class, it is good to create one for Entities and such
	It can set an action when being initialised, even though no animation is created yet

	Attributes:

	action

	frames

	data

	frame'''
	def __init__(self, action=None):
		'Initialising an Animations class'
		self.data = {}
		self.frames = {}
		self.action = action
		self.frame = 0

	def __repr__(self):
		'''Returns a string representation of the object

		Returns: str'''
		return 'pgeng.Animations'

	def load_animation(self, path, frame_durations, repeat=True, colourkey=None, file_type=None, animation_name=None, alpha=255, convert_alpha=False):
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
		The images will be added to frames'''
		path = Path(path).resolve()
		if not path.is_dir():
			raise FileNotFoundError(_ENOENT, _strerror(_ENOENT), f'{path}')
		animation_name = path.name if animation_name is None else animation_name
		self.data[animation_name] = {'durations': [], 'repeat': repeat, 'full': 0}
		if not file_type:
			file_type = most_used([file.suffix for file in path.iterdir() if file.is_file()])[0]
		for i, frame_duration in enumerate(frame_durations):
			if not path.joinpath(f'{path.name}{i + 1}{file_type}').is_file():
				raise pygame.error(f'Too many non image files in \'{path}\' or the image file is not named \'{path.name}{i + 1}{file_type}\'')
			frame_id = f'{animation_name}{i + 1}'
			self.frames[frame_id] = load_image(path.joinpath(f'{path.name}{i + 1}{file_type}'), colourkey, alpha, convert_alpha)
			self.data[animation_name]['durations'].append({'id': frame_id, 'duration': frame_duration})
			self.data[animation_name]['full'] += frame_duration

	def add_image(self, image, animation_name, duration, repeat=True):
		'''Manually add an image to an animation
		If the animation_name does not yes exist, it will be created
		The image will be added to frames with a number, so it has to be added in the correct order'''
		if animation_name not in self.data:
			self.data[animation_name] = {'durations': [], 'repeat': repeat, 'full': 0}
		frame_id = f'{animation_name}{len(self.data[animation_name]["durations"]) + 1}'
		self.frames[frame_id] = image.copy()
		self.data[animation_name]['durations'].append({'id': frame_id, 'duration': duration})
		self.data[animation_name]['full'] += duration

	def current_image(self, delta_time=1):
		'''Get the current image in the animation
		delta_time is how much the frame should update, usually it would be 1

		Returns: pygame.Surface'''
		if self.action not in self.data:
			raise KeyError(f'Action \'{self.action}\' is not defined')
		animation_data = self.data[self.action]
		self.frame += delta_time
		reset_frame = round(self.frame) > animation_data['full']
		if reset_frame:
			self.frame = animation_data['full'] if not animation_data['repeat'] else 0
		for i, frame_data in enumerate(animation_data['durations']):
			if round(self.frame) <= sum([frame_duration['duration'] for frame_duration in animation_data['durations']][:i + 1]): #SUM EVERY FRAME DURATION OF ALL THE FRAMES BEFORE I TO CHECK WHAT THE CURRENT FRAME IT IS
				return self.frames[frame_data['id']]

	def set_action(self, action):
		'Set the current action, the frame will also be reset to 0'
		if action not in self.data:
			raise KeyError(f'Action \'{action}\' is not defined')
		if self.action != action:
			self.action = action
			self.frame = 0