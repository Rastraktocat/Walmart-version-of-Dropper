build_types=(release debug)
architecture=(86 64)
encoding=(both xor base64)
arr=( $(shuf -i 0-255 -n 3) )
both_arr=( $(shuf -i 0-255 -n 3) )
out="all_exe_combinations/exe_num"
i=0
print_log=""




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
					print_log+="$enc\n\n"


					python3 linux_mint_script.py --hardcode \
					 "--$build" --architecture "$arch" \
					--base64 --xor-key "$a_idx" \
					--output "${out}${i}" \
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
					print_log+="$enc\n\n"


					python3 linux_mint_script.py --hardcode \
					"--$build" --architecture "$arch" \
				        --xor-key "$a_idx" \
					--output "${out}${i}" \
					--keep-log --log --log-number "$i"
					i=$((i + 1))
				done
			fi


			if [[ "$enc" == "base64" ]]; then
				print_log+="\nRun number $i:\nBuild type: "
				print_log+="$build\n"
				print_log+="Architecture: "
				print_log+="$arch\n"
				print_log+="Encoding: "
				print_log+=" Encoding values: base64"


				python3 linux_mint_script.py --hardcode \
				"--$build" --architecture "$arch" \
				--base64 \
				--output "${out}${i}" \
				--log --keep-log --log-number "$i"
				i=$((i + 1))
			fi

			print_log+="\n"
		done
	done
done

printf "$print_log">log_file.txt
