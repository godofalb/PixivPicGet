#-*- coding:utf-8 -*-
import cookielib, urllib2
from Cookie import CookieError
import re
import time
import os
class PixivLinker():
    def __init__(self,filepath="G:\\Hp"):
        print "InitStart"
        #初始化
        self.filePath=filepath
        self.newPath=filepath+'\\New'
        self.mynewPath=filepath+'\\NewMy'
        self.recommonedPath=filepath+'\\Recommoned'
        self.authorPath=filepath+'\\Author'
        #self.searchPath=filepath+'\\Search'
        self.mkDir(self.mynewPath)
        self.mkDir(self.newPath)
        self.mkDir(self.recommonedPath)
        self.mkDir(self.authorPath)
        #self.mkDir(self.searchPath)
        self.mainUrl="https://www.pixiv.net/"
        self.newUrl="https://www.pixiv.net/bookmark_new_illust.php?p={0}"
        self.authorUrl="https://www.pixiv.net/member_illust.php?id={0}&type=all&p={1}"
        #self.searchUrl="https://www.pixiv.net/search.php?word={0}&order=date_d&p={1}"
        self.size='600x600'
        self.orgsize='150x150'
        #读取cookie
        self.cookie=cookielib.MozillaCookieJar()
        self.cookie.load("cookies.txt")
        self.handle=urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.handle)
        #用来获得文件名的正则表达式
        self.namefinder=re.compile('/[a-z,A-Z,_,0-9]*?.jpg')
        self.sizeF=re.compile(self.orgsize)
        self.Header=  { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
                                  ,'Host': 'i.pximg.net'
                                  ,'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
                                  ,'Accept-Encoding': 'gzip, deflate, br'
                                  ,'Referer': 'https://www.pixiv.net/'
                                  ,'DNT': '1'
                                  ,'Connection': 'keep-alive'
                                  ,'Accept':'*/*'
                                     }
        
    #创建新目录
    def mkDir(self,path):
        path = path.strip()
        #注意要添加设置文件编码格式
        isExists=os.path.exists(path.decode('utf-8'))
        if not isExists:
            os.makedirs(path.decode('utf-8'))
            return True
        else:
            print "Exists"
            return False
    #保存图片
    def savePic(self,path,filename,link,name):
        #P站不需要这个
        #time.sleep(1)
        reallink=self.sizeF.sub(self.size,link)
        #print reallink
        request=urllib2.Request(reallink,headers=self.Header)
        response = self.opener.open(request)
        file=open((path+'\\'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+name+'.jpg').decode('utf-8'),"wb")
        print (path+'\\'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+name+'.jpg').decode('utf-8')
        file.write(response.read())
        file.close()
    #保存文本
    def saveTxt(self,path,name,linkname,tag,author,aid,pid):
        file=open((path+'\\'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+name+'.txt').decode('utf-8'),'w')
        file.write("作品名:{0}\n文件名:{1}\n作品id:{2}\n作者:{3} \n作者id:{4}\n标签:{5}\n".format(name,linkname,pid,author,aid,tag))
        file.close()
    #改变要求的图片大小
    def setSize(self,newsize):
        self.size=newsize
    def setSizeO(self,newsize):
        self.orgsize=newsize
        self.sizeF=re.compile(newsize)
    #保存推荐内容
    def saveRec(self,contents):
        #0-url 1-pid 2-tag 3-aid 4-title 5-username
        pattern=re.compile(r'<li.*?class="image-item".*?data-src="(.*?)".*?data-id="(.*?)".*?data-tags="(.*?)".*?data-user-id="(.*?)".*?<h1 class="title gtm-recommended-illusts" title="(.*?)">.*?data-user_name="(.*?)".*?</li>',re.S)
        for content in contents:
            for s in re.findall(pattern,content):
                print s[0],s[1],s[2],s[3],s[4],s[5]
                self.saveTxt(self.recommonedPath,
                              s[4], 
                              self.namefinder.search(s[0]).group()[1:], 
                              s[2], 
                              s[5], 
                              s[3], 
                              s[1])
                self.savePic(self.recommonedPath,
                            self.namefinder.search(s[0]).group()[1:],
                            s[0], 
                            s[4])
    #保存大家更新内容
    def saveNew(self,contents):
        #0-url 1-pid 2-tag 3-aid 4-title 5-username
        pattern=re.compile(r'<li.*?class="image-item".*?data-src="(.*?)".*?data-id="(.*?)".*?data-tags="(.*?)".*?data-user-id="(.*?)".*?<h1 class="title gtm-everyone-new-illusts" title="(.*?)">.*?data-user_name="(.*?)".*?</li>',re.S)
        for content in contents:
            for s in re.findall(pattern,content):
                print s[0],s[1],s[2],s[3],s[4],s[5]
                self.saveTxt(self.newPath,
                              s[4], 
                              self.namefinder.search(s[0]).group()[1:], 
                              s[2], 
                              s[5], 
                              s[3], 
                              s[1])
                self.savePic(self.newPath,
                            self.namefinder.search(s[0]).group()[1:],
                            s[0], 
                            s[4])
    #保存订阅更新内容
    def saveMyNew(self,content):
        #0-url 1-pid 2-tag 3-aid 4-title 5-username
      
        pattern=re.compile(r'<li.*?class="image-item".*?data-src="(.*?)".*?data-id="(.*?)".*?data-tags="(.*?)".*?data-user-id="(.*?)".*?<h1 class="title" title="(.*?)">.*?data-user_name="(.*?)".*?</li>',re.S)
        for s in re.findall(pattern,content):
            print s[0],s[1],s[2],s[3],s[4],s[5]
            self.saveTxt(self.mynewPath,
                              s[4], 
                              self.namefinder.search(s[0]).group()[1:], 
                              s[2], 
                              s[5], 
                              s[3], 
                              s[1])
            self.savePic(self.mynewPath,
                            self.namefinder.search(s[0]).group()[1:],
                            s[0], 
                            s[4])
   
    #保存某作家的内容
    def saveAuthor(self,content,path,aname):
        #0-url 1-pid 2-tag 3-aid 4-title 5-username
        pattern=re.compile(r'<li.*?class="image-item".*?data-src="(.*?)".*?data-id="(.*?)".*?data-tags="(.*?)".*?data-user-id="(.*?)".*?<h1 class="title" title="(.*?)">.*?</li>',re.S)
        for s in re.findall(pattern,content):
            print s[0],s[1],s[2],s[3],s[4]
            self.saveTxt(path,
                              s[4], 
                              self.namefinder.search(s[0]).group()[1:], 
                              s[2], 
                              aname, 
                              s[3], 
                              s[1])
            self.savePic(path,
                            self.namefinder.search(s[0]).group()[1:],
                            s[0], 
                            s[4])
    #获得主页信息
    def getMain(self,save=False,wantNew=False,wantRec=True):
        try:
            print "GetMain..."
            print self.mainUrl
           
            req = urllib2.Request(self.mainUrl)
            response = self.opener.open(req)
            self.cookie.save(filename='cookies.txt', ignore_discard=True, ignore_expires=True)
            content=response.read()
            if save:
                file=open('HtmlTmp.txt','w')
                file.write(content)
                file.close()
            if wantRec:
                recommonedpattern=re.compile(r'<section class="item recommended-illusts " data-name="recommended_illusts">.*?</section>',re.S)
                self.saveRec(re.findall(recommonedpattern,content))#recommonedpattern.search(content).group())
            if wantNew: 
                newpattern=re.compile(r'<section class="item everyone-new-illusts" data-name="everyone_new_illusts">.*?</section>',re.S)
                self.saveNew(re.findall(newpattern,content))#newpattern.search(content).group())
            print "Over"
        except CookieError,e:
            print e.reason
    #获得我的更新
    def getMyNew(self,save=False,MaxPage=1): 
        try:
            print "GetMyNew..."
            for i in range(1,MaxPage+1):
                req = urllib2.Request(self.newUrl.format(i))
                print self.newUrl.format(i)
                response = self.opener.open(req)
                self.cookie.save(filename='cookies.txt', ignore_discard=True, ignore_expires=True)
                content=response.read()
                if save:
                    file=open('HtmlTmp{0}.txt'.format(i),'w')
                    file.write(content)
                    file.close()
                self.saveMyNew(content)
            print "Over"
        except CookieError,e:
            print e.reason

    #获得某作者的信息
    def getAuthor(self,aid,save=False,MaxPage=1):
        try:         
            print 'getAuthor...'
            Aname='UnKnown'
            path=''
            for i in range(1,MaxPage+1):
                req = urllib2.Request(self.authorUrl.format(aid,i))
                print self.authorUrl.format(aid,i)
                response = self.opener.open(req)
                self.cookie.save(filename='cookies.txt', ignore_discard=True, ignore_expires=True)
                content=response.read()
                if save:
                    file=open('HtmlTmp{0}.txt'.format(i),'w')
                    file.write(content)
                    file.close()
                if i==1:
                    pattern=re.compile(r'<h1 class="user">(.*?)</h1>',re.S)
                    Aname=re.findall(pattern,content)[0]
                    print Aname
                    path=self.authorPath+'\\'+Aname
                    print path
                    self.mkDir(path)
                    
                self.saveAuthor(content,path,Aname)
            print "Over"
        except CookieError,e:
            print e.reason
p=PixivLinker()
#p.getAuthor('159905',False, 8)#'8189060'
#p.getMyNew(False, 1)
p.getMain(save=True,wantNew=False,wantRec=True)