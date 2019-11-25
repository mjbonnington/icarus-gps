#!/usr/bin/python

# [GPS] menu.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Customises Nuke's menus and toolbars.


# import gpsSave

# Initialise Icarus
from core import icarus
session.icarus = icarus.app(app='nuke')

# Initialise Scene Manager
# from tools.scenemanager import scenemanager_nuke
# session.scnmgr = scenemanager_nuke.SceneManager()
from tools.scenemanager import scenemanager
session.scnmgr = scenemanager.create(app='nuke')
session.scnmgr.set_defaults()

# ----------------------------------------------------------------------------
# Third-party gizmos and plugins

# Cryptomatte
import cryptomatte_utilities
cryptomatte_utilities.setup_cryptomatte_ui()

# Pixelfudger
import pixelfudger

# Deadline integrated submitter
# import DeadlineNukeClient
# menubar = nuke.menu("Nuke")
# tbmenu = menubar.addMenu("&Thinkbox")
# tbmenu.addCommand("Submit Nuke To Deadline", DeadlineNukeClient.main, "")

# ----------------------------------------------------------------------------

if os.environ['IC_VENDOR_INITIALS']:
	vendor = os.environ['IC_VENDOR_INITIALS'] + " "
else:
	vendor = ""

# Detect if running app is Nuke or NukeX
if nuke.env['nukex']:
	nukeType = 'NukeX'
else:
	nukeType = 'Nuke'


# Command strings
readNode = 'import gpsNodes; gpsNodes.read_create()'
writeNode = 'import gpsNodes; gpsNodes.write_create()'
# save = 'import gpsSave; gpsSave.save(incr=False)'
save = 'session.scnmgr.file_save()'
# saveAs = 'import gpsSave; gpsSave.save(saveAs=True)'
saveAs = 'from tools.scenemanager import file_save; file_save.run_nuke(session.scnmgr)'
# incrSave = 'import gpsSave; gpsSave.save(incr=True)'
incrSave = 'session.scnmgr.file_save_new_version()'
# openScript = 'nuke.scriptOpen(\"%s/.\")' % os.environ["NUKESCRIPTSDIR"].replace('\\', '/')
openScript = 'from tools.scenemanager import file_open; file_open.run_nuke(session.scnmgr)'
openScriptsDir = 'from shared import openDirs; openDirs.openNukeScripts()'
openRendersDir = 'from shared import openDirs; openDirs.openNukeRenders()'
openElementsDir = 'from shared import openDirs; openDirs.openNukeElements()'
openShotDir = 'from shared import openDirs; openDirs.openShot()'
openJobDir = 'from shared import openDirs; openDirs.openJob()'
openElementsLibDir = 'from shared import openDirs; openDirs.openElementsLib()'
launchProdBoard  = 'from shared import launchApps; launchApps.prodBoard()'
launchNuke = 'from shared import launchApps; launchApps.launch("%s")' % nukeType
newScript = 'session.scnmgr.file_new()'
# launchIcarus = 'import icarus__main__; icarus__main__.run_nuke()'
launchIcarus = 'session.icarus.show()'
launchDjv = 'import nukeOps; nukeOps.launchDjv()'
launchHieroPlayer = 'from shared import launchApps; launchApps.launch("HieroPlayer")'
versionUp = 'import switchVersion; switchVersion.versionUp()'
versionDown = 'import switchVersion; switchVersion.versionDown()'
versionLatest = 'import switchVersion; switchVersion.versionLatest()'
submitRender = 'import nukeOps; nukeOps.submitRender()'
#submitRenderSelected = 'import nukeOps; nukeOps.submitRenderSelected()'


# NUKE MENU
nukeMenu = nuke.menu('Nuke')
gpsMenu = nukeMenu.addMenu(os.environ['IC_VENDOR_INITIALS'], index=6)


# NODES MENU
nodesMenu = nuke.menu('Nodes')


# GPS NODES MENU
# gps
gpsMenu_nodes = nodesMenu.addMenu(os.environ['IC_VENDOR_INITIALS'], icon='gps.png')
deflickerVelocity_cmd = gpsMenu_nodes.addCommand('Deflicker Velocity', "nuke.createNode('deflickerVelocity')", icon='newScript.png')
# separator
nodesMenu.addSeparator()
# new
newMenu_nodes = nodesMenu.addCommand('New', launchNuke, icon='new.png')
# open
openMenu_nodes = nodesMenu.addMenu('Open', icon='openPopup.png')
openMenu_nodes.addCommand('Open...', openScript, icon='open.png')
openRecentMenu_nodes = openMenu_nodes.addMenu('Open Recent', icon='open.png')
# save
saveMenu = nodesMenu.addMenu('Save', icon='savePopup.png')
saveMenu.addCommand('Save', save, icon='save.png')
saveMenu.addCommand('Save As...', saveAs, icon='saveAs.png')
saveMenu.addCommand('Incremental Save', incrSave, icon='saveIncremental.png')
# switch version
switchVersionMenu = nodesMenu.addMenu('Switch Version', icon='versionSwitchPopup.png')
switchVersionMenu.addCommand('Version to Latest', versionLatest, 'alt+shift+up', icon='versionLatest.png')
switchVersionMenu.addCommand('Version Up', versionUp, 'alt+up', icon='versionUp.png')
switchVersionMenu.addCommand('Version Down', versionDown, 'alt+down', icon='versionDown.png')
# submit render
#submitRenderMenu = nodesMenu.addMenu('Submit to Render Queue', icon='submitRenderPopup.png')
#submitRenderMenu.addCommand('Submit render job', submitRender, icon='submitRender.png')
#submitRenderMenu.addCommand('Submit render job (selected write node only)', submitRenderSelected, icon='submitRender.png')
nodesMenu.addCommand('Submit render job', submitRender, icon='submitRender.png')
# review
nodesMenu.addCommand('Review read or write node', launchDjv, icon='review.png')
# reviewMenu = nodesMenu.addMenu('Review', icon='reviewPopup.png')
# reviewMenu.addCommand('djv_view', launchDjv, icon='djv.png')
# reviewMenu.addCommand('HieroPlayer', launchHieroPlayer, icon='hieroPlayer.png')
# icarus ui
icarusMenu_nodes = nodesMenu.addCommand('Icarus UI', launchIcarus, icon='icarus.png')
# production board
productionBoardMenu_nodes = nodesMenu.addCommand('Production Board', launchProdBoard, icon='productionBoard.png')
# browse
browseMenu_nodes = nodesMenu.addMenu('Browse', icon='browsePopup.png')
browseMenu_nodes.addCommand('Browse Scripts', openScriptsDir, icon='browse.png')
browseMenu_nodes.addCommand('Browse Renders', openRendersDir, icon='browse.png')
browseMenu_nodes.addCommand('Browse Elements', openElementsDir, icon='browse.png')
browseMenu_nodes.addCommand('Browse Shot', openShotDir, icon='browse.png')
browseMenu_nodes.addCommand('Browse Job', openJobDir, icon='browse.png')
browseMenu_nodes.addCommand('Browse Elements Library', openElementsLibDir, icon='browse.png')


# GPS MENU
# switch version
switchVersionMenu_gps = gpsMenu.addMenu('Switch Version', icon='versionSwitch.png')
versionUpMenu_gps = switchVersionMenu_gps.addCommand('Version to Latest', versionLatest, icon='versionLatest.png')
versionUpMenu_gps = switchVersionMenu_gps.addCommand('Version Up', versionUp, icon='versionUp.png')
versionUpMenu_gps = switchVersionMenu_gps.addCommand('Version Down', versionDown, icon='versionDown.png')
# separator
gpsMenu.addSeparator()
# icarus ui
icarusMenu_gps = gpsMenu.addCommand('Icarus UI...', launchIcarus, icon='icarus.png')
# separator
gpsMenu.addSeparator()
# production board
productionBoardMenu_gps = gpsMenu.addCommand('Production Board', launchProdBoard, icon='productionBoard.png')
# separator
gpsMenu.addSeparator()
# browse
browseMenu_gps = gpsMenu.addMenu('Browse', icon='browse.png')
browseMenu_gps.addCommand('Browse Scripts', openScriptsDir, icon='browse.png')
browseMenu_gps.addCommand('Browse Renders', openRendersDir, icon='browse.png')
browseMenu_gps.addCommand('Browse Elements', openElementsDir, icon='browse.png')
browseMenu_gps.addCommand('Browse Shot', openShotDir, icon='browse.png')
browseMenu_gps.addCommand('Browse Job', openJobDir, icon='browse.png')
browseMenu_gps.addCommand('Browse Elements Library', openElementsLibDir, icon='browse.png')


# IMAGE MENU
imageMenu = nodesMenu.menu('Image')
imageMenu.addCommand(vendor+'Read', readNode, icon='newScript.png', index=0)
#imageMenu.addCommand(vendor+'Read', readNode, 'r', icon='newScript.png', index=0)
#imageMenu.addCommand(vendor+'Write', writeNode, icon='newScript.png', index=1)
imageMenu.addCommand(vendor+'Write', writeNode, 'w', icon='newScript.png', index=1)


# RENDER MENU
imageMenu = nukeMenu.menu('Render')
imageMenu.addCommand(vendor+'Submit render job...', submitRender, icon='submitRender.png', index=4)
#imageMenu.addCommand(vendor+'Submit render job (selected write node only)...', submitRenderSelected, icon='submitRender.png', index=5)


# FILE MENU
fileMenu = nukeMenu.menu('File')
# new
newMenu_gps = fileMenu.addCommand(vendor+'New', launchNuke, '^n', icon='new.png', index=0)
# open
openMenu_gps = fileMenu.addCommand(vendor+'Open...', openScript, '^o', icon='open.png', index=1)
# open recent
openRecentMenu_gps = fileMenu.addMenu(vendor+'Open Recent', icon='open.png', index=2)
# separator
fileMenu.addSeparator(index=3)
# save
saveMenu_gps =  fileMenu.addCommand(vendor+'Save', save, '^s', icon='save.png', index=4)
# save as
saveAsMenu_gps =  fileMenu.addCommand(vendor+'Save As...', saveAs, '^shift+s', icon='saveAs.png', index=5)
# incremental save
saveIncrementalMenu_gps =  fileMenu.addCommand(vendor+'Incremental Save', incrSave, 'alt+shift+s', icon='saveIncremental.png', index=6)
# separator
fileMenu.addSeparator(index=7)

# Remove default file menu items
# Nuke 8.x and earlier...
fileMenu = nukeMenu.findItem('File')
fileMenu.removeItem('New')
fileMenu.removeItem('Open...')
fileMenu.removeItem('Save')
fileMenu.removeItem('Save As...')
fileMenu.removeItem('Save New Version')
fileMenu.removeItem('Recent Files')

# Nuke 9.x onwards...
fileMenu.removeItem('New Comp...')
fileMenu.removeItem('Open Comp...')
fileMenu.removeItem('Open Recent Comp')
fileMenu.removeItem('Close Comp')
fileMenu.removeItem('Save Comp')
fileMenu.removeItem('Save Comp As...')
fileMenu.removeItem('Save New Comp Version')

# Initialise recent files menu...
# gpsSave.updateRecentFilesMenu(openRecentMenu_gps)
# gpsSave.updateRecentFilesMenu(openRecentMenu_nodes)
session.scnmgr.update_recents_menu(openRecentMenu_gps)
session.scnmgr.update_recents_menu(openRecentMenu_nodes)

# Add callback function to add script to recent files on script load...
# nuke.addOnScriptLoad(gpsSave.updateRecentFiles)
nuke.addOnScriptLoad(session.scnmgr.update_recent_files)
