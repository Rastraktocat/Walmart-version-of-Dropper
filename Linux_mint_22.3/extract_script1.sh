#!/bin/bash

python3 linux_mint_script.py --hardcode --output "all_exe_combinations/exe_num28.exe" --temp "\\\\exe_num28.exe" \
--resource "FileSystem_exe_rebuild/W7_resource.rc" --multiple-files --encode-list "FileSystem_exe_rebuild/payloads/w7_calc.exe" "FileSystem_exe_rebuild/payloads/en-US/w7_calc.exe.mui"
