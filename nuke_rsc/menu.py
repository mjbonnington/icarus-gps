#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title		:menu
#copyright	:Gramercy Park Studios

#third party gizmos and plugins menu build
import pixelfudger

import gpsSave


#getting if running app is Nuke or Nukex
if nuke.env['nukex']:
	nukeType = 'nukex'
else:
	nukeType = 'nuke'


#command strings
readNode = 'import gpsNodes; gpsNodes.read_()'
writeNode = 'import gpsNodes; gpsNodes.write_()'
save = 'import gpsSave; gpsSave.save(incr=False)'
saveAs = 'import gpsSave; gpsSave.save(saveAs=True)'
incrSave = 'import gpsSave; gpsSave.save(incr=True)'
openScript = 'nuke.scriptOpen(\"%s/\")' % os.environ["NUKESCRIPTSDIR"]
openScriptsDir = 'import openDirs; openDirs.openNukeScripts()'
openRendersDir = 'import openDirs; openDirs.openNukeRenders()'
openElementsDir = 'import openDirs; openDirs.openNukeElements()'
openShotDir = 'import openDirs; openDirs.openShot()'
openJobDir = 'import openDirs; openDirs.openJob()'
launchProdBoard  = 'import launchApps; launchApps.prodBoard()'
launchNuke = 'import launchApps; launchApps.nuke("%s")' % nukeType
launchIcarus = 'reload(icarus__main__)'
versionUp = 'import switchVersion; switchVersion.versionUp()'
versionDown = 'import switchVersion; switchVersion.versionDown()'
versionLatest = 'import switchVersion; switchVersion.versionLatest()'


#NUKE MENU
nukeMenu = nuke.menu('Nuke')
gpsMenu = nukeMenu.addMenu('GPS', index=6)


#NODES MENU
nodesMenu = nuke.menu('Nodes')


#GPS NODES MENU
#gps
gpsMenu_nodes = nodesMenu.addMenu('GPS', icon='gps.png')
deflickerVelocity_cmd = gpsMenu_nodes.addCommand('Deflicker Velocity', "nuke.createNode('deflickerVelocity')", icon='newScript.png')
#separator
nodesMenu.addSeparator()
#new
newMenu_nodes = nodesMenu.addCommand('GPS - New', launchNuke, '^n', icon='newScript.png')
#open
openMenu_nodes = nodesMenu.addCommand('GPS - Open', openScript, '^o', icon='openScript.png')
#save
incrementalSaveMenu_nodes =  nodesMenu.addCommand('GPS - Incremental Save', incrSave, 'alt+shift+s', icon='incrementalSave.png')
saveMenu_nodes =  nodesMenu.addCommand('GPS - Save', save, '^s', icon='saveScript.png')
#switch version
switchVersionMenu = nodesMenu.addMenu('Switch Version', icon='switchVersion.png')
versionLatestMenu_nodes = switchVersionMenu.addCommand('GPS - Version To Latest', versionLatest, 'alt+shift+up', icon='versionLatest.png')
versionUpMenu_nodes = switchVersionMenu.addCommand('GPS - Version Up', versionUp, 'alt+up', icon='versionUp.png')
versionDownMenu_nodes = switchVersionMenu.addCommand('GPS - Version Down', versionDown, 'alt+down', icon='versionDown.png')
#icarusUI
icarusMenu_nodes = nodesMenu.addCommand('Icarus UI', launchIcarus, icon='icarus.png')
#trello
trelloMenu_nodes = nodesMenu.addCommand('Production Board', launchProdBoard, icon='productionBoard.png')
#browse
browseMenu_nodes = nodesMenu.addMenu('Browse', icon='browse.png')
browseMenu_nodes.addCommand('Browse Scripts', openScriptsDir)
browseMenu_nodes.addCommand('Browse Renders', openRendersDir)
browseMenu_nodes.addCommand('Browse Elements', openElementsDir)
browseMenu_nodes.addCommand('Browse Shot', openShotDir)
browseMenu_nodes.addCommand('Browse Job', openJobDir)


#GPS MENU
#switch version
switchVersionMenu_gps = gpsMenu.addMenu('Switch Version')
versionUpMenu_gps = switchVersionMenu_gps.addCommand('GPS - Version Latest', versionLatest)
versionUpMenu_gps = switchVersionMenu_gps.addCommand('GPS - Version Up', versionUp)
versionUpMenu_gps = switchVersionMenu_gps.addCommand('GPS - Version Down', versionDown)
#separator
gpsMenu.addSeparator()
#icarusUI
icarusMenu_gps = gpsMenu.addCommand('Icarus UI...', launchIcarus)
#separator
gpsMenu.addSeparator()
#trello
trelloMenu_gps = gpsMenu.addCommand('Production Board', launchProdBoard)
#separator
gpsMenu.addSeparator()
#browse
browseMenu_gps = gpsMenu.addMenu('Browse')
browseMenu_gps.addCommand('Browse Scripts', openScriptsDir)
browseMenu_gps.addCommand('Browse Renders', openRendersDir)
browseMenu_gps.addCommand('Browse Elements', openElementsDir)


#IMAGE MENU
imageMenu = nodesMenu.menu('Image')
imageMenu.addCommand('GPS - Read', readNode, 'r', icon='newScript.png', index=0)
imageMenu.addCommand('GPS - Write', writeNode, 'w', icon='newScript.png', index=1)


#FILE MENU
fileMenu = nukeMenu.menu('File')
#new
newMenu_gps = fileMenu.addCommand('GPS - New', launchNuke, '^n', index=0)
#open
openMenu_gps = fileMenu.addCommand('GPS - Open...', openScript, '^o', index=1)
#open recent
openRecentMenu_gps = fileMenu.addMenu('GPS - Open Recent', index=2)
#separator
fileMenu.addSeparator(index=3)
#save
saveMenu_gps =  fileMenu.addCommand('GPS - Save', save, '^s', index=4)
#save as
saveAsMenu_gps =  fileMenu.addCommand('GPS - Save As...', saveAs, '^shift+s', index=5)
#incremental save
saveIncrementalMenu_gps =  fileMenu.addCommand('GPS - Incremental Save', incrSave, 'alt+shift+s', index=6)
#separator
fileMenu.addSeparator(index=7)


#removing default menu items
fileMenu = nukeMenu.findItem('File')
fileMenu.removeItem('New')
fileMenu.removeItem('Open...')
fileMenu.removeItem('Save')
fileMenu.removeItem('Save As...')
fileMenu.removeItem('Save New Version')
fileMenu.removeItem('Recent Files')

#updated names for nuke 9 menus
fileMenu.removeItem('New Comp...')
fileMenu.removeItem('Open Comp...')
fileMenu.removeItem('Open Recent Comp')
fileMenu.removeItem('Close Comp')
fileMenu.removeItem('Save Comp')
fileMenu.removeItem('Save Comp As...')
fileMenu.removeItem('Save New Comp Version')


# Initialise recent files menu...
gpsSave.updateRecentFilesMenu(openRecentMenu_gps)


# Add callback function to add script to recent files on script load...
nuke.addOnScriptLoad( gpsSave.updateRecentFiles )
