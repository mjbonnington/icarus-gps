#!/usr/bin/python

# deadline__env__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Set Deadline-specific environment variables.

import os

from shared import os_wrapper

def set_env():
	os.environ['DEADLINE_PATH'] = os.path.dirname(os.environ['IC_DEADLINE_EXECUTABLE'])

	if os.environ['IC_RUNNING_OS'] == "MacOS":
		os.environ['IC_DEADLINE_CMD_EXECUTABLE'] = os_wrapper.absolutePath('$DEADLINE_PATH/../../../Resources/deadlinecommand')
	else:  # Windows or Linux
		os.environ['IC_DEADLINE_CMD_EXECUTABLE'] = os_wrapper.absolutePath('$DEADLINE_PATH/deadlinecommand')
