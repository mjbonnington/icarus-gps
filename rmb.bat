@echo off

if "%~1"=="" (
	set src=.
) else (
	set src=%1
)

del /s %src%\*.pyc
for /d /r %src% %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
