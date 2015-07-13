import id3reader
import os
import urllib2
import urllib
import simplejson
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from bs4 import BeautifulSoup, NavigableString, Tag
import pafy
import ctypes
from ctypes import POINTER, Structure, c_wchar, c_int, sizeof, byref
from ctypes.wintypes import BYTE, WORD, DWORD, LPWSTR, LPSTR
import win32api
import win32con
import shutil #Used for copying files


def Option1():

    HICON = c_int
    LPTSTR = LPWSTR
    TCHAR = c_wchar
    MAX_PATH = 260
    FCSM_ICONFILE = 0x00000010
    FCS_FORCEWRITE = 0x00000002
    SHGFI_ICONLOCATION = 0x000001000    

    class GUID(Structure):
        _fields_ = [
            ('Data1', DWORD),
            ('Data2', WORD),
            ('Data3', WORD),
            ('Data4', BYTE * 8)]

    class SHFOLDERCUSTOMSETTINGS(Structure):
        _fields_ = [
            ('dwSize', DWORD),
            ('dwMask', DWORD),
            ('pvid', POINTER(GUID)),
            ('pszWebViewTemplate', LPTSTR),
            ('cchWebViewTemplate', DWORD),
            ('pszWebViewTemplateVersion', LPTSTR),
            ('pszInfoTip', LPTSTR),
            ('cchInfoTip', DWORD),
            ('pclsid', POINTER(GUID)),
            ('dwFlags', DWORD),
            ('pszIconFile', LPTSTR),
            ('cchIconFile', DWORD),
            ('iIconIndex', c_int),
            ('pszLogo', LPTSTR),
            ('cchLogo', DWORD)]

    class SHFILEINFO(Structure):
        _fields_ = [
            ('hIcon', HICON),
            ('iIcon', c_int),
            ('dwAttributes', DWORD),
            ('szDisplayName', TCHAR * MAX_PATH),
            ('szTypeName', TCHAR * 80)]    

    def seticon(folderpath, iconpath, iconindex):
        """Set folder icon.

        >>> seticon(".", "C:\\Windows\\system32\\SHELL32.dll", 10)

        """
        shell32 = ctypes.windll.shell32

        folderpath = unicode(os.path.abspath(folderpath), 'mbcs')
        iconpath = unicode(os.path.abspath(iconpath), 'mbcs')
        win32api.SetFileAttributes("E:\Test\JFX Bits.ico", win32con.FILE_ATTRIBUTE_READONLY)
        win32api.SetFileAttributes("E:\Test\JFX Bits.ico",win32con.FILE_ATTRIBUTE_HIDDEN)
        fcs = SHFOLDERCUSTOMSETTINGS()
        fcs.dwSize = sizeof(fcs)
        fcs.dwMask = FCSM_ICONFILE
        fcs.pszIconFile = iconpath
        fcs.cchIconFile = 0
        fcs.iIconIndex = iconindex

        hr = shell32.SHGetSetFolderCustomSettings(byref(fcs), folderpath,
                                                  FCS_FORCEWRITE)
        if hr:
            raise WindowsError(win32api.FormatMessage(hr))

        sfi = SHFILEINFO()
        hr = shell32.SHGetFileInfoW(folderpath, 0, byref(sfi), sizeof(sfi),
                                    SHGFI_ICONLOCATION)
        if hr == 0:
            raise WindowsError(win32api.FormatMessage(hr))

        index = shell32.Shell_GetCachedImageIndexW(sfi.szDisplayName, sfi.iIcon, 0)
        if index == -1:
            raise WindowsError()

        shell32.SHUpdateImageW(sfi.szDisplayName, sfi.iIcon, 0, index)
    
    def getArtist(path):
        path.split('\\')
        id3r=id3reader.Reader(path)
        artist=str(id3r.getValue('performer'))
        return artist


    ##CONFIG
    source_dir = "C:\\Users\Vineeth\Documents\Test\\" #set the root folder that you want to     scan and move files from.  This script will scan recursively.
    destPath = "C:\\Users\Vineeth\Documents\Music\\" #set the destination root that you want to move files to.  Any non-existing sub directories will be created.
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
                        seticon(d,"C:\\Users\Vineeth\Documents\Test\icons\\" + Artist +".ico",0)
                    except IOError:
                        print('There was an error copying the file:  "' + fname + '"')
                        print 'error'            

    print "\n"
    print str(count) + " files were moved."
    print "\n"

    #seticon("C:\\Users\Vineeth\Documents\Test\\","C:\\Users\Vineeth\Documents\icons\\",0)

def Option2():
    p="E:\\test"
    Mfiles=[]
    for (dirname, dirs, files) in os.walk(p):
        for filename in files:
            if filename.endswith('.mp3') :
                Mfiles += [filename]
                #print Mfiles

    #Updating Album Arts
    def update_albumart(name):
        audio = MP3(name+'.mp3', ID3=ID3)

        # add ID3 tag if it doesn't exist
        try:
            audio.add_tags()
        except error:
            pass

        audio.tags.add(
            APIC(
                encoding=3, # 3 is for utf-8
                mime='image/png', # image/jpeg or image/png
                type=3, # 3 is for the cover image
                desc=u'Cover',
                data=open(name+'.png').read()
            )
        )
        audio.save()
        print "Album Art Updated.."
        print "\n\n\n"
    add_search=""
    #List Music dir
    def getTags(path,nam):
        path.split('\\')
        id3r=id3reader.Reader(path)
        artist=str(id3r.getValue('performer'))
        album=str(id3r.getValue('album'))
        track=str(id3r.getValue('title'))
        genre=str(id3r.getValue('genre'))
        if "Bollywood" in genre: add_search="site:albumartindia.com"
        if "bollywood" in genre: add_search="site:albumartindia.com"
        if "hindi" in genre: add_search="site:albumartindia.com"
        if "Hindi" in genre: add_search="site:albumartindia.com"
        if artist == None: artist = ''
        if album == None: album = ''
        if track == None: track ='' 
        search_term=artist + " " +nam+ " " +add_search
        print search_term
        nam=nam.split('.mp3')[0]
        getPic(search_term,nam)
        update_albumart(nam)

    #Downloading the appropriate image from google images using ajax
    def getPic(search,track):
        search= search.split()
        search='+'.join(search)
        req = urllib2.Request("http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q="+search+"&start=1&imgsz=medium|large&as_filetype=png", None, {'user-agent':'Mozilla'})
        opener = urllib2.build_opener()
        f = opener.open(req)
        a=simplejson.load(f)
        imageurl=a['responseData']['results'][0]['url']
        print track
        print "Image Downloading.."
        urllib.urlretrieve(imageurl,track+".png")
        print "Image Downloaded.."

    for nam in Mfiles:
        getTags(p+"\\"+nam,nam)

    def getLyrics(name,artist,album):
        url="http://search.azlyrics.com/search.php?q="
        search=name+" "+artist
        search= search.split()
        search='+'.join(search)

        url=url+search
        html=urllib2.urlopen(url)
        soup=BeautifulSoup(html)
        results=soup.findAll('a')
        a=[]
        for r in results:
            if "/lyrics/" in r['href']:
                a.append(r['href'])
                break
        print a[0]

        lyric=""

        html=urllib2.urlopen(a[0])
        soup=BeautifulSoup(html)
        i=0
        for br in soup.findAll('br'):
            next = br.nextSibling
            if not (next and isinstance(next,NavigableString)):
                continue
            next2 = next.nextSibling
            if next2 and isinstance(next2,Tag) and next2.name == 'br':
                text = str(next).strip()
                if text:
                    lyric+=next + "\n"
                    print next
                    i+=1
        os.remove("C:\Users\sandeepwww\\test.lrc")
        with open("test.lrc", "a") as myfile:
            myfile.write("[ti:"+name+"]\n[ar:"+artist+"]\n[ar:"+album+"]\n"+lyric)









def Option3():
    search=raw_input("Enter The Search Query : \n")
    search= search.split()
    search='+'.join(search)
    google_url="http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="+search+"site:youtube.com"

    req = urllib2.Request(google_url, None, {'user-agent':'Mozilla'})
    opener = urllib2.build_opener()
    f = opener.open(req)
    a=simplejson.load(f)
    videourl=a['responseData']['results'][0]['url']
    newstr = videourl[-11:]
    final_url="https://www.youtube.com/watch?v="+newstr

    video=pafy.new(final_url)
    path1=video.videostreams[8]
    best = video.getbest()
    vlc_url=best.url
    print vlc_url
    path1.download()
    #file1=best.download()



print "         Music Organizer    "
print "------------------------------------"
print "\n"
print " 1. Organize Musics Files"
print " 2. Download Lyrics and Album Art"
print " 3. Download Video"
print "\n"
k=0
while(k==0):
    p=raw_input(" Select one of the option:")
    if p=="1":
        Option1()
        k=1
    elif p=="2":
        Option2()
        k=1
    elif p=="3":
        Option3()
        k=1
    else:
        print "Please select a valid option \n"


