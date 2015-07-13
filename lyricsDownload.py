import urllib2
import urllib
import os
from bs4 import BeautifulSoup, NavigableString, Tag

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
