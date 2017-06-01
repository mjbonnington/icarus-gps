#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@hogarthww.com
#title    :vCtrl


import os, string

def version(vCtrlFolder, current=False):

	#####################DETERMINES CURRENT VERSION BASED ON VC OR DIRECTORY CONTENTS######################
	#######################################################################################################
	
	##CHECKS FOR DIRECTORY EXISTENCE##
	if not os.path.isdir(vCtrlFolder):
		print("vCtrl: directory doesn't exist.")
		currentVersion = 0
	else:
		##TRIES TO FIGURE OUT VERSIONING BASED ON EXISTENT CONTENTS##
		try:
			vCtrlFileLs = os.listdir(vCtrlFolder)
			vrsLs = []
			##CHECKS ALL ITEMS OF vCtrlFolder CHECKS FOR v### PATTERN.##
			for vCtrlItem in vCtrlFileLs:
				##gets first item of split list if _ found to strip out 'approved' from version'
				contentVrs = vCtrlItem.split("_")[0]
				##IF FOUND STRIPS v
				if contentVrs.startswith("v"):
					contentVrs = string.replace(contentVrs, "v", "")
				elif contentVrs.startswith(".v"):
					contentVrs = string.replace(contentVrs, ".v", "")
				##CHECKS FOR NUMERIC AND ADDS IT TO vrsLs.
				if contentVrs.isdigit():
					vrsLs.append(contentVrs)
			##SORTS vrsLs AND RETRIEVES LAST ITEM (HIGHEST DIGIT)##
			vrsLs.sort()
		#	print(vrsLs)
			currentVersion = int(vrsLs[-1])
		
		##IF NO VERSIONING DETECTED IN CONTENTS STARTS NEW VERSIONING##
		except IndexError:
			currentVersion = 0
	
	
	########################################PADDING CONTROL AND VERSIONING INCREMENTING#########################
	############################################################################################################
	
	padding = "00"
	if current:
		newVersion = currentVersion
	else:
		newVersion = currentVersion + 1
	if newVersion > 9:
		padding = "0"
	
		
	#####################################################RETURN####################################################
	###############################################################################################################
	
	##APPEDING "v" AND PADDING TO VERSION##
	newVersion = "v%s%s" % (padding, newVersion)
	
	
	return newVersion
