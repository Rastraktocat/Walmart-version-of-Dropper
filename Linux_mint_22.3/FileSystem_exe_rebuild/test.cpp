#include <iostream>
#include "windows.h"

char* name = "C:\\Windows\\System32\\calc.exe";

int main(){

	STARTUPINFOA si;
	PROCESS_INFORMATION pi;
	ZeroMemory(&si, sizeof(si));
	si.cb = sizeof(si);
	ZeroMemory(&pi, sizeof(pi));
	BOOL err = CreateProcessA(name, NULL, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
	if (!err) {
		printf("%u\n", GetLastError());
	}
	return 0;
}
