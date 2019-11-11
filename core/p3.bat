@echo off

rem 32-bit...
rem for %%A in ("%USERPROFILE%\AppData\Local\Programs\Python\Python36-32\python.exe" "C:\Program Files (x86)\Python36-32\python.exe") do if exist %%A %%A %* && exit /b

rem 64-bit...
for %%A in ("%USERPROFILE%\AppData\Local\Programs\Python\Python36\python.exe" "C:\Program Files\Python36\python.exe") do if exist %%A %%A %* && exit /b
