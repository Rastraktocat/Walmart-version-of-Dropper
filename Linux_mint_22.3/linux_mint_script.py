import os
import subprocess
import argparse
import base64
#from pathlib import Path

# converts the release/debug and x86/x64 into a PE executable with mingw.
def mingw_run(file_path, file_exe_path, configuration_bool, x64_bool, test_output):

	if (test_output):
		print("This is the file path: " + file_path + " This is the output path: " + file_exe_path)

	if (x64_bool == 64):
		mingw_version = "x86_64-w64-mingw32-g++"
		print("mingw is compiling in x64 mode. ")
	elif (x64_bool == 86):
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
		"-o",
		file_exe_path
		])
	else:
		success = subprocess.run([
		mingw_version,
		file_path,
		"-w",
		"-fpermissive",
		"-o",
		file_exe_path
		])


	# 0 for success
	return success.returncode

# This makes it so that the python file can take arguments.
def parse_args():
	parser = argparse.ArgumentParser(description="This is a script to encode a payload, build a malware file, run the file and then decode the payload.")

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

	parser.add_argument("--keep-log", action="store_true")
	parser.add_argument("--log-number", type=int, default=0)
	parser.add_argument("--logging-output", type=str, default="")

	# would handle the printing out of data.
	parser.add_argument("--test-output", action="store_true")

	args = parser.parse_args()

	return args

def base64_file(payload_file, encode, decode, payload_preserve_path, log, log_number, test_output):

	with open(payload_file, "rb") as file_read:
		payload_bytes = file_read.read()
		try:
			payload = payload_bytes.decode("utf-8")
		except UnicodeDecodeError:
			payload = "<This couldn't be decoded in a way that was visible from command line. That doesn't mean the base64 didn't work.>"

		if (test_output == True):
			print("This is the original version (in the base64 function) of your payload (in hexadecimal): " + payload_bytes.hex())

#//////////////////////////////////////////

# Encoding logic

#//////////////////////////////////////////

	if (encode):
		if (log != ""):
			with open(payload_preserve_path, "a", encoding="utf-8") as file_preserve_read:
				message = "This is what is preserved before applying base64 to the payload (utf-8 decoded) from log number " + str(log_number) + ": " + payload + "\nThis is what is preserved before applying base64 to the payload (raw bytes in hexadecimal) :" + payload_bytes.hex() + "\n\n"
				file_preserve_read.write(message)
				print("Original base64 input preserved.\n")

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

def xor_file(payload_file, xor_key, encode, payload_preserve_path, log, log_number, test_output):

	with open(payload_file, "rb") as file_read: 
		payload_bytes = file_read.read()

# ////////////////////////////////////////////////////////////////////////////

# Reading from file.

# ////////////////////////////////////////////////////////////////////////////

	if (encode and log != ""):
		try:
			payload = payload_bytes.decode("utf-8")
		except UnicodeDecodeError:
			payload = "<Message was not utf-8 decode compatible. This doesn't mean the write didn't go through.>"

		with open(payload_preserve_path, "a", encoding="utf-8") as preserve_file_write:
			message = "This is what is preserved before applying xor to the payload (utf-8 decoded) from log number " + str(log_number) + " : " + payload + "This is what is preserved before applying xor to the payload (raw byte format in hexadecimal): " + payload_bytes.hex() + "\n\n"
			preserve_file_write.write(message)
			print("Original xor input preserved.\n")
	if (test_output == True):
		print("This is the original version of your payload (in hexadecimal) : " + payload_bytes.hex())


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

# default file path to the payload that the dropper will inject (the relative file path of the absolute file path in the .rc file)
		"file_payload_path" : r"payload_contents.txt",

# The actual exe path that mingw outputs.
		"file_exe_path" : r"FileSystem_exe_rebuild/FileSystem_exe_rebuild.exe",

# Give the location of the file that will take the original contents of the payload file
		"file_payload_preserve_path" : r"preserve_original_payload.txt"

	}

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

		if (args.logging_output != ""):
			script_info["file_payload_preserve_path"] = args.logging_output

		if (args.test_output == True):
			print("The file_payload_path is: " + script_info["file_payload_path"])
			print("The file_payload_preserve_path is: " + script_info["file_payload_preserve_path"])

		if (script_info["file_exe_path"] == "" or script_info["file_payload_path"] == "" or script_info["file_path"] == "" or script_info["file_payload_preserve_path"] == ""):
			print("One or more of the variables in script_info.txt or the cmd line was blank.")
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

		if (args.logging_output != ""):
			if (args.test_output == True):
				print("This is file_payload_preserve_path: " + args.logging_output + " It was gotten from the logging output.")
			else:
				print("file_payload_preserve_path gotten from logging output.\n")
			script_info["file_payload_preserve_path"] = args.logging_output

		if (args.test_output == True):
			print("The file_payload_path is: " + script_info["file_payload_path"])

		if (script_info["file_exe_path"] == "" or script_info["file_path"] == "" or script_info["file_payload_path"] == "" or script_info["file_payload_preserve_path"] == ""):
			print("Hardcode files have not been set. Open up linux_mint_script.py and set them in the main function.")
			return 1

	# The script comes with no extra files besides the payload. If there is no preserve file already and logging is not opted for then file resetting will be skipped.

	if (args.log_number == 0):
		with open(script_info["file_payload_preserve_path"], "w", encoding="utf-8") as file_write:
				file_write.write("")
				if (args.test_output):
					print("file_payload_preserve_path has been reset.")

	#//////////////////////////////////////////////////////

	# Encode payload

	#//////////////////////////////////////////////////////

	if (args.default_xor == True or args.both_encoding == True):
		encode = True
		xor_file(script_info["file_payload_path"], 115, encode, script_info["file_payload_preserve_path"], args.logging_output, args.log_number, args.test_output)
		if (args.test_output):
			print("The xor key used is 115")

	elif (args.xor_key != 0): # Handling custom xor keys and keeping them in a 0 - 255 range
		if (args.xor_key > 255):
			print("This script only lets positive xor_keys up to 255. No more. The script will now handle the xor_key as 255.")
			args.xor_key = 255
		elif (args.xor_key < 0):
			print("This script only lets positive xor_keys up to 255. No more. The script will now handle the xor_key as 255.")
			args.xor_key = 255

		xor_file(script_info["file_payload_path"], args.xor_key, True, script_info["file_payload_preserve_path"], args.logging_output, args.log_number, args.test_output)
		if (args.test_output):
			print(f"This xor key used is {args.xor_key} \n")

	# Handling base64 encoding.
	if (args.base64 == True or args.both_encoding == True):
		encode = True
		decode = False
		base64_file(script_info["file_payload_path"], encode, decode, script_info["file_payload_preserve_path"], args.logging_output, args.log_number, args.test_output)

	#//////////////////////////////////////////////////////

	# building and running malware

	#//////////////////////////////////////////////////////

	if (args.release == True):
		set_mingw_release = True
		success = mingw_run(script_info["file_path"], script_info["file_exe_path"], set_mingw_release, args.architecture, args.test_output)
		if (success == 0):
			print("mingw ran successfully in release mode. Warnings are turned off.")
	elif (args.debug == True):
		set_mingw_release = False
		success = mingw_run(script_info["file_path"], script_info["file_exe_path"], set_mingw_release, args.architecture, args.test_output)
		if (success == 0):
			print("mingw ran successfully in debug mode. Warnings are turned off. ")
	else:
		# will run in Release mode.
		set_mingw_release = True
		success = mingw_run(script_info["file_path"], script_info["file_exe_path"], set_mingw_release, args.architecture, args.test_output)
		if (success == 0):
			print("mingw ran successfully in release mode. Warnings are turned off. ")


	#//////////////////////////////////////////////////////

	# Decode payload

	#//////////////////////////////////////////////////////

	if (args.base64 == True or args.both_encoding == True):
		encode = False
		decode = True
		base64_file(script_info["file_payload_path"], encode, decode, script_info["file_payload_preserve_path"], args.logging_output, args.log_number, args.test_output)

	if (args.both_encoding == True or args.default_xor == True):
		xor_file(script_info["file_payload_path"], 115, False, script_info["file_payload_preserve_path"], args.logging_output, args.log_number, args.test_output)
		if (args.test_output):
			print("The xor key used is 115")

	elif (args.xor_key != 0):
		xor_file(script_info["file_payload_path"], args.xor_key, False, script_info["file_payload_preserve_path"], args.logging_output, args.log_number,  args.test_output)
		if (args.test_output):
			print(f"This xor key used is {args.xor_key} \n")

main()
