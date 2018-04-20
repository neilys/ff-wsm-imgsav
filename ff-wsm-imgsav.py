import re
import sys
import urllib.request
import urllib.parse
import http.cookiejar
import hashlib
import img2pdf

def login(uname,passwd):
    url='https://fordforums.com.au/login.php?do=login'
    md5pwd=hashlib.md5(passwd.encode('utf-8')).hexdigest()
    param={ 'do':'login',
            'vb_login_md5password':md5pwd,
            'vb_login_md5password_utf':md5pwd,
            's': '',
            'vb_login_username':uname,
            'securitytoke':'guest',
            }
    dat=urllib.parse.urlencode(param).encode('utf-8')
    cj=http.cookiejar.CookieJar()
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    r=opener.open(url,dat)
    return opener

def carlist(openhandle,url):
    r=openhandle.open(url)
    content=r.read().decode('utf-8','ignore')
    ttl=re.findall(r'<a href=[\S]*?articleid=(\d+)[\W]+title=[\s\S]+?\">(.*)</a>',content)
    ttlen=len(ttl)
    for i in range(ttlen):
        print('{0:4}.   {1:}'.format(i,ttl[i][1]))
    try:
        sel=int(input('select the num for the right vehicle: '))
    except sel>ttlen:
        print('invalid input')
    return ttl[sel]

def wsmlist(carsel):
    url='https://fordforums.com.au/vbportal/viewarticle.php?articleid='+carsel[0]
    r=openhandle.open(url)
    content=r.read().decode('utf-8','ignore')
    ttl=re.findall(r'<a href=\"(http[\S]*)\.html\"\starget[\S]+?\">(.*)</a>',content)
    ttlen=len(ttl)
    for i in range(ttlen):
        print('{0:4}.  {1:}'.format(i,ttl[i][1]))
    try:
        sel=int(input('select the num for the section you want: '))
    except sel>ttlen:
        print('invalid input')
    return ttl[sel]

def imglist(wsmsel):
    url=wsmsel[0]+'.html'
    r=openhandle.open(url)
    while 1:
        content=r.readline().decode('utf-8','ignore')
        pgn=re.search(r'<title>.*Page.\d\sof\s(\d+)<\/title>',content)
        if pgn!=None:
            break

    fname=wsmsel[1][0:6]+'.pdf'
    print('You have '+pgn.group(1)+' page(s) to download...')
    fo=open(fname,'wb')
    io=[]
    for i in range(1,int(pgn.group(1))+1):
        url=wsmsel[0]+str(i).zfill(5)+'im.jpg'
        fname=str(i).zfill(5)+'im.jpg'
        r=openhandle.open(url).read()
        io.append(r)
        print('downloading ...    ', fname)
        sys.stdout.flush()
    fo.write(img2pdf.convert(io))
    fo.close()
    print(fname+' download completed')

if __name__=='__main__':
  header={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}
  affurl='https://fordforums.com.au/vbportal/viewcategory.php?moduleid=82'
  uname=input('Your Fordforums username: ')
  passwd=input('Your Fordforums passwd: ')
  openhandle=login(uname,passwd)
  carsel=carlist(openhandle,affurl)
  wsmsel=wsmlist(carsel)
  imglist(wsmsel)
