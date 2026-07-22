@echo off

copy "C:\Windows\System32\calc.exe" "%USERPROFILE%\Downloads"

cd %USERPROFILE%\Downloads

git clone https://github.com/Rastraktocat/Walmart-version-of-Dropper.git

cd "%USERPROFILE%\Downloads\Walmart-version-of-Dropper\Linux_mint_22.3\FileSystem_exe_rebuild"

git add "calc.exe"

git commit -m "added calc.exe from cuckoo"

git push origin
