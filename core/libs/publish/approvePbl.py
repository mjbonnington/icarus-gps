#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:renderPbl
#copyright	:Gramercy Park Studios


#approval publish module

import os
import verbose

def publish(apvDir, pblDir, assetDir, version):
	verbose.approval(start=True)
	approvedPblDir = str(os.path.join(apvDir, assetDir))
	
	#creating approved publish directory if not existent
	if not os.path.isdir(approvedPblDir):
		os.system('mkdir -p %s' % approvedPblDir)
	
	#softlinking
	os.system('ln -Fs %s %s' % (pblDir, approvedPblDir))
	verbose.approval(end=True)
	
