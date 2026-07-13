# Controls how many times the python file is run.
build_types=(release)
architecture=(86 64)
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
encode="FileSystem_exe_rebuild/calc1.exe"
i=0
print_log=""


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

				print_log+="---------------------Python file size Details----------------------\n"
					print_log+="input size: $(wc -c < $input)\n"
					print_log+="output size: $(wc -c < ${out}${i}.exe)\n"
					print_log+="resource size: $(wc -c <$resource)\n"
					print_log+="header size: $(wc -c < $header)\n"
					print_log+="encode size: $(wc -c <$encode)\n"

					python3 linux_mint_script.py --hardcode \
					"--$build" --architecture "$arch" \
					--xor-key "$a_idx" --base64 \
					--input "$input" --output "${out}${i}.exe" --resource "$resource" --header "$header" --encode "$encode" --temp "\\\\exe_num${i}.exe" \
					--log --log-number "$i" --keep-log

					print_log+="---------------------After Python file size Details----------------------\n"
					print_log+="input size: $(wc -c < $input)\n"
					print_log+="output size: $(wc -c < ${out}${i}.exe)\n"
					print_log+="resource size: $(wc -c <$resource)\n"
					print_log+="header size: $(wc -c < $header)\n"
					print_log+="encode size: $(wc -c <$encode)\n"

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
					print_log+="encode: $encode\n"

					print_log+="---------------------Python file size Details----------------------\n"
					print_log+="input size: $(wc -c < $input)\n"
					print_log+="output size: $(wc -c < ${out}${i}.exe)\n"
					print_log+="resource size: $(wc -c <$resource)\n"
					print_log+="header size: $(wc -c < $header)\n"
					print_log+="encode size: $(wc -c <$encode)\n"

					python3 linux_mint_script.py --hardcode \
					"--$build" --architecture "$arch" \
				        --xor-key "$a_idx" \
					--input "$input" --output "${out}${i}.exe" --resource "$resource" --header "$header" --encode "$encode" --temp "\\\\exe_num${i}.exe" \
					--log --log-number "$i" --keep-log

					print_log+="---------------------After Python file size Details----------------------\n"
					print_log+="input size: $(wc -c < $input)\n"
					print_log+="output size: $(wc -c < ${out}${i}.exe)\n"
					print_log+="resource size: $(wc -c <$resource)\n"
					print_log+="header size: $(wc -c < $header)\n"
					print_log+="encode size: $(wc -c <$encode)\n"

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
				print_log+="encode: $encode\n"

				print_log+="---------------------Python file size Details----------------------\n"
				print_log+="input size: $(wc -c < $input)\n"
				print_log+="output size: $(wc -c < ${out}${i}.exe)\n"
				print_log+="resource size: $(wc -c <$resource)\n"
				print_log+="header size: $(wc -c < $header)\n"
				print_log+="encode size: $(wc -c <$encode)\n"

				python3 linux_mint_script.py --hardcode \
				"--$build" --architecture "$arch" \
				--base64 \
				--input "$input" --output "${out}${i}.exe" --resource "$resource" --header "$header" --encode "$encode" --temp "\\\\exe_num${i}.exe"\
				--log --log-number "$i" --keep-log

				print_log+="---------------------After Python file size Details----------------------\n"
				print_log+="input size: $(wc -c < $input)\n"
				print_log+="output size: $(wc -c < ${out}${i}.exe)\n"
				print_log+="resource size: $(wc -c <$resource)\n"
				print_log+="header size: $(wc -c < $header)\n"
				print_log+="encode size: $(wc -c <$encode)\n"

				i=$((i + 1))
			fi

			print_log+="\n"
		done
	done
done

python3 linux_mint_script.py --debug --hardcode --xor-key 24 --base64 --encode "$encode" --temp "\\\exe_num14.exe" --output "all_exe_combinations/exe_num14.exe"
python3 linux_mint_script.py --debug --hardcode --xor-key 179 --base64 --encode "$encode" --temp "\\\exe_num15.exe" --output "all_exe_combinations/exe_num15.exe"
python3 linux_mint_script.py --debug --hardcode --xor-key 67 --base64 --encode "$encode" --temp "\\\exe_num16.exe" --output "all_exe_combinations/exe_num16.exe"

python3 linux_mint_script.py --debug --hardcode --xor-key 171 --encode "$encode" --temp "\\\exe_num17.exe" --output "all_exe_combinations/exe_num17.exe"
python3 linux_mint_script.py --debug --hardcode --xor-key 52 --encode "$encode" --temp "\\\exe_num18.exe" --output "all_exe_combinations/exe_num18.exe"
python3 linux_mint_script.py --debug --hardcode --xor-key 128 --encode "$encode" --temp "\\\exe_num19.exe" --output "all_exe_combinations/exe_num19.exe"

python3 linux_mint_script.py --debug --hardcode --base64 --encode "$encode" --temp "\\\exe_num20.exe" --output "all_exe_combinations/exe_num20.exe"

python3 linux_mint_script.py --architecture 86 --debug --hardcode --xor-key 21 --base64 --encode "$encode" --temp "\\\exe_num21.exe" --output "all_exe_combinations/exe_num21.exe"
python3 linux_mint_script.py --architecture 86 --debug --hardcode --xor-key 37 --base64 --encode "$encode" --temp "\\\exe_num22.exe" --output "all_exe_combinations/exe_num22.exe"
python3 linux_mint_script.py --architecture 86 --debug --hardcode --xor-key 253 --base64 --encode "$encode" --temp "\\\exe_num23.exe" --output "all_exe_combinations/exe_num23.exe"

python3 linux_mint_script.py --architecture 86 --debug --hardcode --xor-key 223 --encode "$encode" --temp "\\\exe_num24.exe" --output "all_exe_combinations/exe_num24.exe"
python3 linux_mint_script.py --architecture 86 --debug --hardcode --xor-key 30 --encode "$encode" --temp "\\\exe_num25.exe" --output "all_exe_combinations/exe_num25.exe"
python3 linux_mint_script.py --architecture 86 --debug --hardcode --xor-key 149 --encode "$encode" --temp "\\\exe_num26.exe" --output "all_exe_combinations/exe_num26.exe"

python3 linux_mint_script.py --architecture 86 --debug --hardcode --base64 --encode "$encode" --temp "\\\exe_num27.exe" --output "all_exe_combinations/exe_num27.exe"

printf "$print_log">log_file.txt
