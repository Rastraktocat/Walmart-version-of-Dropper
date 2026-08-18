#include <windows.h>
#include <iostream>

int main(){

	LoadLibraryW(L"C:\\Windows\\System32\\mscoree.dll");
	LockResource();
	std::cout << GetLastError();
}
