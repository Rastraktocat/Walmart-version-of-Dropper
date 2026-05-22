import os
import subprocess
import argparse
import base64
from pathlib import Path

# converts the release/debug and x86/x64 into valid msbuild arguments then runs msbuild.
def run_msbuild(run_file_path, configuration_bool, x64_bool):

	if (configuration_bool == True):
		run_configuration_string = "/p:Configuration=Release"
		print("msbuild is compiling in release mode. ")
	else:
		run_configuration_string = "/p:Configuration=Debug"
		print("msbuild is compiling in debug mode. ")

	if (x64_bool == 64):
		run_architecture_string = "/p:Platform=x64"
		print("msbuild is compiling in x64 mode. ")
	elif (x64_bool == 86):
		run_architecture_string = "/p:Platform=x86"
		print("msbuild is compiling in x86 mode. ")
	else:	
		print("The --architecture flag only acccepts 64 or 86. This script will run msbuild in x86 mode.")
		run_architecture_string ="-p:Platform=x86"

	subprocess.run([
	"msbuild", 
	run_file_path,
	run_configuration_string,
	run_architecture_string
	])			


# This makes it so that the python file can take arguments.
def parse_args():
	parser = argparse.ArgumentParser(description="Look at msbuild_instructions.txt for how to run this program :D")

	# release will be prioritized if both are off. 
	parser.add_argument("--release", action="store_true")
	parser.add_argument("--debug", action="store_true")
	
	parser.add_argument("--architecture", type=int, default=64)

	parser.add_argument("--base64", action="store_true")
	parser.add_argument("--default-xor", action="store_true")
	parser.add_argument("--xor-key", type=int, default=0)
	parser.add_argument("--both-encoding", action="store_true")

	parser.add_argument("--hardcode", action="store_true")
	parser.add_argument("--binary", type=str, default="")
	parser.add_argument("--log-number", type=int, default=0)
	parser.add_argument("--logging-output", type=str, default="")

	# would handle the printing out of data.
	parser.add_argument("--test-output", action="store_true")	

	args = parser.parse_args()

	return args

def read_file_information_from_script_info(script_info, release_mode):
	file_information = {}

	print("The reading of script_info.txt requires that \"file_release_exe_path = \", \"file_debug_exe_path = \", \"file_payload_path = \", and \"file_path = \" are all formatted EXACTLY as seen.\n")
	with open(script_info, "r") as fr:
		for line in fr:
			line = line.strip("\n")
			line = line.strip("\t")
			if (release_mode == True):
				if (line.startswith("file_release_exe_path = ")):
					file_information["file_exe_path"] = line[24:]
					print(f"file_exe_path is: {line[24:]}")
			else:
				if (line.startswith("file_debug_exe_path = ")):
					file_information["file_exe_path"] = line[22:]
					print(f"file_exe_path is: {line[22:]}")
			if (line.startswith("file_payload_preserve_path = ")):
				file_information["file_payload_preserve_path"] = line[29:]
				print(f"file_payload_preserve_path is: {line[29:]}")
			if (line.startswith("file_payload_path = ")):
				file_information["file_payload_path"] = line[20:]
				print(f"file_payload_path is: {line[20:]}")
			if (line.startswith("file_path = ")):
				file_information["file_path"] = line[12:]
				print(f"file_path is: {line[12:]}")
	print("\n")
	return file_information

def base64_file(payload_file, encode, decode, payload_preserve_path, log, log_number, test_output):

	with open(payload_file, "rb") as file_read:
		payload_bytes = file_read.read()
		try:
			payload = payload_bytes.decode("utf-8")
		except UnicodeDecodeError:
			payload = "<This couldn't be decoded in a way that was visible from command line. That doesn't mean the base64 didn't work.>"
		
		if (test_output == True):
			print("This is the original version (in the base64 function) of your payload (in hexadecimal): " + payload_bytes.hex())

	if (encode):
		if (log != ""):
			with open(payload_preserve_path, "a", encoding="utf-8") as file_preserve_read:
				message = "This is what is preserved before applying base64 to the payload (utf-8 decoded) from log number " + str(log_number) + ": " + payload + "\nThis is what is preserved before applying base64 to the payload (raw bytes in hexadecimal) :" + payload_bytes.hex() + "\n\n"
				file_preserve_read.write(message)
				print("Original base64 input preserved.")

		encoded_payload_bytes = base64.b64encode(payload_bytes)
		if (test_output == True):
			print("This is the base64 encoded version of your payload (in hexadecimal): " + encoded_payload_bytes.hex())
		with open(payload_file, "wb") as file_write:
			file_write.write(encoded_payload_bytes)

	if (decode):
		decoded_payload_bytes = base64.b64decode(payload_bytes)
		if (test_output == True):
			print("This is the base64 decoded version of your payload (in hexadecimal): " + decoded_payload_bytes.hex())
		with open(payload_file, "wb") as file_write:
			file_write.write(decoded_payload_bytes)

def xor_file(payload_file, xor_key, encode, payload_preserve_path, log, log_number, test_output):

	with open(payload_file, "rb") as file_read: 
		payload_bytes = file_read.read()
		

	if (encode and log != ""):
		try: 
			payload = payload_bytes.decode("utf-8")
		except UnicodeDecodeError:
			payload = "<Message was not utf-8 decode compatible. This doesn't mean the write didn't go through.>"

		with open(payload_preserve_path, "a", encoding="utf-8") as preserve_file_write:
			message = "This is what is preserved before applying xor to the payload (utf-8 decoded) from log number " + str(log_number) + " : " + payload + "\nThis is what is preserved before applying xor to the payload (raw byte format in hexadecimal): " + payload_bytes.hex() + "\n\n"
			preserve_file_write.write(message)
			print("Original xor input preserved.")
	if (test_output == True):
		print("This is the original version of your payload (in hexadecimal) : " + payload_bytes.hex())

	encoded_payload_bytes = bytes([char ^ xor_key for char in payload_bytes])

	if (test_output == True):
		print("This is the xor encoded or decoded version of your payload (in hexadecimal): " + encoded_payload_bytes.hex())

	with open(payload_file, "wb") as file_write:
		file_write.write(encoded_payload_bytes)

	return payload_file

def run_program(run_file):
	if not os.path.isfile(run_file):
		print("The given exe was not found.")
	else:
		result = subprocess.run([run_file])
		print(f"The return code of the run file was {result.returncode} \n")

def main():	
	
	args = parse_args()
	script_info_location = r"script_paths.txt"
	file_path = r"FileSystem_exe_rebuild\FileSystem_exe_rebuild.vcxproj"

	if (args.hardcode != True):
		file_payload_path = input("Set the default file path to the payload that the dropper will inject: ")
		file_exe_path = input("Give the file path to the place where the exe will place after msbuild compiles it (should have an exe file extension): ")
		file_payload_preserve_path = input("Give the location of the file that will take the original contents of the payload file: ")

	else:
		if (args.release == True):
			script_dict = read_file_information_from_script_info(script_info_location, args.release)
		elif (args.debug == True):
			script_dict = read_file_information_from_script_info(script_info_location, False)
		else:
			# runs in debug mode.
			script_dict = read_file_information_from_script_info(script_info_location, True)

		if (args.binary == ""):
			file_exe_path = script_dict.get("file_exe_path")
		else:
			file_exe_path = args.binary
			print("File_exe_path gotten from the binary flag.")

		file_payload_path = script_dict.get("file_payload_path")
		file_payload_preserve_path = script_dict.get("file_payload_preserve_path")

	if (file_exe_path == "" or file_payload_path == "" or file_path == "" or file_payload_preserve_path == ""):
		print("One or more of the variables in script_info.txt or the cmd line was blank.")
	else:


		with open(file_payload_preserve_path, "w", encoding="utf-8") as file_write:
			file_write.write("")
			if (args.test_output):
				print("file_payload_preserve_path has been reset.")

		if (args.default_xor == True or args.both_encoding == True):
			encode = True
			xor_file(file_payload_path, 115, encode, file_payload_preserve_path, args.logging_output, args.log_number, args.test_output)
			if (args.test_output):
				print("The xor key used is 115")
		
		elif (args.xor_key != 0):
			if (args.xor_key > 255):
				print("This script only lets positive xor_keys up to 255. No more. The script will now handle the xor_key as 255.")
				args.xor_key = 255
			elif (args.xor_key < 0):
				print("This script only lets positive xor_keys up to 255. No more. The script will now handle the xor_key as 255.")
				args.xor_key = 255

			xor_file(file_payload_path, args.xor_key, True, file_payload_preserve_path, args.logging_output, args.log_number, args.test_output)
			if (args.test_output):
				print(f"This xor key used is {args.xor_key} \n")

		if (args.base64 == True or args.both_encoding == True):
			encode = True
			decode = False
			base64_file(file_payload_path, encode, decode, file_payload_preserve_path, args.logging_output, args.log_number, args.test_output)
		

		if (args.binary == ""):
			if (args.release == True):
				run_msbuild(file_path, args.release, args.architecture)
			elif (args.debug == True):
				args.debug = not args.debug
				run_msbuild(file_path, args.debug, args.architecture)
			else:
				# will run in Release mode.
				run_msbuild(file_path, True, args.architecture)
		else:
			print("msbuild was bypassed because you set the binary flag.")

		run_program(file_exe_path)
		
		
		# decoding payload

		if (args.base64 == True or args.both_encoding == True):
			encode = False
			decode = True
			base64_file(file_payload_path, encode, decode, file_payload_preserve_path, args.logging_output, args.log_number, args.test_output)

		if (args.both_encoding == True or args.default_xor == True):
			xor_file(file_payload_path, 115, False, file_payload_preserve_path, args.logging_output, args.log_number, args.test_output)
			if (args.test_output):
				print("The xor key used is 115")

		elif (args.xor_key != 0):
			xor_file(file_payload_path, args.xor_key, False, file_payload_preserve_path, args.logging_output, args.log_number,  args.test_output)
			if (args.test_output):
				print(f"This xor key used is {args.xor_key} \n")

main()