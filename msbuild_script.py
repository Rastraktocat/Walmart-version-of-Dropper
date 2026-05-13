import subprocess
import argparse

#implement some form of xor key checking so that the key
#cannot be 100000000000000000000
def run_msbuild(run_file_path, configuration_bool, x64_bool):
	if (configuration_bool == True):
		run_configuration_string = "/p:Configuration=Release"
	else:
		run_configuration_string = "/p:Configuration=Debug"

	if (x64_bool == 64):
		run_architecture_string = "-p:Platform=x64"
	elif (x64_bool == 86):
		run_architecture_string = "-p:Platform=x86"
	else: 
		parser.error("Platform must be 86 or 64")

	subprocess.run([
	"msbuild", 
	run_file_path,
	run_configuration_string,
	run_architecture_string
	])			


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--release", action="store_true")
	parser.add_argument("--architecture", type=int, default=64, required=True)
	parser.add_argument("--use-base64", type=str, default="false")
	parser.add_argument("--set-and-use-xor", type=str, default="0")
	parser.add_argument("--use-hardcode", action="store_true")

	args = parser.parse_args()
	arr = []
	
	arr.append(args.release)
	arr.append(args.architecture)
	arr.append(args.use_base64)
	arr.append(args.set_and_use_xor)
	arr.append(args.use_hardcode)

	return arr		

def run_program(run_file, payload_file, base64_setting, xor_key):
	subprocess.run([run_file, "--payload", payload_file,
	"--base64", base64_setting, "--xor-key", xor_key])

def main():
	# payload_path = r"C:\Users\adind\Dropper\FileSystem_exe_rebuild\calc"
	# file_exe_path = r"C:\Users\adind\Dropper\FileSystem_exe_rebuild \FileSystem_exe_rebuild\x64\Release\FileSystem_exe_rebuild.exe"
	# file_path = r"C:\Users\adind\Dropper\FileSystem_exe_rebuild\FileSystem_exe_rebuild\FileSystem_exe_rebuild.vcxproj"
	
	flag_arr = parse_args()

	if (flag_arr[4] != True):
		file_exe_path = input("Give the file path to the place where the exe will be dropped to: ")	
		payload_path = input("Set the default file path to the payload that the dropper will inject (no file extension should be applied): ")
		file_path = input("Give the file path to the program you want to run msbuild on (should end in .vcxproj) : ")
	else:
		file_exe_path = r""
		payload_path = r""
		file_path = r""
	
	if (file_exe_path == "" or payload_path == "" or file_path == ""):
		print("Hardcode flag set but the variables on lines 62-64 were not set.")
	else:
		run_msbuild(file_path, flag_arr[0], flag_arr[1])

		run_program(file_exe_path, payload_path, flag_arr[2], flag_arr[3])
		# 0 -> build mode (release or debug)
		# 1 -> platform (x86 or x64)
		# 2 -> Whether the program uses base 64 (default is false)
		# 3 -> The xor key if the program uses xor (default is 0)
		# 4 -> Hardcoded argument

main()

