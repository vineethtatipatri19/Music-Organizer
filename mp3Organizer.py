import os
import id3reader
import shutil #Used for copying files

def getArtist(path):
    path.split('\\')
    id3r=id3reader.Reader(path)
    artist=str(id3r.getValue('performer'))
    return artist


##CONFIG
source_dir = "C:\\Users\Vineeth\Downloads\Test\\" #set the root folder that you want to     scan and move files from.  This script will scan recursively.
destPath = "C:\\Users\Vineeth\Downloads\Music\\" #set the destination root that you want to move files to.  Any non-existing sub directories will be created.
ext = ".mp3" #set the type of file you want to search for.
count = 0 #initialize counter variable to count number of files moved
##

##FIND FILES
for dirName, subdirList, fileList in os.walk(source_dir):

    #set the path for the destination folder(s)
    dest = destPath + dirName.replace(source_dir, '') 
    print dest
    #if the source directory doesn't exist in the destination folder
    #then create a new folder
    if not os.path.isdir(dest):
        os.mkdir(dest)
        print('Directory created at: ' + dest)
    print fileList
    for fname in fileList:
        if fname.endswith(ext) :
            #determine source & new file locations
            oldLoc = dirName + '\\' + fname
            Artist = getArtist(oldLoc)
            print Artist
            newLoc = dest + Artist + '\\' + fname

            if os.path.isfile(newLoc): # check to see if the file already exists.  If it does print out a message saying so.
                print ('file "' + newLoc + fname + '" already exists')

            if not os.path.isfile(newLoc): #if the file doesnt exist then copy it and print out confirmation that is was copied/moved
                try:
                    d=dest + Artist 
                    if not os.path.isdir(d):
                        os.mkdir(d)
                        print('Directory created at: ' + dest)
                    shutil.move(oldLoc, newLoc)
                    print('File ' + fname + ' copied.')
                    count = count + 1
                except IOError:
                    print('There was an error copying the file:  "' + fname + '"')
                    print 'error'            

print "\n"
print str(count) + " files were moved."
print "\n"
