build_types=(release debug)
architecture=(86 64)
encoding=(both xor base64)
arr=( $(shuf -i 0-255 -n 10) )
both_arr=( $(shuf -i 0-255 -n 10) )
out="all_exe_combinations/exe_num"
i=0

for build in "${build_types[@]}"; do
	for arch in "${architecture[@]}"; do
		for enc in "${encoding[@]}"; do
			i=$((i + 1))
			if [["$enc" == "both"]]; then
				for a_idx in "${both_arr[@]}"; do 
					python3 linux_mint_script.py --hardcode --no-decode --no-encode "--$build" --architecture "$arch" --base64 --xor-key "$a_idx" --output "$out$i"
				done
			fi

			if [["$enc" == "xor"]]; then
				for a_idx in "${both_arr[@]}"; do 
					python3 linux_mint_script.py --hardcode --no-decode --no-encode "--$build" --architecture "$arch" --base64 --xor-key "$a_idx" --output "$out$i"
				done
			fi

			if [["$enc" == "base64"]]; then
				python3 linux_mint_script.py --hardcode --no-decode --no-encode "--$build" --architecture "$arch" --base64 --xor-key "$a_idx" --output "$out$i"
			fi
		done
	done
done
