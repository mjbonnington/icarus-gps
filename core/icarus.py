#!/usr/bin/python

# [Icarus] icarus.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Launch Icarus.


import os
import sys

# Import custom modules
from core import icarus__main__


def standalone(**kwargs):
	""" Run in standalone mode.
	"""
	main_app = icarus__main__.main_application()

	# Apply application style
	style = icarus__main__.get_style()
	if style is not None:
		main_app.setStyle(style)

	icarus = icarus__main__.get_window(**kwargs)
	icarus.show()
	sys.exit(main_app.exec_())


def app(app=None, parent=None):
	""" Run in DCC app mode. Return the instance of the main app object to add
		to an AppSession object.
	"""
	icarus = icarus__main__.get_window(app=app, parent=parent)
	return icarus
