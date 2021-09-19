'''Many core functions for pgeng'''
#IMPORTS
import pygame, os
from collections import Counter
from glob import glob
from sys import exit as _sysexit #UNDERSCORE SO IT IS NOT VISIBLE AS A FUNCTION
#IMPORTS

#VARIABLES
global animation_frames
animation_frames = {}
#VARIABLES

#LOAD_ANIMATION
def load_animation(path, frame_durations, colourkey=None, file_type=None):
	'''A function for loading still images for a animation
	It loads all images in a directory, the last character before the file type needs to be a number
	The name of the directory it is in needs to be in the file name (directories above that don't matter),
	The file type of the frames should be the most used file type in the directory
	Example:
		\'Run/Run1.png\'
		\'Run/Run2.png\'

	Or you can use file_type variable
	Example:
		file_type='.png'

	Returns: List'''
	if not os.path.isdir(path):
		raise FileNotFoundError(f'Directory \'{path}\' does not exist')
	global animation_frames
	animation_name = path.replace('\\', '/').split('/')[-1]
	if not file_type:
		files = glob(f'{path}/*.*')
		files = [os.path.splitext(file)[1] for file in files]
		file_type = most_used(files)[0]
	animation_frame_data = []
	for i, frame_amount in enumerate(frame_durations):
		animation_frame_id = f'{animation_name}{i + 1}'
		try:
			animation_image = load_image(f'{path}/{animation_frame_id}{file_type}', colourkey)
		except:
			raise pygame.error(f'Too many non image files in \'{path}\'')
		animation_frames[animation_frame_id] = animation_image
		for i in range(frame_amount):
			animation_frame_data.append(animation_frame_id)
	return animation_frame_data
#LOAD_ANIMATION

#SET_ACTION
def set_action(action, new_action, action_frame):
	'''Setting an action in an animation

	Returns: Tuple'''
	if action != new_action:
		action = new_action
		action_frame = 0
	return action, action_frame
#SET_ACTION

#CLIP_SURFACE
def clip_surface(surface, location, size):
	'''Creates a new Surface from a part of another Surface

	Returns: pygame.Surface'''
	new_surface = surface.copy()
	new_surface.set_clip(pygame.Rect(location, size))
	clipped_surface = surface.subsurface(new_surface.get_clip())
	return clipped_surface
#CLIP_SURFACE

#LOAD_IMAGE
def load_image(path, colourkey=None, alpha=None):
	'''Load an image for pygame that will be converted
	You can set a colourkey and alpha as well

	Returns: pygame.Surface'''
	image = pygame.image.load(path).convert()
	image.set_colorkey(colourkey)
	image.set_alpha(alpha)
	return image
#LOAD_IMAGE

#QUIT_GAME
def quit_game():
	'''Exiting a pygame program in the correct way
	Runs:
		pygame.quit() and sys.exit()'''
	pygame.quit()
	_sysexit()
#QUIT_GAME

#READ_FILE
def read_file(path):
	'''Reads a file and returns the that's data in it

	Returns: String'''
	file = open(path)
	data = file.read()
	file.close()
	return data
#READ_FILE

#WRITE_TO_FILE
def write_to_file(path, data):
	'''Writes data to a file
	The data has to be a string'''
	file = open(path, 'w')
	file.write(data)
	file.close()
#WRITE_TO_FILE

#NEAREST
def nearest(input, nearest, int_mode=True):
	'''Returns a number changed to the nearest given
	If int_mode is True, it will truncate every returned number and return an integer

	Returns: Integer (or float)'''
	return int(round(input / nearest) * nearest) if int_mode else round(input / nearest) * nearest
#NEAREST

#MOST_USED
def most_used(values, amount=False):
	'''Return the most used value in a list
	It will return the amount used of the value in the list if amount is True

	Returns: List'''
	list_counter = Counter(values)
	total_times = list(list_counter.values()).count(max(list(list_counter.values())))
	return list_counter.most_common(total_times) if amount else [value[0] for value in list_counter.most_common(total_times)]
#MOST_USED

#STRING_NUMBER
def string_number(string, return_index=None, int_mode=False):
	'''Return numbers from a given string
	If return_index is None it will return everything, except if a list or tuple with the indexes gets given
	Example:
		return_index=[0, 2] This will make it return the first and third number

	If int_mode is True, it will truncate every returned number and return an integer

	Returns: List (None if no number is found)'''
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
		return [int(float(numbers[index])) for index in return_index] if int_mode else [float(numbers[index]) for index in return_index]
	return None #RETURN NONE IF THERE IS NO NUMBER FOUND IN THE STRING
#STRING_NUMBER