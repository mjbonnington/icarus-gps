#!/usr/bin/python

# [Icarus] icarus.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019 Gramercy Park Studios
#
# Launch Icarus.


import os
import sys

# Import custom modules
from core import icarus__main__
from shared import verbose


def standalone(**kwargs):
	""" Run in standalone mode.
	"""
	if kwargs['verbosity'] != -1:
		os.environ['IC_VERBOSITY'] = str(kwargs['verbosity'])

	os.environ['IC_EXPERT_MODE'] = str(kwargs['expert'])

	main_app = icarus__main__.main_application()

	# Apply application style
	style = icarus__main__.get_style()
	if style is not None:
		main_app.setStyle(style)

	icarus = icarus__main__.window(**kwargs)
	icarus.show()
	sys.exit(main_app.exec_())


def app(app=None, parent=None):
	""" Run in DCC app mode. Return the instance of the main app object to add
		to an AppSession object.
	"""
	icarus = icarus__main__.window(app=app, parent=parent)
	return icarus
