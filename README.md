# pgengine
Useful functions and classes for PyGame
### Documentation
#### Core

\
`LoadAnimation(Path, FrameDurations, Colourkey=None, FileType=None)`
\
A function for loading still images for a animation\
It loads all images in a directory, the last character before the file type needs to be a number\
The file type of the frames should be the most used file type in the directory\
Example:\
&emsp;`'Frame1.png', 'Frame2.png'`

Or you can use FileType variable\
Example:\
&emsp;`FileType='.png'`

Return: List