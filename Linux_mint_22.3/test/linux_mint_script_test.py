import random
import pytest
from linux_mint_script import Args, revise_args

@pytest.mark.parameterize
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

