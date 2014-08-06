#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@hogarthww.com
#title     	:openDirs

import os, sys

if sys.platform == 'darwin':
	sysCommand = 'open'
else:
	sysCommand = 'nautilus'
	
def openMaya():
	mayaDir = os.environ['MAYADIR']
	if os.path.isdir(mayaDir):
		os.system('%s %s' % (sysCommand, mayaDir))
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

def openMayaPlayblasts():
	plbDir =  os.environ["MAYAPLAYBLASTSDIR"]
	if os.path.isdir(plbDir):
		os.system('%s %s' % (sysCommand, plbDir))
	return

def openShot():
	jobPath = os.environ['SHOTPATH']
	if os.path.isdir(jobPath):
		os.system('%s %s' % (sysCommand, jobPath))
	return


def openJob():
	jobRoot = os.environ['JOBPATH']
	if os.path.isdir(jobRoot):
		os.system('%s %s' % (sysCommand, jobRoot))
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
