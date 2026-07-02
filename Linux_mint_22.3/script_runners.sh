build_types=(release debug)
architecture=(86 64)
encoding=(both xor base64)
arr=( $(shuf -i 0-255 -n 3) )
both_arr=( $(shuf -i 0-255 -n 3) )
out="all_exe_combinations/exe_num"
i=0
print_log=""



# Runs the python file 28 time in all_the exe_combinations folder
# Logs in preserve_payload_contents.txt by default

for build in "${build_types[@]}"; do
	for arch in "${architecture[@]}"; do
		for enc in "${encoding[@]}"; do


			if [[ "$enc" == "both" ]]; then
				for a_idx in "${arr[@]}"; do
					print_log+="\nRun number $i:\nBuild type: "
					print_log+="$build\n"
					print_log+="Architecture: "
					print_log+="$arch\n"
					print_log+="Encoding: "
					print_log+="$enc\n"
					print_log+="xor_key: "
					print_log+="$a_idx\n"

					python3 linux_mint_script.py --hardcode \
					"--$build" --architecture "$arch" \
					--xor-key "$a_idx" --base64 \
					--output "${out}${i}.exe" \
					--log --log-number "$i" --keep-log
					i=$((i + 1))
				done
			fi


			if [[ "$enc" == "xor" ]]; then
				for a_idx in "${both_arr[@]}"; do
					print_log+="\nRun number $i:\nBuild type: "
					print_log+="$build\n"
					print_log+="Architecture: "
					print_log+="$arch\n"
					print_log+="Encoding: "
					print_log+="$enc\n"
					print_log+="xor_key: "
					print_log+="$a_idx\n"

					python3 linux_mint_script.py --hardcode \
					"--$build" --architecture "$arch" \
				        --xor-key "$a_idx" \
					--output "${out}${i}.exe" \
					--log --log-number "$i" --keep-log
					i=$((i + 1))
				done
			fi


			if [[ "$enc" == "base64" ]]; then
				print_log+="\nRun number $i:\nBuild type: "
				print_log+="$build\n"
				print_log+="Architecture: "
				print_log+="$arch\n"
				print_log+="Encoding: base64\n"

				python3 linux_mint_script.py --hardcode \
				"--$build" --architecture "$arch" \
				--base64 \
				--output "${out}${i}.exe" \
				--log --log-number "$i" --keep-log
				i=$((i + 1))
			fi

			print_log+="\n"
		done
	done
done

printf "$print_log">log_file.txt
