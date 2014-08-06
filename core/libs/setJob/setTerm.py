#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@hogarthww.com
#title     	:setTerm

import os

def term():
	##STARTS PF BASH TERMINAL AS CHILD PROCESS. INHERITS ALL SET ENV VARS AND LOADS CUSTOM .bashrc FILE
	gpsrcfile = "%s/icarus/libs/setJob/.icarus_bash_profile" % os.environ["PIPELINE"]
	os.system("bash --rcfile %s" % gpsrcfile)
	return
