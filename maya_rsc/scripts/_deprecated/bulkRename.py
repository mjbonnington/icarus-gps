import maya.cmds as mc, string

class bulkRename():
	
	def __init__(self, winName="gps_rename"):
		self.winTitle = "GPS - Rename"
		self.winName = "gpsRenameUI"
	
	#Creating UI
	def UI(self):
		
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)
		
		mc.window(self.winName, title=self.winTitle, s=False, mnb=False, mxb=False, w=400, h=350)
		mc.setParent(self.winName)
		self.mainCol = mc.columnLayout(adjustableColumn=False)
		
		mc.rowLayout(nc=1)
		mc.separator(style='none', h=2,w=260)
		mc.setParent('..')
		
		mc.rowLayout(nc=1)
		mc.text(l='   Old String  ')
		mc.setParent('..')
		mc.rowLayout(nc=2)
		mc.text(l='')
		mc.textField('old_string', h=35, w=247)
		mc.setParent('..')
		
		mc.rowLayout(nc=1)
		mc.text(l='   New String')
		mc.setParent('..')
		mc.rowLayout(nc=2)
		mc.text(l='')
		mc.textField('new_string',  h=35, w=247)
		mc.setParent('..')
		
		mc.rowLayout(nc=1)
		mc.separator(style='in', h=15,w=260)
		mc.setParent('..')
		
		mc.rowLayout(nc=3)
		mc.separator(style='none', w=70)
		mc.button(h=30,w=122, l= 'Rename', c='bulkRename.bulkRename().rename()')
		mc.setParent('..')
		
		mc.rowLayout(nc=1)
		mc.separator(style='none', h=5,w=260)
		mc.setParent('..')
		
		mc.showWindow(self.winName)
		
	#Executes renaming
	def rename(self):
		objLs = mc.ls(sl=True)
		oldString = mc.textField('old_string', tx=True, q=True)
		newString = mc.textField('new_string', tx=True, q=True)

		for obj in objLs:
			nameReplace = string.replace(str(obj), oldString, newString)
			mc.rename(obj, nameReplace)

