@echo off

set prompt=$p$_[%USERNAME%$s%JOB%-%SHOT%]$s$g
color 08


rem cd into shot dir
cd /d %SHOTPATH%


rem software aliases
doskey maya="%MAYAVERSION%" -proj %SHOTPATH%\3D\maya
doskey mayarender="%MAYARENDERVERSION%" -proj %SHOTPATH%\3D\maya
doskey Render="%MAYARENDERVERSION%" -proj %SHOTPATH%\3D\maya
doskey nuke="%NUKEVERSION%"
doskey nukex="%NUKEVERSION%" --nukex
doskey mudbox="%MUDBOXVERSION%"
doskey mari="%MARIVERSION%"
doskey realflow="%REALFLOWVERSION%"
doskey djv="%DJV_PLAY%"

rem other aliases
doskey shot=cd %SHOTPATH%
doskey pwd=cd
doskey clear=cls
doskey ls=dir /w
doskey ll=dir
doskey lseq=%PIPELINE%\core\libs\shared\sequenceLs.py
doskey rb=%PIPELINE%\core\tools\renderBrowser\rb__main__.py -style fusion
doskey submit=$PIPELINE%\core\tools\gpsSubmit\submit__main__.py -style fusion
