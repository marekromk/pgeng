'Core functions for pgeng'
import pygame, gzip
from math import ceil
from pathlib import Path
from collections import Counter
from sys import exit as _sysexit
from errno import ENOENT as _ENOENT
from os import strerror as _strerror

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
	return [ceil(location[i]) for i in range(2)]

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
	path = Path(path).resolve()
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
	delta_time = clock.get_time() * fps / 1000
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
	with open(Path(path).resolve()) as file:
		return file.read()

def write_to_file(path, data, mode='w'):
	'''Writes data to a file
	data should be a string
	mode is the mode in which the file should be opened'''
	if type(data) is not str:
		raise TypeError('data should be a string')
	with open(Path(path).resolve(), mode) as file:
		file.write(data)

def read_compressed_file(path, mode='rb', encoding='utf-8'):
	'''Reads a file with gzip compression
	mode is the mode in which the file should be openend
	encoding is the encoding the data that's read is decoded with, not the encoding of the file

	Returns: str'''
	with gzip.open(Path(path).resolve(), mode) as file:
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
	path = Path(path).resolve()
	if gzip_extension:
		path = path.with_suffix(f'{path.suffix}.gz')
	with gzip.open(path, mode, compresslevel) as file:
		file.write(data.encode(encoding))

def nearest(input, nearest, int_mode=True):
	'''Returns a number changed to the nearest given
	If int_mode is True, it will truncate the returned number and return an integer

	Returns: int (or float)'''
	return int(round(input / nearest) * nearest) if int_mode else round(input / nearest) * nearest

def most_used(iterable, amount=False):
	'''Return the most used value in an iterable
	It will return the amount used of the value in the list if amount is True

	Returns: list'''
	list_counter = Counter(iterable)
	total_times = list(list_counter.values()).count(max(list(list_counter.values())))
	return [value[0] for value in list_counter.most_common(total_times)] if not amount else list_counter.most_common(total_times)

def string_number(string, return_index=None, int_mode=False):
	'''Return numbers from a given string
	If return_index is None it will return everything, except if a list or tuple with the indexes gets given
	Example:
		return_index=[0, 2] This will make it return the first and third number

	If int_mode is True, it will truncate every returned number and return an integer

	Returns: list (or NoneType if no number is found)'''
	if any(character.isdigit() for character in string):
		numbers, digits = [], []
		for i in range(len(string)):
			if string[i].isdigit() and (any(string[min(i + 1, len(string) - 1)] == character for character in ['.', ',']) or string[min(i + 1, len(string) - 1)].isdigit()): #CHECK IF THE NEXT CHARACTER IS . OR , OR A NUMBER
				if any(string[min(i + 1, len(string) - 1)] == character for character in ['.', ',']) and string[min(i + 2, len(string) - 1)].isdigit() and not any('.' in digit for digit in digits): #IF NEXT CHARACTER IS . AND AFTER THAT IS A NUMBER AND A . IS NOT ALREADY IN THE DIGITS
					digits.append(f'{string[i]}.')
				elif any(string[min(i + 1, len(string) - 1)] == character for character in ['.', ',']): #CHECK IF ELSE NUMBERS ENDS WITH A . OR ,
					digits.append(string[i])
					numbers.append(''.join(digits))
					digits = []
				else: #NORMAL SITUATION
					digits.append(string[i])
			elif string[i].isdigit(): #IF ELSE IT'S THE LAST DIGIT IN THE NUMBER
				digits.append(string[i])
				numbers.append(''.join(digits))
				digits = []
			if string[i].isdigit() and i == len(string) - 1: #IF THE NUMBER IS THE LAST CHARACTER OF THE STRING
				numbers.append(''.join(digits))
		if type(return_index) is not list and type(return_index) is not tuple:
			return_index = [i for i in range(len(numbers))]
		if return_index and min(return_index) < -len(numbers) or max(return_index) > len(numbers) - 1:
			raise IndexError('Index in return_index is not possible')
		return [float(numbers[index]) for index in return_index] if not int_mode else [int(float(numbers[index])) for index in return_index]