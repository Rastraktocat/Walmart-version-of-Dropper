@echo off

dir "C\Windows\System32\mscoree.dll"
if %ERRORLEVEL% == 0(
	cmd.exe "C:\Windows\System32\calc.exe"
)
