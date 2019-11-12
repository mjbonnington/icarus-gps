#!/usr/bin/python

# [Icarus] inProgress.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Publish in progress tmp file manager.


import os
from shared import os_wrapper


def start(pblDir):
	in_progressFile = open(os.path.join(pblDir, 'in_progress.tmp'), 'w')
	in_progressFile.close()


def end(pblDir):
	in_progressFile = os.path.join(pblDir, 'in_progress.tmp')
	if os.path.isfile(in_progressFile):
		os_wrapper.recurseRemove(in_progressFile)
