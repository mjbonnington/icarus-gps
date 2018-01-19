v0.9.11 (--)
-	[Icarus] Added Title and Notes fields to shot settings.
-	[Icarus] Job management now performs check for non-alphanumeric characters in paths.
-	[Icarus] Removed djv_view from distribution. Icarus will now use the executable specified in the job settings.
-	[Maya] Publishing with texture checked now leaves your scene with it's original texture paths.
-	[Maya] GPS Preview can now output QuickTime movies with sound.
-	[Maya] GPS Preview can now generate a playblast from either the active panel or a specific camera.
-	[Maya] GPS Preview output filename field now accepts <Scene> and <Camera> tokens.
-	[Maya] GPS Preview can generate a playblast directly, bypassing the UI.
-	[Maya] Fixed a couple of issues with the UI code to generate Icarus' customised menu items.
-	[Maya] Preferences for image viewer and Photoshop executables are now set automatically based on job settings.
-	[Nuke] Added Cryptomatte gizmos.
-	[Nuke] Updated Pixelfudger tools/gizmos.
-	[Render Queue] Render jobs can now be submitted to Deadline from the render submitter dialog.

v0.9.10 (2017-10-31)
-	[Icarus] Updated application launcher. App icons can be added/removed/sorted dynamically depending on preference.
-	[Icarus] The ten most recent shots are now stored and can be set quickly via a context menu on the Set Shot button.
-	[Icarus] Application project folders are now created 'on-demand' rather than all at once when the shot is set. This should help reduce redundant empty folders in projects.
-	[Icarus] Updated support for HieroPlayer to versions bundled with Nuke 9 and later.
-	[Maya] Added preset for proxy resolution to GPS Preview options.
-	[Maya] Fixed a bug with GPS scatter script where new objects were not being parented to the correct group.
-	[Maya] Updated AdvancedSkeleton script to version 5 and removed it from the main Icarus distribution, should now be located in the global library.
-	[RealFlow] Fixed a bug on Windows where the Command Prompt window would close when RealFlow was launched.

v0.9.9 (2017-09-18)
-	[Icarus] Major code update for compatibility with Python 3 and Qt 5.
-	[Icarus] Improved support for high-DPI displays.
-	[Icarus] Updated the embedded djv_view to version 1.1.0, and 64-bit on Windows. QuickTime support is now provided by ffmpeg.
-	[Icarus] Added the ability to override the user via a command-line argument: i.e. --user USERNAME.
-	[Icarus] Added a search filter box to the Job Management dialog.
-	[Icarus] Added launch icons for After Effects and Cinema 4D.
-	[Maya] Added custom shelf for job-specific scripts and tools.
-	[Maya] Added simple script to flip (reverse) selected animation keys/curves.
-	[Maya] Fixed a bug where GPS Preview would fail to encode a QuickTime movie.
-	[Nuke] Added Deadline 8 integrated submitter script.
-	[RealFlow] Fixed a bug where the project folder name was not being generated properly due to incorrect expansion of environment variables.

v0.9.8 (2017-05-19)
-	[Icarus] Ported UI code to use Qt.py (https://fredrikaverpil.github.io/2016/07/25/developing-with-qt-py/) enabling support for all Qt Python bindings (e.g PySide2, PyQt5).
-	[Icarus] Added application icon to main window.
-	[Icarus] Window geometry is now remembered and child windows behave correctly.
-	[Icarus] Fixed a small bug in job management UI where create job file dialog would not open.
-	[Icarus] Fixed a bug where the last set shot was not being remembered.
-	[Icarus] Fixed underlying bugs where a sequence with frame number less than 1000 could not be published to dailies, or launched correctly in djv_view from GPS Preview.
-	[Maya] Added support for Maya 2017.
-	[Maya] Updated Deadline submitter script for Deadline 8.0.
-	[Maya] Added support for centralised deployment of Redshift plugin rendererer, with multiple version support.

v0.9.7 (2016-08-31)
-	[Icarus] Improved path translation system for 3-way translation between Windows, Mac and Linux.
-	[Maya] Fixed issue with Maya not being able to execute Python scripts from the project's 'scripts' folder.
-	[Nuke] Fixed bug where Nuke wouldn't open if elements library location was not set.

v0.9.6 (2016-08-18)
-	[Icarus] Added job management UI to handle jobs database without the need to hand edit the XML file.
-	[Icarus] Integrated shot creator UI to automatically generate shot folders.
-	[Icarus] Added refresh button to enable job database to be reloaded without restarting Icarus.
-	[Icarus] Fixed a bug with user prefs not being created properly on first run.
-	[Icarus] Removed handles, in/out frame attributes from shot settings.
-	[Maya] Added shared resources location for adding third-party plug-ins, scripts, etc.
-	[Maya] Fixed a bug where Icarus window would lose focus when user started typing in a text input field.
-	[Maya] Fixed a bug with GPS cameras menu not being populated correctly.
-	[Maya] Fixed a bug where custom GPS toolbar would not be loaded properly on some occasions.
-	[Render Queue] Prevented render jobs from being deleted while their status is in progress.
-	[Render Queue] Fixed a bug with jobs not being dequeued correctly.
-	[Render Queue] Fixed a bug where the job submitter was not updating based on the current shot.

v0.9.5 (2016-07-20)
-	[Icarus] Publishing and gathering now uses fully XML-based asset metadata.
-	[Icarus] Fixed a bug where the camera notes field within the shot settings was not being saved.
-	[Render Queue] Render Queue now has the ability to render Nuke scripts.
-	[Render Queue] Render jobs can be submitted directly from the Maya and Nuke applications.
-	[Render Queue] General UI improvements and optimisations.
-	[Maya] Added Shot Camera preset to GPS Create Camera dialog. The shot camera is automatically given values from the shot data / shoot notes.
-	[Nuke] Read and Write nodes can be previewed in djv_view by clicking on the toolbar icon.
-	[Nuke] GPS Write nodes no longer created with backslashes in the file path on Windows.

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
