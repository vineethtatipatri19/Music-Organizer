#Moves all the music files to the default Music Directory and for each file prints ya stores the iD3 data

import eyeD3
import os
Mfiles = []
for (dirname, dirs, files) in os.walk('/home/stryker'):
   for filename in files:
       if filename.endswith('.mp3') :
           Mfiles += [filename]
#print Mfiles
tag = eyeD3.Tag()
p="/home/stryker/Music/"
for nam in Mfiles:
	tag.link(p+nam)
	print tag.getArtist()
	print tag.getAlbum()
	print tag.getTitle()
	print tag.getYear()
#print tag.getDuration()
