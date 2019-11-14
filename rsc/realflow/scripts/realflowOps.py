#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:realflowOps
#copyright	:Gramercy Park Studios

import os, subprocess
from shared import os_wrapper
from shared import djvOps
	
	
def importObj(scene, GUIFilePickerDialog, FILE_PICKER_LOAD):
	dialog = GUIFilePickerDialog.new()
	defaultPath = os.path.join(os.environ['RFOBJECTSPATH'])
	objPath = dialog.show(FILE_PICKER_LOAD, defaultPath, '*.abc;*.obj;*.sd', 'GPS - Object Import')
	if objPath:
		scene.importObjects(objPath)
	
def newScene(scene):
	scene.new()
	scene.message('GPS - New Scene created.')
		
def openScene(scene, GUIFilePickerDialog, FILE_PICKER_LOAD):
	dialog = GUIFilePickerDialog.new()
	defaultPath = os.path.join(os.environ['RFDEFAULTPROJECT'])
	scenePath = dialog.show(FILE_PICKER_LOAD, defaultPath, '*.flw', 'GPS - Open Scene')
	if scenePath:
		scene.load(scenePath)
		
def saveScene(scene):
	projPath = scene.getRootPath()
	sceneName = scene.getFileName()
	if sceneName == None:
		sceneName = os.path.split(projPath)[-1]
	if not sceneName.endswith('.flw'):
		sceneName += '.flw'
	scene.save(os.path.join(projPath, sceneName))
	scene.message('GPS - Scene Saved.')

	
def purgeScene(scene, GUIFormDialog, particles=True, meshes=True, preview=True):
	dialog = GUIFormDialog.new()
	dialog.setTitle('GPS - Purge Scene')
	dialog.addStringField('All unused data will be deleted.This operation is not undoable. Continue?','')
	dialogResult = dialog.show()
	if not dialogResult:
		return
	
	#purges particles
	if particles:
		#getting particles direcotry and particle emitter names in scene
		particleDir = os.path.join(scene.getRootPath(), 'particles')
		particleLs = os.listdir(particleDir)
		inUseParticleLs = []
		emitters = scene.get_PB_Emitters()
		emitterNameLs = []
		for emitter in emitters:
		 emitterNameLs.append(emitter.getName())

		#determining particles in use	
		for particle in particleLs:
			for emitterName in emitterNameLs:
				if emitterName in particle:
					inUseParticleLs.append(particle)
		#removing unused particles			
		for particle in particleLs:
				if particle not in inUseParticleLs:
					scene.message(str(particle))
					os_wrapper.remove(os.path.join(particleDir,  particle))
	
	#purges meshes
	if meshes:
		meshFileDir = os.path.join(scene.getRootPath(), 'meshes')
		meshFileLs = os.listdir(meshFileDir)
		inUseMeshLs = []
		meshLs = scene.getParticleMeshesLegacy()
		meshNameLs = []
		for mesh in meshLs:
 			meshNameLs.append(mesh.getName())
			
		#determining meshes in use	
		for meshFile in meshFileLs:
			for meshName in meshNameLs:
				if meshName in meshFile:
					inUseMeshLs.append(meshFile)
					
		#removing unused meshes			
		for meshFile in meshFileLs:
			if meshFile not in inUseMeshLs:
				scene.message(str(meshFile))
				os_wrapper.remove(os.path.join(meshFileDir,  meshFile))
				
	#purges preivew
	if preview:
		previewDir = os.path.join(scene.getRootPath(), 'preview')
		os_wrapper.remove(previewDir)
		
def preview(scene, EXECUTE_SHELL_COMMAND):
	from . import versionUp
	#getting scene, project and shot settings
	sceneName = scene.getFileName()
	if not sceneName:
		scene.message('Scene must be saved before using preview')
		return
	
	sceneName = sceneName.replace('.flw', '')
	projectDir = scene.getRootPath()
	playblastDir = os.path.join(projectDir, 'preview')
	version = versionUp.vCtrl(playblastDir)
	imgPreviewDir = os.path.join(projectDir, 'preview', version[1], 'images')
	movPreviewDir = os.path.join(projectDir, 'preview', version[1], 'mov')
	width = float(os.environ['RESOLUTIONX'])
	width = int(round(width / 1.5))
	height = float(os.environ['RESOLUTIONY'])
	height = int(round(height / 1.5))
	startFrame = int(scene.getMinFrame())
	endFrame = int(scene.getLastCachedFrame())
	#creating directories
	os_wrapper.createDir(imgPreviewDir)
	os_wrapper.createDir(movPreviewDir)
	scene.videoPreview(os.path.join(movPreviewDir, sceneName), 
	imgPreviewDir, 
	width, 
	height, 
	True, 
	True, 
	startFrame, 
	endFrame, 
	False, 
	EXECUTE_SHELL_COMMAND)
	#launching viewer
	firstFrame = os.listdir(imgPreviewDir); firstFrame = firstFrame[0] 
	djvOps.viewer(os.path.join(imgPreviewDir, firstFrame))
