#include <windows.h>
#include <shellapi.h>
#include <iostream>

bool LaunchFile(const wchar_t* path)
{
    SHELLEXECUTEINFOW sei = { 0 };

    sei.cbSize = sizeof(sei);
    sei.fMask = SEE_MASK_NOCLOSEPROCESS;
    sei.hwnd = NULL;
    sei.lpVerb = L"open";
    sei.lpFile = path;
    sei.lpParameters = NULL;
    sei.lpDirectory = NULL;
    sei.nShow = SW_SHOWNORMAL;

    if (!ShellExecuteExW(&sei))
    {
        DWORD err = GetLastError();
        std::wcout << L"ShellExecuteEx failed. GetLastError = "
                   << err << std::endl;
        return false;
    }

    std::wcout << L"Process launched successfully." << std::endl;

    if (sei.hProcess)
    {
        WaitForSingleObject(sei.hProcess, INFINITE);
        CloseHandle(sei.hProcess);
    }

    return true;
}

int main()
{
    LaunchFile(L"C:\\Windows\\System32\\calc.exe");
    return 0;
}
