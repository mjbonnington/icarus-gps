#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:pointCloud_importer
#copyright	:Gramercy Park Studios


import maya.cmds as mc
import maya.mel as mel
import os, sys

class pointCloud():
	
	def __init__(self, winName=''):
		self.winTitle = 'GPS - Point Cloud Importer'
		self.winName = 'pCloudImport'
		
	#UI
	def UI(self):

		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)
		
		mc.window(self.winName, title=self.winTitle, s=False, w=575, h=350)
		mc.setParent(self.winName)
		mc.columnLayout(adjustableColumn=False)

		mc.setParent('..')
		mc.rowLayout(nc=2)
		mc.separator(style='none', h=15,w=570)
		mc.setParent('..')
		
		mc.rowLayout(nc=12)
		mc.text(l='', w=6)
		mc.text(l=' Point Cloud File       ')
		mc.textField('pCloud', w=336, h=25)
		mc.text(l='', w=12, h=4)
		pCloudDialog = mc.button(l= 'Browse', h=25, w=80, c='pointCloudImporter.pointCloud().pCloudBrowse()')
		mc.setParent('..')
		
		mc.separator(style='none', h=15, w=10)
		
		mc.rowLayout(nc=12)
		mc.text(l='', w=6)
		mc.text(l=' Camera Cloud File   ')
		mc.textField('camCloud', w=336, h=25)
		mc.text(l='', w=12, h=4)
		mc.button(l= 'Browse', h=25, w=80, c='pointCloudImporter.pointCloud().camCloudBrowse()')
		mc.setParent('..')
				
		mc.rowLayout(nc=1)
		mc.separator(style='in',h=25,w=575)
		mc.setParent('..')
		
		mc.rowLayout(nc=4)
		mc.text(l='', w=230)
		a = mc.button('cloudMe', l= 'Cloud Me', h=30, w=122, c='pointCloudImporter.pointCloud().getClouds()')
		mc.setParent('..')
		
		mc.rowLayout(nc=1)
		mc.separator(style='none', h=10,w=550)
		mc.setParent('..')
		mc.setParent('..')
		mc.showWindow( self.winName )	
	#end UI

	
	#point cloud browse dialog
	def pCloudBrowse(self):
		dialogHome = os.environ['SHOTPATH']
		pCloudFiles = "Point Cloud Files (*.txt)"
		pCloudPath = mc.fileDialog2(ds=2, fm=1, dir=dialogHome, ff=pCloudFiles, cap='Point Cloud File', okc='Ok')
		if pCloudPath:
			mc.textField('pCloud', tx=pCloudPath[0], e=True)

	#camera cloud browse dialog
	def camCloudBrowse(self):
		dialogHome = os.environ['SHOTPATH']
		camCloudFiles = "Camera Cloud Files (*.chan)"
		camCloudPath = mc.fileDialog2(ds=2, fm=1, dir=dialogHome, ff=camCloudFiles, cap='Camera Cloud File', okc='Ok')
		if camCloudPath:
			mc.textField('camCloud', tx=camCloudPath[0], e=True)
	
	    
	#checking for files to run functions
	def getClouds(self):
		pCloudPath = mc.textField('pCloud', tx=True, q=True)
		camCloudPath = mc.textField('camCloud', tx=True, q=True)
		pCloudGroup, camGroup = '', ''
		
		if os.path.isfile(pCloudPath):
			pCloudGroup = self.getPCloud(pCloudPath)
		else:
			print 'Could not find the specified point cloud file'
		    
		if os.path.isfile(camCloudPath):
			camGroup = self.getCamCloud(camCloudPath)
		else:
			print 'Could not find the specified camera cloud file'
		
		#pareting cameras under point cloud group
		if pCloudGroup and camGroup:
			mc.parent(camGroup, pCloudGroup)
		
		#mc.button('cloudMe', l= 'Cloud Me', e=True)
		    
	
	#getting point cloud
	def getPCloud(self, pCloudPath):
		fileName = os.path.split(pCloudPath)
		fileName = fileName[-1].split('.')[0]
		pointCloudFile = open(pCloudPath, 'r')
		pointCloud = pointCloudFile.readlines()
		pCloudGroup = mc.group(n='%s_pointCloud_GRP' % fileName, em=True)

		try:
			pX,pY,pZ,pR,pG,pB = pointCloud[0].split(' ')
		except:
			print 'Bad point cloud file format'
			return

		pCloudParticle = mc.particle(n='pCloud_%s' % fileName)
		mel.eval('addAttr -ln "rgbPP" -dt vectorArray %s' % pCloudParticle[1])
		mel.eval('addAttr -ln "rgbPP0" -dt vectorArray %s' % pCloudParticle[1])

		for point in pointCloud:
			if '\n' in point:
				point.replace('\n', '')
			pX,pY,pZ,pR,pG,pB = point.split(' ')
			pR, pG, pB = float(pR)/255.0, float(pG)/255.0, float(pB)/255.0
			mel.eval('emit -o %s -at "rgbPP" -pos %s %s %s -vv %s %s %s' % (pCloudParticle[0], pX, pY, pZ, pR, pG, pB))

		mc.saveInitialState(pCloudParticle[0])
		mc.setAttr('%s.isDynamic' % pCloudParticle[1], 0)
		mc.parent(pCloudParticle, pCloudGroup)
		
		return pCloudGroup
	
	
	#getting camera cloud
	def getCamCloud(self, camCloudPath):
		fileName = os.path.split(camCloudPath)
		fileName = fileName[-1].split('.')[0]
		cameraCloudFile = open(camCloudPath, 'r')
		cameraLs= cameraCloudFile.readlines()
		cameraCloudFile.close()
		camGroup = mc.group(n='%s_cameraCloud_GRP' % fileName, em=True)

		try:
			ln, cTx, cTy, cTz, cRx, cRy, cRz, focal = cameraLs[0].split('\t')
		except:
			print 'Bad camera file format'
			return

		for camera_ in cameraLs:
			if '\n' in camera_:
				camera_.replace('\n', '')
			ln, cTx, cTy, cTz, cRx, cRy, cRz, focal = camera_.split('\t')
			activeCam = mc.camera(n='camera0%s_%s' % (ln, fileName), fl=float(focal), p=(float(cTx), float(cTy), float(cTz)), rot=(float(cRx), float(cRy), float(cRz)))
			mc.parent(activeCam, camGroup)
		
		return camGroup


pointCloud().UI()
