#include <windows.h>
#include <iostream>

int main(){

	DWORD result = GetFileAttributesW(L"C:\\Windows\\System32\\mscoree.dll");
	std::cout << GetLastError();
}
