@echo off

copy "%SYSTEMROOT%\System32\calc.exe" "%USERPROFILE%\Downloads\"

ren "%USERPROFILE%\Downloads\calc.exe" "w11_calc.exe"

echo "Shell payload ran."
