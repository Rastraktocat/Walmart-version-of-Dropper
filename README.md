**Running msbuild\_script.py instructions**



\#1 Set the file path of victim\_name that will have the payload injected into it in the c++ file. (calc.exe) for testing purposes. 



\#2 Set all the variables in the script\_paths.txt file.



\#3 Set the payload name in the .rc file. 



\#4 In your cmd line give the arguments you want for the python script. Use the -h argument to see all possible arguments.



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

\--binary <binary\_path>



The --hardcode flag make it so that the script takes inputs from the script\_paths.txt. This makes it so that you don't have to add the file paths in manually. The --binary flag allows you to override the flag\_exe\_path in the script\_paths.txt and 

skips running msbuild compilation.



\--log-number <number>

\--logging-output <logging\_output\_path>



\--logging-output makes it so that the script appends the payload before it goes through encryption for both methods of encryption. If you run the script in a loop then you can set the --log-number to differentiate which script had which output.



\--test-output



This flag causes the flags to print out all of the information regarding the running of the script to cmd line. 



**How the script works**



The script starts by getting the file paths from the user or the hardcoded file. 



The script then resets the log payload resets the log payload file (even if the flag is not set) and then runs encryption according to the users selections.



Then script runs msbuild (unless the binary flag is set) and then runs the exe that is made from that. 



The script then decodes the payload. 









