'A class for animations'
import pygame
from pathlib import Path
from .core import load_image, most_used

class Animations:
	'''A class for animations
	Not all the animations should be done in one Animations class, it is good to create one for Entities and such
	It can set an action when being initialised, even though no animation is created yet

	Attributes:

	action

	animation_frames

	animations_data

	frame'''
	def __init__(self, action=None):
		'Initialising an Animations class'
		self.animations_data = {}
		self.animation_frames = {}
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
		The images will be added to animation_frames'''
		path = Path(path).resolve()
		if not path.is_dir():
			raise FileNotFoundError(f'Directory \'{path}\' does not exist')
		animation_name = path.name if animation_name is None else animation_name
		self.animations_data[animation_name] = [[], repeat, 0]
		if not file_type:
			file_type = most_used([file.suffix for file in path.iterdir() if file.is_file()])[0]
		for i, frame_duration in enumerate(frame_durations):
			if not path.joinpath(f'{path.name}{i + 1}{file_type}').is_file():
				raise pygame.error(f'Too many non image files in \'{path}\' or the image file is not named \'{path.name}{i + 1}{file_type}\'')
			animation_frame_id = f'{animation_name}{i + 1}'
			self.animation_frames[animation_frame_id] = load_image(path.joinpath(f'{path.name}{i + 1}{file_type}'), colourkey, alpha, convert_alpha)
			self.animations_data[animation_name][0].append((animation_frame_id, frame_duration))
			self.animations_data[animation_name][2] += frame_duration

	def add_image(self, image, animation_name, duration, repeat=True):
		'''Manually add an image to an animation
		If the animation_name does not yes exist, it will be created
		The image will be added to animation_frames with a number, so it has to be added in the correct order'''
		if animation_name not in self.animations_data:
			self.animations_data[animation_name] = [[], repeat, 0]
		animation_frame_id = f'{animation_name}{len(self.animations_data[animation_name][0]) + 1}'
		self.animation_frames[animation_frame_id] = image.copy()
		self.animations_data[animation_name][0].append((animation_frame_id, duration))
		self.animations_data[animation_name][2] += duration

	def current_image(self, delta_time=1):
		'''Get the current image in the animation
		delta_time is how much the frame should update, usually it would be 1

		Returns: pygame.Surface'''
		if self.action not in self.animations_data:
			raise KeyError(f'Animation \'{action}\' is not defined')
		animation_data = self.animations_data[self.action]
		self.frame += delta_time
		reset_frame = round(self.frame) > animation_data[2]
		if reset_frame and animation_data[1]:
			self.frame = 0
		elif reset_frame and not animation_data[1]:
			self.frame = animation_data[2]
		for i, frame_data in enumerate(animation_data[0]):
			if round(self.frame) <= sum([frame_duration[1] for frame_duration in animation_data[0]][:i + 1]):
				return self.animation_frames[frame_data[0]]

	def set_action(self, action):
		'Set the current action, the frame will also be reset to 0'
		if action not in self.animations_data:
			raise KeyError(f'Animation \'{action}\' is not defined')
		if self.action != action:
			self.action = action
			self.frame = 0