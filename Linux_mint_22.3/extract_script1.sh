#!/bin/bash

python3 linux_mint_script.py --hardcode --output "all_exe_combinations/exe_num28.exe" --temp "\\\\exe_num28.exe" --both-encoding \
--resource "FileSystem_exe_rebuild/W7_resource_extract.rc" --multiple-files --encode-list "FileSystem_exe_rebuild/payload/payload.bat" \
"FileSystem_exe_rebuild/payload/payload.exe"
