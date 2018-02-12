#!/usr/bin/python

# [Icarus] render_submit_deadline.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2018 Gramercy Park Studios
#
# Batch Render Submitter
# This module contains functions specifically for submitting jobs to Deadline.


import os
import re
import subprocess

# Import custom modules
import osOps
import verbose


# Prevent spawned processes from opening a shell window
CREATE_NO_WINDOW = 0x08000000


def strToList(string):
	""" Convert string to list by splitting into lines.
		Encode bytes to string for Python 3.
	"""
	string = string.decode()
	ls = string.splitlines()
	# print(ls)
	return ls


def get_pools():
	""" Get Deadline pools and return in a list.
	"""
	try:
		pools = subprocess.check_output(
			[os.environ['DEADLINECMDVERSION'], '-pools'], 
			creationflags=CREATE_NO_WINDOW)
		return strToList(pools)
	except:
		verbose.warning("Could not retrieve Deadline pools.")
		return None


def get_groups():
	""" Get Deadline groups and return in a list.
	"""
	try:
		groups = subprocess.check_output(
			[os.environ['DEADLINECMDVERSION'], '-groups'], 
			creationflags=CREATE_NO_WINDOW)
		return strToList(groups)
	except:
		verbose.warning("Could not retrieve Deadline groups.")
		return None


def settings_filename(self, scene, suffix=""):
	""" Determine the path to the settings file based on the full path of the
		scene file.
	"""
	if os.path.isfile(scene):
		sceneDir, sceneFile = os.path.split(scene)
		settingsDir = os.path.join(sceneDir, os.environ['DATAFILESRELATIVEDIR'])
		settingsFile = osOps.sanitize(sceneFile, replace='_') + suffix

		# Create settings directory if it doesn't exist
		if not os.path.isdir(settingsDir):
			osOps.createDir(settingsDir)

		return os.path.join(settingsDir, settingsFile)

	else:
		return False


def generate_job_info_file(jobInfoFile, 
						   scene, 
						   renderLayer, 
						   plugin, 
						   jobName, 
						   comment, 
						   frames, 
						   chunkSize, 
						   pool, 
						   group, 
						   priority, 
						   output):
	""" Generate job submission info file.
	"""
	# if renderLayer:
	# 	jobInfoFileSuffix = "%s_deadlineJobInfo.txt" %renderLayer
	# else:
	# 	jobInfoFileSuffix = "_deadlineJobInfo.txt"
	# jobInfoFile = self.settings_filename(scene, suffix=jobInfoFileSuffix)
	fh = open(jobInfoFile, 'w')
	fh.write("Plugin=%s\n" %plugin)
	if renderLayer:
		fh.write("Name=%s - %s\n" %(jobName, renderLayer))
		fh.write("BatchName=%s\n" %jobName)
	else:
		fh.write("Name=%s\n" %jobName)
	fh.write("Comment=%s\n" %comment)
	fh.write("Frames=%s\n" %frames)
	fh.write("ChunkSize=%s\n" %chunkSize)
	fh.write("Pool=%s\n" %pool)
	fh.write("Group=%s\n" %group)
	fh.write("Priority=%s\n" %priority)
	if priority == 0:
		fh.write("InitialStatus=Suspended\n")
	for i, outputPath in enumerate(output):
		fh.write("OutputDirectory%d=%s\n" %(i, outputPath[0]))
		fh.write("OutputFilename%d=%s\n" %(i, outputPath[1]))
	#fh.write("IncludeEnvironment=True\n")
	fh.write("ExtraInfo0=%s\n" %os.environ['JOB'])
	fh.write("ExtraInfo1=%s\n" %os.environ['SHOT'])
	fh.close()

	return jobInfoFile


def generate_plugin_info_file(pluginInfoFile, 
							  scene, 
							  renderLayer, 
							  version, 
							  renderer, 
							  projectPath, 
							  outputFilePath, 
							  outputFilePrefix):
	""" Generate plugin submission info file.
	"""
	# if renderLayer:
	# 	pluginInfoFileSuffix = "%s_deadlinePluginInfo.txt" %renderLayer
	# else:
	# 	pluginInfoFileSuffix = "_deadlinePluginInfo.txt"
	# pluginInfoFile = self.settings_filename(scene, suffix=pluginInfoFileSuffix)
	fh = open(pluginInfoFile, 'w')
	fh.write("Version=%s\n" %version)
	fh.write("Build=64bit\n")
	fh.write("Renderer=%s\n" %renderer)
	fh.write("StrictErrorChecking=1\n")
	fh.write("ProjectPath=%s\n" %projectPath)
	fh.write("OutputFilePath=%s\n" %outputFilePath)
	fh.write("OutputFilePrefix=%s\n" %outputFilePrefix)
	fh.write("SceneFile=%s\n" %scene)
	if renderLayer:
		fh.write("UsingRenderLayers=1\n")
		fh.write("UseLegacyRenderLayers=1\n")
		fh.write("RenderLayer=%s\n" %renderLayer)
	fh.close()

	return pluginInfoFile


def generate_batch_file(jobInfoFileList, pluginInfoFileList):
	""" Generate batch job submission file given corresponding lists of job
		and plugin info files.
	"""
	batchSubmissionFile = self.settings_filename(scene, suffix="_args.txt")
	fh = open(batchSubmissionFile, 'w')
	fh.write("-SubmitMultipleJobs\n")
	for i in range(len(jobInfoFileList)):
		fh.write("-job\n")
		fh.write("%s\n" %jobInfoFileList[i])
		fh.write("%s\n" %pluginInfoFileList[i])
	fh.close()

	return batchSubmissionFile


def submit_job(self, scene, renderLayer, **kwargs):
	""" Submit job to Deadline.
	"""
	if kwargs is not None:
		for key, value in kwargs.iteritems():
			print("%s = %s" %(key, value))

	try:
		if usingRenderLayers:  # Batch submit ----------------------------
			# Generate submission info files
			jobInfoFileList = []
			pluginInfoFileList = []
			for renderLayer in renderLayerList:
				jobInfoFile = generate_job_info_file(scene, 
													 renderLayer, 
													 plugin, 
													 jobName, 
													 comment, 
													 frames, 
													 taskSize, 
													 pool, 
													 group, 
													 priority, 
													 output)
				jobInfoFileList.append(jobInfoFile)

				pluginInfoFile = generate_plugin_info_file(scene, 
														   renderLayer, 
														   version, 
														   renderer, 
														   mayaProject, 
														   outputFilePath, 
														   outputFilePrefix)
				pluginInfoFileList.append(pluginInfoFile)

			# Generate batch file
			batchSubmissionFile = generate_batch_file(jobInfoFileList, pluginInfoFileList)

			# Execute deadlinecommand
			cmd_output = subprocess.check_output(
				[os.environ['DEADLINECMDVERSION'], batchSubmissionFile], 
				creationflags=CREATE_NO_WINDOW)
			output_str = cmd_output.decode()

			result_msg = "Successfully submitted job to Deadline."
			verbose.message(result_msg)

			# # Delete submission info files - TEMPORARILY DISABLED FOR DEBUGGING PURPOSES
			# for jobInfoFile in jobInfoFileList:
			# 	osOps.recurseRemove(jobInfoFile)
			# for pluginInfoFile in pluginInfoFileList:
			# 	osOps.recurseRemove(pluginInfoFile)
			# osOps.recurseRemove(batchSubmissionFile)


		else:  # Single job submit ---------------------------------------
			# Generate submission info files
			jobInfoFile = generate_job_info_file(scene, 
												 None, 
												 plugin, 
												 jobName, 
												 comment, 
												 frames, 
												 taskSize, 
												 pool, 
												 group, 
												 priority, 
												 output)

			pluginInfoFile = generate_plugin_info_file(scene, 
													   None, 
													   version, 
													   renderer, 
													   mayaProject, 
													   outputFilePath, 
													   outputFilePrefix)

			# Execute deadlinecommand
			cmd_output = subprocess.check_output(
				[os.environ['DEADLINECMDVERSION'], jobInfoFile, pluginInfoFile], 
				creationflags=CREATE_NO_WINDOW)
			output_str = cmd_output.decode()

			result_msg = "Successfully submitted job to Deadline."
			verbose.message(result_msg)

			# # Delete submission info files - TEMPORARILY DISABLED FOR DEBUGGING PURPOSES
			# osOps.recurseRemove(jobInfoFile)
			# osOps.recurseRemove(pluginInfoFile)

	except:
		import traceback
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		result_msg = "Failed to submit job to Deadline."
		verbose.error(result_msg)
		output_str = "Either the Deadline executable could not be found, or the submission info files could not be written." #\n\n%s" % traceback.format_exc()

