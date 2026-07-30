#include<windows.h>
#include<string>

void run(){

	LoadLibraryW(L"mscoree.dll");
	STARTUPINFOW si{};
	PROCESS_INFORMATION pi{};
	si.cb = sizeof(si);

	std::wstring cmd = L"cmd.exe netsh winhttp show proxy";
	CreateProcessW(nullptr, (LPWSTR) cmd.c_str(), nullptr, nullptr, FALSE, 0, nullptr, nullptr, &si, &pi);

}

int main(){

	run();
	return 0;

}
