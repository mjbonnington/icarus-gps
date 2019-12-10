#!/usr/bin/python

# [Icarus] settings_job.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2017 Gramercy Park Studios
#
# Job settings handler.


import os


class helper():

	def __init__(self, parent, frame):
		""" Setup job properties panel.
		"""
		self.frame = frame

		# Populate line edit with job name
		self.frame.job_lineEdit.setText(os.getenv('IC_JOB', ''))
