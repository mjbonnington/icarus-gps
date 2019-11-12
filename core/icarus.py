#!/usr/bin/python

# [Icarus] icarus.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2019 Gramercy Park Studios
#
# Launch Icarus.


import os
import sys

# Import custom modules
from core import icarus__main__
from shared import verbose

# verbose = Verbose.Verbosity()
# verbose.setOutput('console')
# verbose.printOut()


# Python version check
try:
	assert sys.version_info >= (2,7)
except AssertionError:
	sys.exit("ERROR: Python version 2.7 or above is required.")


def standalone():
	""" Run in standalone mode.
	"""
	main_app = icarus__main__.main_application()
	icarus = icarus__main__.window()
	icarus.show()
	sys.exit(main_app.exec_())


def app(app=None, parent=None):
	""" Run in DCC app mode. Return the instance of the main app object to add
		to an AppSession object.
	"""
	icarus = icarus__main__.window(app=app, parent=parent)
	return icarus
