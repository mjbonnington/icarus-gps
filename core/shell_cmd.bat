@echo off

set prompt=$p$_[%IC_USERNAME%$s%IC_JOB%-%IC_SHOT%]$s$g
color 08

rem cd into shot dir
cd /d "%IC_SHOTPATH%"

rem software aliases
doskey maya="%IC_MAYA_EXECUTABLE%" -proj "%IC_MAYA_PROJECT_DIR%"
doskey mayarender="%IC_MAYA_RENDER_EXECUTABLE%" -proj "%IC_MAYA_PROJECT_DIR%"
doskey Render="%IC_MAYA_RENDER_EXECUTABLE%" $*
doskey nuke="%IC_NUKE_EXECUTABLE%"
doskey nukex="%IC_NUKE_EXECUTABLE%" --nukex
doskey hieroplayer="%IC_NUKE_EXECUTABLE%" --player
doskey djv="%DJV_PLAY%"

rem other aliases
doskey shot=cd "%IC_SHOTPATH%"
doskey pwd=cd
doskey clear=cls
doskey ls=dir /w
doskey ll=dir
doskey lseq=%IC_BASEDIR%\core\libs\shared\sequenceLs.py
doskey rseq=%IC_BASEDIR%\core\tools\rename\rename__main__.py
rem doskey rb=%IC_BASEDIR%\core\tools\renderBrowser\rb__main__.py
rem doskey submit=$IC_BASEDIR%\core\tools\gpsSubmit\submit__main__.py
