#Moves all the music files to the default Music Directory and for each file prints ya stores the iD3 data

import eyeD3
import os
import datetime
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)
   
#for (dirname, dirs, files) in os.walk('/home/stryker'):
#   for filename in files:
#       if filename.endswith('.mp3') :
#           Mfiles += [filename]
#print Mfiles
Mfiles=[]
os.system("find /home/stryker -iname \"*.mp3\" -type f -print0 | xargs -0 -I '{}' /bin/mv \"{}\" /home/stryker/Music")
p="/home/stryker/Music/"

#List Music dir

Mfiles=os.listdir(p)
tag = eyeD3.Tag()
for nam in Mfiles:
	tag.link(p+nam)
	print tag.getArtist()
	print tag.getAlbum()
	print tag.getTitle()
	print tag.getYear()
	print modification_date(p+nam)
#print tag.getDuration()

