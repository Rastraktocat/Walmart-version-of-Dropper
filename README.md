**Running msbuild\_script.py and linux_mint_script.py instructions**



\#1 Check the default file path for the DROPPER_OUTPUT macro in the cpp file



\#2 Confirm all the variables in the script_info library in the file (keep in mind that these may be modified by the input, output and some of the log flags).



\#3 Set the payload name in the .rc file (calc.exe for demonstration purposes). 



\#4 Set the out variable in the script_runners.sh file if you are compiling with that.



\#5 In your cmd line give the arguments you want for the msbuild_script.py or linux_mint_script.py script. Use the -h argument to see all possible arguments.



**Flags**



\--release 

\--debug 



These control what mode msbuild will run in. If both are set then msbuild will be made in release mode. If both are not set then the script will run in release mode.



\--architecture <architecture>



This controls whether msbuild builds x86 or x64 code. <architecture> can be either 86 or 64. If it isn't either of those then it will default to x64. 
In linux_mint_script.py this will change the program from x86_64-w64-mingw32-g++ to i686-w64-mingw32-g++. 



\--base64

\--default-xor

\--xor-key <key>

\--both-encoding



These control what encryption the payload receives. You can make the payload base64 itself with --base64. --default-xor uses a key value of 115 in decimal. You can set the xor key with --xor-key. To easily have both encryptions set use --both-encoding. If you have no encryption then no encryption is applied. 



\--hardcode


The --hardcode flag make it so that the script takes inputs from the script_info dictionary in the msbuild_script.py file. This makes it so that you don't have to add the file paths in manually. 




\--input <input\_path>

\--output <output\_path>


The --input flag allows you to bypass reading the file\_path from the script_info dictionary msbuild_script.py file. The --output flag allows you to bypass reading the file\_exe\_path from the script_info dictionary in the msbuild_script.py file. Selecting the --output flag only allows you to override using msbuild and just run <output_path>. 

linux_mint_script.py treats input and output swaps x86_64-w64-mingw32-g++ <input_path> -o <output_path> instead of the default path.


--log 

\--keep-log

\--log-number <number>

\--logging-output <logging\_output\_path>


In order for any logging to take place (in linux_mint_script.py) you need to put the --log flag. The default file location for the log is preserve_payload_contents.txt. It will be automatically made for you.

\--logging-output makes it so that the script appends the payload before it goes through encryption for both methods of encryption. If you run the script for the first time and have put no logging flags then no logging files will be made. Otherwise the default logging file is preserve_payload_contents.txt. 

You can stop the preserve file from being overwritten if you don't put the --logging-output on the next time you run the script. This will not write the new the details of the new run. If you run the script in a loop then you can use --keep-log in order to stop the logs from being deleted every time the script runs. and set the --log-number to differentiate which script had which output.



\--test-output



This flag causes the flags to print out all of the information regarding the running of the script to cmd line. 



Linux_mint_script.py Specific flags


--no-encode

--no-compile

--no-decode


These commands skip their respective portion of the script. For example putting --no-encode will skip the encoding portion of the script and only compile and decode.

There is no guarantee that the input you give will not break the python code (For example if you give "This is a file." as the input and only ask the script to decode it the script will give you a padding error). 

If --no-encode is chosen then logging will still occur for whichever encodings were run. 


Some examples are

py msbuild_script.py --release --architecture 64 --both-encoding --hardcode -log-number 1 --logging-output "preserve_original_payload.txt" --test-output

py msbuild_script.py  --debug --base64 --default-xor --hardcode --input FileSystem_exe_rebuild\FileSystem_exe_rebuild.vcxproj --log-number 1 --logging-output "preserve_original_payload.txt" --test-output

python3 linux_mint_script.py --release --both-encoding --hardcode --input FileSystem_exe_rebuild/FileSystem_exe_rebuild.cpp --output FileSystem_exe_rebuild/FileSystem_exe_rebuild.exe --log --log-number 3 --logging-output "preserve_original_payload.txt" --test-output

python3 linux_mint_script.py --release --base64 --hardcode --log --log-number 3 --logging-output "preserve_original_payload.txt" --test-output


**How the msbuild_script.py script works**



The script starts by getting the file paths from the user or the hardcoded file paths in the script. 



The script then resets the log payload resets the log payload file (even if the flag is not set) and then runs encryption according to the users selections.



Then the msbuild_script.py runs msbuild (unless the input flag is not set and the output flag is set) and then runs the exe that is made from that. 



The script then decodes the payload. 


**How the linux_mint_script.py script works**



The script starts by getting the file paths from the user or the hardcoded file paths in the script. 



The script then resets the log payload resets the log payload file (even if the flag is not set) and then runs encryption according to the users selections.



Then the linux_mint_script.py runs mingw without warnings and with the -fpermissive flag set.



The script then decodes the payload. 

