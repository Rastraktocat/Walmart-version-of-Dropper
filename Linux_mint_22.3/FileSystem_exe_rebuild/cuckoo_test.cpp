#include<windows.h>
#include<iostream>

int main(){
	char* name = "C:\\Windows\\System32\\calc.exe";
	SHELLEXECUTEINFO sei = {};
	sei.cbSize = sizeof(sei);
	sei.fMask = SEE_MASK_NOCLOSEPROCESS;
	sei.lpVerb = "open";
	sei.lpFile = name;
	sei.nShow = SW_SHOWNORMAL;
	BOOL result = ShellExecuteEx(&sei);
	if (result == true){
		std::cout << "This succeeds.";
	}
	else {
		std::cout << "This failed.";
	}
}
