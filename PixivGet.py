#import pixivlink
import time
from pixivlink import PixivLinker
from Cookie import CookieError
p=PixivLinker()
p.username='你的用户名'
p.password='你的密码'
while 1==1:
	try:
		p.LoginIn()
		p.getRecommend(num=50)
		
			
	except CookieError,e:
		print e.reason
	except:
		pass
	finally:
		print 'newround'
		time.sleep(86400)
    	
        