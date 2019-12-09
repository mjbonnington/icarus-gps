#!/usr/bin/python

# redshift__env__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Set Redshift-specific environment variables.

import os

#from shared import os_wrapper

def set_env():
	# os.environ['redshift_LICENSE'] = "port@hostname"

	# Enable deployment of Redshift from centralised location as specified in
	# appPaths.xml
	if os.environ['IC_REDSHIFT_EXECUTABLE'] != "":
		os.environ['REDSHIFT_COREDATAPATH'] = os.environ['IC_REDSHIFT_EXECUTABLE']
	elif os.environ['IC_RUNNING_OS'] == "Windows":
		os.environ['REDSHIFT_COREDATAPATH'] = "C:/ProgramData/Redshift"
	elif os.environ['IC_RUNNING_OS'] == "MacOS":
		os.environ['REDSHIFT_COREDATAPATH'] = "/usr/redshift"
	elif os.environ['IC_RUNNING_OS'] == "Linux":
		os.environ['REDSHIFT_COREDATAPATH'] = "/Applications/redshift"
