#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:menu
#copyright	:Gramercy Park Studios


#third party gizmos and plugins menu build
import pixelfudger
import J_Ops_menu

#commands
readNode = 'import gpsNodes; gpsNodes.read_()'
writeNode = 'import gpsNodes; gpsNodes.write_()'
save = 'import gpsSave; gpsSave.save(incr=False)'
saveAs = 'import gpsSave; gpsSave.save(saveAs=True)'
incrSave = 'import gpsSave; gpsSave.save(incr=True)'
openScript = 'nuke.scriptOpen("%s/" % os.environ["NUKESCRIPTSDIR"])'
openScriptsDir = 'import openDirs; openDirs.openNukeScripts()'
openRendersDir = 'import openDirs; openDirs.openNukeRenders()'
openElementsDir = 'import openDirs; openDirs.openNukeElements()'
openShotDir = 'import openDirs; openDirs.openShot()'
launchTrello  = 'import launchApps; launchApps.trello()'
launchNuke = 'import launchApps; launchApps.nuke()'
launchIcarus = 'os.environ["ICARUSENVAWARE"]="NUKE";import icarus__main__;reload(icarus__main__)'
versionUp = 'import switchVersion; switchVersion.versionUp()'
versionDown = 'import switchVersion; switchVersion.versionDown()'
versionLatest = 'import switchVersion; switchVersion.versionLatest()'

#NUKE MENU
nukeMenu = nuke.menu('Nuke')
gpsMenu = nukeMenu.addMenu('GPS', index=6)


#NODES MENU
nodesMenu = nuke.menu('Nodes')


#IMAGE MENU
imageMenu = nodesMenu.menu('Image')
imageMenu.addCommand('GPS - Read', readNode, 'r', icon='newScript.png', index=0)
imageMenu.addCommand('GPS - Write', writeNode, 'w', icon='newScript.png', index=1)

#FILE MENU
fileMenu = nukeMenu.menu('File')
#new
newMenu_gps = fileMenu.addCommand('GPS - New', launchNuke, '^n', index=0)
#open
openMenu_gps = fileMenu.addCommand('GPS - Open', openScript, '^o', index=1)
#save
saveMenu_gps =  fileMenu.addCommand('GPS - Save', save, '^s', index=2)
saveAsMenu_gps =  fileMenu.addCommand('GPS - Save As', saveAs, '^alt+s', index=3)
#separator
fileMenu.addSeparator()


#GPS NODES MENU
#separator
nodesMenu.addSeparator()
#new
newMenu_nodes = nodesMenu.addCommand('GPS - New', launchNuke, '^n', icon='newScript.png')
#open
openMenu_nodes = nodesMenu.addCommand('GPS - Open', openScript, '^o', icon='openScript.png')
#save
incrementalSaveMenu_nodes =  nodesMenu.addCommand('GPS - Incremental Save', incrSave, '^+s', icon='incrementalSave.png')
saveMenu_nodes =  nodesMenu.addCommand('GPS - Save', save, '^s', icon='saveScript.png')
#switch version
switchVersionMenu = nodesMenu.addMenu('Switch Version', icon='switchVersion.png')
versionLatestMenu_nodes = switchVersionMenu.addCommand('GPS - Version To Latest', versionLatest, 'alt+shift+up', icon='versionLatest.png')
versionUpMenu_nodes = switchVersionMenu.addCommand('GPS - Version Up', versionUp, 'alt+up', icon='versionUp.png')
versionDownMenu_nodes = switchVersionMenu.addCommand('GPS - Version Down', versionDown, 'alt+down', icon='versionDown.png')
#icarusUI
icarusMenu_nodes = nodesMenu.addCommand('IcarusUI', launchIcarus, icon='icarus.png')
#trello
trelloMenu_nodes = nodesMenu.addCommand('Trello', launchTrello, icon='trello.png')
#browse
browseMenu_nodes = nodesMenu.addMenu('Browse', icon='browse.png')
browseMenu_nodes.addCommand('Browse Scripts', openScriptsDir)
browseMenu_nodes.addCommand('Browse Renders', openRendersDir)
browseMenu_nodes.addCommand('Browse Elements', openElementsDir)
browseMenu_nodes.addCommand('Browse Shot', openShotDir)


#GPS MENU
#switch version
switchVersionMenu_gps = gpsMenu.addMenu('Switch Version')
versionUpMenu_gps = switchVersionMenu_gps.addCommand('GPS - Version Latest', versionLatest)
versionUpMenu_gps = switchVersionMenu_gps.addCommand('GPS - Version Up', versionUp)
versionUpMenu_gps = switchVersionMenu_gps.addCommand('GPS - Version Down', versionDown)
#separator
gpsMenu.addSeparator()
#icarusUI
icarusMenu_gps = gpsMenu.addCommand('IcarusUI', launchIcarus)
#separator
gpsMenu.addSeparator()
#trello
trelloMenu_gps = gpsMenu.addCommand('Trello', launchTrello)
#separator
gpsMenu.addSeparator()
#browse
browseMenu_gps = gpsMenu.addMenu('Browse')
browseMenu_gps.addCommand('Browse Scripts', openScriptsDir)
browseMenu_gps.addCommand('Browse Renders', openRendersDir)
browseMenu_gps.addCommand('Browse Elements', openElementsDir)


#removing default menu items
fileMenu = nukeMenu.findItem('File')
fileMenu.removeItem('New')
fileMenu.removeItem('Open...')
fileMenu.removeItem('Save')
fileMenu.removeItem('Save As...')
fileMenu.removeItem('Save New Version')
fileMenu.removeItem('Recent Files')