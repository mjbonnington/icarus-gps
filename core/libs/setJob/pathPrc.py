#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@hogarthww.com
#title    :pathPrc

import os
import jobs

#processes job and shot names and returns their full path
def process(job, shot=False):
	if shot:
		shotPath = os.path.join(jobs.dic[job], os.environ['SHOTSROOTRELATIVEDIR'], shot)
	else:
		shotPath = os.path.join(jobs.dic[job], os.environ['SHOTSROOTRELATIVEDIR'])
	return shotPath





	
	
