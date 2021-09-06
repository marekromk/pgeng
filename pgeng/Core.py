'''Many core functions for pgeng'''
#IMPORTS
import pygame, os
from collections import Counter
from glob import glob
from sys import exit as _sysexit #UNDERSCORE SO IT IS NOT VISIBLE AS A FUNCTION
#IMPORTS

#VARIABLES
global AnimationFrames
AnimationFrames = {}
#VARIABLES

#LOADANIMATION
def LoadAnimation(Path, FrameDurations, Colourkey=None, FileType=None):
	'''A function for loading still images for a animation
	It loads all images in a directory, the last character before the file type needs to be a number
	The file type of the frames should be the most used file type in the directory
	Example:
		\'Frame1.png\'
		\'Frame2.png\'

	Or you can use FileType variable
	Example:
		FileType='.png'

	Returns: List'''
	if not os.path.exists(Path):
		raise FileNotFoundError(f'Folder or file \'{Path}\' does not exist')
	global AnimationFrames
	AnimationName = Path.split('/')[-1]
	if not FileType:
		Files = glob(f'{Path}/*.*')
		Files = [os.path.splitext(File)[1] for File in Files]
		FileType = MostUsed(Files)[0]
	AnimationFrameData = []
	for i, FrameAmount in enumerate(FrameDurations):
		AnimationFrameID = f'{AnimationName}{i + 1}'
		try:
			AnimationImage = LoadImage(f'{Path}/{AnimationFrameID}{FileType}', Colourkey)
		except:
			raise pygame.error(f'Too many non image files in \'{Path}\'')
		AnimationFrames[AnimationFrameID] = AnimationImage
		for i in range(FrameAmount):
			AnimationFrameData.append(AnimationFrameID)
	return AnimationFrameData
#LOADANIMATION

#SETANIMATIONACTION
def SetAnimationAction(ActionVariable, NewAction, ActionFrame):
	'''Setting an action in an animation

	Returns: Tuple'''
	if ActionVariable != NewAction:
		ActionVariable = NewAction
		ActionFrame = 0
	return ActionVariable, ActionFrame
#SETANIMATIONACTION

#CLIPIMAGE
def ClipSurface(Surface, Location, Size):
	'''Creates a new Surface from the part of another Surface

	Returns: pygame.Surface'''
	NewSurface = Surface.copy()
	ClipRect = pygame.Rect(Location, Size)
	NewSurface.set_clip(ClipRect)
	Image = Surface.subsurface(NewSurface.get_clip())
	return Image
#CLIPIMAGE

#LOADIMAGE
def LoadImage(File, Colourkey=None, Alpha=None):
	'''Load an image for pygame that will be converted
	You can set a Colourkey and Alpha as well

	Returns: pygame.Surface'''
	Image = pygame.image.load(File).convert()
	Image.set_colorkey(Colourkey)
	Image.set_alpha(Alpha)
	return Image
#LOADIMAGE

#QUITGAME
def QuitGame():
	'''Exiting a pygame program in the correct way
	Runs:
		pygame.quit() and sys.exit()'''
	pygame.quit()
	_sysexit()
#QUITGAME

#READFILE
def ReadFile(Path):
	'''Reads a file and returns the data in it

	Returns: String'''
	File = open(Path)
	Data = File.read()
	File.close()
	return Data
#READFILE

#WRITETOFILE
def WriteToFile(Path, Data):
	'''Writes data to a file
	The data has to be a string'''
	File = open(Path, 'w')
	File.write(Data)
	File.close()
#WRITETOFILE

#NEAREST
def Nearest(Input, Nearest, IntMode=True):
	'''Returns a number changed to the nearest given
	If IntMode is True, it will truncate every returned number and return an integer

	Returns: Integer (or float)'''
	return int(round(Input / Nearest) * Nearest) if IntMode else round(Input / Nearest) * Nearest
#NEAREST

#MOSTUSED
def MostUsed(List, Amount=False):
	'''Return the most used value in the list
	It will return the amount used of the value in the list if Amount is True

	Returns: List'''
	ListCounter = Counter(List)
	TotalTimes = list(ListCounter.values()).count(max(list(ListCounter.values())))
	return ListCounter.most_common(TotalTimes) if Amount else [Value[0] for Value in ListCounter.most_common(TotalTimes)]
#MOSTUSED

#STRINGNUMBER
def StringNumber(String, ReturnIndex=None, IntMode=False):
	'''Return numbers from a given string
	If ReturnIndex is None it will return everything, except if a list or typle with the indexes gets given
	Example:
		ReturnIndex=[0, 2] This will make it return the first and third number

	If IntMode is True, it will truncate every returned number and return an integer

	Returns: List (None if no number is found)'''
	if any(Character.isdigit() for Character in String):
		Numbers = []
		AmountNumber = 0
		Digits = []
		for i in range(len(String)):
			if String[i].isdigit() and (any(String[min(i + 1, len(String) - 1)] == Character for Character in ['.', ',']) or String[min(i + 1, len(String) - 1)].isdigit()): #CHECK IF THE NEXT CHARACTER IS . OR , OR A NUMBER
				if any(String[min(i + 1, len(String) - 1)] == Character for Character in ['.', ',']) and String[min(i + 2, len(String) - 1)].isdigit() and not any('.' in Digit for Digit in Digits): #IF NEXT CHARACTER IS . AND AFTER THAT IS A NUMBER AND A . IS NOT ALREADY IN THE DIGITS
					Digits.append(f'{String[i]}.')
				elif any(String[min(i + 1, len(String) - 1)] == Character for Character in ['.', ',']): #CHECK IF ELSE NUMBERS ENDS WITH A . OR ,
					Digits.append(String[i])
					Numbers.append(''.join(Digits))
					AmountNumber += 1
					Digits = []
				else: #NORMAL SITUATION
					Digits.append(String[i])
			elif String[i].isdigit(): #IF ELSE IT'S THE LAST DIGIT IN THE NUMBER
				Digits.append(String[i])
				Numbers.append(''.join(Digits))
				AmountNumber += 1
				Digits = []
			if String[i].isdigit() and i == len(String) - 1: #IF THE NUMBER IS THE LAST CHARACTER OF THE STRING
				Numbers.append(''.join(Digits))
		if type(ReturnIndex) != list and type(ReturnIndex) != tuple:
			ReturnIndex = [i for i in range(len(Numbers))]
		if ReturnIndex and min(ReturnIndex) < -len(Numbers) or max(ReturnIndex) > len(Numbers) - 1:
			raise IndexError('Index in ReturnIndex is not possible')
		return [int(float(Numbers[Index])) for Index in ReturnIndex] if IntMode else [float(Numbers[Index]) for Index in ReturnIndex]
	return None #RETURN NONE IF THERE IS NO NUMBER FOUND IN THE STRING
#STRINGNUMBER