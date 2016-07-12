#!/usr/bin/python

# [GPS] gpsNodes.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# GPS custom nodes.


import os
import nuke
import gpsSave, osOps, vCtrl


############
# GPS READ #
############
def read_create():
	""" Create a custom GPS Read node.
	"""
	readDir = osOps.normPath('$SHOTPATH/')
	dialogPathLs = nuke.getClipname('Read File(s)', default=readDir, multiple=True)
	if dialogPathLs:
		for dialogPath in dialogPathLs:
			try:
				filePath, frameRange = dialogPath.split(' ')
				startFrame, endFrame = frameRange.split('-')
			except ValueError:
				filePath = dialogPath
				startFrame, endFrame = os.environ['STARTFRAME'], os.environ['ENDFRAME']

			# Make filePath relative
			if os.environ['JOBPATH'] in filePath:
				filePath = filePath.replace(os.environ['JOBPATH'], '[getenv JOBPATH]')

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
	if not gpsSave.getWorkingScriptName():
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
	writeNode.knob('beforeRender').setValue('gpsNodes.w_create_dir()')
	writeNode.knob('afterRender').setValue('gpsNodes.w_openPermissions()')

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
		osOps.createDir(path)
	return path


def w_openPermissions():
	""" Opens up the permissions for all written files.
	"""
	path = os.path.dirname(nuke.filename(nuke.thisNode()))
	osOps.setPermissions(path)


def w_global_preset(writeNode, presetType):
	""" Sets the default presets on the write node.
	"""
	startFrame = os.environ['STARTFRAME']
	endFrame = os.environ['ENDFRAME']
	writeNode = nuke.thisNode()
	writeNode.knob('use_limit').setValue('True')
	writeNode.knob('first').setValue(int(startFrame))
	writeNode.knob('last').setValue(int(endFrame))


def w_path_preset(writeNode, presetType='Precomp'):
	""" Sets the filePath presets.
	"""
	if 'Plate_' in presetType:
		presetType = presetType.replace('Plate_', '')
		filePath = os.path.join('[getenv SHOTPATH]', 'Plate', presetType)
		fullPath = os.path.join(os.environ['SHOTPATH'], 'Plate', presetType)
	else:
		filePath = os.path.join('[getenv NUKERENDERSDIR]', presetType)
		fullPath = os.path.join(os.environ['NUKERENDERSDIR'], presetType)

	version = vCtrl.version(fullPath)
	filePath = osOps.normPath( os.path.join(filePath, version) )

	return filePath


def w_fileName_preset(writeNode, filePath, presetType, ext, proxy=True):
	""" Sets the fileName presets.
	"""
	fileName = '%s_%s.%s.%s' % (os.environ['SHOT'], presetType, r'%04d', ext)
#	fullPath = os.path.join(filePath, 'full', fileName)
#	fileName = '$SHOT_%s.%04d.%s' % (presetType, ext)
	fullPath = osOps.normPath('%s/full/%s' %(filePath, fileName))
	writeNode.knob('file').setValue(fullPath)
	if proxy:
#		proxyPath = os.path.join(filePath, 'proxy', fileName)
		proxyPath = osOps.normPath('%s/proxy/%s' %(filePath, fileName))
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

