#-*- coding:utf-8 -*-
from httplib import HTTPException
import cookielib, urllib2,urllib
from Cookie import CookieError
import re
import time
import types
import os
#import ssl 
#关闭ssl验证
#ssl._create_default_https_context = ssl._create_unverified_context
false=False
true=True
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
        self.findfilename=re.compile(r'/.*?\..*?', re.S)
        self.findworkplace=re.compile(r'<div class="_layout-thumbnail">(.*?)</div>',  re.S)
        self.finder=re.compile(r'(https://i.pximg.net/img-original/.*?)"', re.S)
        #self.finder=re.compile(r'<img.*?data-src="(https://i.pximg.net/img-original/.*?)".*?class="original-image".*?>', re.S)
        self.Header=  { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
                                  ,'Host': 'i.pximg.net'
                                  ,'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
                                  ,'Accept-Encoding': 'gzip, deflate, br'
                                  ,'Referer': 'https://www.pixiv.net/'
                                  ,'DNT': '1'
				                  
                                  ,'Connection': 'keep-alive'
                                  ,'Accept':'*/*'
                                     }

        self.domainfinder=re.compile(r'://(.*?)/')
        self.username=''
        self.password=''
        self.maxList=50
    def UrlChange(self,url):
        domain=re.search(self.domainfinder,url)
        if domain:
            domain=domain.group(1)
            return url.replace(domain,self.pixivDNS[domain])
        return url
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
                                  
                                  ,'Connection': 'keep-alive'
                                  ,'Accept':'*/*'
                                     }
        req1=self.opener.open(loginUrl)
        content=req1.read()
        pattern = re.compile(r'<input.*?"post_key".*?value="(.*?)"') 
 
        match = pattern.search(content)
        if match: 
            
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
    def dealpic(self,pid):
        print 'saving'
        
        reallink=[]
        filename=[]
        try:
            print 'finding'
            tempres=urllib2.Request(self.OrigingalUrl.format(pid))
            print self.OrigingalUrl.format(pid)
            time.sleep(1)
            res = self.opener.open(tempres)
            content=self.finder.search(res.read()).group(1)
            reallink.append(content)
            filename.append(self.findfilename.search(content))
        except Exception,e:
            print e.message
        
         
    #保存图片
    def savePic(self,path,filename,link,name,pid='',date=''):

        reallink=''
        if pid:
            try:
                print 'finding'
                tempres=urllib2.Request(self.OrigingalUrl.format(pid))
                print self.OrigingalUrl.format(pid)
                time.sleep(3)
                res = self.opener.open(tempres)
                reallink=self.finder.search(res.read()).group(1)
                name+="."+reallink[-3:]
            except Exception,e:
                print e.message
        else:
            reallink=self.sizeF.sub(self.size,link)
            name+='.jpg'
        if not reallink:
            reallink=self.sizeF.sub(self.size,link)   
            name+='.jpg'  
        print reallink,name
        request=urllib2.Request(reallink,headers=self.Header)
        response = self.opener.open(request)
       
        try:
            print path+'\\'+date+name
            file=open((path+'\\'+date+name),"wb")
            
           # for byte in response.read():
            file.write( response.read())
            file.close()
        except Exception,e:
            print e.message
            print path+'\\'+date+filename+'.jpg'
            file=open((path+'\\'+date+filename+'.jpg'),"wb")
           
           # for byte in response.read():
            file.write( response.read())
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
                              s[1])
                self.savePic(
                            FPath,
                            self.namefinder.search(s[0]).group()[1:],
                            s[0], 
                            s[4],
                            s[1])
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
                              s[1])
                self.savePic(
                            
                             FPath,
                             
                            self.namefinder.search(s[0]).group()[1:],
                            s[0], 
                            s[4],
                            s[1])
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
    def saveList(self,ids,path,header,tt):
        
        #https://www.pixiv.net/rpc/illust_list.php?illust_ids=65473011%2C65419178%2C65074614%2C65185576%2C65508558%2C65456275%2C65144502%2C65531239%2C65414423%2C65409762%2C65074959%2C65373539%2C65525510%2C65382906%2C65518224%2C65467454%2C65520983%2C65353027%2C65108280%2C65127935%2C65290068%2C65397514%2C65346015%2C65433918%2C65407698%2C65281689%2C65185350%2C65422835%2C65364898%2C65259574%2C65326536%2C65374516%2C65474412%2C65204968%2C65471083%2C65440000%2C65535513%2C65481378%2C65115686%2C65435274%2C65202162%2C65511561%2C65089638%2C65096039%2C65540233%2C65472225%2C65178994%2C65202055%2C65256707%2C65486757&page=discover&exclude_muted_illusts=1&tt=b4424083a29b1aa069dcf38eaf318dbc
        listurl='https://www.pixiv.net/rpc/illust_list.php?illust_ids='
        b=True
        for id in ids:
            if b:
                b=False
                listurl+='{0}'.format(id)
            else:
                listurl+='%2C{0}'.format(id)
        listurl+='&page=discover&exclude_muted_illusts=1&tt=%s'%(tt)
        req=urllib2.Request(listurl,headers=header)
        response=self.opener.open(req)
        content=response.read()
        
       # pattern=re.compile(r'"tags":(?P<tags>.*?),"url":(?P<url>.*?),"user_name":(?P<user_name>.*?),"illust_id":(?P<illust_id>.*?),"illust_title":(?P<illust_title>.*?),"illust_user_id":(?P<illust_user_id>.*?),"user_name":(?P<user_name>.*?),"user_name":(?P<user_name>.*?),"user_name":(?P<user_name>.*?),"user_name":(?P<user_name>.*?),"user_name":(?P<user_name>.*?),"user_name":(?P<user_name>.*?),"user_name":(?P<user_name>.*?),"user_name":(?P<user_name>.*?),"user_name":(?P<user_name>.*?),"user_name":(?P<user_name>.*?)', re.S)
        for match in re.findall(r'{.*?}',content,re.S):
            
            time.sleep(1)
            jsons=eval(match)
            '''
            for k in jsons:
                if type(jsons[k])==types.StringType:
                    jsons[k]=jsons[k].decode('unicode-escape')
                if types(jsons[k])==types.ListType:
            '''        
         
            tags=''
            for tag in jsons['tags']:
               
                if tag[0]=='\\' and tag[1]=='u' :
                    tags+=tag.decode('unicode-escape')+' , '
                    
                else:
                    tags+=tag+' , '
                    
            jsons['tags']=tags
         
            for k in jsons:
                if type(jsons[k])==types.StringType:
                    if jsons[k][0]=='\\' and jsons[k][1]=='u' :
                        jsons[k]=jsons[k].decode('unicode-escape')
            #path,name,linkname,tag,author,aid,pid,date=''
            '''
            print jsons['illust_title']
            print self.namefinder.search(jsons['url']).group()[1:]
            print jsons['tags']
            print jsons['user_name']
            print jsons['illust_user_id']
            print jsons['illust_id']
            print jsons['url']
            print jsons['illust_page_count']
            print re.sub(r'\\/',r'/',jsons['url'])
            '''
            self.saveTxt(path,jsons['illust_title'],self.namefinder.search(jsons['url']).group()[1:],jsons['tags'],jsons['user_name'],jsons['illust_user_id'],jsons['illust_id'])
            #self,path,filename,link,name,pid='',date='' path,filename,link,name,pid='',date=''
            #savePic(self,path,filename,link,name,pid='',date=''):
        
            self.savePic(path, self.namefinder.search(jsons['url']).group()[1:], re.sub(r'\\/','/',jsons['url']),jsons['illust_title'],pid=jsons['illust_id'])
        pass
    def getRecommend(self,num=10):
       
        req=urllib2.Request('https://www.pixiv.net/discovery')
        response=self.opener.open(req)
        content=response.read()
        tokenfinder=re.compile(r'pixiv.context.token = "(.*?)"', re.S)
        tokenmatch = re.search(tokenfinder, content)
        Header=  { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
                                  ,'Host': 'www.pixiv.net'
                                  ,'Referer': 'https://www.pixiv.net/discovery'
                                  ,'DNT': '1'
                                 
                                  ,'Accept':'*/*'
                                     }
        tt=tokenmatch.group(1)
        datareq=urllib2.Request('https://www.pixiv.net/rpc/recommender.php?type=illust&sample_illusts=auto&num_recommendations={0}&page=discovery&mode=all&tt={1}'.format(num,tt),headers=Header)
        datasresponse=self.opener.open(datareq)
        data=datasresponse.read()
        FPath=self.recommonedPath+'\\'+time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.mkDir(FPath)
        
        i=0
        L=[]
        for match in re.findall(r'\d+',data,re.S):
            i+=1
            L.append(match)
            if i>=self.maxList:
                print 'sending-------------------'
                self.saveList(L,FPath,Header,tt)
                i=0
                L=[]
        self.saveList(L,FPath,Header,tt) 
            
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
