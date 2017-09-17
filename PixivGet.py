#import pixivlink
import time
from pixivlink import PixivLinker
from Cookie import CookieError
p=PixivLinker()
p.username='你的用户名'
p.password='你的密码'
count=1
while 1==1:
	try:
		p.getMain(save=True,wantNew=True,wantRec=True)
		count+=1
		if count==12:
			count=0
			p.LoginIn()
	except CookieError,e:
		print e.reason
	except:
		pass
	finally:
		print 'newround'
		time.sleep(7200)
    	
        