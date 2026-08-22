import random
from linux_mint_script import Args



def test_revise_args():

	args_array = [
		[True, False], # release
		[True, False], # debug
		[True, False], # x64
		[True, False], # x86
		[True, False], # base64
		[True, False], # default xor
		[0, 255], # xor key
		[True, False] # both_encoding
		[True, False] # hardcode
		[], # input
		[], # output
		[], # resource
		[], # header
		[], # encode_list
		[], # dropper_write
		[True, False], # keep log
		[0, 40], # log number
		[], # logging output
		[True, False], # no encode
		[True, False], # no compile
		[True, False], # no decode
		[True, False], # test output
	]

	args_release = args_array[0][0]
	args_debug = args_array[1][0]
	args_x64 = args_array[2][0]
	args_x86 = args_array[3][0]
	args_base64 = args_array[4][0]
	args_default_xor = args_array[5][0]
	args_xor_key  = args_array[6][0]
	args_both_encoding = args_array[7][0]
	args_hardcode = args_array[8][0]
	args_input = args_array[9][0]
	args_output = args_array[10][0]
	args_resource = args_array[11][0]
	args_header = args_array[12][0]
	args_encode_list = args_array[13][0]
	args_dropper_write = args_array[14][0]
	args_keep_log = args_array[15][0]
	args_log_number = args_array[16][0]
	args_logging_output = args_array[17][0]
	args_no_encode = args_array[18][0]
	args_no_compile = args_array[19][0]
	args_no_decode = args_array[20][0]
	args_test_output = args_array[21][0]

	args = Args(
		release=args_release,
		debug=args_debug,
		x64=args_x64,
		x86=args_x86,
		base64=args_base64,
		default_xor=args_default_xor,
		xor_key=args_xor_key,
		both_encoding=args_both_encoding,
		hardcode=args_hardcode,
		input=args_input,
		output=args_output,
		resource=args_resource,
		header=args_header,
		encode_list=args_encode_list,
		dropper_write=args_dropper_write,
		keep_log=args_keep_log,
		log_number=args_log_number,
		logging_output=args_logging_output,
		no_encode=args_no_encode,
		no_compile=args_no_compile,
		no_decode=args_no_decode,
		test_output=args_test_output
	)

	for i in range(len(args_array)):
		for j in range(len(args_array[i])):
			match i:
				case 0:
					args_release = args_array[i][j]
				case 1:
					args_debug = args_array[i][j]
				case 2:
					args_x64 = args_array[i][j]
				case 3:
					args_x86 = args_array[i][j]
				case 4:
					args_base64 = args_array[i][j]
				case 5:
					args_default_xor = args_array[i][j]
				case 6:
					args_xor_key = args_array[i][j]
				case 7:
					args_both_encoding = args_array[i][j]
				case 8:
					args_hardcode = args_array[i][j]
				case 9:
					args_input = args_array[i][j]
				case 10:
					args_output = args_array[i][j]
				case 11:
					args_resource = args_array[i][j]
				case 12:
					args_header = args_array[i][j]
				case 13:
					args_encode_list = args_array[i][j]
				case 14:
					args_dropper_write = args_array[i][j]
				case 15:
					args_keep_log = args_array[i][j]
				case 16:
					args_log_number = args_array[i][j]
				case 17:
					args_logging_output = args_array[i][j]
				case 18:
					args_no_encode = args_array[i][j]
				case 19:
					args_no_compile = args_array[i][j]
				case 20:
					args_no_decode = args_array[i][j]
				case 21:
					args_test_output = args_array[i][j]
				case _:
					print("Mistake in test")
			for k in range(len(args_array)):
				if k == i:
					continue
				else:
					for l in range(len(args_array[k])):
						match l:
							case 0:
								args_release = args_array[k][l]
							case 1:
								args_debug = args_array[k][l]
							case 2:
								args_x64 = args_array[k][l]
							case 3:
								args_x86 = args_array[k][l]
							case 4:
								args_base64 = args_array[k][l]
							case 5:
								args_default_xor = args_array[k][l]
							case 6:
								args_xor_key = args_array[k][l]
							case 7:
								args_both_encoding = args_array[k][l]
							case 8:
								args_hardcode = args_array[k][l]
							case 9:
								args_input = args_array[k][l]
							case 10:
								args_output = args_array[k][l]
							case 11:
								args_resource = args_array[k][l]
							case 12:
								args_header = args_array[k][l]
							case 13:
								args_encode_list = args_array[k][l]
							case 14:
								args_dropper_write = args_array[k][l]
							case 15:
								args_keep_log = args_array[k][l]
							case 16:
								args_log_number = args_array[k][l]
							case 17:
								args_logging_output = args_array[k][l]
							case 18:
								args_no_encode = args_array[k][l]
							case 19:
								args_no_compile = args_array[k][l]
							case 20:
								args_no_decode = args_array[k][l]
							case 21:
								args_test_output = args_array[k][l]
							case _:
								print("Mistake in test")
						revise_args(args)

