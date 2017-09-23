#-*- coding:utf-8 -*-
from httplib import HTTPException
import cookielib, urllib2,urllib
from Cookie import CookieError
import re
import time
import os
#import ssl 
#关闭ssl验证
#ssl._create_default_https_context = ssl._create_unverified_context
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
        self.size=r'600x600'
        self.orgsize=r'150x150'
        #self.delete=re.compile(r'_master\d*')
        self.OrigingalUrl="https://www.pixiv.net/member_illust.php?mode=medium&illust_id={0}"
        #读取cookie
        self.cookie=cookielib.MozillaCookieJar()
        self.handle=urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.handle)
        #用来获得文件名的正则表达式
        self.namefinder=re.compile('/[a-z,A-Z,_,0-9]*?.jpg')
        self.sizeF=re.compile(self.orgsize)
        self.finder=re.compile(r'<img.*?data-src="(.*?)".*?class="original-image">.*?>')
        self.Header=  { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
                                  ,'Host': 'i.pximg.net'
                                  ,'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
                                  ,'Accept-Encoding': 'gzip, deflate, br'
                                  ,'Referer': 'https://www.pixiv.net/'
                                  ,'DNT': '1'
                                  ,'User-Agent':'godofalb'
                                  ,'Connection': 'keep-alive'
                                  ,'Accept':'*/*'
                                     }
        
        self.username=''
        self.password=''
    #登入
    def LoginIn(self):
        url="https://accounts.pixiv.net/api/login?lang=zh"
        loginUrl="https://accounts.pixiv.net/login"
        Header=  { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
                                  ,'Host': 'accounts.pixiv.net'
                                  ,'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
                                  ,'Accept-Encoding': 'gzip, deflate, br'
                                  ,'Referer': 'https://accounts.pixiv.net/login'
                                  ,'DNT': '1'
                                  ,'User-Agent':'godofalb'
                                  ,'Connection': 'keep-alive'
                                  ,'Accept':'*/*'
                                     }
        req1=self.opener.open(loginUrl)
        content=req1.read()
        pattern = re.compile(r'<input.*?"post_key".*?value="(.*?)"') 
 
        match = pattern.search(content)
        if match: 
            print match.group(1)
            datas={'pixiv_id':self.username,'password':self.password
                   ,'post_key':match.group(1)
                   ,'ref':'wwwtop_accounts_index'
                   ,'return_to':'https://www.pixiv.net/'
                   ,'source':'pc'
            }
            postdata = urllib.urlencode(datas)
            req=urllib2.Request(url,headers=Header,data=postdata)
            res=self.opener.open(req)
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
    def savePic(self,path,filename,link,name,pid='',date='',saveOrigingal=True):
        #P站不需要这个
        #time.sleep(1)
        print 'saving'
        reallink=''
        if saveOrigingal and pid:
            try:
                print 'finding'
                tempres=urllib2.Request(self.OrigingalUrl.format(pid))
                print self.OrigingalUrl.format(pid)
                time.sleep(1)
                res = self.opener.open(tempres)
                reallink=self.finder.search(res.read()).group(1)
            except Exception,e:
                print e.message
        else:
            reallink=self.sizeF.sub(self.size,link)
        if not reallink:
            reallink=self.sizeF.sub(self.size,link)     
        print reallink
        request=urllib2.Request(reallink,headers=self.Header)
        response = self.opener.open(request)
        try:
            file=open((path+'\\'+date+name+'.jpg').decode('utf-8'),"wb")
            print (path+'\\'+date+name+'.jpg').decode('utf-8')
            file.write(response.read())
            file.close()
        except:
            file=open((path+'\\'+date+filename+'.jpg').decode('utf-8'),"wb")
            print (path+'\\'+date+name+'.jpg').decode('utf-8')
            file.write(response.read())
            file.close()
    #保存文本 https://i.pximg.net/img-original/img/2017/09/15/19/41/41/64969252_p0.jpg
    def saveTxt(self,path,name,linkname,tag,author,aid,pid,date=''):
        try:
            file=open((path+'\\'+date+name+'.txt').decode('utf-8'),'w')
            file.write("作品名:{0}\n文件名:{1}\n作品id:{2}\n作者:{3} \n作者id:{4}\n标签:{5}\n".format(name,linkname,pid,author,aid,tag))
            file.close()
        except:
            file=open((path+'\\'+date+linkname+'.txt').decode('utf-8'),'w')
            file.write("作品名:{0}\n文件名:{1}\n作品id:{2}\n作者:{3} \n作者id:{4}\n标签:{5}\n".format(name,linkname,pid,author,aid,tag))
            file.close()
    #保存推荐内容
    def saveRec(self,contents,NewDate=True):
        #0-url 1-pid 2-tag 3-aid 4-title 5-username
        pattern=re.compile(r'<li.*?class="image-item".*?data-src="(.*?)".*?data-id="(.*?)".*?data-tags="(.*?)".*?data-user-id="(.*?)".*?<h1 class="title gtm-recommended-illusts" title="(.*?)">.*?data-user_name="(.*?)".*?</li>',re.S)
        FPath= self.recommonedPath
        
        if NewDate:
            FPath=FPath+'\\'+time.strftime('%Y-%m-%d',time.localtime(time.time()))
            self.mkDir(FPath)
        for content in contents:
            for s in re.findall(pattern,content):
                print s[0],s[1],s[2],s[3],s[4],s[5]
                self.saveTxt(
                              FPath,
                              s[4], 
                              self.namefinder.search(s[0]).group()[1:], 
                              s[2], 
                              s[5], 
                              s[3], 
                              s[1],
                              time.strftime('%Y-%m-%d',time.localtime(time.time())))
                self.savePic(
                            FPath,
                            self.namefinder.search(s[0]).group()[1:],
                            s[0], 
                            s[4],
                            s[1],
                            time.strftime('%Y-%m-%d',time.localtime(time.time())))
    #保存大家更新内容
    def saveNew(self,contents,NewDate=True):
        #0-url 1-pid 2-tag 3-aid 4-title 5-username
        pattern=re.compile(r'<li.*?class="image-item".*?data-src="(.*?)".*?data-id="(.*?)".*?data-tags="(.*?)".*?data-user-id="(.*?)".*?<h1 class="title gtm-everyone-new-illusts" title="(.*?)">.*?data-user_name="(.*?)".*?</li>',re.S)
        FPath=self.newPath
        if NewDate:
            FPath=FPath+'\\'+time.strftime('%Y-%m-%d',time.localtime(time.time()))
            self.mkDir(FPath)
        for content in contents:
            for s in re.findall(pattern,content):
                print s[0],s[1],s[2],s[3],s[4],s[5]
                self.saveTxt(
                              FPath,
                              s[4], 
                              self.namefinder.search(s[0]).group()[1:], 
                              s[2], 
                              s[5], 
                              s[3], 
                              s[1],
                              time.strftime('%Y-%m-%d',time.localtime(time.time())))
                self.savePic(
                            
                             FPath,
                             
                            self.namefinder.search(s[0]).group()[1:],
                            s[0], 
                            s[4],
                            s[1],
                            time.strftime('%Y-%m-%d',time.localtime(time.time())))
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
                            s[4],
                            s[1])
   
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
                            s[4],
                            s[1])
    #获得主页信息
    def getMain(self,save=False,wantNew=False,wantRec=True,NewDate=True):
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
                self.saveRec(re.findall(recommonedpattern,content),NewDate)#recommonedpattern.search(content).group())
            if wantNew: 
                newpattern=re.compile(r'<section class="item everyone-new-illusts" data-name="everyone_new_illusts">.*?</section>',re.S)
                self.saveNew(re.findall(newpattern,content),NewDate)#newpattern.search(content).group())
            print "Over"
        except CookieError,e:
            print e.reason
        except Exception, e:
            print e.message
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
                    
                    pattern=re.compile(r'<a.*?class="user-name".*?>(.*?)</a>',re.S)
                    Aname=pattern.search(content).group(1)
                    
                    print Aname
                    path=self.authorPath+'\\'+Aname
                    print path
                    self.mkDir(path)
                    
                self.saveAuthor(content,path,Aname)
            print "Over"
        except CookieError,e:
            print e.reason
if __name__=='__main__':
    pass
p=PixivLinker()
	#p.getAuthor('4239212',False, 9)#'8189060'
	#p.getMyNew(False, 1)
p.getMain(save=True,wantNew=False,wantRec=True)
