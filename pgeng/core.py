'Core functions for pgeng'
#import functions with underscore so it doesn't get imported by pgeng itself
import pygame, gzip
from math import ceil as _ceil
from sys import exit as _sysexit
from pathlib import Path as _Path
from errno import ENOENT as _ENOENT
from os import strerror as _strerror
from collections import Counter as _Counter

def int_location(location):
	'''Return a list with the coordinates truncated

	Returns: list'''
	if len(location) != 2:
		raise ValueError('location must be 2 coordinates')
	return [int(location[i]) for i in range(2)]

def round_location(location):
	'''Return a list with the coordinates rounded

	Returns: list'''
	if len(location) != 2:
		raise ValueError('location must be 2 coordinates')
	return [round(location[i]) for i in range(2)]

def ceil_location(location):
	'''Return a list with the coordinates ceiled

	Returns: list'''
	if len(location) != 2:
		raise ValueError('location must be 2 coordinates')
	return [_ceil(location[i]) for i in range(2)]

def clip_surface(surface, location, size):
	'''Creates a new Surface from a part of another Surface

	Returns: pygame.Surface'''
	new_surface = surface.copy()
	new_surface.set_clip(pygame.Rect(location, size))
	clipped_surface = surface.subsurface(new_surface.get_clip())
	return clipped_surface.copy()

def load_image(path, colourkey=None, alpha=255, convert_alpha=False):
	'''Load an image for pygame that will be converted
	You can set a colourkey and alpha as well

	Returns: pygame.Surface'''
	path = _Path(path).resolve()
	if not path.is_file():
		raise FileNotFoundError(_ENOENT, _strerror(_ENOENT), f'{path}')
	image = pygame.image.load(path).convert() if not convert_alpha else pygame.image.load(path).convert_alpha()
	image.set_colorkey(colourkey)
	if alpha != 255:
		image.set_alpha(alpha)
	return image

def delta_time(clock, fps):
	'''Get the time since the last frame, it needs a pygame.time.Clock object and the fps
	It will return a number that is around 1 if the game is running at the intended speed
	For example, if the game is running at 30 fps, but it should run at 60 fps, it would return 2.0

	Returns: float'''
	delta_time = clock.get_time() * fps / 1000 #divide by 1000, becuase it is in millisecond, but it needs to be seconds
	return delta_time if delta_time else 1.0

def quit_game():
	'''Exiting a pygame program in the correct way
	Runs:
		pygame.quit() and sys.exit()'''
	pygame.quit()
	_sysexit()

def read_file(path, mode='r'):
	'''Reads a file and returns the that's data in it
	mode is the mode in which the file should be openend

	Returns: str'''
	with open(_Path(path).resolve()) as file:
		return file.read()

def write_to_file(path, data, mode='w'):
	'''Writes data to a file
	data should be a string, except if it is in byte mode
	mode is the mode in which the file should be opened'''
	if not 'b' in mode and type(data) is not str:
		raise TypeError('data should be a string')
	if 'b' in mode and type(data) is not bytes:
		raise TypeError(f'data should be bytes if mode is {mode}')
	with open(_Path(path).resolve(), mode) as file:
		file.write(data)

def read_compressed_file(path, mode='rb', encoding='utf-8'):
	'''Reads a file with gzip compression
	mode is the mode in which the file should be openend
	encoding is the encoding the data that's read is decoded with, not the encoding of the file

	Returns: str'''
	with gzip.open(_Path(path).resolve(), mode) as file:
		return file.read().decode(encoding)

def write_to_compressed_file(path, data, mode='wb', compresslevel=9, encoding='utf-8', gzip_extension=False):
	'''Writes data to a file with gzip compression
	data should be a string
	mode is the mode in which the file should be openend
	compresslevel is how much it should be compressed the minimum is 0, 9 is the maximum
	encoding is the encoding that the data will be encoded with
	gzip_extension is if it should add '.gz', it will be added behind the extension it already had
	Example:
		'file.txt' -> 'file.txt.gz\''''
	if type(data) is not str:
		raise TypeError('data should be a string')
	if type(compresslevel) is not int:
		raise TypeError('compresslevel has to be an integer')
	if not -1 <= compresslevel <= 9:
		raise ValueError('compresslevel must be between -1 and 9')
	path = _Path(path).resolve()
	if gzip_extension:
		path = path.with_suffix(f'{path.suffix}.gz')
	with gzip.open(path, mode, compresslevel) as file:
		file.write(data.encode(encoding))

def clamp(input, minimum, maximum):
	'''Clamps a number between a minimum and maximum value

	Returns: int or float'''
	if minimum >= maximum:
		raise ValueError('minimum is larger or the same as maximum')
	if input < minimum:
		return minimum
	if input > maximum:
		return maximum
	return input

def nearest(input, nearest):
	'''Returns a number changed to the nearest given

	Returns: float'''
	return float(round(input / nearest) * nearest)

def most_used(iterable, amount=False):
	'''Return the most used value in an iterable
	It will return the amount used of the value in the list if amount is True

	Returns: list'''
	if not len(iterable):
		raise ValueError('return_index can\'t be an empty iterable')
	list_counter = _Counter(iterable)
	total_times = list(list_counter.values()).count(max(list(list_counter.values())))
	return [value[0] for value in list_counter.most_common(total_times)] if not amount else list_counter.most_common(total_times)