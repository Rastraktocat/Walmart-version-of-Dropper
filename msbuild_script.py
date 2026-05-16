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
	parser = argparse.ArgumentParser()
	parser.add_argument("--release", action="store_true")
	parser.add_argument("--architecture", type=int, default=64, required=True)
	parser.add_argument("--use-base64", action="store_true")
	parser.add_argument("--use-115-as-xor", action="store_true")
	parser.add_argument("--set-and-use-xor", type=int, default=0)
	parser.add_argument("--use-base64-and-xor-default", action="store_true")
	parser.add_argument("--use-hardcode", action="store_true")

	args = parser.parse_args()
	arr = []
	
	arr.append(args.release)
	arr.append(args.architecture)
	arr.append(args.use_base64)
	arr.append(args.use_115_as_xor)
	arr.append(args.set_and_use_xor)
	arr.append(args.use_base64_and_xor_default)
	arr.append(args.use_hardcode)

	return arr		

def read_file_information_from_script_info(script_info):
	file_information = {}

	print("The reading of script_info.txt requires that \"file_exe_path = \", \"file_payload_path = \", and \"file_path = \" are all formatted EXACTLY as seen.")
	with open(script_info, "r") as fr:
		for line in fr:
			print(line)
			line = line.strip("\n")
			print(repr(line))
			if (line[0:16] == "file_exe_path = "):
				file_information["file_exe_path"] = line[16:]
				print("file_exe_path is: " + line[16:])
			if (line[0:20] == "file_payload_path = "):
				file_information["file_payload_path"] = line[20:]
				print("file_payload_path is: " + line[20:])
			if (line[0:12] == "file_path = "):
				file_information["file_path"] = line[12:]
				print("file_path is: " + line[12:])
				
	return file_information

def base64_file(payload_file):

	return payload_file	


def xor_file(payload_file):
	return payload_file

def run_program(run_file):
	subprocess.run([run_file])

def main():
	
	flag_arr = parse_args()
	script_info_location = r"C:\Users\adind\Dropper\Walmart-version-of-Dropper\script_info.txt"

	if (flag_arr[6] != True):
		file_path = input("Give the file path to the program you want to pass in to msbuild so that msbuild can compile it (should end in .vcxproj) : ")
		payload_path = input("Set the default file path to the payload that the dropper will inject (no file extension should be applied): ")
		file_exe_path = input("Give the file path to the place where the exe will place after msbuild compiles it (should have an exe file extension): ")

	else:
		script_dict = read_file_information_from_script_info(script_info_location)	
		file_path = script_dict.get("file_path")
		payload_path = script_dict.get("payload_path")
		file_exe_path = script_dict.get("file_exe_path")
	
	if (script_info_location = "" or file_exe_path == "" or payload_path == "" or file_path == ""):
		print("Hardcode flag set but one or more of the variables was blank.")
	else:
		run_msbuild(file_path, flag_arr[0], flag_arr[1])

		run_program(file_exe_path)

		# 0 -> build mode (release or debug)
		# 1 -> platform (x86 or x64)
		# 2 -> Whether the program uses base 64 
		# 3 -> Uses 115 as the xor key.
		# 4 -> The xor key if the program uses xor (default is 0)
		# 5 -> Runs base64 and xor with key 115 automatically
		# 6 -> Hardcoded argument
main()

