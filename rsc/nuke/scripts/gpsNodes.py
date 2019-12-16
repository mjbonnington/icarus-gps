#!/usr/bin/python

# [GPS] gpsNodes.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2018 Gramercy Park Studios
#
# GPS custom nodes.


import os
import nuke

from shared import os_wrapper
from shared import vCtrl


############
# GPS READ #
############
def read_create():
	""" Create a custom GPS Read node.
	"""
	readDir = os_wrapper.absolutePath('$IC_SHOTPATH/')
	dialogPathLs = nuke.getClipname('Read File(s)', default=readDir, multiple=True)
	if dialogPathLs:
		for dialogPath in dialogPathLs:
			try:
				filePath, frameRange = dialogPath.split(' ')
				startFrame, endFrame = frameRange.split('-')
			except ValueError:
				filePath = dialogPath
				startFrame, endFrame = os.environ['IC_STARTFRAME'], os.environ['IC_ENDFRAME']

			# Make filePath relative
			filePath = os_wrapper.relativePath(filePath, 'IC_JOBPATH', tokenFormat='nuke')

			readNode = nuke.createNode('Read', 'name GPS_Read')
			readNode.knob('file').setValue(filePath)
			readNode.knob('cacheLocal').setValue('always')
			readNode.knob('cached').setValue('True')
			readNode.knob('first').setValue(int(startFrame))
			readNode.knob('last').setValue(int(endFrame))

		return readNode


#############
# GPS WRITE #
#############
def write_create():
	""" Create a custom GPS Write node.
	"""
	if not getWorkingScriptName():  # re-write this function
		nuke.message('Please save your script first')
		return

	writeNode = nuke.createNode('Write', 'name GPS_Write')
	presetLs = ['Comp', 'CG_Comp', 'Precomp', 'Roto', 'Elements', 'Plate_Raw', 'Plate_Graded', 'Plate_CG']
	gps_presets_tab = nuke.Tab_Knob('gps_presets', 'GPS_Write_Presets')
	gps_write_presets = nuke.Enumeration_Knob('write_presets', 'Write Preset', presetLs)
	writeNode.addKnob(gps_presets_tab)
	writeNode.addKnob(gps_write_presets)
	writeNode['knobChanged'].setValue('gpsNodes.w_presets_callback()')
	writeNode.knob('write_presets').setValue('Precomp')

	try:
		writeNode.knob('create_directories').setValue('True')
	# Create directories option added in Nuke 10.5x makes this redundant...
	except:
		writeNode.knob('beforeRender').setValue('gpsNodes.w_create_dir()')
		# writeNode.knob('afterRender').setValue('gpsNodes.w_openPermissions()')

	renderSubmit_button = nuke.PyScript_Knob('renderSubmit_button', 'Submit to Render Queue', 'gpsNodes.w_render_submit()')
	renderSubmit_button.setFlag(nuke.STARTLINE)
	writeNode.addKnob(renderSubmit_button)

	return writeNode


def w_presets_callback():
	""" Callback function to fill write nodes automatically with standard GPS presets.
	"""
	writeNode = nuke.thisNode()
	if nuke.thisKnob().name() == 'write_presets':
		presetType = nuke.thisKnob().value()
		w_global_preset(writeNode, presetType)
		filePath = w_path_preset(writeNode, presetType)
		if presetType in ('CG_Comp', 'Precomp', 'Roto', 'Elements'):
			w_fileName_preset(writeNode, filePath, presetType, 'exr', proxy=True)
			w_exr_preset(writeNode)
		elif presetType in ('Comp', 'Plate_Raw', 'Plate_Graded'):
			w_fileName_preset(writeNode, filePath, presetType, 'dpx', proxy=True)
			w_dpx_preset(writeNode)
		elif presetType == 'Plate_CG':
			w_fileName_preset(writeNode, filePath, presetType, 'jpg', proxy=True)
			w_jpg_preset(writeNode)
		return presetType


def w_create_dir():
	""" Automatically create write node directory.
	"""
	path = os.path.dirname(nuke.filename(nuke.thisNode()))
	if not os.path.isdir(path):
		os_wrapper.createDir(path)
	return path


def w_openPermissions():
	""" Opens up the permissions for all written files.
	"""
	path = os.path.dirname(nuke.filename(nuke.thisNode()))
	os_wrapper.setPermissions(path)


def w_global_preset(writeNode, presetType):
	""" Sets the default presets on the write node.
	"""
	startFrame = os.environ['IC_STARTFRAME']
	endFrame = os.environ['IC_ENDFRAME']
	writeNode = nuke.thisNode()
	writeNode.knob('use_limit').setValue('True')
	writeNode.knob('first').setValue(int(startFrame))
	writeNode.knob('last').setValue(int(endFrame))


def w_path_preset(writeNode, presetType='Precomp'):
	""" Sets the filePath presets.
	"""
	if 'Plate_' in presetType:
		presetType = presetType.replace('Plate_', '')
		filePath = os.path.join('[getenv IC_SHOTPATH]', 'plate', presetType)
		fullPath = os.path.join(os.environ['IC_SHOTPATH'], 'plate', presetType)
	else:
		filePath = os.path.join('[getenv IC_NUKE_RENDERS_DIR]', presetType)
		fullPath = os.path.join(os.environ['IC_NUKE_RENDERS_DIR'], presetType)

	version = vCtrl.version(fullPath)
	filePath = os_wrapper.absolutePath(os.path.join(filePath, version))

	return filePath


def w_fileName_preset(writeNode, filePath, presetType, ext, proxy=True):
	""" Sets the fileName presets.
	"""
	fileName = '%s_%s.%s.%s' % (os.environ['IC_SHOT'], presetType, r'%04d', ext)
	# fullPath = os.path.join(filePath, 'full', fileName)
	# fileName = '$IC_SHOT_%s.%04d.%s' % (presetType, ext)
	fullPath = os_wrapper.absolutePath('%s/full/%s' %(filePath, fileName))
	writeNode.knob('file').setValue(fullPath)
	if proxy:
		# proxyPath = os.path.join(filePath, 'proxy', fileName)
		proxyPath = os_wrapper.absolutePath('%s/proxy/%s' %(filePath, fileName))
		writeNode.knob('proxy').setValue(proxyPath)


def w_exr_preset(writeNode):
	""" Sets the OpenEXR type specific presets.
	"""
	writeNode.knob('channels').setValue('rgba')
	writeNode.knob('file_type').setValue('exr')
	writeNode.knob('datatype').setValue('16 bit half')
	writeNode.knob('compression').setValue('Zip (16 scanlines)')


def w_dpx_preset(writeNode):
	""" Sets the DPX type specific presets.
	"""
	writeNode.knob('channels').setValue('rgb')
	writeNode.knob('file_type').setValue('dpx')
	writeNode.knob('datatype').setValue('10 bit')
	writeNode.knob('colorspace').setValue('sRGB')


def w_jpg_preset(writeNode):
	""" Sets the JPEG type specific presets.
	"""
	writeNode.knob('channels').setValue('rgb')
	writeNode.knob('file_type').setValue('jpeg')
	writeNode.knob('_jpeg_quality').setValue(0.75)
	writeNode.knob('colorspace').setValue('sRGB')


def w_render_submit():
	""" Launches GPS Render Submitter dialog.
	"""
	writeNode = nuke.thisNode()

	if writeNode.knob('use_limit').value():
		first = int(writeNode.knob('first').value())
		last = int(writeNode.knob('last').value())
		frameRange = "%s-%s" %(first, last)
	else:
		frameRange = None

	from tools.renderqueue import submit
	submit.run_nuke(
		session, 
		layers=writeNode.name(), 
		frameRange=frameRange)


def getWorkingScriptName():
	""" Strips all naming conventions and returns script name.
		Moved from redundant gpsSave module. Should be re-written ultimately.
	"""
	workingScript = nuke.root().name()
	if not os.path.isfile(workingScript):
		return
	try:
		#spliting path and getting file name only
		scriptName = os.path.split(workingScript)[1]
		#getting rid of all naming conventions to get script name only
		scriptName = scriptName.split('%s_' % os.environ['IC_SHOT'])[-1]
		version = scriptName.split('_')[-1]
		scriptName = scriptName.split('_%s' % version)[0]
		#getting rid of padding and extension
		scriptName = scriptName.split('.')[0]
		return scriptName
	except:
		return
