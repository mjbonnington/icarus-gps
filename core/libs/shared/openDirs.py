#!/usr/bin/python
#support    :Nuno Pereira - nuno.pereira@hogarthww.com
#title      :openDirs

import os

if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
	sysCommand = 'open'
elif os.environ['ICARUS_RUNNING_OS'] == 'Windows':
	sysCommand = 'explorer'
else:
	sysCommand = 'nautilus'


def openElementsLib():
	elementsLibDir = os.environ['ELEMENTSLIBRARY']
	if os.path.isdir(elementsLibDir):
		os.system('%s %s' % (sysCommand, elementsLibDir))

def openJob():
	jobRoot = os.path.split(os.environ['JOBPATH'])[0]
	if os.path.isdir(jobRoot):
		os.system('%s %s' % (sysCommand, jobRoot))
	return

def openMaya():
	mayaDir = os.environ['MAYADIR']
	if os.path.isdir(mayaDir):
		os.system('%s %s' % (sysCommand, mayaDir))
	return

def openMayaPlayblasts():
	plbDir =  os.environ["MAYAPLAYBLASTSDIR"]
	if os.path.isdir(plbDir):
		os.system('%s %s' % (sysCommand, plbDir))
	return

def openMayaRenders():
	rendersDir =  os.environ["MAYARENDERSDIR"]
	if os.path.isdir(rendersDir):
		os.system('%s %s' % (sysCommand, rendersDir))
	return

def openMayaScenes():
	scenesDir =  os.environ["MAYASCENESDIR"]
	if os.path.isdir(scenesDir):
		os.system('%s %s' % (sysCommand, scenesDir))
	return

def openMayaSourceimages():
	cachesDir =  os.environ["MAYASOURCEIMAGESDIR"]
	if os.path.isdir(cachesDir):
		os.system('%s %s' % (sysCommand, cachesDir))
	return

def openNuke():
	nukeDir = os.environ['NUKEDIR']
	if os.path.isdir(nukeDir):
		os.system('%s %s' % (sysCommand, nukeDir))
	return

def openNukeElements():
	nukeDir = os.environ['NUKEELEMENTSDIR']
	if os.path.isdir(nukeDir):
		os.system('%s %s' % (sysCommand, nukeDir))
	return

def openNukeRenders():
	nukeDir = os.environ['NUKERENDERSDIR']
	if os.path.isdir(nukeDir):
		os.system('%s %s' % (sysCommand, nukeDir))
	return

def openNukeScripts():
	nukeDir = os.environ['NUKESCRIPTSDIR']
	if os.path.isdir(nukeDir):
		os.system('%s %s' % (sysCommand, nukeDir))
	return

def openRealflowScenes():
	realflowDir = os.environ['REALFLOWSCENESDIR']
	if os.path.isdir(realflowDir):
		os.system('%s %s' % (sysCommand, realflowDir))
	return

def openShot():
	jobPath = os.environ['SHOTPATH']
	if os.path.isdir(jobPath):
		os.system('%s %s' % (sysCommand, jobPath))
	return
