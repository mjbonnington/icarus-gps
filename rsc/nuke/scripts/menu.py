#!/usr/bin/python

# [Icarus] menu.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Customises Nuke's menus and toolbars.


# Initialise Icarus
from core import icarus
session.icarus = icarus.app(app='nuke')

# Initialise Scene Manager
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

# Detect if running app is Nuke or NukeX
if nuke.env['nukex']:
	nuke_flags = "--nukex"
else:
	nuke_flags = None

# Get vendor name and initials
if os.environ['IC_VENDOR_INITIALS']:
	vendor = os.environ['IC_VENDOR_INITIALS'] + " "
else:
	vendor = ""

# Get job and shot
job = os.environ['IC_JOB']
shot = os.environ['IC_SHOT']
shotInfoStr = job + " - " + shot

# ----------------------------------------------------------------------------
# Command strings

readNode = 'import gpsNodes; gpsNodes.read_create()'
writeNode = 'import gpsNodes; gpsNodes.write_create()'
launchNuke = 'from shared import launchApps; launchApps.launch("Nuke", executable="%s", flags=%s)' % (os.environ['IC_NUKE_EXECUTABLE'], nuke_flags)
clearScript = 'session.scnmgr.file_new()'
newScript = clearScript # launchNuke | clearScript - change the way Nuke deals with a new script
openScript = 'session.scnmgr.file_open_dialog()'
saveScript = 'session.scnmgr.file_save()'
saveScriptAs = 'session.scnmgr.file_save_dialog()'
incrementAndSave = 'session.scnmgr.file_save_new_version()'
browseScriptsDir = 'from shared import openDirs; openDirs.openNukeScripts()'
browseRendersDir = 'from shared import openDirs; openDirs.openNukeRenders()'
browseElementsDir = 'from shared import openDirs; openDirs.openNukeElements()'
browseShotDir = 'from shared import openDirs; openDirs.openShot()'
browseJobDir = 'from shared import openDirs; openDirs.openJob()'
browseElementsLibDir = 'from shared import openDirs; openDirs.openElementsLib()'
launchProdBoard  = 'from shared import launchApps; launchApps.prodBoard()'
launchIcarus = 'session.icarus.show()'
shotInfo = 'from shared import shot_info; shot_info.show()'
launchDjv = 'import nukeOps; nukeOps.launchDjv()'
launchHieroPlayer = 'from shared import launchApps; launchApps.launch("HieroPlayer")'
versionUp = 'import switchVersion; switchVersion.versionUp()'
versionDown = 'import switchVersion; switchVersion.versionDown()'
versionLatest = 'import switchVersion; switchVersion.versionLatest()'
submitRender = 'import nukeOps; nukeOps.submitRender()'
#submitRenderSelected = 'import nukeOps; nukeOps.submitRenderSelected()'

# ----------------------------------------------------------------------------
# Customise menus

nukeMenu = nuke.menu('Nuke')  # Get Nuke's main menu
nodesMenu = nuke.menu('Nodes')  # Get Nuke's side menu

# Add custom items to nodes menu (toolbar on left-hand side)
gpsMenu_nodes = nodesMenu.addMenu(os.environ['IC_VENDOR_INITIALS'], icon='gps.png')
deflickerVelocity_cmd = gpsMenu_nodes.addCommand('Deflicker Velocity', "nuke.createNode('deflickerVelocity')", icon='newScript.png')

# ----------------------------------------------------------------------------

# Custom menu
icCustomMenu = nukeMenu.addMenu(vendor, index=6)

icShotInfoMenuItem = icCustomMenu.addCommand(shotInfoStr, shotInfo)

icCustomMenu.addSeparator()

icIcarusMenuItem = icCustomMenu.addCommand('Icarus...', launchIcarus, icon='icarus.png')

icCustomMenu.addSeparator()

icReviewMenuItem = icCustomMenu.addCommand('Review', launchDjv, icon='review.png')
icProductionBoardMenuItem = icCustomMenu.addCommand('Production board', launchProdBoard, icon='productionBoard.png')
icBrowseDirsMenu = icCustomMenu.addMenu('Browse project folders', icon='browse.png')
icBrowseDirsMenu.addCommand('Scripts', browseScriptsDir, icon='browse.png')
icBrowseDirsMenu.addCommand('Renders', browseRendersDir, icon='browse.png')
icBrowseDirsMenu.addCommand('Elements', browseElementsDir, icon='browse.png')
icBrowseDirsMenu.addCommand('Elements Library', browseElementsLibDir, icon='browse.png')
icBrowseDirsMenu.addSeparator()
icBrowseDirsMenu.addCommand('Shot - '+shot, browseShotDir, icon='browse.png')
icBrowseDirsMenu.addCommand('Job - '+job, browseJobDir, icon='browse.png')

icCustomMenu.addSeparator()

# icPublishMenuItem = icCustomMenu.addCommand('Publish...', publish, icon='publish.png')
# icGatherMenuItem = icCustomMenu.addCommand('Gather...', gather, icon='gather.png')
# icAssetManagerMenuItem = icCustomMenu.addCommand('Asset Manager...', assetManager, icon='assets.png')

# icCustomMenu.addSeparator()

icCustomMenu.addCommand(vendor+'Submit Render...', submitRender, icon='submitRender.png')

icSwitchVersionMenu = icCustomMenu.addMenu('Switch Version', icon='versionSwitch.png')
icSwitchVersionMenu.addCommand('Version to Latest', versionLatest, icon='versionLatest.png')
icSwitchVersionMenu.addCommand('Version Up', versionUp, icon='versionUp.png')
icSwitchVersionMenu.addCommand('Version Down', versionDown, icon='versionDown.png')

# ----------------------------------------------------------------------------

# Image menu
imageMenu = nodesMenu.menu('Image')
imageMenu.addCommand(vendor+'Read', readNode, icon='newScript.png', index=0)
#imageMenu.addCommand(vendor+'Read', readNode, 'r', icon='newScript.png', index=0)
#imageMenu.addCommand(vendor+'Write', writeNode, icon='newScript.png', index=1)
imageMenu.addCommand(vendor+'Write', writeNode, 'w', icon='newScript.png', index=1)

# ----------------------------------------------------------------------------

# Render menu
imageMenu = nukeMenu.menu('Render')
imageMenu.addCommand(vendor+'Submit Render...', submitRender, icon='submitRender.png', index=4)
#imageMenu.addCommand(vendor+'Submit Render (selected write node only)...', submitRenderSelected, icon='submitRender.png', index=5)

# ----------------------------------------------------------------------------

# Add custom file menu items
fileMenu = nukeMenu.menu('File')

icNewMenuItem = fileMenu.addCommand(vendor+'New', newScript, '^n', icon='new.png', index=0)
icOpenMenuItem = fileMenu.addCommand(vendor+'Open...', openScript, '^o', icon='open.png', index=1)
icOpenRecentMenu = fileMenu.addMenu(vendor+'Open Recent', icon='open.png', index=2)

fileMenu.addSeparator(index=3)

icSaveMenuItem =  fileMenu.addCommand(vendor+'Save', saveScript, '^s', icon='save.png', index=4)
icSaveAsMenuItem =  fileMenu.addCommand(vendor+'Save As...', saveScriptAs, '^shift+s', icon='saveAs.png', index=5)
icIncrementAndSaveMenuItem =  fileMenu.addCommand(vendor+'Increment and Save', incrementAndSave, 'alt+shift+s', icon='saveIncremental.png', index=6)

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

# Initialise recent files menu
session.scnmgr.update_recents_menu(icOpenRecentMenu)

# Add callback function to add script to recent files on script load
# nuke.addOnScriptLoad(session.scnmgr.update_recent_files)
