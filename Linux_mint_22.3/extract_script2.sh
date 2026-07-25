#!/bin/bash

python3 linux_mint_script.py --hardcode --output "all_exe_combinations/exe_num29.exe" --temp "\\\\exe_num29.exe" --both-encoding \
--resource "FileSystem_exe_rebuild/W11_resource.rc" --extract --multiple-files --encode-list "FileSystem_exe_rebuild/payload/payload.bat" \
"FileSystem_exe_rebuild/payload/w11_calc.exe"
