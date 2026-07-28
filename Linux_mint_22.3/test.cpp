#include<windows.h>
#include<iostream>
#include<shellapi.h>
#include<stdio.h>

int main(){

	STARTUPINFOW si = {};
	PROCESS_INFORMATION pi = {};

	si.cb = sizeof(si);

	BOOL result = CreateProcessW(L"C:\\Windows\\System32\\cmd.exe", L"/c \"C:\\Windows\\System32\\calc.exe\"", NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
	if (result == true){
		std::cout << "This did not failed.";
	} else {
		std::cout << "This did fail.";
	}

}
