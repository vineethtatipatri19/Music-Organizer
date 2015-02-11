#Searches for music files 
import os
Mfiles = []
for (dirname, dirs, files) in os.walk('/home/stryker'):
   for filename in files:
       if filename.endswith('.mp3') :
           Mfiles += [filename]
print Mfiles
