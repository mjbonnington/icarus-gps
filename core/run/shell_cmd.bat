@echo off

set prompt=$p$_[%IC_USERNAME%$s%JOB%-%SHOT%]$s$g
color 08


rem cd into shot dir
cd /d "%SHOTPATH%"


rem software aliases
doskey maya="%MAYAVERSION%" -proj "%MAYADIR%"
doskey mayarender="%MAYARENDERVERSION%" -proj "%MAYADIR%"
doskey Render="%MAYARENDERVERSION%" $*
doskey nuke="%NUKEVERSION%"
doskey nukex="%NUKEVERSION%" --nukex
doskey mudbox="%MUDBOXVERSION%"
doskey mari="%MARIVERSION%"
doskey realflow="%REALFLOWVERSION%"
doskey djv="%DJV_PLAY%"

rem other aliases
doskey shot=cd "%SHOTPATH%"
doskey pwd=cd
doskey clear=cls
doskey ls=dir /w
doskey ll=dir
doskey lseq=%IC_BASEDIR%\core\libs\shared\sequenceLs.py
doskey rb=%IC_BASEDIR%\core\tools\renderBrowser\rb__main__.py -style fusion
doskey br=%IC_BASEDIR%\core\tools\renderBrowser\rename__main__.py -style fusion
doskey submit=$IC_BASEDIR%\core\tools\gpsSubmit\submit__main__.py -style fusion
