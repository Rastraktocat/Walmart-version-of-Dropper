**Running msbuild\_script.py instructions**



\#1 Set the file path of victim\_name that will have the payload injected into it in the c++ file. (calc.exe) for testing purposes. 



\#2 Confirm all the variables in the script_info library in the file msbuild_script.py file.



\#3 Set the payload name in the .rc file. 



\#4 In your cmd line give the arguments you want for the msbuild_script.py script. Use the -h argument to see all possible arguments.



**Flags**



\--release 

\--debug 



These control what mode msbuild will run in. If both are set then msbuild will be made in release mode. If both are not set then the script will run in release mode.



\--architecture <architecture>



This controls whether msbuild builds x86 or x64 code. <architecture> can be either 86 or 64. If it isn't either of those then it will default to x64. 



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


\--keep-log

\--log-number <number>

\--logging-output <logging\_output\_path>



\--logging-output makes it so that the script appends the payload before it goes through encryption for both methods of encryption. If you run the script for the first time and have put no logging flags then no logging files will be made. Otherwise they will be made. 
You can stop the preserve file from being overwritten if you don't put the --logging-output on the next time you run the script. This will not write the new the details of the new run. If you run the script in a loop then you can use --keep-log in order to stop the logs from being deleted every time the script runs. and set the --log-number to differentiate which script had which output.



\--test-output



This flag causes the flags to print out all of the information regarding the running of the script to cmd line. 


Some examples are

py msbuild_script.py --release --architecture 64 --both-encoding --hardcode -log-number 1 --logging-output "preserve_original_payload.txt" --test-output

py msbuild_script.py  --debug --base64 --default-xor --hardcode --input FileSystem_exe_rebuild\FileSystem_exe_rebuild.vcxproj --log-number 1 --logging-output "preserve_original_payload.txt" --test-output


**How the script works**



The script starts by getting the file paths from the user or the hardcoded file paths in the script. 



The script then resets the log payload resets the log payload file (even if the flag is not set) and then runs encryption according to the users selections.



Then the msbuild_script.py runs msbuild (unless the input flag is not set and the output flag is set) and then runs the exe that is made from that. 



The script then decodes the payload. 
