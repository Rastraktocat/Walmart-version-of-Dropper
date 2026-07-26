@echo off

cd /d "%USERPROFILE%\Downloads"

copy "C:\Windows\System32\calc.exe" "%USERPROFILE%\Downloads\"

ren "%USERPROFILE%\Downloads\calc.exe" "W11_calc.exe"