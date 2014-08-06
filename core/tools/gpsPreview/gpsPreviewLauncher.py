#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:gpsPreviewLauncher

import os
import gpsPreview__main__; reload(gpsPreview__main__)
	
def launch(env=None):
	if not env:
		return
	os.environ['ICARUSENVAWARE'] = env
	gpsPreview__main__.previewUI()
