
import urllib
import urllib2
import mechanize 
from bs4 import BeautifulSoup
from urlparse import urlparse
import hashlib
import simplejson
import cStringIO


url="http://www.google.com/search?q=maroon+5&tbm=isch"
fetcher = urllib2.build_opener()
searchTerm = 'maroon 5'
startIndex = 0
searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + searchTerm + "&start=" +str(startIndex)
f = fetcher.open(searchUrl)
deserialized_output = simplejson.load(f)
deserialized_output['responseData']['results'][0]['url']
file = cStringIO.StringIO(urllib.urlopen(imageUrl).read())
img = Image.open(file)
#def getPic ():
        #htmltext = urllib.urlopen(url)
        #soup = BeautifulSoup(htmltext)
        #results= soup.findall('a')
        #print results
        #a=[]
        #k=1
       # for result in results:
        #  result['href'].split("&")[0].split('=')[1]
         # a.append(result['href'])
        #if k!=0:
         #   urllib.urlretrieve(a[0],"image0"+".png")
        #else:
         #   print "Error!"
        #print("done..")
