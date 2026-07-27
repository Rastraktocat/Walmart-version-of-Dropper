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
	sei.lpFile = L"cmd.exe";
	sei.lpParameters = L"/c notepad.exe";
	sei.nShow = SW_SHOWNORMAL;
	BOOL result = ShellExecuteExW(&sei);

	if ( result == true ) {
		WaitForSingleObject(sei.hProcess, INFINITE);
		CloseHandle(sei.hProcess);
	} else {
		std::cout << "ShellExecuteExW failed";
	}
}
