v0.9.4 (2016-05-27)
-	[Icarus] Added distributed render queue system. This UI is intended to replace the command-line submitter and provide a simple queuing system for Maya renders.
-	[Icarus] Status bar messages are displayed for a variable duration dependent on message length.
-	[Icarus] Implemented check for Python version at startup - Icarus requires at least version 2.7.
-	[Maya] Improved V-Ray rendering tools shelf and icons.
-	[Maya] Added support for Maya 2016 Extension 2.

v0.9.3 (2016-05-10)
-	[Icarus] Added status bar to main Icarus window to display errors, warnings and info messages.
-	[Icarus] Added Notes field to job settings.
-	[Icarus] Added 'In/Out Frame' attributes to job/shot time settings. This is intended to replace the 'Handles' value, although functionality is not yet implemented.
-	[Maya] Added MEL script for import/export of PFTrack survey points.
-	[Maya] Enabled by default the Redshift setting 'Abort Rendering on License Failure'. Render farm nodes that cannot check out a license will fail rather than render a watermarked image.
-	[Maya] Improved behaviour of 'Load Base Settings' function with Redshift so that the RedshiftOptions node is created correctly before attempting to set any attributes.

v0.9.2 (2016-04-08)
-	[Maya] Playblasting using GPS Preview no longer screws up the HUD.
-	[Maya] Fixed bug causing an error when gathering published cameras into Maya.

v0.9.1 (2016-04-07)
-	[Maya] Fixed a bug with node publishing not creating the correct folder names.
-	[Maya] Fixed a bug with GPS Preview not working if HUD guides are turned off.

v0.9.0 (2016-04-06)
-	[Icarus] Removed 'approved' publish option.
-	[Icarus] Published asset metadata now written out as XML files. Python source is still written out alongside as the gather code still uses it.
-	[Icarus] Added metadata tag to published assets to keep track of the asset's source.
-	[Icarus] Added Render Browser UI, enables quick checking of image sequences, render layers, passes/AOVs.
-	[Icarus] Added a check that the app path environment variable is set before attempting to launch an app.
-	[Icarus] Job Management UI deals with missing jobs / shots in a more elegant way.
-	[Icarus] Added sequence renaming tool.
-	[Icarus] Resolution settings values are now remembered and stored correctly when edited in the settings dialog.
-	[Maya/Nuke] Improved publish tab layout with icons.
-	[Maya] Save operations now print confirmation message.
-	[Maya] Added dockable Outliner panel.
-	[Maya] Added Redshift icon and tools to GPS Lighting shelf.
-	[Maya] Improved behaviour when loading base render settings.
-	[Maya] Added additional command-line arguments field for local batch render submitter.
-	[Maya] Improved 'Randomise Vertices' script, now works with lattice points and NURBS CVs as well as polygon vertices.

v0.8.16 (2015-12-17)
-	[Maya] Added Redshift support.
-	[Maya] Updated Render View AOV script to behave better with Maya 2016 Color Management.

v0.8.15 (2015-12-07)
-	[Maya] GPS Preview now uses scene name by default.

v0.8.14 (2015-12-04)
-	[Maya] Changed V-Ray subdivision and displacement default settings.
-	[Maya] Plugin loader no longer uses absolute MacOS paths.
-	[Nuke] Removed 'R' key override in Nuke, so that red channel keyboard shortcut works again.

v0.8.13 (2015-11-03)
-	[Icarus] Removed redundant umask command from app launch function.
-	[Icarus] Fixed bug where djv_view wouldn't launch on Windows.
-	[Icarus] Shot 'Plate' directories are be created automatically based on resolution values in shot settings.
-	[Maya] Adding V-Ray utility render elements no longer sets EXR to 32 bits per pixel.

v0.8.12 (2015-10-30)
