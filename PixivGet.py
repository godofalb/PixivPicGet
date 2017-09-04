#import pixivlink
import time
from pixivlink import PixivLinker
from Cookie import CookieError
p=PixivLinker()

while 1==1:
	try:
		p.getMain(save=True,wantNew=False,wantRec=True)
	except CookieError,e:
		print e.reason
	finally:
		print 'newround'
		time.sleep(3600)
    	
        
