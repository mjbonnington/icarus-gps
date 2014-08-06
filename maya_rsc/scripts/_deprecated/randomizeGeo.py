import maya.cmds as mc
import random

class randGeo():
	
	def __init__(self):

		self.winTitle = 'GPS - Geo Randomize'
		self.winName = 'geoRandomize'
	
				
	##ui##
	def UI(self):			
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)
		
		mc.window(self.winName, title=self.winTitle, s=False, w=450, h=350)
		mc.setParent(self.winName)
		self.mainCol = mc.columnLayout(adjustableColumn=False)
		
				
		mc.rowLayout(nc=1)
		mc.separator(style='none',h=10,w=450)
		mc.setParent('..')
		
		mc.rowLayout(nc=3)
		mc.floatSliderGrp('factorSlider',
		l='Random Factor', 
		value=0, 
		field=True, 
		precision=3, 
		minValue=0, 
		maxValue=1, 
		fieldMinValue=0, 
		fieldMaxValue=100000)
		mc.setParent('..')
		
		mc.rowLayout(nc=3)
		mc.separator(style='in',h=20,w=450)
		mc.setParent('..')
		
		mc.rowLayout(nc=4)
		mc.separator(style='none',h=20,w=175)
		mc.button(l= 'Randomize', h=30, w=122, c='randomizeGeo.randGeo().randomize()')
		mc.setParent('..')
		
		mc.rowLayout(nc=1)
		mc.separator(style='none', h=10,w=450)
		mc.setParent('..')
		mc.setParent('..')
		mc.showWindow( self.winName )
	###end ui###
	
	def randomize(self):
		factor = mc.floatSliderGrp('factorSlider', v=True, q=True)
		vtxLsGrp = mc.ls(sl=True)
		selVtxLs = []
		try:
			for vtxLs in vtxLsGrp:
				obj = vtxLs.partition('.vtx')[0]
				vtxLs = vtxLs.partition('[')[2]
				vtxLs = vtxLs.rpartition(']')[0]
				vtxLs = vtxLs.partition(':')
				vtxLs = list(vtxLs)
				while ':' in vtxLs:
					vtxLs.remove(':')
				while '' in vtxLs:
					vtxLs.remove('')
				if len(vtxLs)>1:
					for vtx in range(int(vtxLs[0]),int(vtxLs[1])+1):
						selVtxLs.append(vtx)
				else:
					selVtxLs.append(vtxLs[0])

			#getting current vertices position and setting new position
			for selVtx in selVtxLs:
				selVtxPosLs = mc.xform('%s.vtx[%s]' % (obj, selVtx), q=True, t=True, ws=True)
				#set postion x
				randValue = random.uniform(-1, 1)
				randValue = randValue * factor
				selVtxPosLs[0] += randValue
				#set position y
				randValue = random.uniform(-1, 1)
				randValue = randValue * factor
				selVtxPosLs[1] += randValue
				#set position z
				randValue = random.uniform(-1, 1)
				randValue = randValue * factor
				selVtxPosLs[2] += randValue
				mc.xform('%s.vtx[%s]' % (obj, selVtx), t=selVtxPosLs, ws=True)
		except (ValueError, IndexError):
			print 'Geo randomize currently only supports vertices'
			return
