#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@hogarthww.com
#title    :pathPrc

import os
import jobs

#processes job and shot names and returns their full path
def process(job, shot=False):
	if shot:
		path_ = os.path.join(jobs.dic[job], os.environ['SHOTSROOTRELATIVEDIR'], shot)
	else:
		path_ = os.path.join(jobs.dic[job], os.environ['SHOTSROOTRELATIVEDIR'])
	return path_





	
	
