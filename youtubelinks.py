import pafy
import urllib2
import simplejson
import os

search=raw_input("Enter Shit : \n")
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
best = video.getbestaudio()
vlc_url=best.url
print vlc_url
path1.download()
#file1=best.download()
