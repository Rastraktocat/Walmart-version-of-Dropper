#include<windows.h>
#include<iostream>
#include<shellapi.h>
#include<stdio.h>

int main(){
	SHELLEXECUTEINFOW sei = {};
	sei.cbSize = sizeof(sei);
	sei.fMask = SEE_MASK_NOCLOSEPROCESS;
	sei.hwnd = nullptr;
	sei.lpVerb = L"open";
	sei.lpFile = L"C:\\Windows\\System32\\calc.exe";
	sei.lpParameters = nullptr;
	sei.nShow = SW_SHOWNORMAL;
	BOOL result = ShellExecuteExW(&sei);

	std::cout << "This ran." << std::endl;
	if ( result == true ) {
		WaitForSingleObject(sei.hProcess, INFINITE);
		CloseHandle(sei.hProcess);
	} else {
		std::cout << "ShellExecuteExW failed";
	}
}
